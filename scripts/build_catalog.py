"""Render every catalog item to saved-output notebooks, one per activity round.

Usage: PYTHONPATH=courseware .venv/bin/python scripts/build_catalog.py
"""
from __future__ import annotations

import json
import pathlib
import sys

import nbformat

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "courseware"))

import catalog  # noqa: E402

WIDGETS = ROOT / "courseware/widgets"
CORE = (WIDGETS / "core.js").read_text()
SHELL = (WIDGETS / "shell.html").read_text()
OUT = ROOT / "notebooks/catalog"


def render(item: dict) -> str:
    js = (WIDGETS / "items" / (item["item"] + ".js")).read_text()
    payload = item["data"]()
    html = SHELL.replace("__ID__", "cw-" + item["id"].lower().replace(".", "-"))
    html = html.replace("__CORE__", CORE)
    html = html.replace("__DATA__", json.dumps(payload, separators=(",", ":")))
    html = html.replace("__OPT__", json.dumps(item.get("opts", {}), separators=(",", ":")))
    return html.replace("__ITEM__", js.strip().rstrip(";"))


def notebook_for(round_key: str, entries: list[dict]) -> nbformat.NotebookNode:
    nb = nbformat.v4.new_notebook()
    title = catalog.ROUNDS[round_key]
    index = "\n".join(f"- **{e['id']}** {e['title']} — {e['blurb']}" for e in entries)
    nb.cells.append(nbformat.v4.new_markdown_cell(
        f"# {title}\n\n"
        "Every item below already works: tap, drag, and choose. Nothing needs to be signed in to "
        "or run. Tell us which item IDs you want and we will refine those.\n\n"
        f"{index}\n"))
    for e in entries:
        nb.cells.append(nbformat.v4.new_markdown_cell(
            f"## {e['id']} — {e['title']}\n\n"
            f"{e['blurb']}\n\n"
            f"*Grades {e['grades']}. Data: {e['source']}.*"))
        cell = nbformat.v4.new_code_cell(source=f"# {e['id']}: the working version is saved below.")
        cell.outputs = [nbformat.v4.new_output(
            "display_data", data={"text/html": render(e), "text/plain": f"<{e['id']} widget>"})]
        nb.cells.append(cell)
    nb.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3"}
    return nb


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    items = catalog.items()
    if not items:
        print("no items registered")
        return 1
    total = 0
    for key in catalog.ROUNDS:
        entries = [e for e in items if e["round"] == key]
        if not entries:
            continue
        path = OUT / f"{key}.ipynb"
        nbformat.write(notebook_for(key, entries), path)
        kb = path.stat().st_size / 1024
        total += kb
        print(f"{path.relative_to(ROOT)}: {len(entries)} items, {kb:.0f} KB")
    print(f"{len(items)} items, {total / 1024:.1f} MB total")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
