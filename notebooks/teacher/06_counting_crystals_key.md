# Teacher key — Counting Crystals: Grains, Samples, and Populations

Student notebook: `notebooks/06_counting_crystals.ipynb` (source: `notebooks/src/06_counting_crystals.py`).

All numbers below were **printed by running the notebook** against the current slice
(`data/slice/camel-2dcc-v1.zip` → `camel-2dcc/grains/`, 879 rows in `grains.csv`), not typed from
memory — see Verification. Give students **ranges**, not single values: the slice can be
rebuilt with re-measured/re-detected grains, which will move these numbers slightly. Always trust
a fresh run of the notebook over this document.

`grains.csv` is one row per detected blob from a simple height-threshold rule (see
`src/camel_data/grains.py` docstring), not a hand count or a validated triangle detector. A `kind`
of `single` means "one blob that passed simple shape checks" — not-too-tall, not-too-stretched,
not-too-concave — never a confirmed triangle. `whole_single()` further keeps only `single` blobs
that don't touch the scan edge or a bad ("glitch") scan row — that's the set used for every
population/sample calculation. Treat every count in this notebook as "what the rule kept," and say
so to students.

**Scope reminder for this lesson:** the 501-triangle set built in Part 4 is every triangle *we
measured*, across three small 2 µm × 2 µm fields on wafer 17458 — it is **not** a census of the
whole wafer, and nothing in this notebook proves a wafer-wide effect. Keep that distinction in your
own framing, not just the student-facing text.

## Learning targets (student language)

- I can judge an automated measurement rule against the actual picture, and explain a specific way
  it can be fooled (HSG.MG.A.3).
- I can measure a length from a scaled image and use it to predict an area with
  A = (√3/4)s², checking that prediction against a differently-measured value (HSG.GMD.A;
  HSN.Q.A.1–3).
- I can read a height profile (line scan) and describe widths and heights in real units, including
  a case where a measured value doesn't match a textbook value (HSN.Q.A.1–3).
- I can distinguish a population from a sample, build a random sample, and explain why a sample
  mean varies from sample to sample (HSS.IC.A.1–2).
- I can describe, from a simulation, how the spread of a sampling distribution shrinks as sample
  size grows (HSS.IC.B.4).
- I can distinguish bias (a systematic error from *how* a sample was chosen) from random error
  (chance variation that shrinks with more data) (HSS.IC.B.4).

## Timing (about 45 min core; +10–15 optional)

| Minutes | Section |
|---|---|
| 0–4 | Setup cell, dependency check, load data |
| 4–10 | Part 1 — spot the mistake (Task 1) |
| 10–17 | Part 2 — why triangles, measure a grain two ways (Task 2) |
| 17–24 | Part 3 — one line scan across a grain (Task 3) |
| 24–34 | Part 4 — population vs. sample, sampling distributions (Tasks 4, 5) |
| 34–41 | Part 5 — comparing the 3 fields, sampling-vs-bias discussion (Task 6) |
| 41–46 | Exit ticket |
| (+10–15 optional) | Task 3b (two more line scans, Explore) and Task 7 (second recipe + merged grains, Extend) |

Task 3b was moved out of the timed core — it's a second and third line-scan read that repeats the
Task 3 skill without adding a new concept. If a class is fast, run it; if not, skip it and the exit
ticket still stands on its own.

## Expected answers (ranges)

- **Task 1 (mistake):** `wse2_17458_center` currently has 251 detected blobs total, 191 whole
  single-candidate blobs (expect 240–260 / 180–200 on a rebuild). Grains 3 and 7 are the mistake: a
  glitch in scan row 1 (heights spuriously ~8+ nm there, versus a normal background under ~0.2 nm)
  cuts one real bright particle into a thin edge-touching sliver (grain 3, `streak`, area 320 nm²,
  `touches_edge=True`) and a rounder blob below it (grain 7, `dust`, area 2,197 nm², taller than
  typical because part of its top is missing). **Both are flagged `touches_glitch=True`** and are
  excluded by `whole_single()` before any population/sample work — the point isn't that the rule is
  broken, it's that a student can verify why a specific grain was thrown out.
