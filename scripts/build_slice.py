"""Stage 4: assemble the classroom data slice from the raw pulls.

Inputs (from stages 1-3): data/raw/list_samples.json, afm_files.json,
afm_measurements.json, afm64/*.npy, recipes.json, spm/*.spm; plus
data/curated/*.csv and scripts/gallery_picks.json.

Output: data/slice/camel-2dcc/ (the folder students unzip) and
data/slice/camel-2dcc-v1.zip. Nothing here touches the network.
"""

from __future__ import annotations

import hashlib
import json
import shutil
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from camel_data.classroom import AFMScan, to_stl  # noqa: E402
from camel_data.spm import flatten, height_channel, read_spm  # noqa: E402

RELEASE = "camel-2dcc-v1"
RAW = ROOT / "data/raw"
CURATED = ROOT / "data/curated"
OUT = ROOT / "data/slice/camel-2dcc"

DOI_PREFIX = "10."


def _package(row: dict) -> tuple[str | None, str | None]:
    if not row["dataPackages"]:
        return None, None
    d = row["dataPackages"][0]
    doi = d["routeKey"] if d["routeKey"].startswith(DOI_PREFIX) else None
    return d["label"], doi


def build_samples(rows: list[dict]) -> pd.DataFrame:
    """One row per public sample. Material spellings are left as entered (messy on purpose)."""
    out = []
    for r in rows:
        pkg, doi = _package(r)
        out.append({
            "sample_id": r["id"],
            "sample_label": r["sampleLabel"],
            "materials": "; ".join(r["materials"]),
            "substrate": "; ".join(r.get("substrateMaterials") or []),
            "growth_method": "; ".join(r["synthesisTechniques"]),
            "measurements": "; ".join(r["characterizationTechniques"]),
            "n_measurement_types": len(r["characterizationTechniques"]),
            "date_created": (r.get("creationDate") or "")[:10],
            "growth_date": ((r.get("growthDates") or [""])[0] or "")[:10],
            "data_package": pkg,
            "doi": doi,
        })
    return pd.DataFrame(out).sort_values("sample_id")


def build_afm_summary(samples: pd.DataFrame, meas: dict) -> pd.DataFrame:
    s = samples.set_index("sample_id")
    out = []
    for sid, m in meas.items():
        row = s.loc[int(sid)]
        out.append({
            "sample_id": int(sid),
            "material": row["materials"].split("; ")[0] if row["materials"] else None,
            "substrate": row["substrate"] or None,
            "growth_method": row["growth_method"] or None,
            "date_created": row["date_created"],
            "scan_size_um": m["scan_size_um"],
            "pixels": m["pixels"],
            "rms_roughness_nm": m["rms_nm"],
            "avg_roughness_nm": m["ra_nm"],
            "height_range_nm": m["range_nm"],
            "instrument": m["instrument"],
            "data_package": row["data_package"],
            "doi": row["doi"],
        })
    return pd.DataFrame(out).sort_values("sample_id")


def _num(value) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


# Recipe templates in LiST name the same quantity differently. Map each
# step-based template onto: duration (min), temperature (°C), pressure (Torr).
# Plain "MBE" recipes are timestamped instrument logs, not step tables, so they
# are left out of the classroom table (still in data/raw/recipes.json).
_TEMPLATES = {
    "MOCVD": {"duration": ("t", 1 / 60), "temp": "T", "pressure": "P"},
    "Hybrid MBE": {"duration": ("time", 1.0), "temp": "t_subst", "pressure": "p"},
}


def build_recipes(samples: pd.DataFrame, recipes: dict) -> pd.DataFrame:
    """One row per growth step for MOCVD and hybrid-MBE recipes."""
    s = samples.set_index("sample_id")
    out = []
    for sid, recs in recipes.items():
        for r_i, rec in enumerate(recs, 1):
            spec = _TEMPLATES.get(rec.get("technique"))
            if spec is None:
                continue
            for group in rec["groups"]:
                if group.get("symbol") != "recipe":
                    continue
                elapsed = 0.0
                for i, row in enumerate(group["rows"], 1):
                    key, factor = spec["duration"]
                    dur = _num(row.get(key))
                    dur = None if dur is None else round(dur * factor, 3)
                    out.append({
                        "sample_id": int(sid),
                        "material": s.loc[int(sid), "materials"],
                        "growth_method": rec["technique"],
                        "recipe_number": r_i,
                        "step_number": i,
                        "step": (row.get("step") or "").strip() or None,
                        "duration_min": dur,
                        "start_min": round(elapsed, 3),
                        "temperature_C": _num(row.get(spec["temp"])),
                        "pressure_torr": _num(row.get(spec["pressure"])),
                        "open_shutters": row.get("shutters"),
                    })
                    elapsed += dur or 0.0
    return pd.DataFrame(out)


