# Teacher key — Counting Crystals: Grains, Samples, and Populations

Student notebook: `notebooks/06_counting_crystals.ipynb` (source: `notebooks/src/06_counting_crystals.py`).

All numbers below were **printed by running the notebook** against the current slice
(`data/slice/camel-2dcc-v1.zip` → `camel-2dcc/grains/`, 879 rows in `grains.csv`), not typed from
memory — see Verification. Give students **ranges**, not single values: the slice can be
rebuilt with re-measured/re-detected grains, which will move these numbers slightly. Always trust
a fresh run of the notebook over this document.

`grains.csv` is one row per detected blob from a simple height-threshold rule (see
`src/camel_data/grains.py` docstring), not a hand count. `whole_single()` keeps only grains
labeled `single` that don't touch the scan edge or a bad ("glitch") scan row — that's the set used
for every population/sample calculation.

## Learning targets (student language)

- I can judge an automated measurement rule against the actual picture, and explain a specific way
  it can be fooled (HSG.MG.A.3).
- I can measure a length from a scaled image and use it to predict an area with
  A = (√3/4)s², checking that prediction against an independently measured value (HSG.GMD.A;
  HSN.Q.A.1–3).
- I can read a height profile (line scan) and describe widths and heights in real units, including
  a case where a measured value doesn't match a textbook value (HSN.Q.A.1–3).
- I can distinguish a population from a sample, build a random sample, and explain why a sample
  mean varies from sample to sample (HSS.IC.A.1–2).
- I can describe, from a simulation, how the spread of a sampling distribution shrinks as sample
  size grows (HSS.IC.B.4).
- I can distinguish bias (a systematic, direction-consistent error from *how* a sample was chosen)
  from random error (chance variation that shrinks with more data) (HSS.IC.B.4).

## Timing (45 min)

| Minutes | Section |
|---|---|
| 0–5 | Setup cell, load data |
| 5–12 | Part 1 — spot the mistake (Task 1) |
| 12–20 | Part 2 — why triangles, measure a grain two ways (Task 2) |
| 20–30 | Part 3 — line scans on 3 different scans (Tasks 3, 3b) |
| 30–40 | Part 4 — population vs. sample, sampling distributions (Tasks 4, 5) |
| 40–43 | Part 5 — comparing the 3 spots, bias (Task 6) |
| 43–45 | Exit ticket |
| (+10–15 optional) | Extension (Task 7): seeds vs. islands, merged grains |

## Expected answers (ranges)

- **Task 1 (mistake):** `wse2_17458_center` currently has 251 detected grains total, 191 whole
  single triangles (expect 240–260 / 180–200 on a rebuild). Grains 3 and 7 are the mistake: a
  glitch in scan row 1 (heights spuriously ~400+ nm there) cuts one real bright particle into a
  thin edge-touching sliver (grain 3, `streak`, `touches_edge=True`) and a rounder blob below it
  (grain 7, `dust`, taller than typical because part of its top is missing). **Both are flagged
  `touches_glitch=True`** and are excluded by `whole_single()` before any population/sample work —
  the point isn't that the rule is broken, it's that a student can verify why a specific grain was
  thrown out.
- **Task 2 (geometry):** grain 217, area ≈ **1,400–1,450 nm²** (currently 1,419 nm², measured by
  counting pixels), true `side_nm` ≈ **57 nm** (not shown to students as the target — it's derived
  from area, so comparing to it would be circular). A reasonable grid read of the side (45–70 nm)
  predicts an area of roughly 880–2,120 nm²; the check-yourself cell accepts any predicted area
  within 2× of the measured 1,419 nm² (ratio 0.5–2.0), which a careful grid read should clear
  comfortably (a read of 50–65 nm gives ratio 0.68–1.15).
