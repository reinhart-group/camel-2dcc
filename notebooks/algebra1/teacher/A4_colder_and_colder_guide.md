# Teacher guide — Colder and Colder: Graphs With a Surprise

Student notebook: `notebooks/algebra1/A4_colder_and_colder.ipynb`
(source: `notebooks/algebra1/src/A4_colder_and_colder.py`).

All numbers below came from running the notebook against the real data slice
(`data/slice/camel-2dcc-v1.zip`) — not typed from memory. Re-run
`.venv/bin/python scripts/run_notebook.py notebooks/algebra1/A4_colder_and_colder.ipynb` any time
the slice is rebuilt, and give students the printed numbers if they differ from this page.

## Goals

- Convert a temperature between Celsius, Kelvin, and Fahrenheit (all three are linear functions
  of each other).
- Read and describe a graph in pieces — informal piecewise reasoning (F.IF.4).
- Find slope from two points, with units (ohms per kelvin) (F.IF.6).
- Read a table honestly, including what a blank cell does and doesn't mean.
- *(Optional)* Use V = I × R, a direct-proportion formula, to compare two situations.

## Sample-identity note for teachers

The AFM picture in "Meet the crystal" is a *different* physical piece (sample 20382) from the
four films whose resistance is graphed later (samples 20198–20201, called Film A–D in the
notebook). All five are FeSe, made the same way, but the picture is not "the same film" as any
one resistance curve — the notebook now says so explicitly. Don't let students infer that the
picture's blocky surface explains a specific curve's transition temperature.

## Timing (30–40 min core; Task 5 is an optional extra)

| Minutes | Section |
|---|---|
| 0–5 | Setup cell, meet-the-crystal hook |
| 5–11 | Task 1 — three temperature scales (3 conversions) |
| 11–21 | Task 2 — graph Film A, describe it (reveal check), read the zero-crossing |
| 21–27 | Task 3 — slope of the middle part |
| 27–33 | Task 4 — compare four films |
| — | *If you have time:* Task 5 — V = I × R at 20 K |
| 33–38 | Exit ticket |

## Expected answers

- **Task 1:** 20 °C = **293 K**; −196 °C = **−320.8 °F**; 5 K = **−268 °C = −450.4 °F**.
- **Task 2 (describe):** roughly — (a) 300 K→150 K: resistance rises a little as it cools (real
  data is a little bumpy); (b) 150 K→40 K: resistance drifts down in a fairly straight line; (c)
  below ~5 K: resistance drops fast until it's too small to measure. A model-answer reveal cell
  now follows this prompt — check that students ran it and compared, not just skipped ahead.
  Zero-crossing reading: accept **2–8 K** (true value **≈4.99 K**).
- **Task 3:** slope ≈ **1.0 ohm/K** (from the rounded points 1156 Ω at 50 K, 1256 Ω at 150 K).
- **Task 4:** **3 of 4** films reach close to zero resistance in this data. By film:
  Film A (20198) ≈ **5.0 K**, Film B (20199) = **never reaches it in this data** (blank), Film C
  (20200) ≈ **14.0 K**, Film D (20201) ≈ **22.9 K** (highest — needs the least cooling). The table
  shown to students now uses these plain Film names and spells out the 1%-of-40K-resistance rule
  behind "Temperature where resistance is near zero" — don't let students read the blank as "hit
  exactly 0 K" or invent a reason (growth difference, etc.) for why Film B has no reading; the
  honest answer is "not measured cold enough in this data."
- **Task 5 (optional):** at 20 K, R ≈ 1015.6 Ω → V = 0.000001 × 1015.6 ≈ **1.02 mV**. The reveal
  notes that at 3 K, R ≈ 0 Ω, so V is about 0 too — same idea, one unit (mV), no digit-piling.

## Common mistakes

1. **Reading a blank "near zero" cell as "reaches zero at 0 K."** It means the film wasn't
   measured cold enough to find out — missing data, not a measured fact, and not evidence the
   film is somehow different.
2. **Calling the middle-section slope "negative" because resistance eventually drops to zero.**
   Between 50 K and 150 K the slope really is positive (resistance rises while warming); the drop
   to zero only happens much further left, below about 5 K. Two different parts of the same graph.
3. **Dropping units on the slope answer.** "1.0" isn't the whole answer — it's 1.0 **ohms per
   kelvin**.

## If you have 10 more minutes

Task 5 (V = I × R) is built into the notebook as an optional extra right before the exit ticket —
have fast finishers do that. If there's still time: have students repeat Task 3's slope
calculation using two points from the 150 K–300 K portion of the full graph instead, and compare
the sign and size to the 50–150 K slope.

## Verification

```
.venv/bin/jupytext --to ipynb notebooks/algebra1/src/A4_colder_and_colder.py -o notebooks/algebra1/A4_colder_and_colder.ipynb
.venv/bin/python scripts/run_notebook.py notebooks/algebra1/A4_colder_and_colder.ipynb
.venv/bin/python scripts/readability.py notebooks/algebra1/src/A4_colder_and_colder.py
```
Last run: `OK   A4_colder_and_colder.ipynb -> notebooks/executed/A4_colder_and_colder.ipynb`;
Flesch–Kincaid grade **6.8** (target ≤ 8.0).
