"""Build the one page a team actually uses during Kathy Hill's summit session.

The catalog notebooks are a menu: forty items grouped by round, for Kathy to choose from.
This is the opposite. It is a single page, sequenced and timed to her deck's four rounds,
holding only the items that earn their place, with the facilitation text that makes a team
of three or four know what to do without a facilitator standing over them.

One page rather than four, for two reasons. Slide 14 carries one link or QR code, and a
team on a conference network should load one page once rather than four pages under time
pressure. A team in round 3 can also scroll back to what they noticed in round 1.

Everything is a saved JavaScript output, so the page works with no Google account, no
sign-in and no runtime. That is the whole delivery mechanism; see
docs/summit/webgl-3d-constraint.md for the one hard limit it comes with.

Usage: PYTHONPATH=courseware:src .venv/bin/python scripts/build_session.py
"""
from __future__ import annotations

import json
import pathlib
import sys

import nbformat

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "courseware"))
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

import catalog  # noqa: E402
import nbutil  # noqa: E402

WIDGETS = ROOT / "courseware/widgets"
CORE = (WIDGETS / "core.js").read_text()
SHELL = (WIDGETS / "shell.html").read_text()
SLICE = ROOT / "data/slice/camel-2dcc"
OUT = ROOT / "notebooks/summit/modeling_the_messy.ipynb"

# One vertical stretch for all three warm-up scans, so a team can compare their
# bumpiness by eye. At true scale every AFM scan looks like a sheet of paper: these
# surfaces are two micrometres wide and a few nanometres tall.
EXAGGERATION = 25

# 160 samples a side rather than the 256 default. The three scans dominate the page's
# download, and at 160 the pyramids and blocks are still clearly resolved while the
# notebook drops from 1.3 MB to a size a conference network can serve.
MAX_PIXELS = 160

GALLERY = [
    ("pyramids", "triangle_pyramids",
     "Bismuth selenide (Bi2Se3). The crystals grow as stacked triangles, so the surface "
     "comes out as a field of pyramids about 6 nm tall."),
    ("city blocks", "superconductor_blocks",
     "Iron selenide (FeSe), a superconductor. Cooled below about 8 kelvin it carries "
     "electricity with no resistance at all. Its crystals grow as rectangular blocks."),
    ("almost flat", "smoothest_surface",
     "Tin telluride (SnTe). This is the smoothest surface in our collection: the typical "
     "bump is 0.36 nm, about two atoms wide. Stretched 25 times like the other two, it is "
     "still nearly a sheet of glass."),
]


HEADER = """# Modeling the Messy

### Breakout 1 — Pennsylvania Department of Education Data Literacy Summit

Every activity on this page is already built and running. You do not need an account, a
sign-in, or an installation, and you never need to press a run button. Tap, drag and
choose. If a grey box with a ▶ appears beside an activity, ignore it.

Work in teams of three or four, one device between you. A second device helps, so one
person can keep notes while another drives.

**What you are looking at.** Penn State's 2D Crystal Consortium grows crystal films two
or three atoms thick — candidate materials for electronics thinner than anything made of
silicon today. This page carries their real records: **1,005 grown samples**, each with
the settings it was grown with and, for **899** of them, one microscope measurement of
how bumpy the surface came out. That measurement is called *roughness* and is given in
nanometres. A nanometre is a millionth of a millimetre; a sheet of paper is about
100,000 nanometres thick.

Some activities below count 1,000 samples and 894 measurements instead. That is because
they first set aside five rows where someone typed the name of the disc the crystal was
grown on into the box meant for the crystal. Each activity says which count it is using.
Noticing that kind of difference is most of round 2.

Nothing here was cleaned up, simplified or invented for the workshop. The mess you find
is the mess the scientists live with.

**How the next 35 minutes go.**

| | Round | Time |
|---|---|---|
| Warm up | What are we even looking at? | 5 min |
| 1 | Notice and wonder | 5 min |
| 2 | Find the mess | 10 min |
| 3 | Model it | 12 min |
| 4 | Turn the dials | 8 min |
"""

WARMUP_MD = """---

## Warm up — what are we even looking at? · 5 minutes

Pick a surface, then tap **spin it**. Drag to rotate and pinch to zoom.

These are not drawings. Each one is a real measurement: a needle sharpened to a single
atom was dragged back and forth across a real film, recording its height 250,000 times.
All three are stretched 25 times vertically, by the same amount, so you can compare them
fairly. Side to side they are one to two micrometres across — about a fiftieth of the
width of a human hair.

**Talk about, in one minute:** which of the three would you call rough, and what would
you have to measure to turn that word into a number?
"""

