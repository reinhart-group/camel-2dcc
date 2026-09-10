from pathlib import Path

from courseware.compose import compose
from courseware.manifest import lesson_from_dict

FIX = [Path(__file__).parent / "fixtures" / "modules"]


def lesson(**over):
    d = {"id": "demo", "title": "Demo", "minutes": 40, "preset": "algebra1",
         "dials": {"messiness": "real"}, "params": {"sample_size": 4},
         "modules": ["frame_demo", "data_demo", {"concept_demo": {"guidance": "worked"}}]}
    d.update(over)
    return lesson_from_dict(d, FIX)


def test_params_cell_comes_first_after_frame_and_holds_numeric_dials():
    nb = compose(lesson())
    params = [c for c in nb.cells if c.cell_type == "code" and c.source.startswith("PARAMS =")]
    assert len(params) == 1 and "'sample_size': 4" in params[0].source


def test_contract_check_follows_each_dataset_module():
    src = [c.source for c in nb_cells()]
    i = next(i for i, s in enumerate(src) if s.startswith("series_values") or "series_values =" in s)
    assert "check_shapes(globals(), ['series'])" in src[i + 1]


def nb_cells():
    return compose(lesson()).cells


def test_every_cell_has_camel_metadata_and_stable_id():
    a, b = compose(lesson()), compose(lesson())
    assert [c.id for c in a.cells] == [c.id for c in b.cells]
    for c in a.cells:
        assert c.metadata["camel"]["lesson"] == "demo"
    concept = [c for c in a.cells if c.metadata["camel"]["module"] == "concept_demo"]
    assert concept and concept[0].metadata["camel"]["dials"] == {"guidance": "worked", "register": "plain"}


def test_variants_follow_resolved_settings():
    text = "\n".join(c.source for c in nb_cells())
    assert "fair-share" in text and "answer = float" in text and "answer = ..." not in text
