# Teacher key — 03: From Micrometres to a Football Field

Notebook: `notebooks/03_micrometers_to_football_field.ipynb` (source: `notebooks/src/03_micrometers_to_football_field.py`).
All numbers below were **printed by executing the real notebook against the actual data slice**
(`.venv/bin/python scripts/run_notebook.py notebooks/03_micrometers_to_football_field.ipynb`,
executed copy at `notebooks/executed/03_micrometers_to_football_field.ipynb`) — none are typed from memory.

## Learning targets
- I can compute a scale factor and use it to predict the scaled size of a much smaller feature.
- I can measure a step height from a real surface and divide by a material's layer thickness to
  estimate a layer count, and explain why the answer isn't a clean integer.
- I can compare a horizontal and a vertical scale factor and explain what "vertical exaggeration" means.
- *(Extension)* I can compute the area of a hexagonal unit cell and use it to estimate how many
  cells fit in a given area, using scientific notation, and explain why surface-area-to-volume ratio
  grows as an object shrinks (SA:V = 6/side for a cube).

## Standards
| Task | CCSS | Student action |
|---|---|---|
| 1–3 | HSN.Q.A.1–3, HSG.SRT | Compute and apply a scale factor; unit conversion µm → m → cm |
| 4–7 | HSA.CED.A.1–4 | Measure a height, divide by a constant, build a linear function (thickness = rate × n) |
| 8–9 | HSG.SRT, HSN.Q.A.1–3 | 3D-print export; compare two independent scale factors (horizontal vs. vertical) |
| 10–12 *(Extension)* | HSG.MG.A.1–3 | Hexagon area formula; area-based counting in scientific notation |
| 13 *(Extension)* | HSG.MG.A.1–3 | Cube surface area/volume scaling, SA:V = 6/s |

## Timing — Core path (45 minutes)
| Minutes | Segment |
|---|---|
| 0–5 | Setup cell + "Meet your crystal" 3D view |
| 5–13 | Part 1: scale factor, feature scaling, MoS₂ layer at scale (Tasks 1–3) |
| 13–26 | Part 2: layer counting from a measured step (Tasks 4–5 required; Task 6 whole-scan survey and
| | Task 7 linear table/graph are Explore — skip both in a tight 45-min class) |
| 26–38 | Part 3: STL export and scale-factor comparison (Tasks 8–9) |
| 38–45 | Exit ticket |

This totals **45 minutes** with Tasks 6 and 7 skipped. If a class has extra time, Tasks 6–7 fit in the
gap between Part 2 and Part 3 at about 6–8 more minutes.

**Core-only path:** Tasks 1–5, 8 (skip Task 6, 7, 9's full derivation — just show the printed
vertical-exaggeration number from Task 9 and discuss it in one sentence).

## Timing — Extension (second class period or homework, ~20–25 minutes)
| Minutes | Segment |
|---|---|
| 0–10 | Hexagon geometry: honeycomb drawing + unit-cell area (Task 10) |
| 10–16 | Unit cells and atoms on a fingernail (Tasks 11–12) |
| 16–24 | Surface-area-to-volume (Task 13) |

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
The helper prints Terrace A ≈ **0.98 nm**, Terrace B ≈ **−0.07 nm**; the very next cell computes
`step_height_nm` directly from those two variables (students no longer retype rounded values), giving
step height ≈ **1.05 nm**. `bi2se3_thickness_nm` from the table = **0.95 nm** → `layers_raw ≈ 1.10` →
**rounds to 1 layer**. Accept `layers_raw` in **0.9–1.4** as "about 1 layer" for this specific edge.
If a student's printed numbers differ from 0.98/−0.07, that's fine — the code always uses whatever the
helper actually printed, so their downstream numbers will differ proportionally; don't flag that as an
error.

**Task 6 — whole-scan window survey (Explore).** The helper slides a ±10-pixel window across every row
of `triangle_pyramids` (step = 2 px) and flags positions whose step falls in [0.5, 1.5] nm with low
noise: **392 qualifying windows** under this rule, median **0.83 nm**, middle-50% range **0.68–0.94 nm**,
versus the reference 0.95 nm/layer.
*Say this exactly, not more:* these are **392 overlapping window positions, not 392 independent step
edges** — a single physical step edge is re-detected by many nearby rows/columns. The [0.5, 1.5] nm
filter was also chosen close to the expected ~0.95 nm answer on purpose, so the close median agreement
is **partly built into the filter**, not independent confirmation of 0.95 nm. Do **not** describe the
0.68–0.94 nm middle-50% range as "measurement uncertainty" — it is the spread of a biased, overlapping
sample, not a calibrated error bar. Frame Task 6 as a demonstration of image-processing counting
pitfalls (double-counting, threshold choice), not as a statistics-grade uncertainty estimate. Any
answer near the printed median (**0.6–1.0 nm**) for "typical single step" is defensible, alongside a
correct statement that the count is not independent step edges.

**Task 8 — STL export.** Runs with the defaults `width_mm = 80`, `relief_mm = 10` on
`triangle_pyramids`; saves `my_crystal.stl`. No numeric answer to check — verify the file is created
and the print statement confirms the save.

