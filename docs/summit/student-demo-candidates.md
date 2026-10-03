# Student demo candidates for the PA Data Literacy Summit

## Recommendation at a glance

| Rank | Candidate | Why it fits | Main caution |
|---|---|---|---|
| **1** | **Hit the target: size a WSe2 chip crystal** | The clearest one-screen mission: real microscope-derived area, one geometry calculation, immediate visual feedback, and a single answer of **57.247 nm**. It feels like setting a nanoscale fabrication target without requiring a chemistry or physics lesson. | The stored `side_nm` is derived from `area_nm2` using the same equilateral-triangle formula, so this is a geometry conversion, not an independent validation of shape. |
| **2** | **Tune the chip-growth curve** | The most direct computer-chip story and the strongest chart interaction. A precisely specified fit gives one reproducible answer: **2.054 years**. | The 18-chip table is hand-picked and heterogeneous; the answer describes this dataset, not a universal law or forecast. |
| **3** | **Calibrate a wafer with X-rays** | Visually high-tech and mathematically elegant: students use a real diffraction peak and right-triangle trigonometry to recover an atomic spacing of **0.2164 nm**. A second peak gives a satisfying built-in check. | **Verification flag:** the CSV contains angle and intensity but not the assumed Cu K-alpha wavelength or reflection order. Those inputs come from the notebook, so the answer is not verifiable from the CSV alone. It also risks feeling more like physics than the first two. |

**Recommendation:** build Candidate 1 for the summit. It best satisfies “hand-holdy, easy, high-tech, one clear answer” in a static single-page site. Candidate 2 is the best fallback if Wes and Kathy want the words *computer chip* to be unavoidable in the mission itself. Candidate 3 is a strong future extension, but it carries more prerequisite context and an external-input caveat.

All three can be implemented in plain HTML, CSS, SVG/canvas, and vanilla JavaScript with the small needed data arrays embedded locally. None requires an account, notebook runtime, CDN, or network request.

## Candidate 1 — Hit the target: size a WSe2 chip crystal

### Student mission

**Set the side length of a triangular, atomically thin WSe2 crystal so its calculated area matches the area measured from a real Penn State microscope scan.**

### Math skill

Geometry and algebra: area of an equilateral triangle, `A = (sqrt(3)/4)s^2`, and solving for `s`.

### Real data used

- File: `data/slice/camel-2dcc/grains/grains.csv`
- Row: `scan = wse2_17458_center`, `sample_id = 17458`, `grain = 217`
- Student-facing measured column: `area_nm2 = 1419.067`
- Filtering/context columns: `kind = single`, `touches_edge = False`, `touches_glitch = False`
- Check column: `side_nm = 57.247`
- Supporting visual data: the full-resolution AFM scan named by `wse2_17458_center` in `grains/scans.json`
- Provenance: sample 17458, WSe2 on sapphire grown by MOCVD, DOI `10.26207/f7b1-fs46`. The slice says its 2DCC data are shared under CC BY 4.0.

### Single checkable answer

Solve

`s = sqrt(4A / sqrt(3)) = sqrt(4(1419.067) / sqrt(3)) = 57.246789... nm`.

The single answer should be **57.247 nm**, or **57.2 nm** to one decimal place. I recomputed this directly from `area_nm2`; it matches the stored `side_nm = 57.247`.

This answer does **not** depend on an unverified external number. It does depend on the stated modeling assumption that the island is treated as an equilateral triangle. The stored side length is derived from the same measured area and formula, so the agreement is intentionally a self-check, not a second measurement.

### Interactive control

A **side-length slider** from roughly 20 to 90 nm. Moving it should simultaneously:

- scale an SVG triangle over or beside the real AFM crop;
- update the calculated area live;
- move a marker on a “calculated area vs. measured target” bar; and
- change the state from “too small” to “too large,” with a narrow green lock-on state at 57.2 nm.

A small `show measurement outline` toggle can reveal the thresholded pixel outline after the answer without changing the task.

### Guided steps

1. Read the microscope result: this island covers **1419.067 nm2**.
2. Use the provided equilateral-triangle formula and move the side-length slider; watch the predicted area change.
3. Stop when the predicted area meets the measured target, then enter the side length to the nearest 0.1 nm.
4. Reveal the algebraic check and compare the ideal triangle with the real, imperfect island outline.

### MATSE 219 figures that could illustrate it

- `courses/fall-2026/sketches/matsci_grain_microstructure_sketch.svg`: useful only as a brief “materials scientists measure features in microscope images” bridge. It depicts irregular alloy grains, **not** WSe2 islands, so label that distinction explicitly.
- `courses/fall-2026/sketches/matsci_crystal_structures_sketch.svg`: optional opening context that solids have repeating atomic arrangements; do not imply its FCC/BCC/HCP cells are the structure of WSe2.
- The real CAMEL AFM image should be the hero graphic; it is more relevant than either generic MATSE sketch.

