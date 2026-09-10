# Teacher key — How Smooth Is Smooth? Statistics of Atom-Scale Surfaces

Student notebook: `notebooks/02_how_smooth_is_smooth.ipynb` (source: `notebooks/src/02_how_smooth_is_smooth.py`).

All numbers below were **computed by running the notebook** against two real slice builds
(`data/slice/camel-2dcc/` at 543 rows and `data/slice/camel-2dcc-v1.zip` at 1,004 rows), not typed
from memory. Give ranges to students, not single values — the final build (~1,000 rows) will land
somewhere in these ranges, and running the notebook always prints the current numbers.

## Learning targets

- Compute RMS roughness by hand and recognize it as the standard deviation of heights (HSS.ID.A.4).
- Compare center and spread of two distributions using mean, median, and histograms; identify how
  outliers pull the mean (HSS.ID.A.1–3).
- Read box plots: median, IQR, the 1.5×IQR outlier rule; justify a log-scale choice when values
  span orders of magnitude (HSS.ID.A.1–3).
- Make a data-cleaning decision explicitly, and observe that "missing" is not "zero" (HSS.ID.A.1).
- Evaluate a causal claim from observational data and name a confound (HSS.IC.B.6).

## Timing (45–50 min)

| Minutes | Section |
|---|---|
| 0–5 | Setup cell, hook |
| 5–15 | Part 1 — RMS by hand + on a real scan (Task 1, 1b) |
| 15–22 | Part 2 — histograms, predict-then-check, mean vs. median (Task 2, 2b) |
| 22–30 | Part 3 — cleaning decisions on `afm_summary.csv` (Task 3, 3b) |
| 30–40 | Part 4 — box plots by material and growth method (Task 4a, 4b) |
| 40–45 | Part 5 — claim/evidence/reasoning, confounding (Task 5) |
| 45–50 | Exit ticket (+ Task 6 Extend if time allows) |

## Expected answers (ranges)

- **Task 1/1b:** by-hand RMS on `[8,10,12,9,11]` is exactly **1.414 nm** (deterministic — matches
  `np.std` and `rms()` to 4 decimals). `smoothest_surface` (SnTe) RMS ≈ **0.36 nm** — from the
  curated gallery, stable across builds.
- **Task 2:** `gallium_selenide_bumps` (GaSe) RMS ≈ **17–18 nm**, about 50× the smooth scan.
  Median height for both scans is ≈0 (the array is centered), but the **mean** of the bumpy scan
  is pulled well above its median (≈1.4 nm vs. 0 nm) by a small number of very tall bumps — a
  clean illustration of mean vs. median with outliers.
- **Task 3:** raw row count is **500–1,050** (grows toward 1,000). With defaults
  (`EXCLUDE_BARE_SUBSTRATES=True`, `MISSING_GROWTH_METHOD="drop"`), expect **7–9** bare-substrate
  rows removed and **35–90** missing-growth-method rows removed — roughly **10–12% of rows**
  removed overall. Median RMS roughness after cleaning is **0.5–0.75 nm**; it moves only slightly
  between cleaning choices because the removed rows are a small fraction of the table — the
  intended lesson is that the *row count* is much more sensitive to the cleaning decision than the
  *median* is here.
- **Task 4a/4b:** the top-6-by-count materials are consistently **MoS2, WSe2, WS2, GaSe, In2Se3,
  MoSe2** (same set in both builds, order by median varies slightly with sample size). **In2Se3**
  has the highest median RMS roughness among the top 6 in both builds (median **3.3–3.5 nm**, IQR
  **5–5.5 nm**, n=33 in both builds — likely the full population of published In2Se3 AFM scans).
  MoS2 is the smoothest of the top 6 (median **0.35–0.40 nm**). By growth method: **MOCVD** median
  **0.48–0.55 nm** (n grows from ~350 to ~750); **Hybrid MBE** median **1.5–1.6 nm** (n≈144, stable
  — likely all published Hybrid MBE AFM scans); **MBE** has only **n=3** — flag this as too few
  points to trust a box plot from, a good discussion point about sample size.
- **Task 5 (confounding):** the material × growth-method crosstab shows growth method is nearly
  **completely confounded with material** in this slice — MOCVD rows are essentially only
  MoS2/WSe2/WS2/MoSe2 family films, Hybrid MBE rows are a disjoint set of materials (In2Se3, GaSe,
  InSe, MnTe, ...). Any claim "growth method X is smoother" cannot be separated from "material Y is
  smoother" with this data. Accept any answer that identifies confounding by material (also valid:
  substrate, scan size, or publication/selection bias).
- **Task 6 (Extend):** scan size vs. RMS roughness correlation coefficient is **essentially flat**,
  r between **−0.05 and +0.05** in both builds (Pearson) — no clear linear trend. A Spearman rank
  check (not in the student notebook) gives a weak positive value (~0.3) in the smaller build,
  worth mentioning only to advanced students as "a rank trend can exist even when the straight-line
  r looks like zero."

## Common misconceptions

- "RMS roughness is a totally different formula from standard deviation." It is the same formula;
  the notebook shows this numerically in Task 1.
- "Missing growth method = 0, or can be ignored safely." Missing is not zero — dropping vs. labeling
  "Unknown" changes which rows are analyzed.
- "The box plot proves growth method causes roughness differences." It shows a difference; the
  crosstab in Part 5 shows why cause can't be isolated here (confounding by material).
- "A small r means no relationship at all." It only rules out a *straight-line* relationship at
  this scale; nonlinear/rank relationships can still exist (see Task 6 note).

## Troubleshooting

- No widgets or Plotly are used in this notebook — only Matplotlib static figures, so there is no
  custom-widget-manager dependency to debug.
- If `plot_box_by` errors on an older/newer Matplotlib inside Colab, note the fix already applied
  here: use `ax.set_xticks`/`ax.set_xticklabels` after `boxplot()` rather than the `labels=`/
  `tick_labels=` boxplot kwarg, which was renamed then removed across recent Matplotlib versions.
- If a student sets `MISSING_GROWTH_METHOD` to anything other than `"drop"`/`"unknown"`, the helper
  raises a clear `ValueError` — have them re-read the two allowed values.

## Verification

```
.venv/bin/jupytext --to ipynb notebooks/src/02_how_smooth_is_smooth.py -o notebooks/02_how_smooth_is_smooth.ipynb
.venv/bin/python scripts/run_notebook.py notebooks/02_how_smooth_is_smooth.ipynb
```
Last run: `OK   02_how_smooth_is_smooth.ipynb -> notebooks/executed/02_how_smooth_is_smooth.ipynb`
(1,004-row zip build).
