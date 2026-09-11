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
    ns["series_values"] = v
    _labels(ns, "series_label", "series_unit")


def _groups(ns):
    t = ns["groups_table"]
    for col in ("value", "group"):
        if col not in getattr(t, "columns", []):
            raise ContractError(f"groups_table needs a '{col}' column")
    if len(t) < 4:
        raise ContractError("groups_table needs at least 4 rows")
    values = np.asarray(t["value"], dtype=float)
    if not np.all(np.isfinite(values)):
        raise ContractError("groups_table values must be finite")
    if t["group"].isna().any() or t["group"].nunique() < 2:
        raise ContractError("groups_table needs at least 2 non-blank groups")
    _labels(ns, "groups_label", "groups_unit")


def _curve(ns):
    x, y = np.asarray(ns["curve_x"], float), np.asarray(ns["curve_y"], float)
    if x.shape != y.shape or x.ndim != 1 or len(x) < 2:
        raise ContractError("curve_x and curve_y must be 1-D and the same length")
    if not np.all(np.isfinite(x)) or not np.all(np.isfinite(y)):
        raise ContractError("curve values must be finite")
    ns["curve_x"], ns["curve_y"] = x, y
    _labels(ns, "curve_x_label", "curve_y_label")


def _map(ns):
    z = np.asarray(ns["map_values"], dtype=float)
    if z.ndim != 2 or min(z.shape) < 2 or not np.all(np.isfinite(z)):
        raise ContractError("map_values must be a finite 2-D numeric array")
    if not isinstance(ns["map_width_nm"], (int, float)) or ns["map_width_nm"] <= 0:
        raise ContractError("map_width_nm must be positive")
    ns["map_values"] = z
    _labels(ns, "map_label", "map_unit")


def _labels(ns, *names):
    for name in names:
        if not isinstance(ns[name], str) or not ns[name].strip():
            raise ContractError(f"{name} must be a non-empty string")


SHAPES = {
    "series": (("series_values", "series_label", "series_unit"), _series),
    "groups": (("groups_table", "groups_label", "groups_unit"), _groups),
    "curve": (("curve_x", "curve_y", "curve_x_label", "curve_y_label"), _curve),
    "map": (("map_values", "map_width_nm", "map_label", "map_unit"), _map),
}


def check_shapes(namespace: dict, shapes: list[str]) -> None:
    for shape in shapes:
        if shape not in SHAPES:
            raise ContractError(f"unknown data shape '{shape}'")
        names, check = SHAPES[shape]
        missing = [n for n in names if n not in namespace]
        if missing:
            raise ContractError(f"data shape '{shape}' is missing {missing}")
        check(namespace)


def clear_shapes(namespace: dict, shapes: list[str]) -> None:
    """Remove standard variables before a producer runs, preventing stale-data checks."""
    for shape in shapes:
        if shape not in SHAPES:
            raise ContractError(f"unknown data shape '{shape}'")
        for name in SHAPES[shape][0]:
            namespace.pop(name, None)