The two SVGs appear to be locally authored MATSE 219 course schematics described in `sketches/MANIFEST.md`. I found no repository-wide license in the private MATSE 219 repo, so treat them as Wes-owned/internal assets or get explicit permission before public reuse. Do not use `images/grain_boundaries_ti_alloy.jpg` as if it showed this material; it is a Ti-alloy micrograph by Edward Pleshakov, licensed CC BY 3.0, and is only a generic microscopy example.

## Candidate 2 — Tune the chip-growth curve

### Student mission

**Calibrate the doubling-time control on a chip-design dashboard so one exponential curve best matches 18 real chips from 1971–2024.**

### Math skill

Statistics and exponential functions: transform counts with `log2`, fit a straight line, and interpret the reciprocal of its slope as a doubling time.

### Real data used

- File: `data/slice/camel-2dcc/chips_timeline.csv`
- Fit columns: `year`, `transistors`
- Display/context columns: `chip`, `maker`, `dies_in_package`, `used_for`
- Rows: all 18 packaged records, from the Intel 4004 through NVIDIA B200
- Provenance limitation: `SOURCES.md` says the rounded counts come from chip-maker announcements and datasheets as compiled in Wikipedia's transistor-count article. It also says the set is hand-picked, changes device category over time, and counts both B200 dies.

### Single checkable answer

Define the result precisely as the ordinary least-squares slope of

`log2(transistors) = intercept + slope * (year - 1971)`

over all 18 rows, then `doubling time d = 1/slope`.

Direct recomputation from the CSV gives:

- `slope = 0.4868682154 doublings/year`
- `d = 2.053943898 years`

The single answer is **2.054 years**, or **2.05 years** to two decimal places.

This is fully verifiable from the packaged data and stated method. It is selection-sensitive: the same calculation on the 11 Intel rows gives **2.096 years**. That caveat should appear after the student locks in the answer, not turn the mission into an open-ended discussion.

### Interactive control

A **doubling-time slider** from 1.0 to 4.0 years overlays the model curve on the 18 real chip points. Use a log y-axis by default so model mismatch is visible across seven orders of magnitude. A `linear / log` toggle can visibly demonstrate why the log view is useful while leaving the answer unchanged. A small mismatch meter can reach its minimum at 2.05 years.

### Guided steps

1. Inspect the real chip points and note that transistor counts multiply rather than rise by a fixed amount.
2. Move the doubling-time slider until the curve tracks the points across the whole timeline; use the log-axis toggle to check early and late chips together.
3. Read the transformed straight-line rule: the fitted slope is `1/d`.
4. Enter `d` to two decimal places, reveal **2.05 years**, then read the one-sentence warning that this describes a curated historical set rather than guaranteeing the future.

### MATSE 219 figures that could illustrate it

- `courses/fall-2026/sketches/data_residuals_least_squares_sketch.svg`: directly useful for explaining that “best fit” means making the vertical residuals collectively small.
- `courses/fall-2026/sketches/data_mean_vs_line_residuals_sketch.svg`: optional teacher-facing or reveal-panel visual showing why a fitted line is better than one constant prediction after log transformation.
- `courses/fall-2026/sketches/matsci_crystal_structures_sketch.svg`: optional decorative bridge from materials to devices, but it is not a chip schematic.

These are locally authored MATSE 219 course SVGs, not externally attributed photos. The private repo has no repository-wide license file, so public reuse should be cleared with Wes. I did **not** find a suitably licensed transistor/chip photograph already curated in the current MATSE 219 image library; use a locally drawn chip/package schematic rather than introducing a network dependency or uncertain photo license.

## Candidate 3 — Calibrate a wafer with X-rays

### Student mission

**Use two sharp peaks in a real wafer scan to calculate the spacing between repeating atomic planes before a semiconductor film is built on top.**

### Math skill

Geometry/trigonometry and arithmetic: halve `2theta`, use sine in Bragg's law, substitute units, and compare two results.

### Real data used

- File: `data/slice/camel-2dcc/extras/xrd_20958.csv`
- Columns: `two_theta_deg`, `intensity_counts`
- First peak: maximum in the 35–48 degree window, `2theta = 41.705 degrees`
- Second peak: maximum in the 85–95 degree window, `2theta = 90.755 degrees`
- Sample context from `samples.csv`: sample 20958, `(Bi,Sb)2Te3; Bi,Sb` grown by MBE on sapphire, DOI `10.26207/fmb5-6297`
- The notebook identifies the two sharp peaks as the sapphire substrate and uses Cu K-alpha wavelength `lambda = 0.15406 nm`, with orders `n = 1` and `n = 2`.

