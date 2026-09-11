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


def _grade(nb, plain_only: bool = False) -> float:
    """Flesch-Kincaid grade of markdown cells, with math/code/HTML stripped.

    Note: This is not the same as scripts/readability.py's markdown_text(),
    which also strips links, pipes, and emoji. The CLI gate uses this narrower
    stripping to focus on mathematical and code-fence complexity only.

    Important: ``nb`` here is a COMPOSED notebook (every module in the lesson,
    concatenated). This grade is not comparable to running textstat on a single
    module file's markdown in isolation — a short excerpt swings wildly on one
    long word. Always re-measure via a built notebook, never a module alone.
    """
    cells = [c for c in nb.cells if c.cell_type == "markdown"]
    if plain_only:
        cells = [c for c in cells
                 if c.metadata.get("camel", {}).get("dials", {}).get("register", "plain") == "plain"]
    text = "\n".join(c.source for c in cells)
    text = re.sub(r"\$[^$]*\$|`[^`]*`|<[^>]+>", " ", text)
    return textstat.flesch_kincaid_grade(text)


def _is_plain(lesson: Lesson) -> bool:
    return any(rm.settings.get("register", "plain") == "plain" for rm in lesson.modules)


def _write(lesson: Lesson, nb: nbformat.NotebookNode, out: Path) -> Path:
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"{lesson.id}.ipynb"
    nbformat.write(nb, path)
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
        try:
            data = yaml.safe_load(Path(mpath).read_text())
        except (FileNotFoundError, yaml.YAMLError) as exc:
            print(f"FAIL {mpath}: {exc}")
            failures += 1
            continue
        try:
            lessons = [lesson_from_dict(data, roots)]
            if args.random:
                random_combos = random_lessons(data, roots, n=args.random, seed=args.seed)
                if not random_combos:
                    print(f"FAIL {mpath}: --random {args.random} produced 0 valid lesson combinations from {', '.join(str(r) for r in roots)}")
                    failures += 1
                    continue
                lessons += random_combos
        except ManifestError as exc:
            print(f"FAIL {mpath}: {exc}")
            failures += 1
            continue
        for lesson in lessons:
            nb = compose(lesson)
            if _is_plain(lesson):
                grade = _grade(nb, plain_only=True)
                if grade > PLAIN_MAX_GRADE:
                    print(f"FAIL {lesson.id}: reading grade {grade:.1f} > {PLAIN_MAX_GRADE} for register=plain")
                    failures += 1
                    continue
            path = _write(lesson, nb, out)
            built.append((lesson, path))
            print(f"built {path.relative_to(ROOT) if path.is_relative_to(ROOT) else path}")

    if args.execute and built:
        sys.path.insert(0, str(ROOT / "scripts"))
        from run_notebook import run  # executes against data/slice/camel-2dcc-v1.zip
        for _, path in built:
            if not run(path):
                failures += 1
    return 1 if failures else 0
