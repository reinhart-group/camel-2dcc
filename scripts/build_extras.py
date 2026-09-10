"""Turn the raw non-AFM files into clean classroom tables for notebook 07 (offline).

Inputs: data/raw/extras/fetched.json + data/raw/extras/raw/* (fetch_extras.py) and
data/raw/survey/ (XRD sample 20958, SEM sample 32096).
Outputs in data/raw/extras/clean/:
- transport_fese.csv   sample_id, temperature_K, resistance_ohm (Rxx), one row per reading
- transport_summary.csv sample_id, R_300K, R_15K, onset/mid/zero temperatures (K)
- raman_spectra.csv    sample_id, material, raman_shift_cm1, intensity (long format)
- raman_peaks.csv      sample_id, material, E2g_cm1, A1g_cm1, separation_cm1 (MoS2 only)
- xrd_20958.csv        two_theta_deg, intensity_counts
- sem_32096.png + sem_32096.json (nm per pixel from the burned-in scale bar)
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data/raw"
SURVEY = RAW / "survey"
OUT = RAW / "extras/clean"


REF_K = 40.0  # above every film's transition in this set (highest onset ≈ 32 K)


def transport(index: dict) -> None:
    """One resistance-vs-temperature curve per sample (files of one sample are
    combined, e.g. a 300→40 K run plus a 40→2 K run) and a summary of where
    each curve drops to 90%, 50%, and ~0 of its 40 K resistance."""
    rows, summary = [], []
    for v in index.values():
        if v.get("kind") != "transport":
            continue
        parts = []
        for f in v.get("files", []):
            df = pd.read_csv(ROOT / f["local"])
            if {"Temp_K", "Rxx"} <= set(df.columns):
                parts.append(df[["Temp_K", "Rxx"]].dropna())
        if not parts:
            continue
        df = pd.concat(parts).sort_values("Temp_K").drop_duplicates("Temp_K")
        for t, r in zip(df.Temp_K, df.Rxx):
            rows.append({"sample_id": v["sample_id"], "temperature_K": round(t, 3), "resistance_ohm": round(r, 3)})
        r_ref = float(np.interp(REF_K, df.Temp_K, df.Rxx))
        cold = df[df.Temp_K <= REF_K]

        def highest_below(frac):
            """Highest temperature at which R is already below frac × R(40 K)."""
            below = cold[cold.Rxx < frac * r_ref]
            return round(float(below.Temp_K.max()), 2) if len(below) else None

        summary.append({"sample_id": v["sample_id"], "lowest_T_measured_K": round(float(df.Temp_K.min()), 2),
                        "R_300K_ohm": round(float(np.interp(300, df.Temp_K, df.Rxx)), 1),
                        "R_40K_ohm": round(r_ref, 1),
                        # No 90% "onset" column: normal-state resistance keeps falling as the
                        # metal cools, so a 90% threshold lands above the real transition.
                        "T_mid_50pct_K": highest_below(0.5),
                        "T_zero_1pct_K": highest_below(0.01)})
    pd.DataFrame(rows).to_csv(OUT / "transport_fese.csv", index=False)
    pd.DataFrame(summary).sort_values("sample_id").to_csv(OUT / "transport_summary.csv", index=False)
    print(f"transport: {len(summary)} samples")


def _peak(x, y, lo, hi):
    """Peak position in [lo, hi]: parabola through the 5 points around the maximum."""
    m = (x >= lo) & (x <= hi)
    if m.sum() < 7:
        return None
    xs, ys = x[m], y[m]
    i = int(np.argmax(ys))
    i = min(max(i, 2), len(xs) - 3)
    a, b, _ = np.polyfit(xs[i - 2:i + 3], ys[i - 2:i + 3], 2)
    return round(float(-b / (2 * a)), 2) if a < 0 else round(float(xs[i]), 2)


def raman(index: dict) -> None:
    spectra, peaks = [], []
    for v in index.values():
        if v.get("kind") != "raman":
            continue
        for f in v.get("files", []):
            try:
                d = np.loadtxt(ROOT / f["local"])
            except ValueError:
                continue
            if d.ndim != 2 or d.shape[1] < 2:
                continue
            x, y = d[:, 0], d[:, 1]
            order = np.argsort(x)
            x, y = x[order], y[order]
            material = "MoS2" if "MoS2" in v["materials"] else "WS2"
            keep = (x >= 150) & (x <= 600)
            for a, b in zip(x[keep], y[keep]):
                spectra.append({"sample_id": v["sample_id"], "material": material,
                                "raman_shift_cm1": round(float(a), 2), "intensity": round(float(b), 2)})
            if material == "MoS2":
                e2g, a1g = _peak(x, y, 375, 392), _peak(x, y, 398, 412)
                if e2g and a1g:
                    # A peak must stand clearly above the local baseline to count.
                    base = np.median(y[(x > 340) & (x < 370)]) if ((x > 340) & (x < 370)).any() else np.min(y)
                    height = min(np.interp(e2g, x, y), np.interp(a1g, x, y)) - base
                    noise = np.std(y[(x > 340) & (x < 370)]) if ((x > 340) & (x < 370)).sum() > 5 else 1
                    if height > 5 * noise:
                        peaks.append({"sample_id": v["sample_id"], "material": material, "E2g_cm1": e2g,
                                      "A1g_cm1": a1g, "separation_cm1": round(a1g - e2g, 2)})
    pd.DataFrame(spectra).to_csv(OUT / "raman_spectra.csv", index=False)
    pd.DataFrame(peaks).to_csv(OUT / "raman_peaks.csv", index=False)
    print(f"raman: {len({s['sample_id'] for s in spectra})} spectra, {len(peaks)} MoS2 with clear peaks")


def xrd() -> None:
    df = pd.read_csv(SURVEY / "20958_1hr_2theta-omega_program_1_export.csv")
    df.columns = ["two_theta_deg", "intensity_counts"]
    df.to_csv(OUT / "xrd_20958.csv", index=False)
    print(f"xrd: {len(df)} points")


def sem() -> None:
    """Crop the information bar off the SEM image and measure its red scale bar."""
    from PIL import Image

    im = Image.open(SURVEY / "32096_SEM.tif").convert("RGB")
    a = np.asarray(im).astype(int)
    red = (a[:, :, 0] > 150) & (a[:, :, 1] < 80) & (a[:, :, 2] < 80)

    def longest_run(row_mask):
        best = run = 0
        for v in row_mask:
            run = run + 1 if v else 0
            best = max(best, run)
        return best

    # The scale bar is the one long *unbroken* red line in the bottom strip; the
    # red text on the same rows (filename, voltage) is broken into letters, so
    # counting all red pixels in a row would merge them (that gave 945 px).
    bar_px = max(longest_run(red[r]) for r in range(740, a.shape[0]))
    if bar_px < 30:
        raise ValueError("SEM scale bar not found")
    info_top = 690  # the grey/white information strip starts near here in this image
    Image.fromarray(np.asarray(im)[:info_top]).convert("L").save(OUT / "sem_32096.png")
    meta = {"sample_id": 32096, "source_file": "MCV1-211025B-NT00.tif", "material": "MoS2",
            "scale_bar_um": 3.0, "scale_bar_px": bar_px, "nm_per_px": round(3000 / bar_px, 3),
            "width_px": a.shape[1], "height_px": info_top,
            "note": "Cropped above the instrument's information strip; scale from the 3 µm bar."}
    (OUT / "sem_32096.json").write_text(json.dumps(meta, indent=1))
    print(f"sem: scale bar {bar_px} px = 3 µm -> {meta['nm_per_px']} nm/px")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    index = json.loads((RAW / "extras/fetched.json").read_text())
    transport(index)
    raman(index)
    xrd()
    sem()


if __name__ == "__main__":
    main()
