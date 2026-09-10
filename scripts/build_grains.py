"""Build the grain dataset for notebook 06 from specific AFM scans.

Offline: reads scans already downloaded by fetch_gallery_candidates.py
(data/raw/grain_candidates*.json). Writes data/raw/grains/:
- <key>.npz  height_nm (levelled on the substrate), labels (grain id per pixel)
- grains.csv one row per grain with its scan, wafer position, and shape numbers
- scans.json one entry per scan: sample, position, growth note, threshold, counts
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from camel_data.grains import find_grains, level_on_substrate  # noqa: E402
from camel_data.spm import height_channel, read_spm  # noqa: E402

RAW = ROOT / "data/raw"
OUT = RAW / "grains"

# (key, sample_id, file, wafer position, role, growth note from the LiST record)
SCANS = [
    ("wse2_17458_center", 17458, "Center.0_00000.spm", "center", "population",
     "WSe2 on sapphire, MOCVD, 850 °C nucleation, no ripening step"),
    ("wse2_17458_flat", 17458, "To the flat.0_00000.spm", "toward the flat", "population",
     "WSe2 on sapphire, MOCVD, 850 °C nucleation, no ripening step"),
    ("wse2_17458_edge", 17458, "To the edge.0_00000.spm", "toward the edge", "population",
     "WSe2 on sapphire, MOCVD, 850 °C nucleation, no ripening step"),
    # Recipes (growth_recipes.csv): 17458 = 30 s nucleation at 850 °C, no ripening;
    # 17464 = 30 s nucleation at 875 °C then a 10 min ripening step. Neither has a
    # separate "Growth" step. They differ in two settings, so this is a comparison
    # of two recipes, not a growth time series.
    ("wse2_17464_center", 17464, "Center.0_00000.spm", "center", "second recipe",
     "WSe2 on sapphire, MOCVD, 875 °C nucleation then 10 min ripening"),
    # Left out: 17457 (5 min) — glitch lines and dust dominate the pixels above
    # the noise, so the rule's cutoff jumps to ~7.8 nm; and the 30-min samples
    # (17459/17462/17463) — the film nearly covers the surface, so "substrate =
    # the lower half of pixels" fails (17463 came out at 25% covered).
    ("wse2_24111_center", 24111, "MCV1-230811A-CC_230816-Center-1 um.0_00001.spm", "center", "line scans",
     "WSe2 on sapphire, MOCVD, 20 min growth, big triangles"),
    ("snse_39166_top", 39166, "230723A-JC-32-Top.0_00001.spm", "top", "line scans",
     "SnSe on MgO, hybrid MBE, stacked grains"),
]


def _local(sample_id: int, file: str) -> Path:
    for name in ("grain_candidates.json", "grain_candidates2.json", "gallery_candidates.json"):
        p = RAW / name
        if p.exists():
            for c in json.loads(p.read_text()):
                if c["sample_id"] == sample_id and c["file"] == file and "local" in c:
                    return ROOT / c["local"]
    raise FileNotFoundError(f"{sample_id} {file!r} not downloaded; run fetch_gallery_candidates.py")


def main() -> None:
    import shutil

    shutil.rmtree(OUT, ignore_errors=True)  # no stale maps from earlier scan lists
    OUT.mkdir(parents=True)
    rows, scans = [], []
    for key, sid, file, position, role, note in SCANS:
        h = height_channel(read_spm(_local(sid, file)))
        if h.data.shape[0] != h.data.shape[1]:
            raise ValueError(f"{key}: not square {h.data.shape}")
        z = level_on_substrate(h.data)
        px = h.scan_size_nm / h.data.shape[1]
        if role == "line scans":
            # The height rule outlines bright rims / pyramid tops here, not whole
            # grains, so these scans are shipped for line profiles only.
            labels, table, thr = np.zeros(z.shape, dtype=np.int32), [], float("nan")
        else:
            labels, table, thr = find_grains(z, px)
        np.savez_compressed(OUT / f"{key}.npz", height_nm=z.astype(np.float32),
                            labels=labels.astype(np.int32))
        for t in table:
            rows.append({"scan": key, "sample_id": sid, "position": position, "role": role, **t})
        whole = [t for t in table if t["kind"] == "single" and not t["touches_edge"] and not t["touches_glitch"]]
        covered = float((labels > 0).mean())
        scans.append({"key": key, "sample_id": sid, "file": file, "position": position, "role": role,
                      "growth_note": note, "scan_um": round(h.scan_size_nm / 1000, 4),
                      "pixel_nm": round(px, 4), "threshold_nm": round(thr, 3),
                      "n_grains": len(table), "n_single_whole": len(whole),
                      "covered_fraction": round(covered, 4)})
        print(f"{key:20s} grains {len(table):4d} single+whole {len(whole):4d} covered {covered:.1%}")
    df = pd.DataFrame(rows)
    num = df.select_dtypes("float").columns
    df[num] = df[num].round(3)
    df.to_csv(OUT / "grains.csv", index=False)
    (OUT / "scans.json").write_text(json.dumps(scans, indent=1))


if __name__ == "__main__":
    main()
