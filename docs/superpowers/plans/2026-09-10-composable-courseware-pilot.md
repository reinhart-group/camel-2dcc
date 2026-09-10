# Composable Courseware Pilot Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build CAMEL lessons from reusable dataset modules and concept modules, combined by YAML manifests with granular per-module complexity dials, and prove it with one concept module running on two datasets at several dial settings.

**Architecture:** A small Python package `courseware/` loads modules (jupytext percent `.py` files with a YAML front-matter block), resolves each module's dial settings from preset → lesson → per-module overrides, validates constraints and dataset→concept data-shape bindings, selects the cells whose dial tags match, and writes an executed-ready `.ipynb` with a runtime `PARAMS` cell, runtime data-shape checks after each dataset module, deterministic cell IDs, and per-cell `camel` metadata for future telemetry. The include/front-matter idea is copied from MATSE 219's `build.py`; variants use standard Jupytext cell tags.

**Tech Stack:** Python 3.12 (.venv), jupytext, nbformat, nbclient (via `scripts/run_notebook.py`), PyYAML, pandas/numpy, pytest, textstat (via `scripts/readability.py`).

**Spec:** `docs/specs/2026-09-10-composable-courseware-design.md` (read the "Revisions after Codex design review" and "Decisions from Wes" sections — they supersede earlier text).

## Global Constraints

- Structural dials (`guidance`, `register`, `messiness`, module list, exposed variables) are build-time; only numeric data dials (`sample_size`, `seed`) appear in the runtime `PARAMS` cell.
- Dial levels: `guidance ∈ {worked, fill, open}`, `register ∈ {plain, explorer}`, `messiness ∈ {real, flagged}`.
- Data shapes (contract names): `series`, `groups`, `curve`. Standard variables: `series_values, series_label, series_unit`; `groups_table (columns value, group), groups_label, groups_unit`; `curve_x, curve_y, curve_x_label, curve_y_label`.
- A cell tag has the form `<dial>:<value>`; a cell with tags for a dial is kept only if the effective value is one of them. Cells with no dial tags are always kept.
- Built notebooks must execute top to bottom with the real slice (`scripts/run_notebook.py`), fail closed on any error.
- `register: plain` lessons must read at Flesch–Kincaid grade ≤ 8.0 (`scripts/readability.py` logic).
- Answer checks recompute references from the data variables, never from student-edited variables.
- Telemetry is a no-op; every built cell carries `metadata.camel = {lesson, module, task, dials}`.
- Do not edit `src/camel_data/classroom.py`, `grains.py`, `spm.py`; existing notebooks under `notebooks/` stay untouched.

## File Structure

```
courseware/
  __init__.py
  module.py        # load a module file: front matter + cells; select cells by dial settings
  manifest.py      # load a lesson manifest; resolve per-module dials; validate constraints & bindings
  compose.py       # assemble an nbformat notebook from a resolved lesson
  combos.py        # seeded random valid dial combinations for a lesson
  cli.py           # `python -m courseware build ...`
  __main__.py
  presets.yaml     # named bundles of dial defaults (algebra1, explorer)
  modules/
    frame/setup.py, frame/exit_ticket_stats.py
    datasets/data_grain_areas.py, datasets/data_afm_roughness.py
    concepts/concept_mean_median.py, concepts/concept_outlier_effect.py
lessons/
  pilot-grains-algebra1.yaml
  pilot-grains-mixed.yaml
  pilot-roughness-explorer.yaml
src/camel_data/contracts.py   # runtime data-shape checks (shipped in the slice)
tests/courseware/test_module.py, test_manifest.py, test_compose.py, test_cli.py, fixtures/
```

---

### Task 1: Module loading and dial-based cell selection

**Files:**
- Create: `courseware/__init__.py`, `courseware/module.py`
- Test: `tests/courseware/test_module.py`, `tests/courseware/fixtures/modules/concept_demo.py`, `tests/courseware/fixtures/modules/data_demo.py`

**Interfaces:**
- Produces: `Module` dataclass (`name: str, kind: str, path: Path, meta: dict, cells: list[nbformat.NotebookNode]`), properties `dials -> dict[str, list[str]]`, `produces -> list[str]`, `accepts -> list[str]`, `requires -> dict[str, list[str]]`, `params -> dict[str, dict]`, `minutes -> int`; functions `load_module(path: Path) -> Module`, `find_module(name: str, roots: list[Path]) -> Module`, `select_cells(module: Module, settings: dict[str, str]) -> list[NotebookNode]`, exception `ModuleError`.

