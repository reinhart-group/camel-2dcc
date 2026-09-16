"""Build the compact record list the dial widget carries inside the page."""
from __future__ import annotations

import json
import pathlib

import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[1]
SLICE = ROOT / "data/slice/camel-2dcc"

SUBSTRATE_WORDS = {"Al2O3", "MgO", "GaAs", "InP", "SiO2", "Si", "C-Al2O3"}


def build() -> list[dict]:
    g = pd.read_csv(SLICE / "growth_summary.csv")
    s = pd.read_csv(SLICE / "samples.csv")[
        ["sample_id", "sample_label", "substrate", "growth_date", "doi"]]
    a = pd.read_csv(SLICE / "afm_summary.csv")[
        ["sample_id", "scan_size_um", "pixels", "lines", "height_range_nm"]]
    m = g.merge(s, on="sample_id", how="left").merge(
        a, on="sample_id", how="left", suffixes=("", "_afm"))

    def num(v, nd):
        return None if pd.isna(v) else round(float(v), nd)

    def txt(v):
        return None if pd.isna(v) else str(v)

    rows = []
    for r in m.itertuples():
        rows.append({
            "id": int(r.sample_id),
            "label": txt(r.sample_label),
            "mat": txt(r.material),
            "sub": txt(r.substrate),
            "meth": txt(r.growth_method),
            "steps": num(r.n_steps, 0),
            "time": num(r.growth_time_min, 1),
            "temp": num(r.growth_temperature_C, 0),
            "press": num(r.growth_pressure_torr, 2),
            "rough": num(r.rms_roughness_nm, 3),
            "hrange": num(r.height_range_nm, 2),
            "scan": num(r.scan_size_um, 2),
            "pix": num(r.pixels, 0),
            "lines": num(r.lines, 0),
            "date": txt(r.growth_date),
            "doi": txt(r.doi),
        })
    return rows


if __name__ == "__main__":
    data = build()
    js = json.dumps(data, separators=(",", ":"))
    print(f"{len(data)} rows, {len(js) / 1024:.0f} KB of JSON")
    print(f"missing time {sum(d['time'] is None for d in data)}, "
          f"missing rough {sum(d['rough'] is None for d in data)}, "
          f"material==substrate {sum(d['mat'] == d['sub'] for d in data)}")
