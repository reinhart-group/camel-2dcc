from pathlib import Path

import numpy as np
import pytest

from camel_data.spm import flatten, height_channel, read_spm, rms_roughness

REF = Path(__file__).resolve().parents[1] / "data/raw/spm/24906_MBE2-230811A-MH_AFM_center_2um.0_00000.spm"


@pytest.mark.skipif(not REF.exists(), reason="reference scan not downloaded")
def test_reference_scan_matches_instrument_rms():
    # The operator saved this scan's image as "..._rms0_36nm.jpg" (SnTe, sample 24906).
    chs = read_spm(REF)
    h = height_channel(chs)
    assert h.name == "Height Sensor" and h.unit == "nm"
    assert h.data.shape == (256, 256)
    assert h.scan_size_nm == pytest.approx(2000)
    assert rms_roughness(flatten(h.data)) == pytest.approx(0.36, abs=0.01)


def test_flatten_removes_per_line_tilt():
    x = np.arange(50)
    z = np.array([0.3 * x + i for i in range(20)], dtype=float)  # tilted, offset lines
    assert np.allclose(flatten(z), 0, atol=1e-9)


def test_rms_is_population_std():
    z = np.array([1.0, 2.0, 3.0, 4.0])
    assert rms_roughness(z) == pytest.approx(np.std(z))
