# Teacher key — More Ways to See a Crystal: X-rays, Light, Electrons, and Electricity

Student notebook: `notebooks/07_more_ways_to_see.ipynb` (source: `notebooks/src/07_more_ways_to_see.py`).

All numbers below were **printed by running the notebook** against the current slice
(`data/slice/camel-2dcc-v1.zip` → `camel-2dcc/extras/`), not typed from memory — see
Verification. Give students **ranges**, not single values: a slice rebuild can move these numbers
slightly (a note on the data build: the next slice rebuild removes an unused
`T_onset_90pct_K` column from `transport_summary.csv` — nothing this notebook uses). Always trust
a fresh run of the notebook over this document.

**Format:** four independent stations (A = XRD, B = Raman, C = SEM, D = electrical transport),
each ~12–15 minutes and self-contained. **Pick 2–3 stations for a single 45-minute period** — say
so to students up front. The notebook has no ipywidgets/Colab-widget dependency anywhere; every
figure is a static Matplotlib plot, so there is no widget-manager troubleshooting for any station.

## Learning targets (student language)

- **Station A:** I can use a right-triangle trig ratio (sine) inside Bragg's law to convert a
  measured diffraction angle into an atomic spacing, and I can check that measurement against an
  independent second reading of the same crystal (HSG.SRT.C.8; HSA.CED.A.1, A.4).
- **Station B:** I can read two peak positions off a real spectrum, subtract them, and use a
  reference table to make a reasonable (not exact) estimate; I can read a dot plot of 29
  measurements and describe its center and spread (HSN.Q.A.1–3; HSS.ID.A.1–3).
- **Station C:** I can use a scale bar and a proportion to convert pixels to real distance, measure
  a shape from a picture and check a predicted area against an independently measured one, and
  compute a density from a count and an area (HSG.MG.A.1, A.3; HSN.Q.A.1–3).
- **Station D:** I can describe a real measured graph as a piecewise function, estimate an average
  rate of change (slope) from two data points, and apply V = IR (HSF.IF.B.4, B.6, C.7b;
  HSA.CED.A.4).

## Timing (pick 2–3 of the four ~12–15 min stations for 45 minutes)

| Minutes | Section |
|---|---|
| 0–5 | Setup cell |
| 12–15 each | Station A, B, C, D (choose 2–3) |
| last 3–5 | Exit ticket (only the parts for stations actually done) |

Each station's own internal pacing (~13 min): ~3 min context + first plot, ~7 min on the Core
task(s), ~3 min on the note/discussion question.

## Expected answers (ranges) — from the printed run below

- **Station A, Task A1/A2:** default reads 2θ₁ = 41.7° and 2θ₂ = 90.8° give d₁ ≈ **0.2164 nm** and
  d₂ ≈ **0.2164 nm**; the notebook's own automatic peak search finds the true peaks at 2θ = **41.70°**
  and **90.75°** (accept any student reading within about ±1° of each — the check-yourself cell
  uses that tolerance). Both d's land within **0.001 nm** of the known sapphire c/6 spacing,
  **0.2165 nm**. Task A3 (Extend) is open-ended — accept any answer noting that the film is only a
  few nm thick versus a millimeters-thick wafer, so far fewer identical atomic planes reinforce the
  reflected X-rays, giving a shorter, broader peak (this is the core idea behind peak-width/
  crystallite-size relationships like the Scherrer equation, which this notebook does not compute).
- **Station B, Task B1:** default reads E2g ≈ 383, A1g ≈ 403 give separation ≈ **20 cm⁻¹**; the
  lab's own peak-fit for sample 32093 is E2g = **383.2**, A1g = **403.4**, separation =
  **20.2 cm⁻¹** (check-yourself tolerance: ±3 cm⁻¹). Task B2: 20.2 cm⁻¹ sits **between** the 1-layer
  (≈18–19) and 2-layer (≈21–22) reference rows — a reasonable answer is "probably 1–2 layers, not a
  clean match," not a confident single number. Task B3: across all **29** MoS₂ films, median
  separation ≈ **20.8 cm⁻¹**, range **16.9–23.7 cm⁻¹** — most points cluster between the 1-layer and
  2-layer reference lines, with a handful above 22.5 cm⁻¹ approaching the 3-layer/bulk end; accept
  "mostly 1–2 layers, a few thicker" as well supported by the dot plot.
- **Station C, Task C1:** 139 px = 3 µm gives **21.583 nm/px**, matching the microscope's own
  calibration exactly; full field of view ≈ **22.1 µm × 14.9 µm**. Task C2: the computer's
  pixel-counted area for "blob 8" is **27,018 nm²**; a default grid read of 200 nm predicts
  **17,321 nm²** (ratio 0.64, "✅ Reasonable" — the check-yourself cell accepts ratio 0.5–2.0, same
  rule as notebook 06). A careful read in the 150–280 nm range stays inside that band. Task C3: the
  marked 100×100 px region (≈**4.66 µm²**) has **16** blobs by the threshold rule (dark_below=100,
  min_px=8) → density ≈ **3.43 triangles/µm²**; accept any honest student count in the 12–20 range
  as reasonable given how crowded and merged some blobs are — the point is comparing counts, not
  hitting 16 exactly.
