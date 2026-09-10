"""Execute notebooks headlessly against the local data slice.

Usage: .venv/bin/python scripts/run_notebook.py notebooks/01_nano_landscapes.ipynb [...]

Runs each notebook in a scratch folder that contains the built slice zip, so
the setup cell takes its "uploaded zip" path exactly as it would in Colab.
Executed copies go to notebooks/executed/. Exit code 1 if any notebook fails.
"""

from __future__ import annotations

import shutil
import sys
import tempfile
from pathlib import Path

import nbformat
from nbclient import NotebookClient
from nbclient.exceptions import CellExecutionError

ROOT = Path(__file__).resolve().parents[1]
ZIP = ROOT / "data/slice/camel-2dcc-v1.zip"


def run(path: Path) -> bool:
    nb = nbformat.read(path, as_version=4)
    with tempfile.TemporaryDirectory() as work:
        shutil.copy(ZIP, Path(work) / ZIP.name)
        client = NotebookClient(nb, timeout=300, kernel_name="python3",
                                resources={"metadata": {"path": work}})
        try:
            client.execute()
            ok = True
        except CellExecutionError as exc:
            print(f"FAIL {path.name}\n{str(exc)[:3000]}")
            ok = False
    out = ROOT / "notebooks/executed" / path.name
    out.parent.mkdir(exist_ok=True)
    nbformat.write(nb, out)
    if ok:
        print(f"OK   {path.name} -> {out.relative_to(ROOT)}")
    return ok


if __name__ == "__main__":
    if not ZIP.exists():
        sys.exit(f"missing {ZIP}; run scripts/build_slice.py first")
    results = [run(Path(p)) for p in sys.argv[1:]]
    sys.exit(0 if all(results) else 1)
