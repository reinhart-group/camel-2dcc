"""Runtime checks that a dataset module produced the data shapes a lesson needs.

Concept modules are written against these standard variable names, so any
concept can follow any dataset that produces the shape it accepts.
"""

from __future__ import annotations

import numpy as np


class ContractError(Exception):
    """A dataset module did not produce a required variable of the right kind."""


def _series(ns):
    v = np.asarray(ns["series_values"], dtype=float)
    if v.ndim != 1 or len(v) < 3:
        raise ContractError("series_values must be a 1-D list of at least 3 numbers")
    if not np.all(np.isfinite(v)):
        raise ContractError("series_values must be finite (blanks belong in a separate note, not NaN)")


def _groups(ns):
    t = ns["groups_table"]
    for col in ("value", "group"):
        if col not in getattr(t, "columns", []):
            raise ContractError(f"groups_table needs a '{col}' column")


def _curve(ns):
    x, y = np.asarray(ns["curve_x"], float), np.asarray(ns["curve_y"], float)
    if x.shape != y.shape or x.ndim != 1:
        raise ContractError("curve_x and curve_y must be 1-D and the same length")


SHAPES = {
    "series": (("series_values", "series_label", "series_unit"), _series),
    "groups": (("groups_table", "groups_label", "groups_unit"), _groups),
    "curve": (("curve_x", "curve_y", "curve_x_label", "curve_y_label"), _curve),
}


def check_shapes(namespace: dict, shapes: list[str]) -> None:
    for shape in shapes:
        names, check = SHAPES[shape]
        missing = [n for n in names if n not in namespace]
        if missing:
            raise ContractError(f"data shape '{shape}' is missing {missing}")
        check(namespace)
