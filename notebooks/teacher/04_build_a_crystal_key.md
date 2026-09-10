# Teacher key — Build a Crystal: Reading a Real Recipe as a Graph

Student notebook: `notebooks/04_build_a_crystal.ipynb` (source: `notebooks/src/04_build_a_crystal.py`).
All numbers below were printed by `scripts/run_notebook.py notebooks/04_build_a_crystal.ipynb`
against the real data slice (`data/slice/camel-2dcc-v1.zip`) — not typed from memory. Re-run that
script any time the slice is rebuilt to refresh these.

## Learning targets (student language)
- I can turn a table of durations into a running total (cumulative time) and check my work.
- I can read a piecewise graph, find the slope of one ramp segment, and use it to predict a value.
- I can explain why a blank data cell is not the same as zero, and show what treating it as zero
  would wrongly claim.
- I can convert a temperature between °C, K, and °F, and compare numbers across many orders of
  magnitude using ratios instead of subtraction.
- I can look at a weak correlation honestly and explain why it doesn't prove there's no
  relationship — or that there is one.

## Standards
| Task | CCSS code | Student action | Evidence of learning |
|---|---|---|---|
| 1 | HSF.IF.B.4–6 (cumulative/rate reasoning), HSA.CED | Build running total of `duration_min`; check against `start_min` | Printed lists match; check-yourself prints ✅ |
| 2 | HSF.IF.B.4–6 | Identify the ramp interval and endpoints from table + graph | Correct step name, times, temps named in free response |
| 3 | HSF.IF.B.6 (avg rate of change), HSF.BF, HSA.CED | Compute ramp slope; write T(t); solve for t at 500 °C | Slope and t≈8.3 min printed and self-checked |
| 4 | HSN.Q (data integrity, not a numbered CCSS domain but core to HSF.IF graph reading) | Compare wrong vs. honest graph of missing data | Free response names the false "instant 0 °C" claim |
| 5 | HSN.Q.A.1–3 | Convert 1000 °C to K and °F | 1273.15 K and 1832 °F printed |
| 6 | HSN.Q.A.1–3 (units/scientific notation) | Compute pressure ratios | Ratios printed (see below); free response reasons about vacuum |
| 7 | HSF.IF.B.6 | Recompute slope for a second sample | New slope printed and compared to 23451's |
| 8 | HSS.ID.B.6, HSS.ID.C.8 | Least-squares line + r on `growth_summary`; honest conclusion | r ≈ 0.02 printed; free response lists ≥1 confound |

## Timing (45–50 min class)
- 0–5 min: Setup cell + Part 1 hook (surface_3d of the MoS2 film).
- 5–10 min: Part 2 table + Task 1 (cumulative time check).
- 10–22 min: Part 3, Tasks 2–3 (graph, ramp slope, T(t), 500 °C prediction).
- 22–28 min: Part 4, Task 4 (missing ≠ zero, wrong-vs-honest graphs).
- 28–32 min: Part 5, Task 5 (unit conversions).
- 32–38 min: Part 6, Task 6 (pressure ratios).
- 38–43 min: Part 7, Task 7 (slider, second recipe) — Explore; can be cut for time.
- 43–48 min: Part 8, Task 8 (Extend scatter) — assign as homework/extension if time is short.
- Last 5 min: Exit ticket.

## Expected answers (as ranges, computed from the slice on 2026-09-10)
- **Task 1:** cumulative start times for sample 23451 = `[0, 17, 22, 27, 30, 40, 48]` min, exactly
  matching `start_min`. Check-yourself always prints ✅ for any correct cumulative-sum formula.
- **Task 2:** the ramp step is **"Ramp up T"**, from t = 0 to t = 17 min, 25 °C (assumed) to
  1000 °C.
- **Task 3:** slope ≈ **57.3–57.4 °C/min** (exactly 1000−25 over 17 = 57.35); predicted 500 °C
  crossing at **t ≈ 8.2–8.4 min** (exactly 8.28 min). Accept anything in that narrow band — it's
  arithmetic, not an estimate.
- **Task 4:** free response. Look for: the wrong graph claims the furnace instantly dropped to
  0 °C at minute 40, which is physically impossible for a real cooldown; the honest graph shows a
  gap because the recipe log simply doesn't record a cooldown temperature.
