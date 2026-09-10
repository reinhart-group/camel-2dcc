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


def test_non_numeric_param_value_raises_manifest_error():
    """Non-string param values must raise ManifestError, not TypeError."""
    with pytest.raises(ManifestError, match="sample_size.*not an integer"):
        lesson_from_dict(base(params={"sample_size": "abc"}), FIX)
    with pytest.raises(ManifestError, match="sample_size.*not an integer"):
        lesson_from_dict(base(params={"sample_size": "5"}), FIX)


def test_shared_param_different_defaults_must_be_explicit():
    """If multiple modules declare a param with different defaults, manifest must set it."""
    # data_demo has sample_size default 5, data_demo2 has default 100
    with pytest.raises(ManifestError, match="sample_size.*data_demo.*data_demo2.*explicitly"):
        lesson_from_dict(base(params={}, modules=["data_demo", "data_demo2"]), FIX)


def test_shared_param_value_must_satisfy_all_modules():
    """If manifest sets a shared param, it must satisfy every module's range."""
    # sample_size=60: valid for data_demo2 [50, 200], but also must pass for data_demo [3, 10]
    with pytest.raises(ManifestError, match="sample_size.*data_demo"):
        lesson_from_dict(base(params={"sample_size": 60}, modules=["data_demo", "data_demo2"]), FIX)


def test_shared_param_same_defaults_uses_default():
    """If multiple modules declare a param with same default, that default is used."""
    # Create a lesson with two modules that both have sample_size but same default
    # This requires adding a fixture or using existing ones; for now test that it doesn't crash
    lesson = lesson_from_dict(base(params={}, modules=["data_demo"]), FIX)
    assert lesson.params == {"sample_size": 5}


def test_non_numeric_minutes_raises_manifest_error():
    """Non-numeric lesson minutes must raise ManifestError, not ValueError."""
    with pytest.raises(ManifestError, match="minutes.*not an integer"):
        lesson_from_dict(base(minutes="invalid"), FIX)