- [ ] **Step 1: Write fixtures and failing tests**

`tests/courseware/fixtures/modules/concept_demo.py`:
```python
# ---
# module: concept_demo
# kind: concept
# accepts: [series]
# dials:
#   guidance: [worked, fill, open]
#   register: [plain, explorer]
# minutes: 8
# ---
# %% [markdown]
# ## Mean and median

# %% [markdown] tags=["register:plain"]
# The **mean** is the fair-share number.

# %% [markdown] tags=["register:explorer"]
# The mean is the arithmetic average of all values.

# %% tags=["guidance:worked"]
answer = float(sum(series_values) / len(series_values))

# %% tags=["guidance:fill", "guidance:open"]
answer = ...  # ✏️ type your answer here
```
`tests/courseware/fixtures/modules/data_demo.py`:
```python
# ---
# module: data_demo
# kind: dataset
# produces: [series]
# dials:
#   messiness: [real, flagged]
# params:
#   sample_size: {default: 5, min: 3, max: 10}
# minutes: 2
# ---
# %%
import numpy as np
series_values = np.arange(1.0, PARAMS["sample_size"] + 1)
series_label, series_unit = "demo value", "nm"
```
`tests/courseware/test_module.py`:
```python
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


def test_find_module_searches_subfolders():
    assert find_module("data_demo", [FIX]).kind == "dataset"
    with pytest.raises(ModuleError, match="not found"):
        find_module("nope", [FIX])
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `.venv/bin/python -m pytest tests/courseware/test_module.py -q`
Expected: FAIL (`ModuleNotFoundError: No module named 'courseware'`)

- [ ] **Step 3: Implement**

`courseware/__init__.py`:
```python
"""CAMEL composable courseware: modules + manifests + dials → notebooks."""
```
`courseware/module.py`:
```python
"""Load courseware modules and select their cells for given dial settings.

A module is a jupytext percent-format ``.py`` file that starts with a
front-matter block of ``#``-prefixed YAML between two ``# ---`` lines
(the MATSE 219 convention, here machine-readable). Cells may carry
Jupytext tags of the form ``<dial>:<value>``; see ``select_cells``.
"""

from __future__ import annotations

import copy
import re
from dataclasses import dataclass
from pathlib import Path

import jupytext
import yaml

FRONT_RE = re.compile(r"\A# ---\n(?P<body>(?:#[^\n]*\n)*?)# ---\n")


class ModuleError(Exception):
    """A module file is malformed or cannot be found."""


@dataclass
class Module:
    name: str
    kind: str
    path: Path
    meta: dict
    cells: list

    @property
    def dials(self) -> dict[str, list[str]]:
        return {k: list(v) for k, v in (self.meta.get("dials") or {}).items()}

    @property
    def produces(self) -> list[str]:
        return list(self.meta.get("produces") or [])

    @property
    def accepts(self) -> list[str]:
        return list(self.meta.get("accepts") or [])

    @property
    def requires(self) -> dict[str, list[str]]:
        return {k: list(v) for k, v in (self.meta.get("requires") or {}).items()}

    @property
    def params(self) -> dict[str, dict]:
        return dict(self.meta.get("params") or {})

    @property
    def minutes(self) -> int:
        return int(self.meta.get("minutes") or 0)


def load_module(path: Path) -> Module:
    text = Path(path).read_text()
    m = FRONT_RE.match(text)
    if not m:
        raise ModuleError(f"{path}: missing '# ---' front matter block")
    yaml_text = "\n".join(line[2:] if line.startswith("# ") else line[1:]
                          for line in m.group("body").splitlines())
    meta = yaml.safe_load(yaml_text) or {}
    for key in ("module", "kind"):
        if key not in meta:
            raise ModuleError(f"{path}: front matter needs '{key}'")
    if meta["kind"] not in ("dataset", "concept", "frame"):
        raise ModuleError(f"{path}: kind must be dataset, concept, or frame")
    nb = jupytext.reads(text[m.end():], fmt="py:percent")
    return Module(name=meta["module"], kind=meta["kind"], path=Path(path), meta=meta, cells=nb.cells)


def find_module(name: str, roots: list[Path]) -> Module:
    for root in roots:
        hits = sorted(Path(root).rglob(f"{name}.py"))
        if hits:
            return load_module(hits[0])
    raise ModuleError(f"module not found: {name} (looked in {[str(r) for r in roots]})")


