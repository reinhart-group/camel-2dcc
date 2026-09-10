# Teacher key — How Smooth Is Smooth? Statistics of Atom-Scale Surfaces

Student notebook: `notebooks/02_how_smooth_is_smooth.ipynb` (source: `notebooks/src/02_how_smooth_is_smooth.py`).

All numbers below were **computed by running the notebook** against the current slice
(`data/slice/camel-2dcc/` = `data/slice/camel-2dcc-v1.zip`, 1,004 rows in `afm_summary.csv`), not
typed from memory — see the `Verification` section. Scans were re-measured since the last version
of this key, so several numbers moved (e.g. median cleaned roughness is now ~0.75 nm, not the old
~0.55 nm). Give students **ranges**, not single values: only one current build was available to
compute from, so the ranges below are the measured value widened modestly to allow for the slice
being periodically rebuilt (new samples added/re-measured). Always trust a fresh run of the
notebook over this document.

`afm_summary.csv` holds **one selected AFM scan per sample** (a fixed pick-one-scan rule — skip
files an operator marked "modified," then take the largest scan on file, breaking ties by the
shortest name), not every scan taken. See `docs/slice-README.md`.

## Learning targets

- Compute RMS roughness by hand and recognize it as the standard deviation of heights (HSS.ID.A.4).
- Compare center and spread of two distributions using mean, median, and histograms; identify how
  outliers pull the mean (HSS.ID.A.1–3).
- Read box plots: median, IQR, the 1.5×IQR outlier rule; justify a log-scale choice when values
  span orders of magnitude; recognize why a box from very few points (n<10) can't be compared
  fairly to one from hundreds (HSS.ID.A.1–3).
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
  `np.std` and `rms()` to 4 decimals). `smoothest_surface` (SnTe) RMS ≈ **0.35–0.37 nm** — from the
  curated, fixed gallery, so this doesn't move when `afm_summary.csv` is rebuilt.
- **Task 2:** `gallium_selenide_bumps` (GaSe) RMS ≈ **17–18 nm**, about 50× the smooth scan (also
  gallery-fixed). Median height for both scans is **0.000 nm** (the arrays are centered), but the
  **mean** of the bumpy scan (≈**1.4 nm**) sits well above its median — a small number of very tall
  bumps pull it up. The histogram y-axis is **fraction of pixels per bin** (equal-width bins shared
  between both scans, via `weights=`), not a probability density — so bar heights are directly
  comparable and readable as "what fraction of this scan's pixels fall here."
- **Task 3:** raw row count is **950–1,050** (currently **1,004**). With defaults
  (`EXCLUDE_SUBSTRATE_LABELS=True`, `MISSING_GROWTH_METHOD="drop"`), expect **7–11**
  substrate-label rows excluded and **65–90** missing-growth-method rows dropped (plus a small
  number of rows with no `material` at all, dropped unconditionally) — **~10%** of rows removed
  overall (currently 106 of 1,004). **`EXCLUDE_SUBSTRATE_LABELS` is a classroom heuristic**: it
  excludes rows whose `material` label is one of `{Al2O3, Sapphire, GaAs, H2, Se}`, on the theory
  that those rows likely scanned bare substrate rather than a grown film — but the label alone
  doesn't prove what the AFM tip imaged, and GaAs/Se can be real sample materials on other rows.
  Median RMS roughness after cleaning is **0.65–0.85 nm** (currently **0.755 nm**); mean is
  **1.6–2.1 nm** (currently **1.846 nm**, pulled well above the median by rough outliers like
  In2Se3). The median moves only slightly between cleaning choices because the removed rows are a
  small fraction of the table — the intended lesson is that the *row count* is much more sensitive
  to the cleaning decision than the *median* is here.
- **Task 4a/4b:** the top-6-by-count materials are currently **MoS2 (n=339), WSe2 (212), WS2 (136),
  GaSe (51), MoSe2 (43), In2Se3 (33)** — expect the same set of six materials on a rebuild, counts
  within about ±15%. **In2Se3** has the highest median RMS roughness among the top 6 (currently
  median **3.41 nm**, IQR **5.47 nm**, ~9% outliers — expect median **2.8–4.0 nm**). **MoS2** is
  the smoothest of the top 6 (currently median **0.42 nm**, expect **0.35–0.50 nm**). By growth
  method: **MOCVD** median **0.55–0.70 nm** (currently 0.623 nm, n=751), **12–13%** outliers;
  **Hybrid MBE** median **1.4–1.7 nm** (currently 1.562 nm, n=144), **11–14%** outliers. **MBE has
  only n=3** — the notebook greys that box out and prints "exclude from the core comparison"; do
  not ask students to compare it against the other two. Have students compare *outlier fraction*
  (printed alongside the count), not raw count, since MOCVD's 751 scans will always show more raw
  outliers than Hybrid MBE's 144 even at a similar or lower rate.
