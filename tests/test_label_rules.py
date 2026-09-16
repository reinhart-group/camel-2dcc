"""Run M-05's widget in node against its real payload and check its arithmetic.

This item has been rebuilt twice after the operator rejected it, so what it reports is
worth pinning down. Every number below was computed independently in Python from the same
records; the test fails if the JavaScript and the data ever stop agreeing.
"""
import json
import pathlib
import shutil
import subprocess
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
PROBE = ROOT / "tests/js/label_rules_probe.js"

pytestmark = pytest.mark.skipif(shutil.which("node") is None, reason="node not installed")


@pytest.fixture(scope="module")
def result(tmp_path_factory):
    sys.path.insert(0, str(ROOT / "courseware"))
    import catalog_data_a as cda

    payload = tmp_path_factory.mktemp("m05") / "payload.json"
    payload.write_text(json.dumps(cda.label_pairs()))
    out = subprocess.run(["node", str(PROBE), str(payload)], cwd=ROOT,
                         capture_output=True, text=True, check=True)
    return json.loads(out.stdout)


def test_rules_reduce_the_spelling_count(result):
    """Each rule must visibly do something, or it is a control that teaches nothing."""
    assert [s["spellings"] for s in result["steps"]] == [35, 30, 28, 27, 25, 25]


def test_the_cross_column_rule_sets_aside_five_rows(result):
    """Five rows have the substrate's name typed into the material box."""
    assert [s["moved"] for s in result["steps"]] == [0, 0, 0, 0, 5, 5]


def test_no_sample_disappears_silently(result):
    """Bars, the overflow bar and the set-aside pile must account for all 1,005 samples.

    Cleaning that loses rows without saying so is the failure this whole round is about, so
    the widget must never do it either.
    """
    drawn = sum(int(b.rsplit(": ", 1)[1]) for b in result["bars"])
    assert drawn + result["steps"][-1]["moved"] == 1005


def test_blank_entries_stay_visible(result):
    """The 15 rows with nothing typed are a finding, not something to drop quietly."""
    assert "(nothing typed): 15" in result["bars"]
