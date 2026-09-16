# The session page

This is the page a team uses during Kathy Hill's Breakout 1 at the Pennsylvania Department of
Education Data Literacy Summit. One link, one page, her four rounds in her order and timings.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/reinhart-group/camel-2dcc/blob/summit-menu/notebooks/summit/modeling_the_messy.ipynb)

It needs no Google account, no sign-in, no runtime and no installation. Every activity is
JavaScript saved inside the page, so it works on a phone in a private window. Nothing on the page
should be run; the run buttons are inert.

| Round | Minutes | Activities |
|---|---|---|
| Warm up — what are we even looking at? | 5 | three real scans in 3D |
| 1 — notice and wonder | 5 | W-01, W-02 |
| 2 — find the mess | 10 | M-05, M-02, M-11 |
| 3 — model it | 12 | G-01, G-15, G-06 |
| 4 — turn the dials | 8 | D-01 |

The item IDs point back into `notebooks/catalog/`, which holds all forty candidates. This page is
the subset chosen for the session; changing the selection means editing `ROUNDS` in
`scripts/build_session.py` and rebuilding.

Rebuild with:

    PYTHONPATH=courseware:src .venv/bin/python scripts/build_session.py

Supporting documents:

- `docs/summit/facilitator-crib.md` — what teams find in each round, the numbers, and the claims
  to correct if you hear them.
- `docs/summit/dataset-b-card.md` — replacement text for the Dataset B card on slide 15 and the
  link for slide 14.
- `docs/summit/webgl-3d-constraint.md` — why the page carries exactly one 3D viewer.