- **Task 5 (confounding):** the material × growth-method crosstab shows growth method is
  **essentially completely confounded with material** in this slice — MOCVD rows are only
  MoS2/WSe2/WS2/MoSe2-family films (plus mixed alloys like Mo-WSe2), Hybrid MBE rows are a disjoint
  set of other materials (In2Se3, GaSe, InSe, MnTe, FeSe, SnSe, SnTe, Bi2Se3, ...), and the n=3 MBE
  rows are all Sb2Te3. Any claim "growth method X is smoother" cannot be separated from "material Y
  is smoother" with this data. Accept any answer that identifies confounding by material (also
  valid: substrate, scan size, or publication/selection bias).
- **Task 6 (Extend):** scan size vs. RMS roughness correlation coefficient is **essentially flat**,
  Pearson r currently **0.018**, expect **−0.05 to +0.10** on a rebuild — no clear linear trend.

## Common misconceptions

- "RMS roughness is a totally different formula from standard deviation." It is the same formula;
  the notebook shows this numerically in Task 1.
- "The histogram bar height is the fraction of pixels." True here *because* the notebook uses
  `weights=np.ones(n)/n` with shared bin edges and labels the axis "fraction of pixels per bin" —
  worth flagging that a default Matplotlib `density=True` histogram would *not* have this property
  (its bars are a probability density, area-normalized, not height-normalized).
- "Missing growth method = 0, or can be ignored safely." Missing is not zero — dropping vs. labeling
  "Unknown" changes which rows are analyzed.
- "`EXCLUDE_SUBSTRATE_LABELS` proves those rows aren't films." It's a label-based heuristic, not a
  verified physical fact about what was scanned.
- "The box plot proves growth method causes roughness differences." It shows a difference; the
  crosstab in Part 5 shows why cause can't be isolated here (confounding by material).
- "MOCVD has more outliers because it has more scans." Compare the *fraction*, not the count — at
  similar outlier rates, the bigger group will always show a bigger raw number.
- "A small r means no relationship at all." It only rules out a *straight-line* relationship at
  this scale; nonlinear/rank relationships can still exist.

## Troubleshooting

- No widgets or Plotly are used in this notebook — only Matplotlib static figures, so there is no
  custom-widget-manager dependency to debug.
- If `plot_box_by` errors on an older/newer Matplotlib inside Colab, note the fix already applied
  here: use `ax.set_xticks`/`ax.set_xticklabels` after `boxplot()` rather than the `labels=`/
  `tick_labels=` boxplot kwarg, which was renamed then removed across recent Matplotlib versions.
- The greyed-out, hatched box (n<10 groups, currently just `MBE`) is intentional — it's still drawn
  so nothing is hidden, but it's marked with `*` and excluded from the printed core comparison.
- If a student sets `MISSING_GROWTH_METHOD` to anything other than `"drop"`/`"unknown"`, the helper
  raises a clear `ValueError` — have them re-read the two allowed values.

## Verification

```
.venv/bin/jupytext --to ipynb notebooks/src/02_how_smooth_is_smooth.py -o notebooks/02_how_smooth_is_smooth.ipynb
set -a; . ./.env; set +a
.venv/bin/python scripts/run_notebook.py notebooks/02_how_smooth_is_smooth.ipynb
```
Last run: `OK   02_how_smooth_is_smooth.ipynb -> notebooks/executed/02_how_smooth_is_smooth.ipynb`
(1,004-row build, 2026-09-10). Printed values from that run: by-hand RMS 1.414 nm; SnTe gallery RMS
0.358 nm; GaSe gallery RMS 17.833 nm (mean 1.414 nm, median 0.000 nm); Task 3 raw=1004,
cleaned=898 (106 removed), median=0.755 nm, mean=1.846 nm; top-6 medians MoS2 0.422, WS2 0.516,
MoSe2 0.662, WSe2 0.983, GaSe 1.319, In2Se3 3.409 nm; growth-method MOCVD n=751 median=0.623 nm
(12.3% outliers), MBE n=3 median=1.087 nm (greyed out), Hybrid MBE n=144 median=1.562 nm (12.5%
outliers); scan-size correlation r=0.018.
