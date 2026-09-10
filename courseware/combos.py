"""Seeded random valid dial combinations for a lesson (tests the dial space)."""

from __future__ import annotations

import copy
import random

from courseware.manifest import Lesson, ManifestError, _entries, lesson_from_dict
from courseware.module import find_module


def random_lessons(data: dict, module_roots, n: int, seed: int) -> list[Lesson]:
    rng = random.Random(seed)
    out: list[Lesson] = []
    attempts = 0
    while len(out) < n and attempts < n * 20:
        attempts += 1
        d = copy.deepcopy(data)
        d["id"] = f"{data['id']}-r{len(out)}"
        entries = []
        lesson_dials = {}  # collect all dial choices at lesson level
        for name, override in _entries(data["modules"]):
            mod = find_module(name, module_roots)
            choice = {dial: rng.choice(values) for dial, values in mod.dials.items()}
            lesson_dials.update(choice)  # make dial choices available to all modules
            entries.append({name: {**choice, **{k: v for k, v in override.items() if k not in mod.dials}}})
        d["modules"] = entries
        d["dials"] = {**d.get("dials", {}), **lesson_dials}  # merge with existing lesson dials
        try:
            out.append(lesson_from_dict(d, module_roots))
        except ManifestError:
            continue  # an invalid combination: skip it, the builder would reject it too
    return out