def _dial_tags(cell) -> dict[str, set[str]]:
    out: dict[str, set[str]] = {}
    for tag in cell.metadata.get("tags", []):
        if ":" in tag:
            dial, value = tag.split(":", 1)
            out.setdefault(dial, set()).add(value)
    return out


def select_cells(module: Module, settings: dict[str, str]) -> list:
    """Cells to keep: untagged cells, plus cells whose every dial tag matches.

    A cell tagged ``guidance:fill`` and ``guidance:open`` is kept when guidance
    is either value. Dial tags are removed from the returned copies.
    """
    kept = []
    for cell in module.cells:
        tags = _dial_tags(cell)
        if all(settings.get(dial) in values for dial, values in tags.items()):
            c = copy.deepcopy(cell)
            other = [t for t in c.metadata.get("tags", []) if ":" not in t]
            if other:
                c.metadata["tags"] = other
            else:
                c.metadata.pop("tags", None)
            kept.append(c)
    return kept
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `.venv/bin/python -m pytest tests/courseware/test_module.py -q`
Expected: 6 passed. (If `yaml` is missing: `UV_CACHE_DIR=/Volumes/Samsung990/uv-cache uv pip install --python .venv/bin/python pyyaml`.)

- [ ] **Step 5: Commit**

```bash
git add courseware tests/courseware
git commit -m "courseware: module loader and dial-tag cell selection"
```

---

### Task 2: Manifests — dial resolution, constraints, data-shape binding

**Files:**
- Create: `courseware/manifest.py`, `courseware/presets.yaml`
- Test: `tests/courseware/test_manifest.py`, `tests/courseware/fixtures/modules/frame_demo.py`, `tests/courseware/fixtures/modules/concept_needs_real.py`

**Interfaces:**
- Consumes: `load_module`, `find_module`, `Module`, `ModuleError` (Task 1).
- Produces: `ResolvedModule` dataclass (`module: Module, settings: dict[str, str]`); `Lesson` dataclass (`id: str, title: str, minutes: int, params: dict[str, int], modules: list[ResolvedModule], preset: str | None`); `load_lesson(path: Path, module_roots: list[Path]) -> Lesson`; `lesson_from_dict(data: dict, module_roots: list[Path]) -> Lesson`; exception `ManifestError`.

- [ ] **Step 1: Write fixtures and failing tests**

