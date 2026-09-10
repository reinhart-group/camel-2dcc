# Teacher key — Nano Landscapes: Fly Over a Crystal One Atom Thick

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
- Compare mean and median on a real height distribution and explain what pulls them apart
  (HSS.ID.A.1–3).
- Distinguish a real surface feature from an instrument artifact using evidence, not a guess
  (HSS.ID.A.1–3).

## Timing (45–50 min)

| Minutes | Section |
|---|---|
| 0–5 | Setup cell, AFM hook |
| 5–15 | Fly over a surface (`explore_3d`), Task 1 — vertical exaggeration |
| 15–25 | Line profile (`explore_cross_section`), Task 2 — step-height estimate |
| 25–32 | Unit conversion, Task 3 — hair widths |
| 32–42 | Histogram, Task 4/4b — mean vs. median |
| 42–48 | Spot the glitch, Task 5 |
| 48–50 | Exit ticket |

## Expected answers (ranges)

- **Task 1 (vertical exaggeration):** the real relief of `atomic_staircase` is about **4.3 nm**
  across a **1,000 nm**-wide scan (ratio ≈ **1 part in 233** — computed live in the notebook).
  A stretch of roughly **20×–150×** makes the terraces clearly visible without spiky distortion;
  the notebook's default demo uses 50×. At a stretch of 1, the surface looks essentially flat —
  that's the point of the scientist's note. Accept any answer that ties the chosen stretch back to
  this real relief-to-width ratio.
- **Task 2 (step height):** using a simple peak/trough detector run on every other row of the real
  `atomic_staircase` scan, single step edges cluster **typical (25th–75th pct) ≈ 0.2–0.4 nm**,
  **wider plausible range (10th–90th pct) ≈ 0.15–0.5 nm**, computed from roughly 700–1,500 step
  edges (exact counts print live). The textbook SrTiO3 unit-cell step is **0.39 nm**, which sits at
  the upper end of the typical range — a good real-data illustration that single-line student
  readings will often run a bit low, and that's expected, not wrong. Accept any student estimate in
  **0.15–0.6 nm** as reasonable; anything under 0.05 nm or over 1 nm means they likely read a
  multi-step jump or misread the axis.
- **Task 3 (unit conversion / hair widths):** deterministic arithmetic, not an estimate — the
  check cell verifies the exact formula `hair_nm / scan_nm`. For the default `tin_selenide_grains`
  (5 µm = 5,000 nm), the answer is **16.0** scans per hair width; for `atomic_staircase` (1 µm),
  it's **80.0**; for a 2 µm scan (e.g. `superconductor_blocks`, `ws2_islands`, `wse2_triangles`,
  `memory_material`, `smoothest_surface`, `terraced_triangles`), it's **40.0**.
- **Task 4/4b (mean vs. median):** `gallium_selenide_bumps` (GaSe): **mean ≈ 1.41 nm, median =
  0.00 nm** — a gap of about **1.4 nm**, caused by a small number of very tall rounded mounds
  (max height ≈ 56 nm, min ≈ −44 nm) pulling the mean up while the median (forced to 0 by the
  per-line flattening) ignores them. `ws2_islands` (WS2): **mean ≈ −0.11 nm, median = 0.00 nm** —
  a much smaller gap (~0.1 nm); this scan is mostly flat sapphire background with a few tall WS2
  islands (max ≈ 19 nm) rather than the more uniformly bumpy GaSe surface, so its mean stays close
  to its median. Correct answer to 4b: **gallium selenide bumps has the bigger mean–median gap**,
  meaning it has the more extreme/more numerous height outliers of the two.
- **Task 5 (spot the glitch):** the reveal cell finds the glitch programmatically: in
  `wse2_triangles`, **row 1** (the 2nd row from the top) has a height standard deviation of
  **≈130–140 nm**, versus **≈1–3 nm** for a typical row — roughly **50× noisier**. The scan's
  overall height range is dominated by this one row (global min/max run to roughly **−455 nm /
  +221 nm**, far beyond any plausible WSe2 triangle height of a few nm). Accept any answer that (a)
  identifies a single line/row that looks unlike the surrounding triangles, and (b) gives a
  mechanism tied to how AFM works — e.g., the needle briefly lost contact, a vibration or electrical
  spike hit mid-line, or the feedback loop overshot on that pass.

## Data problem noticed (not fixed — flagging only)

`afm_summary.csv` row for `sample_id 31779` lists `material = Sb2Te3`, but `afm_gallery/gallery.json`
lists the same `sample_id` as `material = CrSb` (key `magnet_grains`), and the row's own
`data_package` column reads "MBE growth and characterization data of **Epitaxial CrSb** (0001) thin
films" — so the gallery label and package title agree with each other and disagree with the CSV's
material column. Likely a mislabel introduced upstream of the slice build. Did not touch
`camel_data/` or the build script per task scope; flagging for whoever owns `scripts/build_slice.py`.

## Common misconceptions

- "The 3D plot shows the crystal's true shape." It's vertically exaggerated by whatever factor is
  printed in the plot title — Task 1 and the scientist's note exist specifically to catch this.
- "A median of 0.00 nm means the surface is perfectly flat." It means the per-line flattening step
  forced each line's *middle* value to 0 nm — real bumps and dips are still there; that's exactly
  why the notebook has students compare mean and median rather than reading either alone.
- "My step-height reading was off from 0.39 nm, so I did something wrong." Real, noisy AFM data
  legitimately gives a range of readings; the check-yourself cell is calibrated to the scan's real
  spread, not to a single "right answer."
- "Anything unusual-looking in a scan must be a real surface feature." The whole point of Task 5 is
  that a single scan-line glitch (an instrument artifact) can look dramatic while being physically
  implausible (heights far outside anything the material could produce).

## Troubleshooting

- `explore_3d` and `explore_cross_section` need `output.enable_custom_widget_manager()` from the
  setup cell to render in Colab; outside Colab (or headless execution) they still run without
  error, they just don't display an interactive widget — the static `fig.show()` fallback cells
  cover that case for students on an unsupported browser.
- If a student changes `scan_key` in the unit-conversion cell to a name not in the gallery listing
  printed earlier, they'll get a `KeyError` — have them re-check the printed key spelling (all
  lowercase with underscores).
- The Task 2 check-yourself cell recomputes its reference range from the real scan every run, so it
  stays correct even if the slice is rebuilt; don't hardcode the printed numbers into a rubric that
  outlives a rebuild.

## Verification

```
.venv/bin/jupytext --to ipynb notebooks/src/01_nano_landscapes.py -o notebooks/01_nano_landscapes.ipynb
.venv/bin/python scripts/run_notebook.py notebooks/01_nano_landscapes.ipynb
```
Last run: PENDING — fill in after execution.