CLOSING_MD = """---

## Reflect

Three questions to take back to the room.

1. **Where did your team disagree?** Every activity above has at least one place where
   two reasonable people make different calls — which spellings mean the same material,
   which extreme readings to trust, whether a line through those points means anything.
   Those disagreements are the data literacy, not the noise around it.
2. **What did the dials cost?** The simplest version of this dataset is easy to teach
   and makes a promise the data cannot keep. The full version is honest and hard to
   start with. Where would you set the dials for your own students, and what would you
   tell them you had turned down?
3. **What is the equivalent dataset in your building?** Attendance, benchmark scores,
   course requests. Which of the messes you found here — hand-typed categories,
   missing values that are not missing at random, outliers that could be real or could
   be an instrument glitch — is already in that file?

### Three claims we are careful not to make

Teams often land on stronger conclusions than these records support, so it is worth
naming the limits out loud.

- Nothing here shows that a smoother film makes a better device. Roughness is one
  quality measurement among many.
- Nothing here shows that these samples became computer chips. 2D materials are
  *researched* as candidates for future electronics. That is the accurate sentence.
- Every relationship on this page is an association found in observational records of
  experiments that were never designed to be compared. None of them is a cause.

### If you want to see how it was built

Everything above is drawn by JavaScript saved inside this page, which is why it works
with no account. The same analyses in Python, with sliders you can rewrite yourself, are
in a separate notebook: **[Build your own widget](https://colab.research.google.com/github/reinhart-group/camel-2dcc/blob/summit-menu/notebooks/python_demo.ipynb)**.
That one needs a Google sign-in, and it is the honest answer to "where does this go in a
high school computer science class."

The full menu these activities were chosen from — forty items across the four rounds — is
at **[notebooks/catalog](https://github.com/reinhart-group/camel-2dcc/tree/summit-menu/notebooks/catalog)**.

*Data: Penn State 2D Crystal Consortium, via the LiST sample records. Built by the
Reinhart group at Penn State.*
"""


ROUNDS = [
    {
        "title": "Round 1 — notice and wonder",
        "minutes": 5,
        "intro":
            "Two things below carry no labels on purpose. Look first, name it second.\n\n"
            "**Your team's job:** write down two things you *notice* and one thing you "
            "*wonder*. Then tap the reveal button and see how close you were. Noticing "
            "something the reveal does not mention counts as a win.",
        "items": [
            ("W-01", "Look at this picture",
             "A picture from an instrument, with nothing explained yet. Zoom in if you can."),
            ("W-02", "Now look at this pile of numbers",
             "Now the same collection of samples as a pile of 894 numbers, again unlabelled. "
             "Shape first, meaning second."),
        ],
    },
    {
        "title": "Round 2 — find the mess",
        "minutes": 10,
        "intro":
            "Every problem in this round is real and is still in the files today. We added "
            "nothing and fixed nothing.\n\n"
            "**Your team's job:** for each activity, decide what you would *do* about the "
            "mess, and write down the rule you would apply — not just the verdict on one "
            "row. A rule is something a computer could follow. A verdict is not.",
        "items": [
            ("M-05", "One text box, thirty-five answers",
             "One box, filled in by hand by many people over several years. You do not need "
             "to know what any of these substances are — every rule you can switch on is "
             "decided from the shape of the text, or by noticing that two columns of the same "
             "row hold the same word. Turn one on and watch the chart."),
            ("M-02", "A reasonable rule that deletes a whole method",
             "A sensible-sounding rule — \"only use samples where both the growth time and "
             "the roughness were recorded\" — turns out to delete almost one entire growth "
             "method. Turn the requirements on and off and watch which group disappears. "
             "This is the single most important thing on the page."),
            ("M-11", "Which extreme readings would you trust?",
             "**If your team has time.** The roughest 66 readings, up to 92 nm, next to a "
             "collection whose typical sample measures 0.74 nm. Some are real mountains and "
             "some are the microscope tripping over a speck of dust. There is no answer key. "
             "Watch what your removals do to the mean, and to the median."),
        ],
    },
    {
        "title": "Round 3 — model it",
        "minutes": 12,
        "intro":
            "Now try to say something general. The recipe setting with enough spread to "
            "model is growth time, so that is where we start.\n\n"
            "**Your team's job:** get to a sentence you would be willing to defend, "
            "including its limits. \"We found no relationship\" is a real finding and is "
            "often the right answer here.",
        "items": [
            ("G-01", "Does growing a film longer make it rougher?",
             "Drag the controls, fit a line, and read its slope and R². Then ask the "
             "question the chart cannot answer for you: how many samples went into that "
             "line, and how many left the picture without saying so?"),
            ("G-15", "Check a claim, then rewrite it",
             "Pick a claim, look at the evidence for and against it, then rewrite the claim "
             "so it is true. The dropdown holds a second claim about growth method — try "
             "both if you can."),
            ("G-06", "How much does one sample tell you?",
             "**If your team has time.** Take a small random sample of measured crystals, "
             "then a bigger one, and watch how far the sample average wanders from the "
             "population average. Then try sampling only from the middle of the wafer and "
             "see what a convenient sample costs you."),
        ],
    },
    {
        "title": "Round 4 — turn the dials",
        "minutes": 8,
        "intro":
            "The same 1,005 samples, shown three different ways. Nothing about the data "
            "changes when you move these dials — only what a student meets first.\n\n"
            "**Your team's job:** find the setting you would hand to your own students on "
            "day one, and the setting you would want them to reach by the end of the unit. "
            "Say what you gave up at each.",
        "items": [
            ("D-01", "Turn all three complexity dials",
             "*Structural* is how many variables are in front of you. *Provenance* is "
             "whether the missing values and the odd spellings are shown or quietly "
             "resolved. *Statistical* is whether the noise and the outliers are left in."),
        ],
    },
]