- **Station D, Task D2:** default two points (T≈250 K, T≈100 K) give T₁ = **249.6 K**, R₁ =
  **1259.7 Ω**; T₂ = **99.6 K**, R₂ = **1222.9 Ω**; slope ≈ **0.245 Ω/K** (resistance *rises* as the
  film warms — falls as it cools, as stated). Task D3: sample 20198's measured "reaches about zero"
  temperature is **4.99 K** (`T_zero_1pct_K`); the visual midpoint of the drop (`T_mid_50pct_K`) is
  **7.00 K**. Task D4 table: 20198 (7.00 / 4.99 K), 20199 (13.66 / **blank**), 20200
  (20.00 / 14.00 K), 20201 (29.28 / 22.87 K) — 20199's blank is missing data (never reached the
  1%-of-normal threshold down to the lowest temperature this run measured, about 4 K), not a
  literal 0 K. Task D5: at 300 K, R = **1236.5 Ω** → V = **1.2365 mV** at 1 µA; at 2.0 K,
  R = **−0.0040 Ω** → V = **−4.00 nV**, i.e. indistinguishable from zero given the instrument's own
  noise floor (a small negative resistance reading here is noise, not "negative resistance").

## Common misconceptions

- "Two different diffraction orders (n=1, n=2) are two different measurements that happen to
  agree." They're the same atomic planes reflecting twice — agreement is expected from the same
  physics, but it's still a genuinely independent *reading* of the raw scan (a different peak,
  different math), which is why it's reassuring rather than circular.
- "The E2g–A1g separation gives an exact layer count." It's a rough estimate from a reference
  table built on other samples — real separations also shift with strain, doping, substrate, and
  the laser used, and a noisy spectrum (like sample 32578) makes the reading less certain still.
- "SEM brightness means height, like AFM." Not here — in this image the MoS₂ triangles are *dark*
  and the bare sapphire is *light*; that's an imaging-mode contrast effect, not a height map.
- "The threshold rule's triangle count is the true count." It's a simple brightness-threshold rule
  — touching/merged triangles get counted as one blob, so densely packed regions are likely
  *undercounted*, not exactly counted. That's exactly why students eyeball their own count first.
- "A blank cell in the T_zero table means the resistance is 0 Ω at that temperature." It means the
  measurement never reached the 1%-of-normal threshold *within the temperatures actually
  measured* — missing is not zero (same idea as notebook 04's recipe gaps).
- "This shows superconductors could cool data centers today." No — reaching zero resistance here
  needs cooling to a few kelvin, which itself costs energy and complex equipment. This is a
  research question (how warm can a superconductor's Tc be pushed), not a working technology.

## Troubleshooting

- No ipywidgets/Plotly widgets anywhere in this notebook — every figure is a static Matplotlib
  plot. If a student's environment can't render one, `plt.show()` still logs a text repr; there is
  no interactive fallback to configure because nothing here is interactive.
- Station A's check-yourself cells filter the raw XRD scan to a fixed angle window (35–48° and
  85–95°) and take the angle of maximum intensity in that window — if a student changes `xrd`
  itself (they shouldn't need to), those windows may no longer contain the intended peak.
- Station C's `find_islands` threshold (`dark_below=100`) and `ROW0/ROW1/COL0/COL1` region are
  fixed in the helper cell — students only change `my_side_nm` and `my_count`, not the detection
  itself. If asked "why 16 and not the obviously-larger real count," point to the Scientist's note:
  touching triangles merge into one blob under this simple rule.
- Station D's `nearest()` helper finds the closest **measured** temperature to whatever a student
  types, so any reasonable `target_T` works — it can't raise an error or return an empty result for
  values inside the sampled range (roughly 2–300 K depending on sample).

## Verification

```
.venv/bin/jupytext --to ipynb notebooks/src/07_more_ways_to_see.py -o notebooks/07_more_ways_to_see.ipynb
.venv/bin/python scripts/run_notebook.py notebooks/07_more_ways_to_see.ipynb
```

Last run: `OK   07_more_ways_to_see.ipynb -> notebooks/executed/07_more_ways_to_see.ipynb`
(2026-09-10, against `data/slice/camel-2dcc-v1.zip`). Printed values from that run:
- Station A: `2θ = 41.7° -> θ = 20.850° -> d ≈ 0.2164 nm (n = 1)`; automatic peak search 2θ = 41.70°;
  `2θ = 90.8° -> θ = 45.400° -> d ≈ 0.2164 nm (n = 2)`; automatic peak search 2θ = 90.75°; sapphire
  c/6 = 0.2165 nm.
- Station B: default separation 20 cm⁻¹; lab fit E2g = 383.2, A1g = 403.4, separation = 20.2 cm⁻¹
  (sample 32093); median separation (n=29) = 20.8 cm⁻¹, range 16.9–23.7 cm⁻¹.
- Station C: 139 px = 3 µm -> 21.583 nm/px (matches metadata exactly); field of view 22.1 µm ×
  14.9 µm; blob 8 computer-measured area 27,018 nm²; default predicted area 17,321 nm² (ratio 0.64,
  "Reasonable"); marked-region count 16, area 4.66 µm², density 3.43 triangles/µm².
- Station D: slope points T=249.6 K/R=1259.7 Ω and T=99.6 K/R=1222.9 Ω -> slope ≈ 0.245 Ω/K;
  T_zero (20198) = 4.99 K; four-film table — 20198: T_mid 7.00 K, T_zero 4.99 K; 20199: T_mid
  13.66 K, T_zero blank (NaN); 20200: T_mid 20.00 K, T_zero 14.00 K; 20201: T_mid 29.28 K, T_zero
  22.87 K; Ohm's law at 1 µA — 300 K: R=1236.5 Ω -> V=1.2365 mV; 2.0 K: R=−0.0040 Ω -> V=−4.00 nV.
