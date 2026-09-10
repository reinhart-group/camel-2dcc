"""Export a standalone showcase for the OneDrive folder: one self-contained
interactive 3D HTML page per gallery scan (plus an index), and the STL files.

Offline: reads data/slice/camel-2dcc/. Output: data/slice/showcase/.
"""

from __future__ import annotations

import html
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from camel_data.classroom import load_gallery, surface_3d, to_stl  # noqa: E402

SLICE = ROOT / "data/slice/camel-2dcc"
OUT = ROOT / "data/slice/showcase"
STRETCH = {"atomic_staircase": 150, "smoothest_surface": 150, "mos2_film": 100}


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "3d").mkdir(parents=True)
    (OUT / "stl").mkdir()
    gallery = load_gallery(SLICE)
    items = []
    for key, scan in gallery.items():
        fig = surface_3d(scan, exaggeration=STRETCH.get(key, 30), max_pixels=200)
        # plotly.js loads from its CDN, keeping each page small; pages need internet access.
        fig.write_html(OUT / "3d" / f"{key}.html", include_plotlyjs="cdn")
        to_stl(scan, OUT / "stl" / f"{key}.stl")
        items.append((key, scan))
    rows = "\n".join(
        f"<li><a href='3d/{k}.html'><b>{html.escape(s.title)}</b></a> ({s.material}, "
        f"{s.scan_um:g} µm) — {html.escape(s.story)} "
        f"<a href='stl/{k}.stl'>STL</a>{' · DOI ' + s.doi if s.doi else ''}</li>"
        for k, s in items)
    (OUT / "index.html").write_text(
        "<meta charset='utf-8'><title>CAMEL × 2DCC AFM gallery</title>"
        "<body style='font-family:system-ui;max-width:900px;margin:2em auto;padding:0 1em'>"
        "<h1>CAMEL × 2DCC AFM gallery</h1><p>Real atomic force microscope scans from Penn State's "
        "2D Crystal Consortium. Drag to rotate; heights are stretched so nanometre bumps show. "
        "Each STL is a 100 mm-wide printable model (15 mm relief on a 3 mm base).</p>"
        f"<ul>{rows}</ul></body>")
    print(f"wrote {len(items)} pages and STLs to {OUT}")


if __name__ == "__main__":
    main()
