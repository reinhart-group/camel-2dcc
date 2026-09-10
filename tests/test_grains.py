import numpy as np
import pandas as pd

from camel_data.grains import find_grains, line_profile, random_sample, whole_single


def _triangles_scene(n=200):
    """Flat substrate with three equilateral-ish triangle islands 1.5 nm tall."""
    z = np.random.default_rng(0).normal(0, 0.05, (n, n))
    yy, xx = np.mgrid[0:n, 0:n]
    for cy, cx, s in ((50, 50, 30), (120, 140, 24), (160, 60, 18)):
        inside = (yy - cy > -s / 2) & (yy - cy < s / 2) & (np.abs(xx - cx) < (yy - cy + s / 2) / np.sqrt(3))
        z[inside] += 1.5
    return z


def test_find_grains_counts_islands_and_reports_area():
    z = _triangles_scene()
    labels, table, thr = find_grains(z, pixel_nm=2.0)
    singles = [t for t in table if t["kind"] == "single"]
    assert len(singles) == 3
    assert 0.3 < thr < 1.5
    assert all(1.3 < t["height_nm"] < 1.7 for t in singles)
    # area in nm^2 = pixel count * pixel_nm^2
    assert abs(sum(t["area_nm2"] for t in singles) - (labels > 0).sum() * 4.0) < 1e-6


def test_whole_single_excludes_edge_and_glitch_grains():
    t = pd.DataFrame({"scan": ["a"] * 4, "kind": ["single", "single", "merged", "single"],
                      "touches_edge": [False, True, False, False],
                      "touches_glitch": [False, False, False, True]})
    assert len(whole_single(t)) == 1


def test_line_profile_crosses_a_step():
    z = np.zeros((50, 100))
    z[:, 50:] = 1.0
    scan = {"z": z, "pixel_nm": 1.0}
    d, h = line_profile(scan, (10, 25), (90, 25), width_px=1)
    assert d[-1] == 80
    assert h[0] == 0 and h[-1] == 1


def test_random_sample_has_no_repeats():
    s = random_sample(np.arange(100), 30, seed=1)
    assert len(set(s)) == 30
