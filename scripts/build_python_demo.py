"""Build notebooks/python_demo.ipynb from its jupytext source, execute it, and give every
interactive cell a still preview.

Why the preview matters: `interact` saves an ipywidgets view, which is inert without a
kernel. A reader who opens this notebook without signing in would see the markdown, two
pictures, and then four blank gaps. This notebook is deliberately the one that needs a
runtime, but a blank gap reads as broken rather than as an invitation, so each interactive
cell also carries a PNG of its default state.

Usage: .venv/bin/python scripts/build_python_demo.py
"""
from __future__ import annotations

import base64
import io
import pathlib
import subprocess
import sys

import nbformat

ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "notebooks/src/python_demo.py"
OUT = ROOT / "notebooks/python_demo.ipynb"
SLICE = ROOT / "data/slice/camel-2dcc"


def previews() -> dict[str, str]:
    """Render the default state of each interactive cell as a base64 PNG.

    These mirror the notebook's own functions. They are kept deliberately short and are
    checked against the notebook source by test_python_demo.py, so a change to one without
    the other is caught rather than silently drifting.
    """
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import pandas as pd

    films = pd.read_csv(SLICE / "growth_summary.csv")
    out = {}

    def grab(key):
        buf = io.BytesIO()
        plt.savefig(buf, format="png", dpi=110, bbox_inches="tight")
        plt.close("all")
        out[key] = base64.b64encode(buf.getvalue()).decode()

    cut_off_at, bins = 15, 30
    kept = films[films["rms_roughness_nm"] <= cut_off_at]["rms_roughness_nm"]
    hidden = films["rms_roughness_nm"].count() - kept.count()
    kept.plot.hist(bins=bins, figsize=(7, 3))
    plt.title("%d films shown, %d above %d nm not shown" % (kept.count(), hidden, cut_off_at))
    plt.xlabel("roughness (nm)")
    grab("roughness")

    keep = films["growth_time_min"].notna() & films["rms_roughness_nm"].notna()
    total = films.groupby("growth_method").size()
    left = films[keep].groupby("growth_method").size().reindex(total.index, fill_value=0)
    ax = total.plot.bar(figsize=(7, 3), color="lightgrey", label="all rows")
    left.plot.bar(ax=ax, color="steelblue", label="rows that survive")
    ax.set_title("%d of %d rows survive" % (keep.sum(), len(films)))
    ax.legend()
    grab("survivors")

    few = ["material", "growth_time_min", "rms_roughness_nm"]
    drawable = films[few].dropna()
    drawable.plot.scatter(x="growth_time_min", y="rms_roughness_nm", alpha=0.4, figsize=(7, 3),
                          title="growth time vs roughness, %d films" % len(drawable))
    grab("dials")
    out["your_version"] = out["roughness"]
    return out


def execute(nb) -> None:
    """Run the notebook so its plain cells carry real output.

    Run in a scratch directory with the local slice symlinked in, so the setup cell finds
    the data it would otherwise download. Only the pip line is skipped: it installs this
    same package from GitHub, which is already importable here. Any cell that raises is a
    build failure, because a demo whose code does not run is worse than no demo.
    """
    import tempfile
    from nbclient import NotebookClient

    for cell in nb.cells:
        if cell.cell_type == "code" and "!pip install" in cell.source:
            cell.source = "\n".join(l for l in cell.source.splitlines()
                                    if not l.lstrip().startswith("!pip"))

    with tempfile.TemporaryDirectory() as tmp:
        (pathlib.Path(tmp) / "camel-2dcc").symlink_to(SLICE, target_is_directory=True)
        NotebookClient(nb, timeout=240, kernel_name="python3",
                       resources={"metadata": {"path": tmp}}).execute()

    errors = [o for c in nb.cells for o in c.get("outputs", []) if o.output_type == "error"]
    if errors:
        raise RuntimeError(f"{len(errors)} cell(s) raised: {errors[0].ename}: {errors[0].evalue}")

    # Put the install line back; readers need it, this machine does not.
    src = SRC.read_text()
    install = next(l for l in src.splitlines() if l.startswith("!pip install"))
    for cell in nb.cells:
        if cell.cell_type == "code" and "DATA_URL =" in cell.source:
            cell.source = install + "\n\n" + cell.source.lstrip("\n")


def main() -> int:
    if not (SLICE / "growth_summary.csv").exists():
        print(f"data slice missing at {SLICE}", file=sys.stderr)
        return 1
    subprocess.run([str(ROOT / ".venv/bin/jupytext"), "--to", "ipynb", str(SRC), "-o", str(OUT)],
                   check=True, capture_output=True)
    nb = nbformat.read(OUT, as_version=4)
    execute(nb)

    pics = previews()
    for cell in nb.cells:
        if cell.cell_type != "code":
            continue
        # Match the function the cell defines, not any substring: "roughness" also occurs
        # inside the column name "rms_roughness_nm", which silently paired the wrong picture.
        key = next((k for k in pics if f"def {k}(" in cell.source), None)
        if key and "interact" in cell.source:
            cell.outputs = [nbformat.v4.new_output(
                "display_data", metadata={},
                data={"image/png": pics[key],
                      "text/plain": "<a still preview; connect a runtime to move the controls>"})]

    nb.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3"}
    nb.metadata["language_info"] = {"name": "python"}
    nb.metadata["colab"] = {"provenance": [], "toc_visible": True}
    nbformat.write(nb, OUT)
    kb = OUT.stat().st_size / 1024
    print(f"{OUT.relative_to(ROOT)}: {len(nb.cells)} cells, {kb:.0f} KB, "
          f"{sum(1 for c in nb.cells if c.get('outputs'))} cells carry a saved picture")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