def render(item: dict) -> str:
    """The same saved-JavaScript rendering the catalog notebooks use."""
    js = (WIDGETS / "items" / (item["item"] + ".js")).read_text()
    html = SHELL.replace("__ID__", "cw-" + item["id"].lower().replace(".", "-"))
    html = html.replace("__CORE__", CORE)
    html = html.replace("__DATA__", json.dumps(item["data"](), separators=(",", ":")))
    html = html.replace("__OPT__", json.dumps(item.get("opts", {}), separators=(",", ":")))
    return html.replace("__ITEM__", js.strip().rstrip(";"))


def gallery_html() -> str:
    """The warm-up 3D viewer: three scans, one live WebGL context, ever.

    Safari on this page cannot keep a second 3D scene alive; it kills every one of them,
    including the newest. So all three share one viewer that purges the previous scan
    before drawing the next, and this is the only 3D output allowed on the page.
    """
    from camel_data.classroom import load_gallery, surface_3d, surface_gallery_html, surface_preview

    scans = load_gallery(SLICE)
    entries = []
    for name, key, caption in GALLERY:
        scan = scans[key]
        spec = json.loads(surface_3d(scan, exaggeration=EXAGGERATION, max_pixels=MAX_PIXELS).fig.to_json())
        blob = json.dumps(spec)
        if "bdata" in blob:  # a base64 array would draw axes and colourbar but no surface
            raise ValueError(f"{key}: figure carries base64 arrays, not plain lists")
        entries.append((name, caption, spec, surface_preview(scan, exaggeration=EXAGGERATION)))
    return surface_gallery_html(entries, height=440, uid="summit-warmup")


def widget_cell(html: str, label: str) -> nbformat.NotebookNode:
    cell = nbformat.v4.new_code_cell(
        source=f"# {label} — already built and running below. Nothing to run.")
    cell.outputs = [nbformat.v4.new_output(
        "display_data", data={"text/html": html, "text/plain": f"<{label}>"})]
    return cell


def build() -> nbformat.NotebookNode:
    by_id = {e["id"]: e for e in catalog.items()}
    nb = nbformat.v4.new_notebook()
    md = nb.cells.append

    md(nbformat.v4.new_markdown_cell(
        nbutil.badge("notebooks/summit/modeling_the_messy.ipynb") + "\n\n" + HEADER))
    md(nbformat.v4.new_markdown_cell(WARMUP_MD))
    nb.cells.append(widget_cell(gallery_html(), "three real scans in 3D"))

    for rnd in ROUNDS:
        md(nbformat.v4.new_markdown_cell(
            f"---\n\n## {rnd['title']} · {rnd['minutes']} minutes\n\n{rnd['intro']}"))
        for item_id, heading, lead in rnd["items"]:
            item = by_id[item_id]
            md(nbformat.v4.new_markdown_cell(
                f"### {heading}\n\n{lead}\n\n<sub>{item_id} · "
                f"data: {item['source']}</sub>"))
            nb.cells.append(widget_cell(render(item), item_id))

    md(nbformat.v4.new_markdown_cell(CLOSING_MD))
    return nb


def main() -> int:
    nbutil.write(build(), OUT)
    kb = OUT.stat().st_size / 1024
    n = sum(len(r["items"]) for r in ROUNDS)
    print(f"{OUT.relative_to(ROOT)}: {n} activities + 3D warm-up, {kb:.0f} KB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
