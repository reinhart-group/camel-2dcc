"""The catalog of browsable widget items, grouped by the four activity rounds."""
from __future__ import annotations

import importlib
import pathlib

ROUNDS = {
    "warmup": "Round 0 - warm up: notice and wonder",
    "mess": "Round 2 - find the mess",
    "model": "Round 3 - model it",
    "dials": "Round 4 - turn the dials",
}

PARTS = ["catalog_items_core", "catalog_items_a", "catalog_items_b"]


def items() -> list[dict]:
    out = []
    for name in PARTS:
        path = pathlib.Path(__file__).with_name(name + ".py")
        if not path.exists():
            continue
        mod = importlib.import_module(name)
        out.extend(mod.ITEMS)
    seen = set()
    for it in out:
        assert it["id"] not in seen, f"duplicate item id {it['id']}"
        assert it["round"] in ROUNDS, f"{it['id']}: unknown round {it['round']}"
        seen.add(it["id"])
    return sorted(out, key=lambda d: (list(ROUNDS).index(d["round"]), d["id"]))
