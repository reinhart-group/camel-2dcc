"""Assemble a notebook from a resolved lesson."""

from __future__ import annotations

import hashlib

import nbformat

from courseware.manifest import Lesson
from courseware.module import select_cells


def _cell_id(*parts: str) -> str:
    return hashlib.sha1("/".join(parts).encode()).hexdigest()[:12]


def _stamp(cell, lesson: Lesson, module: str, settings: dict, index: int):
    cell.metadata["camel"] = {"lesson": lesson.id, "module": module,
                              "task": f"{module}#{index}", "dials": dict(settings)}
    cell.id = _cell_id(lesson.id, module, str(index))
    return cell


def compose(lesson: Lesson) -> nbformat.NotebookNode:
    nb = nbformat.v4.new_notebook()
    nb.metadata["camel"] = {"lesson": lesson.id, "title": lesson.title, "preset": lesson.preset,
                            "modules": [{"module": rm.module.name, "dials": rm.settings}
                                        for rm in lesson.modules]}
    params_placed = False
    for rm in lesson.modules:
        cells = select_cells(rm.module, rm.settings)
        for i, cell in enumerate(cells):
            nb.cells.append(_stamp(cell, lesson, rm.module.name, rm.settings, i))
        if rm.module.kind == "frame" and not params_placed:
            src = ("PARAMS = " + repr(dict(lesson.params)) +
                   "  # teachers: you may change these numbers, then Runtime → Restart and run all")
            nb.cells.append(_stamp(nbformat.v4.new_code_cell(src), lesson, "params", {}, 0))
            params_placed = True
        if rm.module.kind == "dataset" and rm.module.produces:
            check = ("from camel_data.contracts import check_shapes\n"
                     f"check_shapes(globals(), {rm.module.produces!r})")
            nb.cells.append(_stamp(nbformat.v4.new_code_cell(check), lesson,
                                   f"{rm.module.name}.check", {}, 0))
    if not params_placed:
        nb.cells.insert(0, _stamp(nbformat.v4.new_code_cell("PARAMS = " + repr(dict(lesson.params))),
                                  lesson, "params", {}, 0))
    return nb
