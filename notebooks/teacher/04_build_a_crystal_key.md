# Teacher key — Build a Crystal: Reading a Real Recipe as a Graph

Student notebook: `notebooks/04_build_a_crystal.ipynb` (source: `notebooks/src/04_build_a_crystal.py`).
All numbers below were printed by `scripts/run_notebook.py notebooks/04_build_a_crystal.ipynb`
against the real data slice (`data/slice/camel-2dcc-v1.zip`) — not typed from memory. Re-run that
script any time the slice is rebuilt to refresh these.

## Learning targets (student language)
- I can turn a table of durations into a running total (cumulative time) and check my work.
- I can read a piecewise graph, and build a *hypothetical* linear model of one ramp segment —
  conditional on an assumed starting value — to make a conditional prediction.
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
| 2 | HSF.IF.B.4–6 | Identify the ramp interval and endpoints from table + graph; name the 25 °C starting assumption | Correct step name, times, temps named in free response |
| 3 | HSF.IF.B.6 (avg rate of change), HSF.BF, HSA.CED | Build a hypothetical linear model conditional on an assumed start; compute its slope; solve for t at 500 °C; compare against a 200 °C assumption | Slope and t≈8.3 min printed and self-checked; 200 °C comparison printed |
| 4 | HSN.Q (data integrity, not a numbered CCSS domain but core to HSF.IF graph reading) | Compare wrong vs. honest graph of missing data | Free response names the false "instant 0 °C" claim |
| 5 | HSN.Q.A.1–3 | Convert 1000 °C to K and °F | 1273.15 K and 1832 °F printed |
| 6 | HSN.Q.A.1–3 (units/scientific notation) | Compute pressure ratios | Ratios printed (see below); free response reasons about vacuum |
| 7 | HSF.IF.B.6 | Recompute slope for a second, curated sample | New slope printed and compared to 23451's |
| 8 | HSS.ID.B.6, HSS.ID.C.8 | Least-squares line + r on `growth_summary`; honest conclusion | r ≈ 0.09 printed; free response lists ≥1 confound |

## Timing (45-minute class — Tasks 6–8 are optional)
**Core (required, ~30 min) + exit ticket fits a 45-minute period on its own:**
- 0–5 min: Setup cell + Part 1 hook (surface_3d of the MoS2 film).
- 5–10 min: Part 2 table + Task 1 (cumulative time check).
- 10–20 min: Part 3, Tasks 2–3 (graph, hypothetical ramp slope, T(t), 500 °C estimate, the
  200 °C comparison).
- 20–26 min: Part 4, Task 4 (missing ≠ zero, wrong-vs-honest graphs).
- 26–30 min: Part 5, Task 5 (unit conversions).
- 30–40 min: buffer / early finishers start Part 6 (Explore) — do not need this time to reach the
  exit ticket.
- 40–45 min: Exit ticket.

**Explore (Tasks 6–7) and Extend (Task 8) are optional** — assign as homework, or let early
finishers continue past minute 30 instead of using the buffer above. Announce this split *before*
starting Task 1, not when time runs out.
- Task 6 (pressure ratios): ~6 min.
- Task 7 (dropdown, second recipe): ~5 min.
- Task 8 (Extend scatter/correlation): ~5–10 min, good homework candidate.

## Expected answers (as ranges, computed from the slice on 2026-09-10)
- **Task 1:** cumulative start times for sample 23451 = `[0, 17, 22, 27, 30, 40, 48]` min, exactly
  matching `start_min`. Check-yourself always prints ✅ for any correct cumulative-sum formula.
- **Task 2:** the ramp step is **"Ramp up T"**, from t = 0 to t = 17 min, ending at 1000 °C. Its
  *starting* temperature is not recorded; a good answer names 25 °C as an assumption, not a fact.
- **Task 3:** this is a **hypothetical model**, conditional on assuming the ramp started at 25 °C
  — not a measurement. Under that assumption: hypothetical slope ≈ **57.35 °C/min** (exactly
  975/17); estimated 500 °C crossing at **t ≈ 8.28 min**. The follow-up "what if it started at
  200 °C?" comparison (built into the notebook, not optional) prints hypothetical slope
  **47.06 °C/min** and crossing **t ≈ 6.37 min** — changing one assumed number changes both
  answers by a lot. A good answer states both results as conditional estimates and names the
  assumption they depend on.
- **Task 4:** free response. Look for: the wrong graph claims the furnace instantly dropped to
  0 °C at minute 40, which is physically impossible for a real cooldown; the honest graph shows a
  gap because the recipe log simply doesn't record a cooldown temperature.
- **Task 5:** 1000 °C = **1273.15 K** = **1832 °F**, exactly (linear formulas, no estimation).
- **Task 6:** MOCVD chamber 50 Torr (sample 23451's own recipe — about **97%** of the 334 MoS2
  MOCVD samples with a ramp step in the slice also use 50 Torr); Hybrid MBE deposition pressure ≈
  **4.41 × 10⁻¹⁰ Torr** (median of 15 deposition steps that recorded a pressure, out of 26 total —
  11 deposition steps have *no* recorded pressure, another honest "missing ≠ zero" moment worth
  pointing out if a student asks). Ratios (printed by the notebook): air is about **15× fuller**
  than the MOCVD chamber; MOCVD is about **1.13 × 10¹¹× fuller** than the MBE chamber; air is
  about **1.72 × 10¹²× fuller** than the MBE chamber.
