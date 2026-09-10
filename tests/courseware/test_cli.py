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
