"""The summit session page has to work for a team with no account and no runtime.

These tests guard the properties that break silently. A team at a conference cannot debug a
page, so each of these was a real failure mode at some point in this project.
"""
import json
import pathlib

import nbformat
import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
PATH = ROOT / "notebooks/summit/modeling_the_messy.ipynb"


@pytest.fixture(scope="module")
def nb():
    return nbformat.read(PATH, as_version=4)


@pytest.fixture(scope="module")
def widget_outputs(nb):
    out = []
    for cell in nb.cells:
        if cell.cell_type == "code":
            for o in cell.get("outputs", []):
                html = o.get("data", {}).get("text/html")
                if html:
                    out.append((cell.source.strip(), html))
    return out


def test_every_code_cell_carries_a_saved_picture(nb):
    """A code cell with no saved output shows nothing to a reader without a kernel."""
    for cell in nb.cells:
        if cell.cell_type == "code":
            assert cell.get("outputs"), f"{cell.source!r} has no saved output"


def test_expected_activities_are_present(widget_outputs):
    labels = [src for src, _ in widget_outputs]
    for item_id in ("W-01", "W-02", "M-05", "M-02", "M-11", "G-01", "G-15", "G-06", "D-01"):
        assert any(item_id in label for label in labels), f"{item_id} missing from the page"


def test_exactly_one_3d_viewer(widget_outputs):
    """Safari keeps at most one live WebGL context per page; a second blanks them all.

    See docs/summit/webgl-3d-constraint.md. The three warm-up scans are allowed because they
    share a single viewer inside a single output, which is why this counts outputs rather
    than scans.
    """
    with_plotly = [src for src, html in widget_outputs if "Plotly.newPlot" in html]
    assert len(with_plotly) == 1, f"expected one 3D output, found {len(with_plotly)}: {with_plotly}"


def test_nothing_fetches_data_at_read_time(nb):
    """Every activity must run from data carried inside the page, on a dead conference network."""
    blob = json.dumps(nb)
    for pattern in ("fetch(", "XMLHttpRequest", "<script src"):
        assert pattern not in blob, f"the page reaches out over the network with {pattern}"


def test_3d_figures_use_plain_arrays(widget_outputs):
    """plotly.py encodes numpy as base64; older plotly.js draws the axes and no surface."""
    for src, html in widget_outputs:
        assert "bdata" not in html, f"{src} carries base64 arrays"


def test_the_glitch_image_is_legible():
    """W-01's picture was shipped twice at a resolution and colour depth that hid its point.

    The scan's one corrupted line is the strongest provenance lesson on the page, and at
    317x237 with a 64-colour palette it was banded and hard to see.
    """
    import base64
    import io
    import sys

    sys.path.insert(0, str(ROOT / "courseware"))
    from PIL import Image

    import catalog_data_a as cda

    img = Image.open(io.BytesIO(base64.b64decode(cda.small_heightmap("wse2_triangles")["img"])))
    assert img.width >= 480 and img.height >= 380, f"too small at {img.size}"
    assert len(img.convert("RGB").getcolors(maxcolors=100000)) > 128, "too few colours; it bands"
