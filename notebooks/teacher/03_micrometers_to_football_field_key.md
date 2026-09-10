# Teacher key — 03: From Micrometres to a Football Field

Notebook: `notebooks/03_micrometers_to_football_field.ipynb` (source: `notebooks/src/03_micrometers_to_football_field.py`).
All numbers below were **printed by executing the real notebook against the actual data slice**
(`.venv/bin/python scripts/run_notebook.py notebooks/03_micrometers_to_football_field.ipynb`,
executed copy at `notebooks/executed/03_micrometers_to_football_field.ipynb`) — none are typed from memory.

## Learning targets
- I can compute a scale factor and use it to predict the scaled size of a much smaller feature.
- I can measure a step height from a real surface and divide by a material's layer thickness to
  estimate a layer count, and explain why the answer isn't a clean integer.
- I can compute the area of a hexagonal unit cell and use it to estimate how many cells fit in a
  given area, using scientific notation.
- I can explain why surface-area-to-volume ratio grows as an object shrinks (SA:V = 6/side for a cube).
- I can compare a horizontal and a vertical scale factor and explain what "vertical exaggeration" means.

## Standards
| Task | CCSS | Student action |
|---|---|---|
| 1–3 | HSN.Q.A.1–3, HSG.SRT | Compute and apply a scale factor; unit conversion µm → m → cm |
| 4–7 | HSA.CED.A.1–4 | Measure a height, divide by a constant, build a linear function (thickness = rate × n) |
| 8–10 | HSG.MG.A.1–3 | Hexagon area formula; area-based counting in scientific notation |
| 11 | HSG.MG.A.1–3 | Cube surface area/volume scaling, SA:V = 6/s |
| 12–13 | HSG.SRT, HSN.Q.A.1–3 | Compare two independent scale factors (horizontal vs. vertical) |

## Timing (45–50 min)
| Minutes | Segment |
|---|---|
| 0–5 | Setup cell + "Meet your crystal" 3D view |
| 5–15 | Part 1: scale factor, feature scaling, MoS₂ layer at scale (Tasks 1–3) |
| 15–28 | Part 2: layer counting from a measured step (Tasks 4–7) — Task 6 (whole-scan survey) and Task 7 (linear table/graph) are Explore, can be skipped in a tight 45-min class |
| 28–36 | Part 3: hexagon geometry (Tasks 8–10) — Task 10 (atoms) is Extend |
| 36–41 | Part 4: surface-area-to-volume (Task 11) |
| 41–48 | Part 5: STL export, scale-factor comparison, download (Tasks 12–13) |
| 48–50 | Exit ticket |

**Core-only 45-minute path:** Tasks 1–5, 8–9, 11, 12 (skip Task 6, 7, 10, 13's full derivation —
just show the printed vertical-exaggeration number and discuss it).

## Expected answers (ranges, from the real slice)

**Task 1 — scale factor.** With `scan_width_um = 5`, `field_length_m = 100`:
`scale_factor = 2×10⁷`. Accept anything in **1×10⁷–4×10⁷** if students reasonably vary the field
length (100–110 m) or pick a different gallery scan width (1–5 µm).

**Task 2 — feature scaling.** `feature_width_nm = 300` → **6.00 m** at scale. Accept **4–8 m** for
feature widths students choose in the 200–400 nm range.

**Task 3 — MoS₂ layer at scale.** MoS₂ layer thickness from `materials_reference.csv` = 0.65 nm →
at 2×10⁷× that is **1.3 cm** ("about as thick as a smartphone"). This number is fixed by the table,
not student choice — flag any answer far from 1.3 cm as a units error (nm vs. m).

**Task 4/5 — measured step and layer count (Bi₂Se₃, `triangle_pyramids`, row 206).**
Printed: Terrace A ≈ **0.98 nm**, Terrace B ≈ **−0.07 nm** → step height ≈ **1.07 nm**.
`bi2se3_thickness_nm` from the table = **0.95 nm** → `layers_raw ≈ 1.13` → **rounds to 1 layer**.
Accept `layers_raw` in **0.9–1.4** as "about 1 layer" for this specific edge.

**Task 6 — whole-scan survey (Explore).** Scanning ~800 candidate edges across the full
`triangle_pyramids` image and keeping single-layer-like ones (window ±10 px, noise < 0.15 nm,
0.5–1.5 nm step) found **392 clean single-layer edges**: median **0.83 nm**, middle-50% range
**0.68–0.94 nm**, versus the reference 0.95 nm/layer. This is the real uncertainty spread — expect
students to notice the single Task 4 measurement (1.07 nm) sits a bit above the whole-scan median,
and to attribute the gap to tip convolution / local noise / which specific edge you land on, not to
error. Any answer in the range **0.6–1.1 nm** for "typical single step" is defensible.