`tests/courseware/fixtures/modules/frame_demo.py`:
```python
# ---
# module: frame_demo
# kind: frame
# minutes: 3
# ---
# %% [markdown]
# # Demo lesson
```
`tests/courseware/fixtures/modules/concept_needs_real.py`:
```python
# ---
# module: concept_needs_real
# kind: concept
# accepts: [series]
# requires:
#   messiness: [real]
# minutes: 5
# ---
# %%
biggest = max(series_values)
```
`tests/courseware/test_manifest.py`:
```python
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
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `.venv/bin/python -m pytest tests/courseware/test_manifest.py -q`
Expected: FAIL (`No module named 'courseware.manifest'`)

- [ ] **Step 3: Implement**

`courseware/presets.yaml`:
```yaml
# Named bundles of dial defaults. A lesson picks one; its own `dials` and each
# module's overrides win over the preset.
algebra1: {register: plain, guidance: fill, messiness: flagged}
explorer: {register: explorer, guidance: open, messiness: real}
```
`courseware/manifest.py`:
```python
"""Lesson manifests: resolve each module's dial settings and validate the lesson.

Resolution order for a module's dial: preset < lesson ``dials`` < the module's
own override in ``modules:``. Only dials the module declares are kept.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml

from courseware.module import Module, ModuleError, find_module

PRESETS = yaml.safe_load((Path(__file__).parent / "presets.yaml").read_text())


class ManifestError(Exception):
    """A lesson manifest asks for something its modules cannot do."""


@dataclass
class ResolvedModule:
    module: Module
    settings: dict[str, str]


@dataclass
class Lesson:
    id: str
    title: str
    minutes: int
    params: dict[str, int]
    modules: list[ResolvedModule] = field(default_factory=list)
    preset: str | None = None


def _entries(items):
    for item in items:
        if isinstance(item, str):
            yield item, {}
        elif isinstance(item, dict) and len(item) == 1:
            (name, over), = item.items()
            yield name, dict(over or {})
        else:
            raise ManifestError(f"bad module entry: {item!r}")


def lesson_from_dict(data: dict, module_roots: list[Path]) -> Lesson:
    preset = data.get("preset")
    if preset and preset not in PRESETS:
        raise ManifestError(f"unknown preset {preset!r}; choose from {sorted(PRESETS)}")
    lesson_dials = {**(PRESETS.get(preset) or {}), **(data.get("dials") or {})}
    resolved: list[ResolvedModule] = []
    for name, override in _entries(data.get("modules") or []):
        try:
            mod = find_module(name, module_roots)
        except ModuleError as exc:
            raise ManifestError(str(exc)) from exc
        wanted = {**lesson_dials, **override}
        settings = {}
        for dial, allowed in mod.dials.items():
            value = wanted.get(dial, allowed[0])
            if value not in allowed:
                raise ManifestError(f"{name}: dial {dial}={value!r} not supported (allowed: {allowed})")
            settings[dial] = value
        for dial, allowed in mod.requires.items():
            if wanted.get(dial) not in allowed:
                raise ManifestError(f"{name}: requires {dial} in {allowed}, lesson has {wanted.get(dial)!r}")
        resolved.append(ResolvedModule(mod, settings))

    produced: set[str] = set()
    for rm in resolved:
        missing = [s for s in rm.module.accepts if s not in produced]
        if missing:
            raise ManifestError(f"{rm.module.name}: needs data shape(s) {missing}; add a dataset module "
                                f"that produces them earlier in the lesson")
        produced |= set(rm.module.produces)

    params: dict[str, int] = {}
    wanted_params = data.get("params") or {}
    for rm in resolved:
        for pname, spec in rm.module.params.items():
            value = wanted_params.get(pname, spec.get("default"))
            lo, hi = spec.get("min"), spec.get("max")
            if (lo is not None and value < lo) or (hi is not None and value > hi):
                raise ManifestError(f"param {pname}={value} outside [{lo}, {hi}] for {rm.module.name}")
            params[pname] = value
    unknown = set(wanted_params) - set(params)
    if unknown:
        raise ManifestError(f"params not used by any module: {sorted(unknown)}")

    minutes = int(data.get("minutes") or 0)
    need = sum(rm.module.minutes for rm in resolved)
    if minutes and need > minutes:
        raise ManifestError(f"modules need {need} minutes but the lesson allows {minutes}")

    return Lesson(id=data["id"], title=data["title"], minutes=minutes, params=params,
                  modules=resolved, preset=preset)


def load_lesson(path: Path, module_roots: list[Path]) -> Lesson:
    return lesson_from_dict(yaml.safe_load(Path(path).read_text()), module_roots)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `.venv/bin/python -m pytest tests/courseware -q`
Expected: 12 passed.

- [ ] **Step 5: Commit**

```bash
git add courseware tests/courseware
git commit -m "courseware: manifests with preset/lesson/module dial resolution and validation"
```

---

### Task 3: Composer and runtime data-shape contracts

**Files:**
- Create: `courseware/compose.py`, `src/camel_data/contracts.py`
- Modify: `scripts/build_slice.py` (add `"contracts.py"` to `PACKAGE_FILES`)
- Test: `tests/courseware/test_compose.py`, `tests/test_contracts.py`

**Interfaces:**
- Consumes: `Lesson`, `ResolvedModule` (Task 2); `select_cells` (Task 1).
- Produces: `compose(lesson: Lesson) -> nbformat.NotebookNode`; `camel_data.contracts.check_shapes(namespace: dict, shapes: list[str]) -> None` raising `ContractError`; `SHAPES: dict[str, dict[str, type | tuple]]`.

- [ ] **Step 1: Write failing tests**

`tests/test_contracts.py`:
```python
import numpy as np
import pandas as pd
import pytest

from camel_data.contracts import ContractError, check_shapes


def test_series_ok_and_bad():
    ns = {"series_values": np.array([1.0, 2.0, 3.0]), "series_label": "area", "series_unit": "nm²"}
    check_shapes(ns, ["series"])
    with pytest.raises(ContractError, match="series_unit"):
        check_shapes({k: v for k, v in ns.items() if k != "series_unit"}, ["series"])
    with pytest.raises(ContractError, match="finite"):
        check_shapes({**ns, "series_values": np.array([1.0, np.nan, 3.0])}, ["series"])


def test_groups_needs_value_and_group_columns():
    ok = {"groups_table": pd.DataFrame({"value": [1.0, 2.0], "group": ["a", "b"]}),
          "groups_label": "area", "groups_unit": "nm²"}
    check_shapes(ok, ["groups"])
    with pytest.raises(ContractError, match="group"):
        check_shapes({**ok, "groups_table": pd.DataFrame({"value": [1.0]})}, ["groups"])
```
`tests/courseware/test_compose.py`:
```python
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
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `.venv/bin/python -m pytest tests/test_contracts.py tests/courseware/test_compose.py -q`
Expected: FAIL (missing modules `camel_data.contracts`, `courseware.compose`)

- [ ] **Step 3: Implement**

`src/camel_data/contracts.py`:
```python
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
```
`courseware/compose.py`:
```python
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
```
In `scripts/build_slice.py` change:
```python
PACKAGE_FILES = ("classroom.py", "spm.py", "grains.py")
```
to:
```python
PACKAGE_FILES = ("classroom.py", "spm.py", "grains.py", "contracts.py")
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `.venv/bin/python -m pytest -q`
Expected: all tests pass (previous 15 + new). Note: the fixture `data_demo` has no frame before it in `test_contract_check...`; the fixture lesson includes `frame_demo` first, so the params cell precedes `data_demo`.

- [ ] **Step 5: Commit**

```bash
git add courseware src/camel_data/contracts.py scripts/build_slice.py tests
git commit -m "courseware: composer with params cell, shape checks, and telemetry metadata"
```

---

### Task 4: CLI — build, execute, readability gate, random dial combinations

**Files:**
- Create: `courseware/combos.py`, `courseware/cli.py`, `courseware/__main__.py`
- Test: `tests/courseware/test_cli.py`

**Interfaces:**
- Consumes: `load_lesson`, `lesson_from_dict`, `ManifestError` (Task 2); `compose` (Task 3); `scripts/run_notebook.py` `run(path: Path) -> bool`; `scripts/readability.py` `markdown_text(path)` is for `.py`, so the CLI computes FK grade directly with `textstat` on the built notebook's markdown.
- Produces: `random_lessons(data: dict, module_roots, n: int, seed: int) -> list[Lesson]`; CLI `python -m courseware build LESSON.yaml... [--out build/lessons] [--execute] [--random N] [--seed S]`, exit code 1 on any failure.

- [ ] **Step 1: Write failing tests**

`tests/courseware/test_cli.py`:
```python
import json
from pathlib import Path

import yaml

from courseware.cli import main
from courseware.combos import random_lessons

FIX = Path(__file__).parent / "fixtures" / "modules"


def manifest(tmp_path, **over):
    d = {"id": "demo", "title": "Demo", "minutes": 40, "preset": "algebra1",
         "dials": {"messiness": "real"}, "params": {"sample_size": 4},
         "modules": ["frame_demo", "data_demo", "concept_demo"]}
    d.update(over)
    p = tmp_path / "demo.yaml"
    p.write_text(yaml.safe_dump(d, sort_keys=False))
    return p, d


def test_build_writes_notebook(tmp_path):
    p, _ = manifest(tmp_path)
    assert main(["build", str(p), "--out", str(tmp_path / "out"), "--modules", str(FIX)]) == 0
    nb = json.loads((tmp_path / "out" / "demo.ipynb").read_text())
    assert nb["metadata"]["camel"]["lesson"] == "demo"


def test_build_reports_manifest_error(tmp_path, capsys):
    p, _ = manifest(tmp_path, modules=["frame_demo", "concept_demo"])
    assert main(["build", str(p), "--out", str(tmp_path / "out"), "--modules", str(FIX)]) == 1
    assert "series" in capsys.readouterr().out


def test_random_lessons_are_valid_and_seeded(tmp_path):
    _, d = manifest(tmp_path)
    a = random_lessons(d, [FIX], n=5, seed=3)
    b = random_lessons(d, [FIX], n=5, seed=3)
    assert [[rm.settings for rm in l.modules] for l in a] == [[rm.settings for rm in l.modules] for l in b]
    assert all(l.id.startswith("demo-r") for l in a)
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `.venv/bin/python -m pytest tests/courseware/test_cli.py -q`
Expected: FAIL (`No module named 'courseware.cli'`)

- [ ] **Step 3: Implement**

`courseware/combos.py`:
```python
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
        for name, override in _entries(data["modules"]):
            mod = find_module(name, module_roots)
            choice = {dial: rng.choice(values) for dial, values in mod.dials.items()}
            entries.append({name: {**choice, **{k: v for k, v in override.items() if k not in mod.dials}}})
        d["modules"] = entries
        try:
            out.append(lesson_from_dict(d, module_roots))
        except ManifestError:
            continue  # an invalid combination: skip it, the builder would reject it too
    return out
```
`courseware/cli.py`:
```python
"""`python -m courseware build lessons/*.yaml [--execute] [--random N]`."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import nbformat
import textstat
import yaml

