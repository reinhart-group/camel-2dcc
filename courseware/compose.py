"""Assemble a notebook from a resolved lesson."""

from __future__ import annotations

import hashlib

import nbformat

from courseware.manifest import Lesson
from courseware.module import select_cells


def _cell_id(*parts: str) -> str:
    return hashlib.sha1("/".join(parts).encode()).hexdigest()[:12]


def _stamp(cell, lesson: Lesson, module: str, settings: dict, slot: int, index: int):
    task = f"{module}@{slot}#{index}"
    cell.metadata["camel"] = {"lesson": lesson.id, "module": module,
                              "task": task, "dials": dict(settings)}
    cell.id = _cell_id(lesson.id, str(slot), module, str(index))
    return cell


def compose(lesson: Lesson) -> nbformat.NotebookNode:
    nb = nbformat.v4.new_notebook()
    nb.metadata["camel"] = {"lesson": lesson.id, "title": lesson.title, "preset": lesson.preset,
                            "objective": lesson.objective, "standards": lesson.standards,
                            "modules": [{"module": rm.module.name, "dials": rm.settings}
                                        for rm in lesson.modules]}
    params_placed = False
    for slot, rm in enumerate(lesson.modules):
        if rm.module.params and not params_placed:
            src = ("PARAMS = " + repr(dict(lesson.params)) +
                   "  # teachers: change these numbers, then Runtime → Restart and run all")
            nb.cells.append(_stamp(nbformat.v4.new_code_cell(src), lesson, "params", {}, -1, 0))
            params_placed = True
        if rm.module.kind == "dataset" and rm.module.produces:
            clear = ("from camel_data.contracts import clear_shapes\n"
                     f"clear_shapes(globals(), {rm.module.produces!r})")
            nb.cells.append(_stamp(nbformat.v4.new_code_cell(clear), lesson,
                                   f"{rm.module.name}.clear", {}, slot, 0))
        cells = select_cells(rm.module, rm.settings)
        for i, cell in enumerate(cells):
            nb.cells.append(_stamp(cell, lesson, rm.module.name, rm.settings, slot, i))
        if rm.module.kind == "dataset" and rm.module.produces:
            check = ("from camel_data.contracts import check_shapes\n"
                     f"check_shapes(globals(), {rm.module.produces!r})")
            nb.cells.append(_stamp(nbformat.v4.new_code_cell(check), lesson,
                                   f"{rm.module.name}.check", {}, slot, len(cells)))
    if not params_placed:
        insert_at = 1 if lesson.modules and lesson.modules[0].module.kind == "frame" else 0
        nb.cells.insert(insert_at, _stamp(nbformat.v4.new_code_cell("PARAMS = " + repr(dict(lesson.params))),
                                         lesson, "params", {}, -1, 0))
    return nb
