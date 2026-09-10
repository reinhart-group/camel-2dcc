from pathlib import Path

import pytest

from courseware.manifest import ManifestError, lesson_from_dict

FIX = [Path(__file__).parent / "fixtures" / "modules"]


def base(**over):
    d = {"id": "t", "title": "T", "minutes": 40, "preset": "algebra1",
         "dials": {"messiness": "real"}, "params": {"sample_size": 5},
         "modules": ["frame_demo", "data_demo", "concept_demo"]}
    d.update(over)
    return d


def test_preset_then_lesson_then_module_override():
    lesson = lesson_from_dict(base(modules=["frame_demo", "data_demo",
                                            {"concept_demo": {"guidance": "worked"}}]), FIX)
    concept = lesson.modules[2]
    assert concept.settings == {"guidance": "worked", "register": "plain"}   # preset register, override guidance
    assert lesson.modules[1].settings == {"messiness": "real"}               # only dials the module declares


def test_unsupported_dial_value_is_rejected():
    with pytest.raises(ManifestError, match="concept_demo.*guidance.*bogus"):
        lesson_from_dict(base(modules=["data_demo", {"concept_demo": {"guidance": "bogus"}}]), FIX)


def test_requires_constraint_uses_lesson_setting():
    lesson_from_dict(base(modules=["data_demo", "concept_needs_real"]), FIX)
    with pytest.raises(ManifestError, match="concept_needs_real.*messiness"):
        lesson_from_dict(base(dials={"messiness": "flagged"},
                              modules=["data_demo", "concept_needs_real"]), FIX)


def test_concept_needs_a_dataset_that_produces_its_shape():
    with pytest.raises(ManifestError, match="concept_demo.*series"):
        lesson_from_dict(base(modules=["frame_demo", "concept_demo"]), FIX)


def test_params_default_and_range():
    assert lesson_from_dict(base(params={}), FIX).params == {"sample_size": 5}
    with pytest.raises(ManifestError, match="sample_size"):
        lesson_from_dict(base(params={"sample_size": 99}), FIX)


def test_minutes_budget():
    with pytest.raises(ManifestError, match="minutes"):
        lesson_from_dict(base(minutes=5), FIX)
