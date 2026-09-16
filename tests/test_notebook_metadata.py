"""Every notebook we ship must open cleanly in Colab.

A notebook with no kernelspec makes Colab announce "No runtime specified; defaulting to
python3" before the reader has done anything, which reads as a broken file. This test fails
if any generated notebook is missing that metadata.
"""
import pathlib

import nbformat
import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
NOTEBOOKS = sorted(ROOT.glob("notebooks/**/*.ipynb"))


@pytest.mark.parametrize("path", NOTEBOOKS, ids=lambda p: p.name)
def test_has_kernelspec(path):
    nb = nbformat.read(path, as_version=4)
    assert nb.metadata.get("kernelspec", {}).get("name") == "python3", (
        f"{path.relative_to(ROOT)} has no kernelspec; Colab will say 'No runtime specified'"
    )
