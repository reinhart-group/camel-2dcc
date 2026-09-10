"""Copy the canonical setup code cell (notebooks/src/_setup_cell.py) into every
notebook source, then rebuild the .ipynb files with jupytext.

The setup code cell is identified as the block that starts with the
``DATA_URL = `` line and ends with the ``print("✅ Data ready`` line.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "notebooks/src"
BLOCK = re.compile(r"^DATA_URL = .*?^print\(\"✅ Data ready.*?$", re.S | re.M)


def main() -> None:
    canonical = BLOCK.search((SRC / "_setup_cell.py").read_text()).group(0)
    for path in sorted(SRC.glob("[0-9][0-9]_*.py")):
        text = path.read_text()
        if not BLOCK.search(text):
            print(f"SKIP {path.name}: no setup block found")
            continue
        path.write_text(BLOCK.sub(lambda _: canonical, text, count=1))
        out = ROOT / "notebooks" / (path.stem + ".ipynb")
        subprocess.run([str(ROOT / ".venv/bin/jupytext"), "--to", "ipynb", str(path), "-o", str(out)],
                       check=True, capture_output=True)
        print(f"synced {path.name} -> {out.name}")


if __name__ == "__main__":
    main()