from courseware.combos import random_lessons
from courseware.compose import compose
from courseware.manifest import Lesson, ManifestError, lesson_from_dict

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MODULES = ROOT / "courseware" / "modules"
PLAIN_MAX_GRADE = 8.0


def _grade(nb) -> float:
    text = "\n".join(c.source for c in nb.cells if c.cell_type == "markdown")
    text = re.sub(r"\$[^$]*\$|`[^`]*`|<[^>]+>", " ", text)
    return textstat.flesch_kincaid_grade(text)


def _is_plain(lesson: Lesson) -> bool:
    return all(rm.settings.get("register", "plain") == "plain" for rm in lesson.modules)


def _write(lesson: Lesson, out: Path) -> Path:
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"{lesson.id}.ipynb"
    nbformat.write(compose(lesson), path)
    return path


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="courseware")
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build")
    b.add_argument("manifests", nargs="+")
    b.add_argument("--out", default=str(ROOT / "build" / "lessons"))
    b.add_argument("--modules", action="append", default=None)
    b.add_argument("--execute", action="store_true")
    b.add_argument("--random", type=int, default=0)
    b.add_argument("--seed", type=int, default=0)
    args = ap.parse_args(argv)

    roots = [Path(m) for m in (args.modules or [DEFAULT_MODULES])]
    out = Path(args.out)
    failures = 0
    built: list[tuple[Lesson, Path]] = []
    for mpath in args.manifests:
        data = yaml.safe_load(Path(mpath).read_text())
        try:
            lessons = [lesson_from_dict(data, roots)]
            lessons += random_lessons(data, roots, n=args.random, seed=args.seed) if args.random else []
        except ManifestError as exc:
            print(f"FAIL {mpath}: {exc}")
            failures += 1
            continue
        for lesson in lessons:
            path = _write(lesson, out)
            nb = nbformat.read(path, as_version=4)
            if _is_plain(lesson) and _grade(nb) > PLAIN_MAX_GRADE:
                print(f"FAIL {lesson.id}: reading grade {_grade(nb):.1f} > {PLAIN_MAX_GRADE} for register=plain")
                failures += 1
            built.append((lesson, path))
            print(f"built {path.relative_to(ROOT) if path.is_relative_to(ROOT) else path}")

    if args.execute and built:
        sys.path.insert(0, str(ROOT / "scripts"))
        from run_notebook import run  # executes against data/slice/camel-2dcc-v1.zip
        for _, path in built:
            if not run(path):
                failures += 1
    return 1 if failures else 0