def build_growth_summary(steps: pd.DataFrame, afm: pd.DataFrame) -> pd.DataFrame:
    """One row per sample: total growth-step time and temperature, joined to AFM roughness.

    A 'growth step' is any step whose name contains 'growth' or 'deposit'
    (case-insensitive) but is not a pre-/post-growth anneal ('pre-growth',
    'post-growth', 'P.G.'). Samples with no such step keep blank growth values.
    """
    name = steps["step"].fillna("").str.lower()
    is_growth = (name.str.contains("growth|deposit")
                 & ~name.str.contains(r"pre-growth|post-growth|p\.g\.", regex=True))
    g = steps[is_growth].groupby("sample_id").agg(
        growth_time_min=("duration_min", "sum"),
        growth_temperature_C=("temperature_C", "max"),
        growth_pressure_torr=("pressure_torr", "median"),
        n_growth_steps=("step", "size"),
    )
    base = steps.groupby("sample_id").agg(material=("material", "first"),
                                          growth_method=("growth_method", "first"),
                                          total_recipe_min=("duration_min", "sum"),
                                          n_steps=("step_number", "size"))
    out = base.join(g).reset_index()
    return out.merge(afm[["sample_id", "rms_roughness_nm", "scan_size_um"]], on="sample_id", how="left")


def build_gallery(picks: list[dict], meas: dict, samples: pd.DataFrame) -> list[dict]:
    gdir = OUT / "afm_gallery"
    gdir.mkdir(parents=True, exist_ok=True)
    s = samples.set_index("sample_id")
    cands = {(c["sample_id"], c["file"]): c["local"]
             for c in json.loads((RAW / "gallery_candidates.json").read_text()) if "local" in c}
    meta = []
    for p in picks:
        spm = ROOT / cands[(p["sample_id"], p["file"])]
        h = height_channel(read_spm(spm))
        if h.data.shape[0] != h.data.shape[1]:
            raise ValueError(f"gallery pick {p['key']} is not square: {h.data.shape}")
        z = flatten(h.data).astype(np.float32)
        n = z.shape[0]
        axis_um = np.linspace(0, h.scan_size_nm / 1000, n, dtype=np.float32)
        np.savez_compressed(gdir / f"{p['key']}.npz", height_nm=z, x_um=axis_um, y_um=axis_um)
        meta.append({
            "key": p["key"], "sample_id": p["sample_id"], "material": p["material"],
            "title": p["title"], "story": p["story"], "scan_um": round(h.scan_size_nm / 1000, 4),
            "pixels": n, "rms_roughness_nm": round(float(np.std(z)), 4),
            "processing": "per-line linear flatten, median set to 0",
            "data_package": s.loc[p["sample_id"], "data_package"], "doi": s.loc[p["sample_id"], "doi"],
            "source_file": spm.name.split("_", 1)[1],
        })
    (gdir / "gallery.json").write_text(json.dumps(meta, indent=1))
    return meta


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    rows = json.loads((RAW / "list_samples.json").read_text())
    meas = json.loads((RAW / "afm_measurements.json").read_text())
    recipes = json.loads((RAW / "recipes.json").read_text())
    picks = json.loads((ROOT / "scripts/gallery_picks.json").read_text())

    samples = build_samples(rows)
    samples.to_csv(OUT / "samples.csv", index=False)
    afm = build_afm_summary(samples, meas)
    afm.to_csv(OUT / "afm_summary.csv", index=False)
    steps = build_recipes(samples, recipes)
    steps.to_csv(OUT / "growth_recipes.csv", index=False)
    build_growth_summary(steps, afm).to_csv(OUT / "growth_summary.csv", index=False)
    for f in CURATED.glob("*"):
        shutil.copy(f, OUT / f.name)

    small = {str(p.stem): np.load(p) for p in sorted((RAW / "afm64").glob("*.npy")) if p.stem in meas}
    np.savez_compressed(OUT / "afm_small.npz", **small)

    gallery = build_gallery(picks, meas, samples)
    (OUT / "stl").mkdir()
    for g in gallery[:2]:
        with np.load(OUT / "afm_gallery" / f"{g['key']}.npz") as blob:
            scan = AFMScan(key=g["key"], z=blob["height_nm"].astype(float), scan_um=g["scan_um"],
                           material=g["material"], title=g["title"], story=g["story"],
                           sample_id=g["sample_id"], doi=g["doi"])
        to_stl(scan, OUT / "stl" / f"{g['key']}.stl")

    shutil.copytree(ROOT / "src/camel_data", OUT / "camel_data",
                    ignore=shutil.ignore_patterns("__pycache__", "list_public.py"))
    shutil.copy(ROOT / "docs/slice-README.md", OUT / "README.md")

    files = sorted(p for p in OUT.rglob("*") if p.is_file())
    manifest = {
        "release_id": RELEASE,
        "created_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "source_system": "2DCC-MIP LiST (Lifetime Sample Tracking), public Published records only",
        "public_sample_count_at_extract": len(rows),
        "afm_scans_measured": len(meas),
        "license": "CC-BY-4.0 — cite the 2DCC data package DOI listed for each sample",
        "files": [{"path": str(p.relative_to(OUT)), "bytes": p.stat().st_size, "sha256": sha256(p)}
                  for p in files],
    }
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=1))

    # Write the zip beside the final name, then swap it in atomically so a
    # notebook run that is copying the old zip never sees a half-written file.
    zpath = OUT.parent / f"{RELEASE}.zip"
    tmp = zpath.with_suffix(".zip.tmp")
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zf:
        for p in sorted(OUT.rglob("*")):
            if p.is_file():
                zf.write(p, Path("camel-2dcc") / p.relative_to(OUT))
    tmp.replace(zpath)
    print(f"wrote {zpath} ({zpath.stat().st_size / 1e6:.1f} MB), {len(files)} files")


if __name__ == "__main__":
    main()
