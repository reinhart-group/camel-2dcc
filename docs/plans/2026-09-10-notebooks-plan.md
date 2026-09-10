# Implementation plan — CAMEL × 2DCC Colab notebooks

Spec: `docs/specs/2026-09-10-camel-2dcc-data-and-demos-design.md`. Codex brainstorm:
`docs/codex/brainstorm-response.md` (read sections 2, 4, 5 before writing any notebook).

## Conventions every notebook follows

- **Source format:** jupytext percent-format Python in `notebooks/src/NN_name.py`
  (`# %% [markdown]` and `# %%` cells). Build: `.venv/bin/jupytext --to ipynb notebooks/src/*.py`
  writes `notebooks/NN_name.ipynb`. Never hand-edit `.ipynb`.
- **Cell 1 (markdown):** title, one-sentence hook, "What you'll do" (3 bullets), time (45–50 min),
  a "Materials science words" box defining every technical word used later.
- **Cell 2 (code): Teacher setup** — copy exactly from `notebooks/src/_setup_cell.py`. It downloads the
  slice zip from `DATA_URL` (one line to change), verifies it is a zip, unzips to `camel-2dcc/`,
  caches it for the session, adds `camel-2dcc` to `sys.path`, and enables Colab's custom widget
  manager. It also accepts a manually uploaded zip.
- **Student cells:** short. Students change numbers marked `# <-- change me` or move sliders. No
  student cell over ~12 lines. Any heavier code goes in `camel_data/classroom.py` (add helpers there
  if needed; keep them readable).
- **Tasks:** each numbered task is a markdown cell headed `### Task N` with a question; answers go in a
  markdown cell `**Your answer:**` or a variable like `my_estimate = ...  # <-- change me`.
- **Complexity dials:** tasks tagged **Core**, **Explore**, or **Extend** (Core fits a 45-minute
  non-AP class alone).
- **Check-yourself cells** give feedback on numeric answers with ranges, not exact values.
- **Exit ticket** last: 2–3 questions answerable without code.
- **Physics guardrails** from Codex section 2 appear as short "Scientist's note" callouts.
- **Tone:** exciting and concrete, Grade 9–12 reading level, no hype, no claims that a sample is in a
  commercial product. Say "about" for approximate numbers.
- **Accessibility:** colour-blind-safe colourscales (Viridis/Cividis), every plot has axis labels with
  units, every interactive view has a static fallback line (`fig.show()` or `plt`).
- **Teacher key:** `notebooks/teacher/NN_name_key.md` — learning targets, CCSS codes per task,
  minute-by-minute timing, expected answers as ranges computed from the real slice, common
  misconceptions, troubleshooting.

## Data available (in `camel-2dcc/` after setup)

`samples.csv`, `afm_summary.csv`, `afm_small.npz`, `afm_gallery/*.npz` + `gallery.json`,
`mbe_recipes.csv`, `chips_timeline.csv`, `materials_reference.csv`, `superconductors.csv`,
`SOURCES.md`, `stl/*.stl`. Helpers: `from camel_data.classroom import *` gives `load_gallery`,
`load_table`, `load_small_maps`, `surface_3d`, `explore_3d`, `cross_section`,
`explore_cross_section`, `to_stl`, `rms`.

## Notebooks

1. **01_nano_landscapes** — Geometry + intro statistics. Plotly 3D AFM terrain with ipywidgets
   (sample dropdown, height-stretch slider, colours); line-profile slider; read scan size and height
   range; unit conversion µm ↔ nm; histogram of heights for one scan; mean vs median with a dust
   particle; spot a scan artifact.
2. **02_how_smooth_is_smooth** — AFM statistics. RMS roughness as "typical distance from average
   height" (build it by hand on 5 numbers, then on a scan); `afm_summary.csv` box plots by material
   and by growth method (MOCVD vs MBE); median/IQR/outliers; missing values are not zero; claim–
   evidence–reasoning about which method grows smoother films and why the data can't prove cause.
3. **03_micrometers_to_football_field** — Algebra + geometry. Scale factor from a 5 µm scan to a
   100 m field; layer counting from a measured step (height ÷ layer thickness, per material, with
   uncertainty); hexagon lattice geometry (area of a hexagonal cell from `materials_reference.csv`,
   atoms per fingernail in scientific notation); surface-area-to-volume scaling; export an STL with
   chosen width/relief and download it (`google.colab.files.download`).
4. **04_build_a_crystal** — Algebra: piecewise functions and rates. Turn a real recipe (MOCVD MoS2
   or hybrid-MBE SnSe from `growth_recipes.csv`) into a cumulative-time temperature timeline; slopes on ramps (°C/min);
   pressure in scientific notation and ratios; linear °C ↔ K ↔ °F conversions; missing ≠ zero.
5. **05_chips_for_ai** — Exponential functions + inverse proportion. Transistor counts
   (`chips_timeline.csv`) on linear vs log axes, doubling time fit, "Moore's law is a trend not a
   law"; why thin channels help (MoS2 0.65 nm vs silicon); stacking layers (monolithic 3D) as a
   multiplication model; photonics: λ = 1240 / E (nm, eV) → colour of light each 2D material emits;
   superconductors (`superconductors.csv`, FeSe) and why zero resistance matters for data-centre
   energy (IEA figures in `SOURCES.md`); LiST catalog shows which of these materials 2DCC grows.
0. **00_teacher_live_list** — Teacher/researcher only. Uses `camel_data.list_public.PublicLiST` with
   the key from Colab Secrets (`LIST_API_KEY`); explains the Penn State network requirement; pulls
   one AFM record live and compares it with the slice.

## Verification per notebook

1. `jupytext --to ipynb` then execute headlessly: `.venv/bin/python scripts/run_notebook.py
   notebooks/NN_name.ipynb` (runs with the local slice; must finish with no errors).
2. Teacher-key numbers must be printed by the executed notebook or computed from the slice — never
   typed from memory.
3. Final gate (Claude): run in a real Colab VM via the Colab CLI; Codex review.
