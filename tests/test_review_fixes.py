"""Regression tests for the Codex review findings that were fixed."""

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from build_afm_summary import downsample  # noqa: E402
from build_slice import build_growth_summary, build_recipes  # noqa: E402
from camel_data.classroom import AFMScan, surface_3d, to_stl  # noqa: E402
from camel_data.spm import AFMChannel, height_channel  # noqa: E402


def test_downsample_covers_whole_scan_without_cropping():
    z = np.zeros((125, 512))
    z[-10:, :] = 100.0  # a feature in the bottom rows that cropping would drop
    small = downsample(z, 64)
    assert small.shape == (64, 64)
    assert small[-1].mean() == 100.0  # the last scan lines are kept, not cropped away
    assert small[0].mean() == 0.0
    # when the size divides evenly, every bin has equal weight and the mean is preserved
    even = np.random.default_rng(1).normal(size=(512, 512))
    assert downsample(even, 64).mean() == pytest.approx(even.mean(), abs=1e-12)


def test_height_channel_refuses_uncalibrated_data():
    raw = AFMChannel(name="Height", data=np.zeros((4, 4)), unit="raw", scan_size_nm=1000)
    with pytest.raises(LookupError):
        height_channel([raw])


def test_views_reject_non_square_scans(tmp_path):
    scan = AFMScan(key="r", z=np.zeros((10, 20)), scan_um=1, material="x", title="x", story="", sample_id=1)
    with pytest.raises(ValueError):
        surface_3d(scan)
    with pytest.raises(ValueError):
        to_stl(scan, tmp_path / "r.stl")


def test_max_pixels_is_a_true_maximum():
    scan = AFMScan(key="s", z=np.random.default_rng(0).normal(size=(528, 528)), scan_um=1,
                   material="x", title="x", story="", sample_id=1)
    fig = surface_3d(scan, max_pixels=256)
    assert np.asarray(fig.data[0].z).shape[0] <= 256


def _recipe(technique, rows):
    return {"technique": technique,
            "groups": [{"symbol": "recipe", "rows": rows}]}


def test_missing_duration_makes_later_start_times_unknown_and_totals_blank():
    samples = pd.DataFrame({"sample_id": [1, 2], "materials": ["MoS2", "MoS2"]})
    recipes = {
        "1": [_recipe("MOCVD", [{"step": "Ramp up T", "t": "600", "T": "1000"},
                                {"step": "Growth"},  # no duration recorded
                                {"step": "Cooldown 1", "t": "480"}])],
        "2": [_recipe("MOCVD", [{"step": "Growth", "t": "180", "T": "1000"}]),
              _recipe("MOCVD", [{"step": "Growth", "t": "900", "T": "950"}])],  # a second, separate run
    }
    steps = build_recipes(samples, recipes)
    s1 = steps[steps.sample_id == 1]
    assert list(s1.start_min.iloc[:2]) == [0.0, 10.0]
    assert pd.isna(s1.start_min.iloc[2])  # after an unknown duration, elapsed time is unknown

    afm = pd.DataFrame({"sample_id": [1, 2], "rms_roughness_nm": [0.5, 0.6], "scan_size_um": [5, 5]})
    g = build_growth_summary(steps, afm).set_index("sample_id")
    assert pd.isna(g.loc[1, "growth_time_min"])  # missing is not zero
    assert not g.loc[1, "durations_complete"]
    assert g.loc[2, "growth_time_min"] == pytest.approx(3.0)  # first recipe only, not 3 + 15
    assert g.loc[2, "n_recipes"] == 2