- **Task 2 (geometry):** grain 217, area ≈ **1,400–1,450 nm²** (currently 1,419 nm², measured by
  counting pixels), measured height ≈ 1.6 nm, true `side_nm` ≈ **57 nm** (not shown to students as
  the target — it's derived from area, so comparing to it would be circular). The numbered-map
  panel lets students pick any candidate id shown there instead of guessing one off an unlabeled
  picture; picking an id that isn't a whole single-candidate now raises a friendly `ValueError`
  listing valid ids instead of crashing on `.iloc[0]`. A reasonable grid read of the side (50–64 nm)
  predicts an area within the accepted **±25%** window (ratio 0.75–1.25) around the measured
  1,419 nm²; the default `my_side_nm = 55` gives ratio 0.92, "Reasonable!" Remind students the grid
  read and the pixel count aren't independent checks — both come from the same thresholded image and
  the same x-y calibration, so a shared calibration error would show up in both; treat agreement as
  self-consistency, not outside confirmation.
- **Task 3 (grain profile):** grain 217, angle 90°, measured peak height currently **1.9–2.0 nm** on
  this run (expect **1.5–2.2 nm** on a rebuild); the raised region is roughly **40–55 nm** wide at
  half the peak height. This motivates the Scientist's note: measured peak height (~1.5–2.0 nm)
  reads noticeably above the ~0.65–0.7 nm textbook WSe2 monolayer step. The note now explicitly
  blames adsorbed water, leveling, and calibration/substrate-level choices — **not** tip shape,
  which mainly affects lateral size, not vertical height. Do not let students conclude a specific
  layer count from this measurement.
- **Task 3b (Explore, optional):** `wse2_24111_center` from (615, 882) nm to (695, 882) nm: flat
  substrate ≈0.07–0.16 nm for the first ~30 nm, rising to about **1.3–1.5 nm** by the end of the
  line. `snse_39166_top` from (3200, 1550) nm to (4900, 1550) nm: a clear staircase with **3–5**
  distinguishable flat treads between roughly −0.9 nm and +1.3 nm; accept any answer in that range —
  the point is counting distinguishable flat-ish segments, not an exact number.
- **Task 4/5 (population & sampling):** our population is N = **501** whole single-candidate
  triangles across the three `wse2_17458_*` fields (currently center 191, flat 206, edge 104 —
  expect each within about ±15 on a rebuild); this is *every triangle we measured in these three
  fields*, not a wafer census. Population mean μ ≈ **1,850–1,950 nm²** (currently 1,889 nm²),
  population SD ≈ **950–1,100 nm²** (currently 1,024 nm²). A single n=10 sample can reasonably land
  anywhere roughly **μ ± 700 nm²** (SE ≈ σ/√10 ≈ 324 nm²; differences of 1–2 SE are common and
  expected — don't treat any single draw as "wrong"). Note for discussion: `random_sample` draws an
  equal-chance sample of individual *triangles* from the 501 — a real area scan instead samples
  whichever triangles happen to fall inside a chosen patch, which is a different (spatially
  clustered) process; this simulation approximates "a smaller sample," not "a smaller scanned area."
  Sampling-distribution SD of the mean: currently **n=5 → ≈465 nm²**, **n=20 → ≈221 nm²**,
  **n=50 → ≈134 nm²** (expect each within about ±15%). These are close to but systematically below
  the naive σ/√n prediction (458, 229, 145 nm²) because the simulation samples *without replacement*
  from a finite population of 501: the exact prediction includes the finite-population correction
  σ/√n · √((N−n)/(N−1)), giving 456.1, 224.6, and 137.5 nm² for n=5, 20, 50 — noticeably closer to
  the simulated values, and about **5% smaller than the naive σ/√n figure at n=50** (correction
  factor √((501−50)/500) ≈ 0.95). Either teach the correction or tell students σ/√n is a
  large-population approximation that overestimates the spread as the sampled fraction grows.
- **Task 6 (bias):** "toward the edge" field mean currently ≈ **2,800–2,850 nm²**, about **+45% to
  +55%** above μ — expect this gap to persist in sign and rough size on a rebuild. **Frame this as a
  question, not a proven wafer fact:** we only scanned one field at each position, so this contrast
  could reflect a real wafer-position effect, or it could just be a property of this one edge field
  (spatial correlation, or how that patch happened to look) — to actually establish a wafer-position
  effect you'd need several independently placed fields near the edge, not more grains from the same
  field. "center" mean currently ≈ **1,450–1,500 nm²** (about 20–25% *below* μ); "toward the flat" is
  closest to μ (currently ≈1,800–1,820 nm², within ~5%). Push students toward "bias" as a
  *systematic* offset from how/where you sampled — not a guarantee that every possible sample from
  that spot misses by exactly the same amount, just that repeated sampling *from that same spot*
  keeps missing in the same direction, unlike random error which shrinks with more data.
- **Task 7 (extension):** `wse2_17458_center` (850 °C, no ripening) and `wse2_17464_center` (875 °C,
  then 10 min ripening) are two *different* recipes, not a seed/no-seed or before/after pair —
  temperature and the ripening step both differ, so nothing here isolates a single cause. Currently
  17458 shows an above-threshold pixel fraction of **≈10–11%** in its field vs. **≈4%** for 17464
  (this fraction includes every detected blob — merged, dust, streak, and single — not just clean
  triangles, and it describes only that one scanned field, not the wafer); 17464 has *far fewer*
  whole single-candidate triangles per µm² (currently ≈7–8/µm² vs. ≈45–50/µm²) despite a *larger*
  mean triangle area (currently ≈4,000–4,500 nm² vs. ≈1,450–1,500 nm²). The two scans also don't
  share a pixel size — 17458's pixels are about 3.9 nm (minimum detectable blob ≈183 nm²) while
  17464's are about 9.8 nm (minimum detectable blob ≈1,144 nm², about 6× larger) — so any density or
  coverage comparison between them is approximate, not apples-to-apples; the coarser scan
  structurally can't detect the smallest seeds the finer one can. Accept any answer that reasons from
  the printed numbers while naming this resolution caveat, rather than declaring a confident cause.
  Merged grains: currently **≈11–13%** of all detections in the three population fields, with mean
  area (≈3,400–3,800 nm²) roughly **1.8–2×** the clean-single mean (≈1,850–1,950 nm²) — counting
  merged blobs as single triangles would push the population mean *up*; accept any answer noting that
  excluding them could still bias the population *down* somewhat, since bigger/more numerous
  neighbors are more likely to touch and merge, so the truly biggest grains are undercounted.

## Common misconceptions

- "The 501 triangles are every triangle on the wafer." They're every triangle *we measured*, in
  three small 2 µm × 2 µm fields — a useful classroom population for practicing sampling ideas, but
  not a census of the wafer. Say this explicitly; it's the most important framing correction in this
  lesson.
- "The computer's grain rule is just wrong." It correctly measured what was in the pixels; a bad
  scan row physically disconnected one particle into two blobs. The lesson is verifying an
  automated measurement against the picture, not distrusting all automation.
- "A `single`-labeled blob is a confirmed clean triangle." It only passed simple shape checks
  (height, elongation, concavity) — the rule never checks that the shape is actually a triangle.
  Call it a candidate, and say so to students.
- "`side_nm` in the table proves the area formula." It doesn't — `side_nm` was calculated *from*
  `area_nm2` using this exact formula, so it can't independently verify itself. The notebook's
  check compares a grid-measured side against the pixel-counted area instead — and even that pair
  shares the same image and calibration, so don't call them "independent."
- "Higher measured AFM height means more atomic layers." Not without more evidence — height here
  reads well above the textbook monolayer step; adsorbed water, scan leveling, and calibration all
  can inflate AFM height on sapphire. (Tip shape mainly affects *lateral* size, not vertical height —
  don't blame it for this.) The notebook deliberately does not claim a layer count.
- "A random sample of 10 should give exactly μ." It won't, usually — sampling variability is the
  point of Task 4/5. Only the *distribution* of many sample means clusters tightly around μ, and
  only once n is reasonably large.
- "The edge field being bigger proves a real wafer-position effect." One field per position is one
  data point per position — it's consistent with a real effect but doesn't establish one. Treat
  Task 6 as an illustration of bias using this data, not proof about the wafer.
- "More grains always fixes a bad estimate." Only fixes *random* error. The edge-only "lazy
  scientist" in Task 6 keeps sampling the *same* biased field — scanning more grains there doesn't
  move the estimate toward μ, because the problem is which field, not how many grains from it.
- "Throwing out merged grains is obviously the fair, unbiased choice." It's the defensible choice
  for measuring individual-triangle geometry, but it isn't automatically unbiased — bigger/more
  crowded triangles are more likely to have merged, so excluding them could still skew the
  remaining "clean" population smaller than the truth. Accept students who raise this critically.
- "The bar of tiny grains at the far left of the population histogram is an error." Partly real,
  partly the rule: grains of about 200–400 nm² are only 12–26 pixels, so they mix genuinely small
  (late-forming) triangles with a few specks the rule kept. The smallest size the rule accepts is
  12 pixels (about 180 nm² on these scans). Good discussion point: where you set a cutoff changes
  the population you study.
- "17458 and 17464 are a seed-stage vs. grown-out pair." They're two different recipes (different
  temperature *and* a ripening step 17458 didn't get), scanned at two different pixel resolutions.
  Neither difference alone explains what's observed — that's the point of Task 7.

## Troubleshooting

- No ipywidgets/Plotly widgets are used anywhere in this notebook — every figure is a static
  Matplotlib plot, so there's no Colab custom-widget-manager dependency to debug.
- `ax.boxplot` in Part 5 uses `ax.set_xticks`/`ax.set_xticklabels` after `boxplot()`, not the
  `labels=`/`tick_labels=` boxplot keyword — that keyword was renamed then removed across recent
  Matplotlib versions (same fix already applied in notebook 02).
- Task 2 now validates `GRAIN` before using it: picking an id that isn't a whole single-candidate
  triangle in `wse2_17458_center` raises a `ValueError` that lists valid ids, instead of an opaque
  `IndexError` on `.iloc[0]`. Point students at the numbered left-hand panel in that cell's output —
  every id shown there is a valid choice.
- A short dependency check now runs right after setup and before `camel_data.grains` is imported:
  if scikit-image is missing from a Colab runtime, students get a one-line `%pip install
  scikit-image` instruction instead of a bare `ModuleNotFoundError` partway through the notebook.
- `random_sample` draws without replacement, so `n` can never exceed the population size (501 here,
  well above anything asked).

## Verification

```
.venv/bin/jupytext --to ipynb notebooks/src/06_counting_crystals.py -o notebooks/06_counting_crystals.ipynb
.venv/bin/python scripts/run_notebook.py notebooks/06_counting_crystals.ipynb
```

Last run: `OK   06_counting_crystals.ipynb -> notebooks/executed/06_counting_crystals.ipynb`
(879-row `grains.csv` build, 2026-09-10, after the code-review revision). Printed values from that
run: mistake grains 3 (`streak`, area 320 nm², row 0.000) and 7 (`dust`, area 2,197 nm², row 5.958),
both `touches_glitch=True`; scan `wse2_17458_center` has 251 detected blobs, 191 whole
single-candidate blobs; grain 217 area 1,419 nm², measured height 1.61 nm; Task 2 predicted area
1,310 nm² vs. measured 1,419 nm² (ratio 0.92, "Reasonable!" — inside the ±25% window); Task 3
grain-217 profile measured peak height 1.94 nm; population N=501, μ=1,889 nm², σ=1,024 nm²; sample
seed=3, n=10, x̄=2,243 nm² (+354 nm² from μ); sampling-distribution SD of the mean — n=5: 465 nm²
(finite-population-corrected prediction 456.1 nm², naive σ/√n 457.9 nm²), n=20: 221 nm² (corrected
224.6 nm², naive 228.9 nm²), n=50: 134 nm² (corrected 137.5 nm², naive 144.8 nm², about 5% higher
than corrected); field means — center 1,469 nm² (n=191), toward the flat 1,809 nm² (n=206), toward
the edge 2,818 nm² (n=104, +49% vs. μ); Task 7 — `wse2_17458_center` (850 °C, no ripening): 10.4%
above-threshold pixel fraction, 191 triangles, 47.8 per µm², mean 1,469 nm², pixel 3.91 nm (min
detectable blob ≈183 nm²); `wse2_17464_center` (875 °C, then 10 min ripening): 4.3% above-threshold
pixel fraction, 191 triangles, 7.6 per µm², mean 4,277 nm², pixel 9.77 nm (min detectable blob
≈1,144 nm²); merged grains 77 of 643 total population-field detections (12%), mean merged area
3,628 nm² vs. mean clean-single area 1,889 nm².
