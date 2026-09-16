"""The 3D surfaces once rendered an empty box on a phone.

plotly.py 7.0.0 encodes numeric arrays as base64 ("bdata") but reports its paired
plotly.js version as 4.0.0, so include_plotlyjs="cdn" emitted a script tag for a 2019
build that cannot decode that format: axes and colourbar drew, the surface did not.
These tests fail if either half of the fix is undone.
"""
import re
from pathlib import Path

import pytest

from camel_data.classroom import PLOTLYJS_URL, load_gallery, surface_3d

SLICE = Path(__file__).resolve().parents[1] / "data/slice/camel-2dcc"


@pytest.fixture(scope="module")
def html():
    if not (SLICE / "afm_gallery/gallery.json").exists():
        pytest.skip(f"data slice not present at {SLICE}")
    scan = load_gallery(SLICE)["triangle_pyramids"]
    return surface_3d(scan, exaggeration=3).to_html()


def test_no_base64_arrays(html):
    """Heights must travel as plain JSON arrays, readable by any plotly.js build."""
    assert "bdata" not in html
    assert re.search(r'"z":\s*\[\[', html), "z should be a nested array of numbers"


def test_plotlyjs_version_is_pinned(html):
    """Never trust get_plotlyjs_version(); it reports 4.0.0 from a 7.0.0 install.

    figure_html builds its own loader, so the URL appears in a script assignment rather
    than a src attribute. Match either form: what matters is which version is requested.
    """
    urls = re.findall(r'["\']([^"\']*cdn\.plot\.ly[^"\']*)["\']', html)
    assert urls, "the figure must reference a plotly.js bundle"
    assert set(urls) == {PLOTLYJS_URL}, f"unexpected plotly.js URLs: {set(urls)}"
    assert "plotly-4.0.0" not in html


def test_loader_restores_requirejs(html):
    """The loader hides define.amd while plotly.js loads; it must put it back both on
    success and on failure, or it leaves the page unable to load any other AMD module."""
    assert html.count("window.define = undefined") == 1
    assert html.count("window.define = amd") == 2, "restore define on both onload and onerror"


def test_offline_failure_is_explained(html):
    """A blocked CDN must say so rather than leaving a silent empty box."""
    assert "onerror" in html
    assert "works offline" in html
