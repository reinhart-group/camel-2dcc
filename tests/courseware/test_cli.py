import json
from pathlib import Path

import yaml

from courseware.cli import main
from courseware.combos import random_lessons

FIX = Path(__file__).parent / "fixtures" / "modules"


def manifest(tmp_path, **over):
    d = {"id": "demo", "title": "Demo", "minutes": 40, "preset": "algebra1",
         "dials": {"messiness": "real"}, "params": {"sample_size": 4},
         "modules": ["frame_demo", "data_demo", "concept_demo"]}
    d.update(over)
    p = tmp_path / "demo.yaml"
    p.write_text(yaml.safe_dump(d, sort_keys=False))
    return p, d


def test_build_writes_notebook(tmp_path):
    p, _ = manifest(tmp_path)
    assert main(["build", str(p), "--out", str(tmp_path / "out"), "--modules", str(FIX)]) == 0
    nb = json.loads((tmp_path / "out" / "demo.ipynb").read_text())
    assert nb["metadata"]["camel"]["lesson"] == "demo"


def test_build_reports_manifest_error(tmp_path, capsys):
    p, _ = manifest(tmp_path, modules=["frame_demo", "concept_demo"])
    assert main(["build", str(p), "--out", str(tmp_path / "out"), "--modules", str(FIX)]) == 1
    assert "series" in capsys.readouterr().out


def test_random_lessons_are_valid_and_seeded(tmp_path):
    _, d = manifest(tmp_path)
    a = random_lessons(d, [FIX], n=5, seed=3)
    b = random_lessons(d, [FIX], n=5, seed=3)
    assert [[rm.settings for rm in l.modules] for l in a] == [[rm.settings for rm in l.modules] for l in b]
    assert all(l.id.startswith("demo-r") for l in a)


def test_random_lessons_respects_requires_constraints(tmp_path):
    """Regression: random_lessons must satisfy requires constraints across modules.

    concept_needs_real requires messiness=real and accepts series. If random_lessons
    only puts dial choices into module-level overrides (not lesson-level dials dict),
    the requires constraint check will not see the randomly chosen messiness value
    and will reject every combination with a ManifestError. This test verifies that
    we get the expected number of valid lessons.
    """
    _, d = manifest(tmp_path, modules=["frame_demo", "data_demo", "concept_needs_real"],
                    dials={})  # no preset dials, so random choices must flow through lesson_dials
    lessons = random_lessons(d, [FIX], n=50, seed=1)
    assert len(lessons) == 50, f"expected 50 valid lessons (with requires satisfied), got {len(lessons)}"
    # Every lesson should have concept_needs_real in it, which has requires={messiness: [real]}
    # The fact that we got 50 valid lessons proves the requires constraint was satisfied.
    assert all(any(rm.module.name == "concept_needs_real" for rm in l.modules) for l in lessons)


def test_build_reports_yaml_error(tmp_path, capsys):
    p = tmp_path / "bad.yaml"
    p.write_text("{ invalid yaml }: [")
    assert main(["build", str(p), "--out", str(tmp_path / "out"), "--modules", str(FIX)]) == 1
    assert "FAIL" in capsys.readouterr().out


