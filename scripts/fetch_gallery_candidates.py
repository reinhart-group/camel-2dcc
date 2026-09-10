"""Download a few specific AFM scans per candidate sample and render a contact sheet.

Used once to choose the gallery by eye. Files land in data/raw/spm/gallery/;
the sheet goes to data/raw/gallery_candidates.png and a table to
data/raw/gallery_candidates.json.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from camel_data.list_public import PublicLiST  # noqa: E402
from camel_data.spm import flatten, height_channel, read_spm, rms_roughness  # noqa: E402

RAW = Path("data/raw")
GDIR = RAW / "spm/gallery"
CANDIDATES = [29974, 21724, 20390, 20381, 20382, 29967, 50210, 23451, 20398, 32093, 17393, 17458,
              17406, 26875, 39165, 23056, 22630, 23420, 23410, 17853, 31779, 24906]


def main() -> None:
    # Usage: fetch_gallery_candidates.py [--per N] [--out NAME] [sample_id ...]
    args = sys.argv[1:]
    per, out = 3, "gallery_candidates"
    if "--per" in args:
        i = args.index("--per"); per = int(args[i + 1]); del args[i:i + 2]
    if "--out" in args:
        i = args.index("--out"); out = args[i + 1]; del args[i:i + 2]
    candidates = [int(a) for a in args] or CANDIDATES
    GDIR.mkdir(parents=True, exist_ok=True)
    idx = json.loads((RAW / "afm_files.json").read_text())
    client = PublicLiST()
    table = []
    for sid in candidates:
        spm = [f for f in idx[str(sid)] if f["filename"].lower().endswith(".spm")
               and "modif" not in f["filename"].lower() and "_mod" not in f["filename"].lower()]
        for f in spm[:per]:
            path = GDIR / f"{sid}_{re.sub(r'[^A-Za-z0-9._-]+', '_', f['filename'])}"
            try:
                if not path.exists():
                    path.write_bytes(client.download(f["activity_id"], f["file_id"]))
                h = height_channel(read_spm(path))
            except Exception as exc:  # noqa: BLE001 — shown in the table
                table.append({"sample_id": sid, "file": f["filename"], "error": f"{type(exc).__name__}: {exc}"})
                continue
            z = flatten(h.data)
            table.append({"sample_id": sid, "file": f["filename"], "local": str(path),
                          "scan_um": h.scan_size_nm / 1000, "pixels": h.data.shape[0],
                          "rms_nm": round(rms_roughness(z), 3), "_z": z})
    ok = [t for t in table if "_z" in t]
    cols = 6
    rows = -(-len(ok) // cols)
    fig, axes = plt.subplots(rows, cols, figsize=(cols * 3.2, rows * 3.4))
    for ax, t in zip(axes.flat, ok):
        lo, hi = np.percentile(t["_z"], [1, 99])
        ax.imshow(t["_z"], cmap="viridis", vmin=lo, vmax=hi)
        ax.set_title(f"{t['sample_id']} {t['scan_um']:g}µm rms {t['rms_nm']}\n{t['file'][:34]}", fontsize=7)
        ax.axis("off")
    for ax in list(axes.flat)[len(ok):]:
        ax.axis("off")
    plt.tight_layout()
    plt.savefig(RAW / f"{out}.png", dpi=80)
    for t in table:
        t.pop("_z", None)
    prev = RAW / f"{out}.json"
    old = json.loads(prev.read_text()) if prev.exists() else []
    seen = {(t["sample_id"], t["file"]) for t in table}
    prev.write_text(json.dumps(table + [t for t in old if (t["sample_id"], t["file"]) not in seen], indent=1))
    print(f"{len(ok)} scans rendered, {len(table) - len(ok)} errors")


if __name__ == "__main__":
    main()