```
`courseware/__main__.py`:
```python
import sys

from courseware.cli import main

sys.exit(main())
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `.venv/bin/python -m pytest -q`
Expected: all pass.

- [ ] **Step 5: Commit**

```bash
git add courseware tests/courseware
git commit -m "courseware: CLI with execution, plain-register reading gate, random dial combinations"
```

---

### Task 5: Pilot content — two datasets × two concepts, three manifests

**Files:**
- Create: `courseware/modules/frame/setup.py`, `courseware/modules/frame/exit_ticket_stats.py`,
  `courseware/modules/datasets/data_grain_areas.py`, `courseware/modules/datasets/data_afm_roughness.py`,
  `courseware/modules/concepts/concept_mean_median.py`, `courseware/modules/concepts/concept_outlier_effect.py`,
  `lessons/pilot-grains-algebra1.yaml`, `lessons/pilot-grains-mixed.yaml`, `lessons/pilot-roughness-explorer.yaml`
- Test: `tests/courseware/test_pilot.py`

**Interfaces:**
- Consumes: everything above; slice helpers `camel_data.classroom.load_table`, `camel_data.grains.load_grain_scans`, `whole_single`; `check_shapes`.
- Produces: shipped modules whose names later lessons reuse.

Content rules: follow `docs/plans/2026-09-10-algebra1-edition.md` for `register:plain` cells (≤ grade 8, one new science word, banned words) and the Explorer conventions for `register:explorer`. Mine text from `notebooks/algebra1/src/A2_how_bumpy.py` (plain) and `notebooks/src/02_how_smooth_is_smooth.py` / `06_counting_crystals.py` (explorer). Concept modules must use ONLY the standard shape variables (`series_values`, `series_label`, `series_unit`, `groups_table`, …) — never a dataset-specific name — and their answer checks recompute from `series_values`.

- [ ] **Step 1: Write `frame/setup.py`** — front matter `module: setup, kind: frame, minutes: 3`, then the two cells of `notebooks/src/_setup_cell.py` verbatim, plus one code cell `from camel_data.grains import *`.

