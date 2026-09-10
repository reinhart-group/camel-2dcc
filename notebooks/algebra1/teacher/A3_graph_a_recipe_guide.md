# Teacher guide — Graph a Recipe: Slope Is a Rate

Student notebook: `notebooks/algebra1/A3_graph_a_recipe.ipynb`
(source: `notebooks/algebra1/src/A3_graph_a_recipe.py`).

All numbers below came from running the notebook against the real data slice
(`data/slice/camel-2dcc-v1.zip`) — not typed from memory. Re-run
`.venv/bin/python scripts/run_notebook.py notebooks/algebra1/A3_graph_a_recipe.ipynb` any time the
slice is rebuilt, and give students the printed numbers if they differ from this page.

## Goals

- Read a piecewise graph and pull specific values off it (F.IF.4).
- Find and interpret slope as a rate of change, °C per minute (F.IF.6).
- Write a linear equation for a real situation and solve it for a target output (A.CED.2, A.REI.3).
- Change one assumption and see how it changes a whole linear model — an early look at
  conditional/what-if reasoning.
- Convert between °C and °F as two linear functions of the same quantity.

## Timing (30–40 min core; Tasks 5–6 are optional extras)

| Minutes | Section |
|---|---|
| 0–5 | Setup cell, meet-the-crystal hook |
| 5–10 | Task 1 — running total of minutes |
| 10–18 | Task 2 — read the graph |
| 18–24 | Task 3 — slope of the heat-up |
| 24–30 | Task 4 — write and solve the equation |
| — | *If you have time:* Task 5 (change one number) and Task 6 (°C to °F) |
| 30–35 | Exit ticket |

## Expected answers

- **Task 1:** running total of the first four steps = **30 minutes** (17+5+5+3). This matches the
  table's own Start minute for step 5 — point that out if a student doesn't notice it themselves.
  The recipe table now shows plain-language step names (Heat up, Hold hot 1/2/3, Grow the
  crystal, Cool down 1/2) instead of the raw `P.G. Annealing` labels, and blank temperatures
  during cool-down read "— not recorded" instead of a bare NaN.
- **Task 2:** peak temperature **1000 °C**; the oven holds there for **23 minutes** (minute 17 to
  minute 40 — three anneal/growth steps back to back).
- **Task 3:** heat-up slope ≈ **57.4 °C/min** (exactly 975/17), *conditional on the 25 °C guess*.
- **Task 4:** reaches 500 °C at **t ≈ 8.3 min** under that same model.
- **Task 5 (optional):** starting at 200 °C instead: slope ≈ **47.1 °C/min**, reaches 500 °C at
  **t ≈ 6.4 min** — faster, because there's less distance to climb.
- **Task 6 (optional):** 1000 °C = **1832 °F**, about **1,282 °F hotter** than a 550 °F home oven
  (a difference, not a multiple — Fahrenheit has an arbitrary zero, so "three times hotter" isn't
  a meaningful comparison).

## Common mistakes

1. **Reading the graph's flat part as "no change happening."** It's a real, deliberate hold step
   (annealing/growth), not the recipe pausing — ask what a flat line on *any* graph means.
2. **Treating the 25 °C start as a fact.** It's stated as a guess in two places (Task 2 intro and
   Task 3). If a student's Task 3 answer is exactly 57.4 but they can't say *why* it's an estimate,
   revisit that before moving on.
3. **Forgetting units when reporting slope.** "57" alone isn't an answer — it's 57.4 **°C per
   minute**. Watch for the "per minute" getting dropped in Tasks 3 and 5.

## If you have 10 more minutes

Tasks 5 (change one number, with a slider) and 6 (°C to °F) are built into the notebook as
optional extras right before the exit ticket — have fast finishers do those while others catch
up. If there's still time after that: ask what starting temperature would make the oven reach
500 °C in exactly 5 minutes (solve backwards for the assumed start).

## Verification

```
.venv/bin/jupytext --to ipynb notebooks/algebra1/src/A3_graph_a_recipe.py -o notebooks/algebra1/A3_graph_a_recipe.ipynb
.venv/bin/python scripts/run_notebook.py notebooks/algebra1/A3_graph_a_recipe.ipynb
.venv/bin/python scripts/readability.py notebooks/algebra1/src/A3_graph_a_recipe.py
```
Last run: `OK   A3_graph_a_recipe.ipynb -> notebooks/executed/A3_graph_a_recipe.ipynb`;
Flesch–Kincaid grade **6.7** (target ≤ 8.0).
