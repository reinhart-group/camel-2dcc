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
- Use V = I × R, a direct-proportion formula, to compare two situations.

## Timing (30–40 min)

| Minutes | Section |
|---|---|
| 0–5 | Setup cell, meet-the-crystal hook |
| 5–12 | Task 1 — three temperature scales (3 conversions) |
| 12–20 | Task 2 — graph film 20198, describe it, read the zero-crossing |
| 20–26 | Task 3 — slope of the middle part |
| 26–32 | Task 4 — compare four films |
| 32–36 | Task 5 — V = I × R at two temperatures |
| 36–40 | Exit ticket |

## Expected answers

- **Task 1:** 20 °C = **293 K**; −196 °C = **−320.8 °F**; 5 K = **−268 °C = −450.4 °F**.
- **Task 2 (describe):** roughly — (a) 300 K→150 K: resistance rises a little as it cools (real
  data is a little bumpy); (b) 150 K→40 K: resistance drifts down in a fairly straight line; (c)
  below ~5 K: resistance drops almost to zero and stays there. Zero-crossing reading: accept
  **2–8 K** (true value **≈4.99 K**).
- **Task 3:** slope ≈ **1.0 ohm/K** (from the rounded points 1156 Ω at 50 K, 1256 Ω at 150 K).
- **Task 4:** **3 of 4** films reach close to zero resistance in this data. By sample:
  20198 ≈ **5.0 K**, 20199 = **never reaches it** (blank), 20200 ≈ **14.0 K**, 20201 ≈ **22.9 K**
  (highest — needs the least cooling).
- **Task 5:** at 20 K, R ≈ 1015.6 Ω → V ≈ **1.02 mV**; at 3 K, R ≈ 0 Ω → V ≈ **essentially 0** (any
  reading there is measurement noise, not real negative resistance).

## Common mistakes

1. **Reading a blank `T_zero_1pct_K` as "reaches zero at 0 K."** It means the film was never
   measured cold enough to find out — missing data, not a measured fact.
2. **Calling the middle-section slope "negative" because resistance eventually drops to zero.**
   Between 50 K and 150 K the slope really is positive (resistance rises while warming); the drop
   to zero only happens much further left, below about 5 K. Two different parts of the same graph.
3. **Dropping units on the slope answer.** "1.0" isn't the whole answer — it's 1.0 **ohms per
   kelvin**.

## If you have 10 more minutes

Have students repeat Task 3's slope calculation using two points from the 150 K–300 K portion of
the full graph instead, and compare the sign and size to the 50–150 K slope. Or: ask them to
predict, using Task 5's formula, what voltage a *bigger* current (like 0.001 A) would give at 3 K
— still basically zero, since R is basically zero.

## Verification

```
.venv/bin/jupytext --to ipynb notebooks/algebra1/src/A4_colder_and_colder.py -o notebooks/algebra1/A4_colder_and_colder.ipynb
.venv/bin/python scripts/run_notebook.py notebooks/algebra1/A4_colder_and_colder.ipynb
.venv/bin/python scripts/readability.py notebooks/algebra1/src/A4_colder_and_colder.py
```
Last run: `OK   A4_colder_and_colder.ipynb -> notebooks/executed/A4_colder_and_colder.ipynb`;
Flesch–Kincaid grade **6.6** (target ≤ 8.0).
