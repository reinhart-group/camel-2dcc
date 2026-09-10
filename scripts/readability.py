"""Report the reading level of the words students read in each notebook source.

Usage: .venv/bin/python scripts/readability.py notebooks/src/*.py notebooks/algebra1/src/*.py

Only markdown cells count (code and comments are skipped). Math, code spans,
links, tables' pipes, and emoji are stripped first. Reports Flesch–Kincaid
grade, average sentence length, and the long "science words" that appear most.
"""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

import textstat


def markdown_text(path: Path) -> str:
    out, in_md = [], False
    for line in path.read_text().splitlines():
        if line.startswith("# %%"):
            in_md = "[markdown]" in line
            continue
        if in_md and line.startswith("#"):
            out.append(line[1:].strip())
    text = "\n".join(out)
    text = re.sub(r"\$[^$]*\$", " ", text)            # inline math
    text = re.sub(r"`[^`]*`", " ", text)              # code spans
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)  # links -> text
    text = re.sub(r"[|*_#>]+", " ", text)
    text = re.sub(r"[^\x00-\x7F°µ×]+", " ", text)     # emoji etc.
    return text


def main() -> None:
    rows = []
    for arg in sys.argv[1:]:
        p = Path(arg)
        if p.name.startswith("_"):
            continue
        t = markdown_text(p)
        words = re.findall(r"[A-Za-z][A-Za-z-]+", t)
        long_words = Counter(w.lower() for w in words if textstat.syllable_count(w) >= 4)
        rows.append((p.name, textstat.flesch_kincaid_grade(t), textstat.words_per_sentence(t),
                     len(words), ", ".join(w for w, _ in long_words.most_common(6))))
    print(f"{'notebook':42s} {'FK grade':>8s} {'words/sent':>10s} {'words':>6s}  frequent long words")
    for name, g, s, n, lw in rows:
        print(f"{name:42s} {g:8.1f} {s:10.1f} {n:6d}  {lw}")


if __name__ == "__main__":
    main()
