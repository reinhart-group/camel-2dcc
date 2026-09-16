"""Shared notebook finalisation.

Every notebook this repo generates must carry a kernelspec. Without one Colab greets the
reader with "No runtime specified; defaulting to python3", which looks like a fault in the
notebook. This has now been forgotten on three separate builders, so it lives in one place.
"""
from __future__ import annotations

import pathlib

import nbformat

REPO = "reinhart-group/camel-2dcc"
BRANCH = "summit-menu"


def badge(path: str) -> str:
    """An Open in Colab badge for a repo-relative notebook path."""
    url = f"https://colab.research.google.com/github/{REPO}/blob/{BRANCH}/{path}"
    return f"[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]({url})"


def write(nb: nbformat.NotebookNode, path: str | pathlib.Path) -> pathlib.Path:
    """Attach the metadata Colab needs, then write the notebook.

    Cell ids are numbered rather than left random. nbformat invents a fresh random id for
    every cell on every build, so rebuilding an unchanged notebook still produced a diff
    touching every cell, which buried the one cell that really did change.
    """
    path = pathlib.Path(path)
    for i, cell in enumerate(nb.cells):
        cell["id"] = f"cell-{i:03d}"
    nb.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3"}
    nb.metadata["language_info"] = {"name": "python"}
    nb.metadata.setdefault("colab", {"provenance": [], "toc_visible": True})
    nbformat.write(nb, str(path))
    return path
