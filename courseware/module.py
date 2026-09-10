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