- **Task 7:** the dropdown now offers 8 curated, contrasting MoS2 MOCVD samples, each verified to
  have exactly one ramp step with both a recorded duration and temperature (no `nan` or
  `IndexError` possible from this list). The notebook's own default comparison is sample 32465
  (**≈33.82 °C/min**, a slow 600 °C ramp) vs. 23451 (**≈57.35 °C/min**). Slopes across all 8
  curated samples range from about 33.8 to 61.1 °C/min. A student who picks a different one of the
  8 will get a different, real value in that range — that variation *is* the point.
- **Task 8:** n = **331** MoS2 samples with both growth time and roughness recorded; **r ≈ 0.09**
  (essentially no linear trend); least-squares line ≈ `roughness ≈ 0.057 × time + 0.508 nm`. One
  sample (32102, 18 min growth, 92.0 nm roughness) is a large outlier; removing it gives r ≈ 0.21
  (n = 330) — still a weak trend, so the "no clear pattern" conclusion doesn't hinge on that one
  point, but don't over-read the *increase* either; both are honest, weak, current-slice numbers.
  Good free responses name at least one of: differing temperature/pressure across samples,
  differing scan sizes (1–70 µm in this slice — a much wider spread than it may look at a glance),
  a few samples regrown more than once when `growth_summary` only describes the first recipe, or
  publication/selection bias in which samples got scanned.

## Common misconceptions
- Treating the furnace **setpoint** (`temperature_C`) as a direct measurement of the crystal
  itself — it's what the furnace was told to hold, not a probe reading on the wafer.
- Treating Task 3's slope and 500 °C crossing as *measured* facts about this recipe. They are
  outputs of a **hypothetical model** conditional on an assumed 25 °C starting temperature — the
  200 °C comparison exists specifically to make that assumption's leverage visible. Do not accept
  "the math is exact so it's not an estimate" — the arithmetic is exact, but what it estimates is
  conditional on an unverified assumption.
- Filling a blank cell with 0 "to make the code work." Reinforce: missing means *unknown*, not
  *zero*, and the notebook's side-by-side plot makes the wrong version's false claim visible.
- Subtracting pressures instead of dividing them (e.g., "50 Torr is basically the same as
  4 × 10⁻¹⁰ Torr because 50 is small") — the whole point of Task 6 is that ratios, not
  differences, are the right comparison across orders of magnitude.
- Treating r ≈ 0.09 as proof that growth time has *no effect at all* — a small r only means no
  clear *straight-line* trend in *this* data; it doesn't rule out an effect too small or too
  confounded to see.
- Assuming every MoS2 recipe ramps at the same rate as 23451's — Task 7's curated dropdown exists
  specifically to show real recipe-to-recipe variation (about 34 to 61 °C/min across the 8
  options).
- Assuming every bump on the AFM surface in Part 1 came from the recipe — the substrate, handling,
  environment, and the measurement/processing pipeline all leave marks too; this notebook follows
  one possible connection, not every cause.
- Treating MOCVD and Hybrid MBE definitions as universal rules rather than descriptions of *this*
  recipe: 1000 °C is sample 23451's MOCVD setpoint, not a temperature every MOCVD recipe uses; not
  every MOCVD film grows strictly layer-by-layer; Hybrid MBE can include a precursor gas alongside
  its atomic/molecular beams.

## Troubleshooting
- **Dropdown (Part 7) shows nothing / errors:** the "static fallback" cell right below it
  (`show_recipe(SAMPLE_ID)`) reproduces the same plot without the widget — use that if
  `enable_custom_widget_manager()` didn't take effect (usually a fresh-runtime or non-Colab
  issue). Confirmed in this build: the notebook runs clean headlessly (no widget frontend at
  all) via `scripts/run_notebook.py`, so the underlying logic doesn't depend on widget rendering.
- **`surface_3d(...).show()` blank:** re-run the setup cell — the custom widget manager call must
  run before any Plotly figure is built in a fresh Colab runtime.
- **A student types a sample id not on the curated list and Task 7 prints a missing-data
  message instead of a slope:** expected and by design — the notebook now detects a missing or
  multi-row ramp and prints a clear message rather than crashing or printing `nan`. Have the
  student pick one of the 8 dropdown options, or use it as a bonus discussion of Part 4's lesson
  recurring in the wild.
- **ipywidgets Dropdown doesn't support typing to search:** correct, it isn't a combobox — that's
  why the dropdown is now a short curated list of 8 instead of the full sample catalog.

## Complexity dials
- **Core (fits 45 min alone, with the exit ticket):** Tasks 1–5.
- **Explore (optional):** Tasks 6–7.
- **Extend (optional, good homework):** Task 8.

## Data story: sample 23451
MoS₂, grown by MOCVD, 2DCC. Recipe: Ramp up T (17 min, assumed 25→1000 °C) → two pre-growth
anneals (5 min each) → Growth (3 min) → post-growth anneal (10 min) → two cooldown steps (8 min
each, temperature not recorded). AFM gallery key `mos2_film` shows the resulting surface (RMS
roughness ≈ 0.30 nm over a 5 µm scan). Honest limitations: the recipe log records furnace
setpoints, not direct measurements of the wafer surface; cooldown temperatures were never logged
for this sample; and the ramp's starting temperature isn't recorded at all — Task 3's slope and
500 °C crossing are a hypothetical model's output, not lab measurements.