- **Task 5:** 1000 °C = **1273.15 K** = **1832 °F**, exactly (linear formulas, no estimation).
- **Task 6:** MOCVD chamber 50 Torr (sample 23451's own recipe — 94% of MoS2 MOCVD recipes in the
  slice also use 50 Torr); Hybrid MBE deposition pressure ≈ **4.4 × 10⁻¹⁰ Torr** (median of 15
  deposition steps that recorded a pressure, out of 26 total — 11 deposition steps have *no*
  recorded pressure, another honest "missing ≠ zero" moment worth pointing out if a student
  asks). Ratios: air is about **15× fuller** than the MOCVD chamber; MOCVD is about
  **1.1 × 10¹¹× fuller** than the MBE chamber; air is about **1.7 × 10¹²× fuller** than the MBE
  chamber. Accept order-of-magnitude agreement (10¹⁰–10¹²) — the exact multiplier depends on
  which MBE deposition steps a student's own filter includes.
- **Task 7:** any two MoS2 MOCVD samples' ramp slopes are valid; the notebook's own default
  comparison is sample 24166 (≈139 °C/min over a much shorter, two-part ramp) vs. 23451
  (≈57 °C/min). Slopes across the 203 MoS2 samples with a step named exactly "Ramp up T" cluster
  tightly: median ≈54.4 °C/min, middle 90% from ≈51 to ≈57 °C/min, with one low outlier near
  34 °C/min for an unusually long ramp. A student who lands on one of those will find a similar
  slope; a student who lands on a differently-named, multi-stage ramp (like 24166's two-part
  "bub closed"/"bub open" ramp) will find a very different one (≈139 °C/min here) — both are
  correct, real data.
- **Task 8:** n = 331 MoS2 samples with both growth time and roughness recorded; **r ≈ 0.02**
  (essentially no linear trend); least-squares line ≈ `roughness ≈ 0.017 × time + 0.75 nm`. A
  single sample (32102) at 129 nm roughness is a large outlier; removing it still leaves r ≈ 0.07
  — the "no clear pattern" conclusion doesn't depend on that one point. Good free responses name
  at least one of: differing temperature/pressure across samples, differing scan sizes (1–5 µm in
  this slice), or publication/selection bias in which samples got scanned.

## Common misconceptions
- Treating the furnace **setpoint** (`temperature_C`) as a direct measurement of the crystal
  itself — it's what the furnace was told to hold, not a probe reading on the wafer.
- Filling a blank cell with 0 "to make the code work." Reinforce: missing means *unknown*, not
  *zero*, and the notebook's side-by-side plot makes the wrong version's false claim visible.
- Subtracting pressures instead of dividing them (e.g., "50 Torr is basically the same as
  4 × 10⁻¹⁰ Torr because 50 is small") — the whole point of Task 6 is that ratios, not
  differences, are the right comparison across orders of magnitude.
- Treating r ≈ 0.02 as proof that growth time has *no effect at all* — a small r only means no
  clear *straight-line* trend in *this* data; it doesn't rule out an effect too small or too
  confounded to see.
- Assuming every MoS2 recipe ramps at the same rate as 23451's — Task 7 exists specifically to
  show real recipe-to-recipe variation (10–17 minute single ramps vs. two-stage short ramps).

## Troubleshooting
- **Slider (Part 7) shows nothing / errors:** the "static fallback" cell right below it
  (`show_recipe(SAMPLE_ID)`) reproduces the same plot without the widget — use that if
  `enable_custom_widget_manager()` didn't take effect (usually a fresh-runtime or non-Colab
  issue). Confirmed in this build: the notebook runs clean headlessly (no widget frontend at
  all) via `scripts/run_notebook.py`, so the underlying logic doesn't depend on widget rendering.
- **`surface_3d(...).show()` blank:** re-run the setup cell — the custom widget manager call must
  run before any Plotly figure is built in a fresh Colab runtime.
- **Task 6 ratio numbers look different from this key:** expected — the MBE median depends on
  which deposition steps happened to record a pressure; order of magnitude (10¹⁰–10¹²) should
  still match.
- **A chosen sample in Task 7 prints `nan` for slope:** a few recipes have a ramp step *named*
  "Ramp..." whose temperature itself wasn't recorded (e.g., "Ramp to 1050C" in a handful of
  samples) — another real missing-data case. Have the student pick a different sample, or use it
  as a bonus discussion of Part 4's lesson recurring in the wild.

## Complexity dials
- **Core (fits 45 min alone):** Tasks 1–5.
- **Explore:** Tasks 6–7.
- **Extend:** Task 8 (can be homework).

## Data story: sample 23451
MoS₂, grown by MOCVD, 2DCC. Recipe: Ramp up T (17 min, 25→1000 °C) → two pre-growth anneals
(5 min each) → Growth (3 min) → post-growth anneal (10 min) → two cooldown steps (8 min each,
temperature not recorded). AFM gallery key `mos2_film` shows the resulting surface
(RMS roughness ≈ 0.30 nm over a 5 µm scan). One honest limitation: the recipe log records
furnace setpoints, not direct measurements of the wafer surface, and cooldown temperatures were
never logged for this sample.
