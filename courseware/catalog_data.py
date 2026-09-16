"""Small data payloads for the catalog widgets. Each returns JSON-able rows, rounded."""
from __future__ import annotations

import base64
import io
import json
import pathlib

import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[1]
SLICE = ROOT / "data/slice/camel-2dcc"
SUBSTRATES = {"Al2O3", "MgO", "GaAs", "InP", "SiO2", "Si", "C-Al2O3"}


def _n(v, nd=3):
    return None if pd.isna(v) else round(float(v), nd)


def _t(v):
    return None if pd.isna(v) else str(v)


def canonical(m):
    if m is None or (isinstance(m, float) and pd.isna(m)):
        return None
    base = str(m).split(";")[0].strip()
    return "MoS2" if base == "2H-MoS2" else base


def samples(clean: bool = False, drop_missing: bool = False) -> list[dict]:
    """One row per grown sample: recipe settings joined to its AFM measurement."""
    g = pd.read_csv(SLICE / "growth_summary.csv")
    s = pd.read_csv(SLICE / "samples.csv")[
        ["sample_id", "sample_label", "substrate", "growth_date", "doi"]]
    a = pd.read_csv(SLICE / "afm_summary.csv")[
        ["sample_id", "scan_size_um", "pixels", "lines", "height_range_nm"]]
    m = g.merge(s, on="sample_id", how="left").merge(a, on="sample_id", how="left", suffixes=("", "_afm"))
    rows = []
    for r in m.itertuples():
        rows.append({
            "id": int(r.sample_id), "label": _t(r.sample_label),
            "mat": canonical(r.material) if clean else _t(r.material),
            "sub": _t(r.substrate), "meth": _t(r.growth_method),
            "steps": _n(r.n_steps, 0), "time": _n(r.growth_time_min, 1),
            "temp": _n(r.growth_temperature_C, 0), "press": _n(r.growth_pressure_torr, 2),
            "rough": _n(r.rms_roughness_nm, 3), "hrange": _n(r.height_range_nm, 2),
            "scan": _n(r.scan_size_um, 2), "pix": _n(r.pixels, 0), "lines": _n(r.lines, 0),
            "date": _t(r.growth_date), "doi": _t(r.doi),
            "year": None if pd.isna(r.growth_date) else int(str(r.growth_date)[:4]),
        })
    if clean:
        rows = [d for d in rows if d["mat"] not in SUBSTRATES and d["mat"] != d["sub"]]
    if drop_missing:
        rows = [d for d in rows if d["time"] is not None and d["rough"] is not None]
    return rows


def grains(sample_id: int = 17458, usable_only: bool = True) -> list[dict]:
    g = pd.read_csv(SLICE / "grains/grains.csv")
    g = g[g.sample_id == sample_id]
    if usable_only:
        g = g[(g.kind == "single") & (~g.touches_edge) & (~g.touches_glitch)]
    return [{"spot": str(r.position), "area": _n(r.area_nm2, 0), "side": _n(r.side_nm, 1),
             "height": _n(r.height_nm, 2), "kind": str(r.kind), "row": int(r.row), "col": int(r.col)}
            for r in g.itertuples()]


def recipe(sample_id: int) -> list[dict]:
    r = pd.read_csv(SLICE / "growth_recipes.csv")
    r = r[(r.sample_id == sample_id) & (r.recipe_number == r.recipe_number.min())]
    return [{"step": str(x.step), "n": int(x.step_number), "dur": _n(x.duration_min, 1),
             "start": _n(x.start_min, 1), "temp": _n(x.temperature_C, 0),
             "press": _n(x.pressure_torr, 3)} for x in r.itertuples()]


def transport() -> list[dict]:
    t = pd.read_csv(SLICE / "extras/transport_fese.csv")
    sid = t.sample_id.iloc[0]
    t = t[t.sample_id == sid].sort_values("temperature_K")
    return [{"T": _n(x.temperature_K, 2), "R": _n(x.resistance_ohm, 4)} for x in t.itertuples()]


def raman_peaks() -> list[dict]:
    p = pd.read_csv(SLICE / "extras/raman_peaks.csv")
    return [{"id": int(x.sample_id), "mat": str(x.material), "e2g": _n(x.E2g_cm1, 2),
             "a1g": _n(x.A1g_cm1, 2), "sep": _n(x.separation_cm1, 2)} for x in p.itertuples()]


def raman_spectrum(sample_id: int, every: int = 3) -> list[list[float]]:
    s = pd.read_csv(SLICE / "extras/raman_spectra.csv")
    s = s[s.sample_id == sample_id].sort_values("raman_shift_cm1").iloc[::every]
    return [[_n(x.raman_shift_cm1, 1), _n(x.intensity, 1)] for x in s.itertuples()]


def heightmap(key: str, size: int = 96) -> dict:
    """A gallery scan as a base64 PNG plus its real extent, so the page carries an image."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    z = np.load(SLICE / f"afm_gallery/{key}.npz")
    h = z["height_nm"]
    step = max(1, h.shape[0] // size)
    h = h[::step, ::step]
    lo, hi = np.percentile(h, [1, 99])
    fig, ax = plt.subplots(figsize=(3.2, 3.2), dpi=110)
    ax.imshow(h, cmap="afmhot", vmin=lo, vmax=hi, origin="lower")
    ax.axis("off")
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", pad_inches=0)
    plt.close(fig)
    meta = json.loads((SLICE / "afm_gallery/gallery.json").read_text())
    info = meta[key] if isinstance(meta, dict) else next(m for m in meta if m.get("key") == key)
    return {"png": base64.b64encode(buf.getvalue()).decode(),
            "width_um": float(z["x_um"].max()), "info": {k: str(v) for k, v in info.items()},
            "heights": [[round(float(v), 3) for v in row] for row in h[::2, ::2]]}


def grain_scan(key: str, size: int = 128) -> dict:
    z = np.load(SLICE / f"grains/{key}.npz")
    h = z["height_nm"] if "height_nm" in z else z[z.files[0]]
    step = max(1, h.shape[0] // size)
    return {"n": int(h.shape[0]), "step": step,
            "heights": [[round(float(v), 2) for v in row] for row in h[::step, ::step]]}


def chips_timeline() -> list[dict]:
    c = pd.read_csv(SLICE / "chips_timeline.csv")
    return [{k: (_n(v) if isinstance(v, (int, float, np.floating)) else _t(v))
             for k, v in row.items()} for row in c.to_dict("records")]


def compact(rows: list[dict], keys: list[str]) -> dict:
    """Columnar form: {"cols": [...], "rows": [[...], ...]}. Halves the payload."""
    return {"cols": keys, "rows": [[r.get(k) for k in keys] for r in rows]}
