# Teacher key — Nano Landscapes: Fly Over Crystal Surfaces Atom-Step by Atom-Step

Student notebook: `notebooks/01_nano_landscapes.ipynb` (source: `notebooks/src/01_nano_landscapes.py`).

All numbers below were **computed by running the notebook** against the real slice
(`data/slice/camel-2dcc-v1.zip`), not typed from memory. Give ranges to students, not single
values — running the notebook always prints the current numbers, and a rebuilt slice may shift
them slightly.

## Learning targets

- Read a 3D height map and explain why its vertical axis is exaggerated (HSF.IF.B.4–6).
- Read a line-profile (cross-section) plot and estimate a step height from noisy real data
  (HSG.MG.A.1–3, HSN.Q.A.1–3).
- Convert between micrometres and nanometres and use the conversion in a ratio problem
  (HSN.Q.A.1–3).
- Compare mean and median on a real height distribution and explain what pulls them apart —
  and why that gap is about skew, not outlier count (HSS.ID.A.1–3).
- Distinguish a real surface feature from an instrument artifact using evidence, not a guess
  (HSS.ID.A.1–3).

## Timing (45–50 min)

| Minutes | Section |
|---|---|
| 0–5 | Setup cell, AFM hook |
| 5–15 | Fly over a surface (`explore_3d`), Task 1 — vertical exaggeration |
| 15–25 | Line profile (`explore_cross_section`), Task 2 — step-height estimate |
| 25–32 | Unit conversion, Task 3 — hair widths |
| 32–42 | Histogram, Task 4/4b — mean vs. median, and a real outlier count |
| 42–48 | Spot the glitch, Task 5 |
| 48–50 | Exit ticket |

## Expected answers (ranges)

- **Task 1 (vertical exaggeration):** `atomic_staircase` full range (every pixel, peak to valley)
  is about **4.3 nm** across a **1,000 nm**-wide scan (ratio ≈ **1 part in 233**). The typical
  range (middle 98% of pixels, ignoring rare spikes) is only about **0.8 nm** (≈ **1 part in
  1,256**) — worth pointing out that a few tall pixels set the full-range number, which is exactly
  why both numbers are printed separately. A stretch of roughly **20×–150×** makes the terraces
  clearly visible without spiky distortion; the notebook's default demo uses 50×. At a stretch of
  1, the surface looks essentially flat — that's the point of the scientist's note. Accept any
  answer that ties the chosen stretch back to either printed ratio.
- **Task 2 (step height):** the checker uses **curator-chosen rows and intervals**, not an
  automatic detector — rows **30–34** of `atomic_staircase`, comparing the terrace median at
  **x = 460–538 nm** against the terrace median at **x = 553–630 nm** (these five rows all cross
  the same clean, sharp step edge, with a flat plateau on each side clear of the jump itself).
  Live run: row 30 → 0.47 nm, row 31 → 0.49 nm, row 32 → 0.46 nm, row 33 → 0.37 nm, row 34 →
  0.38 nm; **mean ≈ 0.43 nm, row-to-row range 0.37–0.49 nm**. The textbook SrTiO3 unit-cell step
  is **0.39 nm**, right inside that range. Accept any student estimate in **0.2–0.6 nm** as
  reasonable; **0.6–1.0 nm** likely means they read across two step edges bunched together
  (mention this really happens on real crystals); under 0.05 nm or over 1.5 nm likely means a
  misread axis.
- **Task 3 (unit conversion / hair widths):** deterministic arithmetic, not an estimate — the
  check cell verifies the µm→nm conversion (`scan_um * 1000`) and the ratio formula
  (`hair_nm / scan_nm`) **independently**, so a broken conversion and a broken formula get
  different feedback. For the default `tin_selenide_grains` (5 µm = 5,000 nm), the answer is
  **16.0** scans per hair width; for `atomic_staircase` (1 µm), it's **80.0**; for a 2 µm scan
  (e.g. `superconductor_blocks`, `ws2_islands`, `wse2_triangles`, `memory_material`,
  `smoothest_surface`, `terraced_triangles`), it's **40.0**.