**Task 8 — unit cell area (MoS₂, a = 0.316 nm).** `area = (√3/2)(0.316)² = 0.0865 nm²` exactly, no
student input — check the formula, not a range.

**Task 9 — unit cells per fingernail.** `1×10¹⁴ nm² ÷ 0.0865 nm² ≈ 1.16×10¹⁵` unit cells. Accept
**1.1×10¹⁵–1.2×10¹⁵**; a student who changes `fingernail_area_nm2` should get a proportionally
scaled answer — check the ratio, not the raw number.

**Task 10 — atoms on the fingernail (Extend).** 3 atoms/cell (1 Mo + 2 S) × 1.16×10¹⁵ ≈
**3.47×10¹⁵ atoms**.

**Task 11 — SA:V table.** Exact by formula: 1 cm → 600 m⁻¹, 1 mm → 6,000 m⁻¹, ... 1 nm → 6×10⁹ m⁻¹.
Growth factor from 1 cm to 1 nm is exactly **10,000,000× (10⁷)**, matching the 10⁷× shrink in side
length — this is the punchline of the "your answer" prompt (SA:V ∝ 1/side, so shrinking side by 10⁷
grows SA:V by 10⁷).

**Task 12/13 — STL scale factors.** With the notebook's suggested defaults `width_mm = 80`,
`relief_mm = 10` on `triangle_pyramids` (scan_um = 1.0, real peak-to-peak relief ≈ 9 nm): printed
**horizontal scale factor ≈ 8×10⁴×**, **vertical scale factor ≈ 1.14×10⁶×**,
**vertical exaggeration ≈ 14.2×**. Accept a wide range here since `width_mm`/`relief_mm` are
student-chosen — the graded quantity is that vertical exaggeration comes out **> 1** (it always
will, by design) and that students can explain why in one sentence.
*Note for teachers:* `real_relief_mm` is computed from `np.ptp(scan.z)` in **nm**, so it is a very
small number of millimetres (~9×10⁻⁶ mm) — this is expected and is exactly the point of the
exercise (a nanometre-scale relief needs enormous vertical stretch to be visible/printable).

## Common misconceptions
- **"The scale factor should apply to height too."** It doesn't have to, and in Part 5 it explicitly
  doesn't — that's the vertical-exaggeration idea. Watch for students who expect
  `vertical_exaggeration ≈ 1`.
- **"1.13 layers means the measurement is wrong."** A non-integer `layers_raw` is expected from any
  real measurement; the skill is rounding sensibly and stating uncertainty, not forcing an exact hit.
- **Using 0.65 nm (MoS₂) for every material.** The notebook forces a table lookup per material to
  head this off; watch for students who hardcode 0.65 in Task 5 instead of using
  `bi2se3_thickness_nm`.
- **Treating the honeycomb picture as literal.** The drawn lattice uses one dot style per sublattice
  vertex, not per real atom position/height — the "Scientist's note" after Task 8 addresses this
  directly; reinforce it verbally.
- **SA:V ratio "explains" nanomaterial behavior by itself.** It's one factor among several
  (confinement, screening, interfaces) — see the guardrail note after Task 11.

## Troubleshooting
- If `explore_cross_section` / `explore_3d` widgets render blank: rerun the setup cell (it calls
  `output.enable_custom_widget_manager()`), then Runtime → Restart and run all.
- If the STL download does nothing outside Colab: expected — the `except ImportError` branch prints
  the local path instead; the file is in the notebook's working directory.
- If printed numbers differ slightly from this key (e.g. scale factor not exactly 2×10⁷): check
  that students didn't change `scan_width_um`/`field_length_m` — expected if they explored, a bug if
  they didn't touch those cells.

## Complexity dials
- **Core:** Tasks 1–5, 8, 9, 11, 12 — all "change the number, run the cell" tasks.
- **Explore:** Task 6 (whole-scan step survey), Task 7 (linear function table/graph), Task 13
  (scale-factor comparison derivation).
- **Extend:** Task 10 (atom count), and challenging students to explain in Task 13 why a school
  printer would refuse an STL with `vertical_exaggeration` pushed too high (nozzle can't resolve a
  too-tall/too-thin spike).
