import collections

import numpy as np
from stl import mesh

from camel_data.classroom import AFMScan, rms, surface_3d, to_stl


def _scan(n=20):
    y, x = np.mgrid[0:n, 0:n]
    z = np.sin(x / 3.0) + 0.5 * np.cos(y / 4.0)
    return AFMScan(key="t", z=z, scan_um=1.0, material="MoS2", title="test", story="", sample_id=1)


def test_stl_is_watertight_with_positive_volume(tmp_path):
    p = to_stl(_scan(), tmp_path / "t.stl", width_mm=50, relief_mm=10, base_mm=2)
    v = mesh.Mesh.from_file(str(p)).vectors.astype(float)
    # every directed edge must be matched by its reverse on a neighbouring triangle
    edges = collections.Counter()
    for t in v:
        for a, b in ((0, 1), (1, 2), (2, 0)):
            edges[(tuple(np.round(t[a], 6)), tuple(np.round(t[b], 6)))] += 1
    assert all(edges.get((b, a), 0) == n for (a, b), n in edges.items())
    volume = np.einsum("ij,ij->i", v[:, 0], np.cross(v[:, 1], v[:, 2])).sum() / 6
    assert 50 * 50 * 2 < volume < 50 * 50 * 12


def test_surface_keeps_true_xy_scale():
    fig = surface_3d(_scan(), exaggeration=1.0)
    assert fig.layout.scene.aspectratio.x == fig.layout.scene.aspectratio.y == 1


def test_rms_matches_numpy_std():
    z = np.array([0.0, 1.0, 2.0, 3.0, 10.0])
    assert rms(z) == np.std(z)
