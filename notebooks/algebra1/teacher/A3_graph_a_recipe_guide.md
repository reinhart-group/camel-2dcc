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

## Timing (30–40 min)

| Minutes | Section |
|---|---|
| 0–5 | Setup cell, meet-the-crystal hook |
| 5–10 | Task 1 — running total of minutes |
| 10–17 | Task 2 — read the graph |
| 17–22 | Task 3 — slope of the heat-up |
| 22–27 | Task 4 — write and solve the equation |
| 27–33 | Task 5 — change one number (slider + fixed check) |
| 33–37 | Task 6 — °C to °F |
| 37–40 | Exit ticket |

## Expected answers

- **Task 1:** running total of the first four steps = **30 minutes** (17+5+5+3). This matches the
  table's own `start_min` for step 5 — point that out if a student doesn't notice it themselves.
- **Task 2:** peak temperature **1000 °C**; the oven holds there for **23 minutes** (minute 17 to
  minute 40 — three anneal/growth steps back to back).
- **Task 3:** heat-up slope ≈ **57.4 °C/min** (exactly 975/17), *conditional on the 25 °C guess*.
- **Task 4:** reaches 500 °C at **t ≈ 8.3 min** under that same model.
- **Task 5:** starting at 200 °C instead: slope ≈ **47.1 °C/min**, reaches 500 °C at **t ≈ 6.4
  min** — faster, because there's less distance to climb.
- **Task 6:** 1000 °C = **1832 °F**.

## Common mistakes

1. **Reading the graph's flat part as "no change happening."** It's a real, deliberate hold step
   (annealing/growth), not the recipe pausing — ask what a flat line on *any* graph means.
2. **Treating the 25 °C start as a fact.** It's stated as a guess in two places (Task 2 intro and
   Task 3). If a student's Task 3 answer is exactly 57.4 but they can't say *why* it's an estimate,
   revisit that before moving on.
3. **Forgetting units when reporting slope.** "57" alone isn't an answer — it's 57.4 **°C per
   minute**. Watch for the "per minute" getting dropped in Tasks 3 and 5.

## If you have 10 more minutes

Have students pick their own alternate starting temperature (change the slider, or edit
`ALT_ROOM_TEMP_C`-style value by hand) and predict, before running, whether the new 500 °C time
will be bigger or smaller than 8.3 minutes — then check. Or: ask what starting temperature would
make the oven reach 500 °C in exactly 5 minutes (solve backwards for the assumed start).

## Verification

```
.venv/bin/jupytext --to ipynb notebooks/algebra1/src/A3_graph_a_recipe.py -o notebooks/algebra1/A3_graph_a_recipe.ipynb
.venv/bin/python scripts/run_notebook.py notebooks/algebra1/A3_graph_a_recipe.ipynb
.venv/bin/python scripts/readability.py notebooks/algebra1/src/A3_graph_a_recipe.py
```
Last run: `OK   A3_graph_a_recipe.ipynb -> notebooks/executed/A3_graph_a_recipe.ipynb`;
Flesch–Kincaid grade **6.5** (target ≤ 8.0).