- **Task 3 (grain profile):** grain 217, angle 90°, peak height currently **1.9–2.0 nm** on this
  run (expect **1.5–2.2 nm** on a rebuild); the raised region is roughly **40–55 nm** wide at half
  the peak height. This motivates the Scientist's note: measured peak height (~1.5–2.0 nm) reads
  noticeably above the ~0.65–0.7 nm textbook WSe2 monolayer step — do not let students conclude a
  specific layer count from it.
- **Task 3b (line scans):** `wse2_24111_center` from (615, 882) nm to (695, 882) nm: flat substrate
  ≈0.1–0.2 nm for the first ~30 nm, then a rise of roughly **1.0–1.5 nm** onto the crystal/rim by
  the end of the line. `snse_39166_top` from (3200, 1550) nm to (4900, 1550) nm: a clear staircase
  with **3–5** distinguishable flat treads between roughly −0.9 nm and +1.3 nm; accept any answer
  in that range — the point is counting distinguishable flat-ish segments, not an exact number.
- **Task 4/5 (population & sampling):** population N = **501** whole single triangles across the
  three `wse2_17458_*` scans (currently center 191, flat 206, edge 104 — expect each within about
  ±15 on a rebuild). Population mean μ ≈ **1,850–1,950 nm²** (currently 1,889 nm²), population SD
  ≈ **950–1,100 nm²** (currently 1,024 nm²). A single n=10 sample can reasonably land anywhere
  roughly **μ ± 700 nm²** (SE ≈ σ/√10 ≈ 324 nm²; differences of 1–2 SE are common and expected —
  don't treat any single draw as "wrong"). Sampling-distribution SD of the mean: currently
  **n=5 → ≈465 nm²**, **n=20 → ≈220 nm²**, **n=50 → ≈135 nm²** (expect each within about ±15%),
  each close to the σ/√n prediction (458, 229, 145 nm²) — small deviations are expected because the
  simulation samples *without replacement* from a finite population of 501.
- **Task 6 (bias):** "toward the edge" mean currently ≈ **2,800–2,850 nm²**, about **+45% to +55%**
  above μ — expect this gap to persist in sign and rough size on a rebuild (it reflects real
  wafer-position dependence, not sampling noise: n=104 there is already large). "center" mean
  currently ≈ **1,450–1,500 nm²** (about 20–25% *below* μ); "toward the flat" is closest to μ
  (currently ≈1,800–1,820 nm², within ~5%). The key point: more grains at the edge would *not* fix
  this — it's bias from *where* you looked, not random error from *how many* you measured.
- **Task 7 (extension):** `wse2_17464_center` (no growth step) currently covers **≈4%** of the
  wafer vs. **≈10–11%** for `wse2_17458_center`; it has *far fewer* whole single triangles per µm²
  (currently ≈7–8/µm² vs. ≈45–50/µm²) despite a *larger* mean triangle area (currently ≈4,000–4,500
  nm² vs. ≈1,450–1,500 nm²) — so the lower coverage here comes from having fewer seeds, not smaller
  ones; flag the caveat that the 5 µm/coarser-pixel scan can under-detect the smallest seeds, so
  this isn't a fully apples-to-apples comparison. Merged grains: currently **≈11–13%** of all
  detections in the three population scans, with mean area (≈3,400–3,800 nm²) roughly **1.8–2×**
  the clean-single mean (≈1,850–1,950 nm²) — counting merged blobs as single triangles would push
  the population mean *up*; accept any answer noting that excluding them could still bias the
  population *down* somewhat, since bigger/more numerous neighbors are more likely to touch and
  merge, so the truly biggest grains are undercounted.

## Common misconceptions

- "The computer's grain rule is just wrong." It correctly measured what was in the pixels; a bad
  scan row physically disconnected one particle into two blobs. The lesson is verifying an
  automated measurement against the picture, not distrusting all automation.
- "`side_nm` in the table proves the area formula." It doesn't — `side_nm` was calculated *from*
  `area_nm2` using this exact formula, so it can't independently verify itself. The notebook's
  check compares a grid-measured side against the pixel-counted area instead.
- "Higher measured AFM height means more atomic layers." Not without more evidence — height here
  reads well above the textbook monolayer step; adsorbed water, tip shape, and calibration all
  inflate AFM height on sapphire. The notebook deliberately does not claim a layer count.
- "A random sample of 10 should give exactly μ." It won't, usually — sampling variability is the
  point of Task 4/5. Only the *distribution* of many sample means clusters tightly around μ, and
  only once n is reasonably large.
- "More grains always fixes a bad estimate." Only fixes *random* error. The edge-only "lazy
  scientist" in Task 6 is biased by *where* they looked — scanning more grains at the same biased
  spot doesn't move the estimate toward μ.
- "Throwing out merged grains is obviously the fair, unbiased choice." It's the defensible choice
  for measuring individual-triangle geometry, but it isn't automatically unbiased — bigger/more
  crowded triangles are more likely to have merged, so excluding them could still skew the
  remaining "clean" population smaller than the truth. Accept students who raise this critically.
- "The bar of tiny grains at the far left of the population histogram is an error." Partly real,
  partly the rule: grains of about 200–400 nm² are only 12–26 pixels, so they mix genuinely small
  (late-forming) triangles with a few specks the rule kept. The smallest size the rule accepts is
  12 pixels (about 180 nm² on these scans). Good discussion point: where you set a cutoff changes
  the population you study.

## Troubleshooting

- No ipywidgets/Plotly widgets are used anywhere in this notebook — every figure is a static
  Matplotlib plot, so there's no Colab custom-widget-manager dependency to debug.
- `ax.boxplot` in Part 5 uses `ax.set_xticks`/`ax.set_xticklabels` after `boxplot()`, not the
  `labels=`/`tick_labels=` boxplot keyword — that keyword was renamed then removed across recent
  Matplotlib versions (same fix already applied in notebook 02).
- If a student picks a different `GRAIN` id in Task 2/3, any id works as long as it's a row from
  `whole_single(table, "wse2_17458_center")`; picking a `grain` id that isn't a whole single (e.g.
  a merged one) will raise on the `.iloc[0]` lookup — tell them to pick from the green-outlined
  triangles in the Part 1 picture.
