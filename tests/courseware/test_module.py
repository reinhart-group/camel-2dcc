from pathlib import Path

import pytest

from courseware.module import ModuleError, find_module, load_module, select_cells

FIX = Path(__file__).parent / "fixtures" / "modules"


def test_load_module_reads_front_matter_and_cells():
    m = load_module(FIX / "concept_demo.py")
    assert m.name == "concept_demo" and m.kind == "concept"
    assert m.accepts == ["series"]
    assert m.dials == {"guidance": ["worked", "fill", "open"], "register": ["plain", "explorer"]}
    assert m.minutes == 8
    assert len(m.cells) == 5
    assert "# ---" not in "".join(c.source for c in m.cells)


def test_select_cells_keeps_untagged_and_matching():
    m = load_module(FIX / "concept_demo.py")
    cells = select_cells(m, {"guidance": "worked", "register": "plain"})
    text = "\n".join(c.source for c in cells)
    assert "fair-share" in text and "arithmetic average" not in text
    assert "answer = float" in text and "answer = ..." not in text
    assert len(cells) == 3


def test_select_cells_multi_value_tag_means_any_of():
    m = load_module(FIX / "concept_demo.py")
    for g in ("fill", "open"):
        text = "\n".join(c.source for c in select_cells(m, {"guidance": g, "register": "explorer"}))
        assert "answer = ..." in text


def test_select_cells_strips_dial_tags():
    m = load_module(FIX / "concept_demo.py")
    for c in select_cells(m, {"guidance": "worked", "register": "plain"}):
        assert not [t for t in c.metadata.get("tags", []) if ":" in t]


def test_missing_front_matter_is_an_error(tmp_path):
    p = tmp_path / "bad.py"
    p.write_text("# %%\nx = 1\n")
    with pytest.raises(ModuleError, match="front matter"):
        load_module(p)


def test_load_module_rejects_cell_tag_for_undeclared_dial():
    """A cell tagged with a dial the front matter never declared must be a hard error, not a
    silent drop (this is exactly the bug that deleted the exit ticket from every built notebook
    while the build still reported OK)."""
    with pytest.raises(ModuleError, match="register"):
        load_module(FIX / "bad_undeclared_dial.py")


def test_load_module_rejects_cell_tag_with_undeclared_value():
    """A cell tagged with a value the dial never declared (e.g. a typo like
    'register:elaboarte') must be a hard error, not a silent drop — same trap
    as the undeclared-dial case, one level deeper."""
    with pytest.raises(ModuleError, match="register") as exc_info:
        load_module(FIX / "bad_undeclared_value.py")
    msg = str(exc_info.value)
    assert "elaboarte" in msg
    assert "plain" in msg and "explorer" in msg


def test_find_module_searches_subfolders():
    assert find_module("data_demo", [FIX]).kind == "dataset"
    with pytest.raises(ModuleError, match="not found"):
        find_module("nope", [FIX])