- **Task 4/4b (mean vs. median):** `gallium_selenide_bumps` (GaSe): **mean ≈ 1.41 nm, median =
  0.00 nm** — a gap of about **1.4 nm**. `ws2_islands` (WS2): **mean ≈ −0.11 nm, median =
  0.00 nm** — a much smaller gap (~0.1 nm). GaSe's bigger gap means its height distribution is
  more **skewed** (a long tail of tall mounds pulling the mean away from the median) — it does
  **not** mean GaSe has more outliers. The printed 1.5×IQR outlier count proves the opposite:
  GaSe has **0 outlier pixels (0.0%)** because its heights are broadly spread (IQR ≈ 28.6 nm, so
  the fence is wide), while WS2 — the *smaller*-gap scan — has **31,615 outlier pixels (12.1%)**
  because it's mostly flat sapphire (tiny IQR ≈ 0.45 nm) with scattered tall islands that clear a
  narrow fence easily. Correct answer to 4b: the mean–median gap tells you about **skew/shape**,
  not outlier count — GaSe is the more skewed distribution, WS2 is the one with more (rule-based)
  outlier pixels, and those are two different surfaces.
- **Task 5 (spot the glitch):** the reveal cell finds the glitch programmatically: in
  `wse2_triangles`, **row 1** (about **3.9 nm** down from the scan edge) has a height standard
  deviation of **≈136.8 nm**, versus **≈0.6 nm** for a typical row — about **245× noisier**. The
  scan's overall height range is dominated by this one row (global min/max **−455 nm / +221 nm**,
  far beyond any plausible WSe2 triangle height of a few nm). The full-resolution static heatmap
  and the `surface_3d(..., max_pixels=512)` call both now render all 512 rows, so row 1 is visible
  even without a working widget; the reveal cell also plots the glitch row's own height profile.
  Accept any answer that (a) identifies a single line/row that looks unlike the surrounding
  triangles, and (b) gives a mechanism tied to how an AFM works — e.g., the feedback loop
  overshot, a vibration or electrical spike hit mid-line, or the probe briefly lost a steady
  signal.

## Common misconceptions

- "The 3D plot shows the crystal's true shape." It's vertically exaggerated by whatever factor is
  printed in the plot title — Task 1 and the scientist's note exist specifically to catch this.
- "A median of 0.00 nm means the surface is perfectly flat." It means the per-line flatten plus
  global-median correction forced the whole processed map's *median* to 0 nm — real bumps and dips
  are still there; that's exactly why the notebook has students compare mean and median rather
  than reading either alone. The processing string is now printed directly from `gallery.json`,
  not something students have to go hunting for.
- "My step-height reading was off from 0.39 nm, so I did something wrong." Real, noisy AFM data
  legitimately gives a range of readings; the check-yourself cell is calibrated to curated
  neighboring-row measurements of the actual scan, not to a single "right answer."
- "A bigger gap between mean and median means more outliers." It means more **skew**. Task 4b's
  outlier-count cell is designed to break this misconception with real numbers: the scan with the
  smaller mean–median gap (WS2) has far more 1.5×IQR outlier pixels than the scan with the bigger
  gap (GaSe).
- "Anything unusual-looking in a scan must be a real surface feature." The whole point of Task 5 is
  that a single scan-line glitch (an instrument artifact) can look dramatic while being physically
  implausible (heights far outside anything the material could produce).
- "An AFM drags a single-atom needle and reads every atom by touch." AFMs raster-scan a probe
  whose tip is a few to tens of nanometres across, using a feedback loop; contact, tapping, and
  non-contact modes all exist. Atom-scale height steps are still measurable under the right
  conditions — that's different from imaging individual atoms one by one.

## Troubleshooting

- `explore_3d` and `explore_cross_section` need `output.enable_custom_widget_manager()` from the
  setup cell to render in Colab; outside Colab (or headless execution) they still run without
  error, they just don't display an interactive widget. Every core task now has a static fallback
  immediately below its widget (a full-resolution `plt.imshow`/cross-section for Task 2 and
  Task 5) so a blocked widget never blocks the task.
- If a student changes `scan_key` in the unit-conversion cell to a name not in the gallery listing
  printed earlier, they'll get a `KeyError` — have them re-check the printed key spelling (all
  lowercase with underscores).
- The Task 2 and Task 3 check-yourself cells recompute their reference values from the real scan
  every run, so they stay correct even if the slice is rebuilt; don't hardcode the printed numbers
  into a rubric that outlives a rebuild. If the slice is rebuilt with different underlying pixel
  data, re-inspect `atomic_staircase` before assuming rows 30–34 / x = 460–630 nm still land on a
  clean step edge.

## Verification

```
.venv/bin/jupytext --to ipynb notebooks/src/01_nano_landscapes.py -o notebooks/01_nano_landscapes.ipynb
.venv/bin/python scripts/run_notebook.py notebooks/01_nano_landscapes.ipynb
```
Last run: `OK   01_nano_landscapes.ipynb -> notebooks/executed/01_nano_landscapes.ipynb`
(against `data/slice/camel-2dcc-v1.zip`, 12-sample gallery build). All numbers in this key are
copied from that run's printed cell outputs.