- `random_sample` draws without replacement, so `n` can never exceed the population size (501 here,
  well above anything asked).

## Verification

```
.venv/bin/jupytext --to ipynb notebooks/src/06_counting_crystals.py -o notebooks/06_counting_crystals.ipynb
.venv/bin/python scripts/run_notebook.py notebooks/06_counting_crystals.ipynb
```

Last run: `OK   06_counting_crystals.ipynb -> notebooks/executed/06_counting_crystals.ipynb`
(879-row `grains.csv` build, 2026-09-10). Printed values from that run: mistake grains 3
(`streak`, area 320 nm², row 0.000) and 7 (`dust`, area 2,197 nm², row 5.958), both
`touches_glitch=True`; scan `wse2_17458_center` has 251 detected grains, 191 whole singles; grain
217 area 1,419 nm², height 1.61 nm; Task 2 predicted area 1,310 nm² vs. measured 1,419 nm² (ratio
0.92, "Reasonable!"); Task 3 grain-217 profile peak 1.94 nm; population N=501, μ=1,889 nm²,
σ=1,024 nm²; sample seed=3, n=10, x̄=2,243 nm² (+354 nm² from μ); sampling-distribution SD of the
mean — n=5: 465 nm², n=20: 221 nm², n=50: 134 nm²; spot means — center 1,469 nm² (n=191), toward
the flat 1,809 nm² (n=206), toward the edge 2,818 nm² (n=104, +49% vs. μ); Task 7 — 17458 center
10.4% coverage / 191 triangles / 47.8 per µm² / mean 1,469 nm², 17464 center 4.3% coverage / 191
triangles / 7.6 per µm² / mean 4,277 nm²; merged grains 77 of 643 total population detections
(12%), mean merged area 3,628 nm² vs. mean clean-single area 1,889 nm².