**Task 9 — STL scale factors.** With the notebook's suggested defaults `width_mm = 80`, `relief_mm =
10` on `triangle_pyramids` (scan_um = 1.0): the scan is **0.0010 mm** wide; the height range that
`to_stl` actually maps to `relief_mm` (its internal 0.5th–99.5th percentile, from
`stl_height_range_nm`) is **6.00 nm** (−2.09 to 3.91 nm) — printed alongside the **full peak-to-peak
range of 8.79 nm** for contrast, since the two differ (a few spike/dip pixels are clipped rather than
setting the scale). Printed **horizontal scale factor ≈ 8×10⁴×**, **vertical scale factor ≈
1.67×10⁶×**, **vertical exaggeration ≈ 20.8×**. Accept a wide range here since `width_mm`/`relief_mm`
are student-chosen — the graded quantity is that vertical exaggeration comes out **> 1** (it always
will, by design) and that students can explain why in one sentence.
*Note for teachers:* if you update `src/camel_data/classroom.py` or the data slice, re-run the
notebook and copy the new printed numbers here rather than reusing this table — `vertical_scale` is
now computed from `stl_height_range_nm(scan)`, the exact range `to_stl` clips to, so it will track any
change to that helper automatically.

**Task 10 — unit cell area (MoS₂, a = 0.316 nm).** `area = (√3/2)(0.316)² = 0.0865 nm²` exactly, no
student input — check the formula, not a range. The honeycomb drawing (`draw_mos2_lattice`) plots Mo
atoms on a triangular lattice with spacing `a_nm`, S atoms (top + bottom, projected to one dot) at the
centres of alternate triangles, and marks one primitive rhombus cell (sides `a_nm`, 60°) — the drawn
hexagon *side* is `a_nm / √3 ≈ 0.182 nm`, not `a_nm` itself. Check that students can point to the
green rhombus and say it holds 1 Mo + 1 S-pair.

**Task 11 — unit cells per fingernail (Extension, Explore).** `1×10¹⁴ nm² ÷ 0.0865 nm² ≈ 1.16×10¹⁵`
unit cells. Accept **1.1×10¹⁵–1.2×10¹⁵**; a student who changes `fingernail_area_nm2` should get a
proportionally scaled answer — check the ratio, not the raw number.

**Task 12 — atoms on the fingernail (Extension, Extend).** 3 atoms/cell (1 Mo + 2 S) × 1.16×10¹⁵ ≈
**3.47×10¹⁵ atoms**.

**Task 13 — SA:V table (Extension, Core).** Exact by formula: 1 cm → 600 m⁻¹, 1 mm → 6,000 m⁻¹, ...
1 nm → 6×10⁹ m⁻¹. Growth factor from 1 cm to 1 nm is exactly **10,000,000× (10⁷)**, matching the 10⁷×
shrink in side length — this is the punchline of the "your answer" prompt (SA:V ∝ 1/side, so shrinking
side by 10⁷ grows SA:V by 10⁷).

## Common misconceptions
- **"The scale factor should apply to height too."** It doesn't have to, and in Part 3 it explicitly
  doesn't — that's the vertical-exaggeration idea. Watch for students who expect
  `vertical_exaggeration ≈ 1`.
- **"1.10 layers means the measurement is wrong."** A non-integer `layers_raw` is expected from any
  real measurement; the skill is rounding sensibly and stating uncertainty, not forcing an exact hit.
- **Using 0.65 nm (MoS₂) for every material.** The notebook forces a table lookup per material to
  head this off; watch for students who hardcode 0.65 in Task 5 instead of using
  `bi2se3_thickness_nm`.
- **"392 windows means 392 measured step edges."** They are overlapping window positions on a sliding
  scan, not independent edges — correct this directly if it comes up; see the Task 6 note above.
- **"A monolayer is one atom thick."** MoS₂'s monolayer is S–Mo–S (three atomic planes, ~0.65 nm);
  Bi₂Se₃'s quintuple layer is five atomic sheets (~0.95 nm). "Monolayer" means one repeating structural
  layer, not one atomic plane — reinforce this whenever the word comes up.
- **Treating the honeycomb picture as an exact atom-for-atom photograph.** It's a straight-down
  projection that collapses the top and bottom S atoms into one dot — the "Scientist's note" after
  Task 10 addresses this directly; reinforce it verbally.
- **SA:V ratio "explains" nanomaterial behavior by itself.** It's one factor among several
  (confinement, screening, interfaces) — see the guardrail note after Task 13.

## Troubleshooting
- If `explore_cross_section` / `explore_3d` widgets render blank: rerun the setup cell (it calls
  `output.enable_custom_widget_manager()`), then Runtime → Restart and run all.
- If the STL download does nothing outside Colab: expected — the `except ImportError` branch prints
  the local path instead; the file is in the notebook's working directory.
- If printed numbers differ slightly from this key (e.g. scale factor not exactly 2×10⁷, or Terrace A
  not exactly 0.98 nm): check that students didn't change `scan_width_um`/`field_length_m` — expected
  if they explored, a bug if they didn't touch those cells. Task 4/5 now always use whatever the helper
  actually printed (no retyped literals), so small differences there should only come from a changed
  data slice, not from a copy error.

## Complexity dials
- **Core (Day 1, ~45 min):** Tasks 1–5, 8 — all "change the number, run the cell" tasks — plus the
  exit ticket.
- **Explore (Day 1, time-permitting):** Task 6 (whole-scan window survey), Task 7 (linear function
  table/graph), Task 9 (scale-factor comparison derivation — the printed numbers alone are Core, the
  derivation is optional).
- **Extension (Day 2 or homework):** Tasks 10–13 — hexagon geometry, unit-cell counting, atom count,
  and surface-area-to-volume. Task 12 (atom count) is the deepest dive within the Extension.