### Single checkable answer

Using `n lambda = 2d sin(theta)` and `theta = (2theta)/2`:

- first peak: `d = 0.2163986571 nm`
- second peak: `d = 0.2164523281 nm`

Both independently round to the single answer **0.2164 nm**.

**Verification flag:** `lambda = 0.15406 nm` and the assignments `n = 1, 2` are supplied by `notebooks/src/07_more_ways_to_see.py`; they are not columns or metadata in `xrd_20958.csv`. The answer is reproducible from our repository, but it cannot be verified from the scan CSV alone. If this candidate advances, add those instrument/interpretation facts to local demo metadata and cite their source.

### Interactive control

A **draggable peak cursor** snapped to actual `two_theta_deg` samples. A two-position `first peak / second peak` toggle changes the highlighted window and reflection order. As students drag, a right-triangle schematic changes angle and a live `d` readout changes. Correct placement makes the two independently calculated spacings converge at 0.2164 nm.

### Guided steps

1. Drag the cursor to the tallest point in the first highlighted angle window and read `2theta`.
2. Halve that value to get `theta`, then substitute it into the provided Bragg-law triangle/formula.
3. Switch to the second peak and repeat with `n = 2`.
4. Submit the shared spacing to four decimal places and reveal why agreement between the two peaks is a useful calibration check.

### MATSE 219 figures that could illustrate it

- `courses/fall-2026/sketches/matsci_xrd_pattern_sketch.svg`: a clean, locally authored schematic of an XRD pattern; good as a small “what counts as a peak?” primer.
- `courses/fall-2026/images/xrd_pattern.png`: Wikimedia Commons `Powder_XRD_schematic_diagram.png`, documented in MATSE 219's `images/LICENSES.md` as **CC BY-SA 4.0**. This is the best existing apparatus/geometry visual, provided attribution, license link, ShareAlike terms, and modification notice are carried into the site.
- `courses/fall-2026/sketches/matsci_unit_cell_sketch.svg`: optional bridge from the computed spacing to repeating crystal geometry; keep it generic because it does not depict this sapphire plane.

The locally authored SVGs again have no explicit public license in the private MATSE 219 repository. The Wikimedia PNG has clear reusable provenance and is the safest MATSE asset for a public-facing demo if its CC BY-SA obligations are followed.

## Why the other inspected notebook ideas did not make the top three

- `04_build_a_crystal`: the real sample-23451 recipe is visually promising, but its most engaging ramp answer depends on an **unrecorded starting temperature**. The teacher key correctly labels the 57.35 degrees C/min result as hypothetical, which conflicts with Kathy's request for one clean answer rooted in verified data. The exact 56-minute total is verifiable arithmetic but less compelling than the three finalists.
- `06_counting_crystals`: random-sampling simulations are excellent data-literacy teaching, but any one random sample has no single correct mean. The selected geometry task above uses the same real dataset while preserving one checkable endpoint.
- `07_more_ways_to_see`, Raman station: sample 32093's 20.2 inverse-centimeter peak separation falls between the one- and two-layer reference bands, so the layer-count conclusion is deliberately uncertain rather than one clear answer.
- `07_more_ways_to_see`, SEM station: manual counts and side-length readings intentionally accept ranges; that is honest science but a poorer summit fit than a fixed-answer demo.
- `05_chips_for_ai`, monolayer-versus-silicon ratio and stacked-device arithmetic: the silicon thickness and devices-per-layer inputs are explicitly illustrative or made up, so those exercises should not be presented as answers established by the real dataset.

## Evidence and licensing notes

- Numerical answers above were recomputed read-only from the current files in `data/slice/camel-2dcc`; no notebook build or data mutation was used.
- The teacher keys independently report the same rounded values: 57 nm/1419 nm2 for grain 217, 2.05 years for the all-chip fit, and 0.2164 nm from both XRD peaks.
- `data/slice/camel-2dcc/README.md` states that the 2DCC data are shared under **CC BY 4.0** and asks users to cite the sample DOI and 2DCC-MIP (NSF DMR-2039351).
- `chips_timeline.csv` is a curated context table rather than LiST measurement data; preserve its source/selection warning from `SOURCES.md`.
- MATSE 219 external-image licensing is documented in `courses/fall-2026/images/LICENSES.md`. The course's hand-drawn SVG sketches have clear internal origin in `sketches/MANIFEST.md`, but the private repository contains no general license file; do not silently infer a public license.