- [ ] **Step 2: Write the two dataset modules.** `data_grain_areas.py`:
```python
# ---
# module: data_grain_areas
# kind: dataset
# produces: [series, groups]
# dials:
#   register: [plain, explorer]
#   messiness: [real, flagged]
# params:
#   sample_size: {default: 40, min: 10, max: 501}
#   seed: {default: 1, min: 0, max: 9999}
# minutes: 4
# ---
# %% [markdown] tags=["register:plain"]
# ## Our data: tiny triangle crystals
# Scientists grew tiny triangle-shaped crystals on a flat wafer and measured each one's area.

# %% [markdown] tags=["register:explorer"]
# ## Data: WSe2 islands on sapphire (sample 17458)
# Areas of islands found by a height rule in three 2 µm × 2 µm AFM fields.

# %%
_scans, _grains = load_grain_scans("camel-2dcc")
_pop = _grains[_grains["role"] == "population"]

# %% tags=["messiness:flagged"]
_pop = whole_single(_pop)   # keep only clean, whole, single triangles

# %% tags=["messiness:real"]
_pop = _pop[_pop["kind"] != "streak"]   # keep merged grains and dust: real data is messy

# %%
_pick = _pop.sample(n=min(PARAMS["sample_size"], len(_pop)), random_state=PARAMS["seed"])
series_values = _pick["area_nm2"].to_numpy(dtype=float)
series_label, series_unit = "triangle area", "nm²"
groups_table = _pick.rename(columns={"area_nm2": "value", "position": "group"})[["value", "group"]]
groups_label, groups_unit = series_label, series_unit
print(f"{len(series_values)} triangles loaded")
```
`data_afm_roughness.py` — same pattern: front matter `produces: [series, groups]`, dials `register`, `messiness`, params `sample_size {default: 60, min: 10, max: 1004}`, `seed`; loads `load_table("afm_summary")`; `messiness:flagged` drops rows with blank `growth_method` and substrate-only materials (`Al2O3`, `Sapphire`); `messiness:real` keeps them (blank growth method becomes the group `"not recorded"`); `series_values` = `rms_roughness_nm` of the sampled rows, label "bumpiness (RMS roughness)" in explorer / "bumpiness" in plain, unit "nm"; `groups_table` value = roughness, group = `growth_method`.

- [ ] **Step 3: Write the two concept modules.** `concept_mean_median.py` front matter: `kind: concept`, `accepts: [series]`, dials `guidance: [worked, fill, open]`, `register: [plain, explorer]`, `minutes: 10`. Cells: (a) plain / explorer intro markdown (mean = fair share; median = middle value) mentioning `series_label` only through code output; (b) a code cell that prints the first 10 values with `series_label` and `series_unit`; (c) `guidance:worked` — code computing `my_mean = series_values.mean()` and `my_median = np.median(series_values)` with comments; (d) `guidance:fill` — `my_mean = ...  # ✏️ add up the numbers and divide by how many` and `my_median = np.median(series_values)`; (e) `guidance:open` — markdown goal "Find the mean and median of the data; store them as `my_mean` and `my_median`." and an empty code cell `# your code here`; (f) an always-present check cell:
```python
import numpy as np
_ref_mean, _ref_median = float(np.mean(series_values)), float(np.median(series_values))
try:
    ok_mean = my_mean is not ... and abs(float(my_mean) - _ref_mean) <= 0.01 * abs(_ref_mean)
    ok_median = my_median is not ... and abs(float(my_median) - _ref_median) <= 0.01 * abs(_ref_median)
except (NameError, TypeError):
    ok_mean = ok_median = False
print("✅ Nice! Mean and median are right." if ok_mean and ok_median
      else f"🔁 Not yet. Hint: the mean adds all {len(series_values)} values and divides by {len(series_values)}.")
```
(g) a histogram of `series_values` with vertical lines at mean and median, axis label `f"{series_label} ({series_unit})"`.
`concept_outlier_effect.py`: `accepts: [series]`, `requires: {messiness: [real]}` (the lesson must keep messy data), dials `guidance` and `register`, `minutes: 8`: add the largest value ×5 as a "dust speck" to a copy of `series_values`, compare mean and median before/after with a two-bar plot, students predict which moves more (worked/fill/open variants), check recomputed from `series_values`.

- [ ] **Step 4: Write `frame/exit_ticket_stats.py`** (`kind: frame`, `minutes: 5`): plain and explorer variants of 3 no-code questions about mean vs median and outliers.

- [ ] **Step 5: Write the three manifests.**
`lessons/pilot-grains-algebra1.yaml`:
```yaml
id: pilot-grains-algebra1
title: "How Big Are the Triangles? Mean and Median"
minutes: 40
preset: algebra1
dials: {messiness: real}
params: {sample_size: 25, seed: 3}
modules:
  - setup
  - data_grain_areas
  - concept_mean_median: {guidance: worked}
  - concept_outlier_effect
  - exit_ticket_stats
```
`lessons/pilot-grains-mixed.yaml`: same modules, `preset: algebra1`, `dials: {messiness: real}`, overrides `concept_mean_median: {guidance: fill}`, `concept_outlier_effect: {guidance: open}`, `params: {sample_size: 100, seed: 3}`.
`lessons/pilot-roughness-explorer.yaml`: `preset: explorer`, modules `setup, data_afm_roughness, concept_mean_median, concept_outlier_effect, exit_ticket_stats`, `params: {sample_size: 300, seed: 1}`.

- [ ] **Step 6: Write `tests/courseware/test_pilot.py`**
```python
from pathlib import Path

from courseware.manifest import load_lesson
from courseware.compose import compose

ROOT = Path(__file__).resolve().parents[2]
ROOTS = [ROOT / "courseware" / "modules"]


def test_same_concept_module_runs_on_two_datasets():
    a = load_lesson(ROOT / "lessons/pilot-grains-algebra1.yaml", ROOTS)
    b = load_lesson(ROOT / "lessons/pilot-roughness-explorer.yaml", ROOTS)
    ma = next(rm for rm in a.modules if rm.module.name == "concept_mean_median")
    mb = next(rm for rm in b.modules if rm.module.name == "concept_mean_median")
    assert ma.module.path == mb.module.path
    assert ma.settings != mb.settings


def test_concept_modules_use_only_standard_shape_names():
    for p in (ROOT / "courseware/modules/concepts").glob("*.py"):
        text = p.read_text()
        for dataset_name in ("area_nm2", "rms_roughness_nm", "load_grain_scans", "load_table"):
            assert dataset_name not in text, f"{p.name} names dataset detail {dataset_name}"


def test_mixed_lesson_has_different_guidance_per_module():
    lesson = load_lesson(ROOT / "lessons/pilot-grains-mixed.yaml", ROOTS)
    g = {rm.module.name: rm.settings.get("guidance") for rm in lesson.modules}
    assert g["concept_mean_median"] == "fill" and g["concept_outlier_effect"] == "open"
    assert compose(lesson).metadata["camel"]["lesson"] == "pilot-grains-mixed"
```

- [ ] **Step 7: Rebuild the slice so it ships `contracts.py`, then build and execute everything**

Run:
```bash
.venv/bin/python scripts/build_slice.py
.venv/bin/python -m pytest -q
.venv/bin/python -m courseware build lessons/*.yaml --execute --random 6 --seed 11
```
Expected: pytest all pass; the CLI prints `built …` for 3 manifests + up to 18 random combinations, `OK` for every executed notebook, exit code 0. Fix module content (not the engine) until it does.

- [ ] **Step 8: Commit**

```bash
git add courseware lessons tests
git commit -m "courseware pilot: grain/roughness datasets × mean-median/outlier concepts, three manifests"
```

---

### Task 6: Real Colab check, docs, and review

**Files:**
- Modify: `README.md` (add "Composable courseware" section: module kinds, manifest example, dial table, build command)
- Create: none

- [ ] **Step 1:** Copy the new zip to OneDrive (same filename; the share link persists), then run the three built pilot notebooks in Colab with fresh kernels:
```bash
cp data/slice/camel-2dcc-v1.zip "$HOME/Library/CloudStorage/OneDrive-ThePennsylvaniaStateUniversity/Funding/Awarded/2026-03-CAMEL/CAMEL-2DCC-data/camel-2dcc-v1.zip"
scripts/colab_check.sh camel-final build/lessons/pilot-grains-algebra1.ipynb build/lessons/pilot-grains-mixed.ipynb build/lessons/pilot-roughness-explorer.ipynb
```
Expected: three lines with `errors []`.

- [ ] **Step 2:** Add the README section (≤ 40 lines) with the manifest example from Task 5 and the command from Task 5 Step 7.

- [ ] **Step 3:** Commit, then request a Codex review of `courseware/` and one built lesson; apply verified findings.

```bash
git add README.md
git commit -m "docs: composable courseware usage"
```
