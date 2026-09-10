# CAMEL × 2DCC: real 2D-materials data for high-school math

Google Colab notebooks and a classroom data slice for the CAMEL project (NSF 2621173, PI Rebecca
Napolitano). Students in typical Grades 9–12 Algebra, Geometry, and Statistics classes explore real
atomic force microscope (AFM) scans and growth recipes from Penn State's 2D Crystal Consortium
(2DCC-MIP), taken from the public records of its LiST sample database.

## Notebooks (`notebooks/`)

| # | Notebook | Math |
|---|----------|------|
| 00 | `00_teacher_live_list` — pull live public records from LiST (Penn State network only) | teachers |
| 01 | `01_nano_landscapes` — fly over crystals in 3D, line profiles, height distributions | geometry, intro statistics |
| 02 | `02_how_smooth_is_smooth` — RMS roughness, box plots across 1,004 real scans | statistics |
| 03 | `03_micrometers_to_football_field` — scale factors, layer counting, hexagons, 3D printing | algebra, geometry |
| 04 | `04_build_a_crystal` — a real growth recipe as a piecewise function | algebra, functions |
| 05 | `05_chips_for_ai` — Moore's law, light from band gaps, superconductors, data-centre energy | exponential and inverse functions |

Teacher keys with timing, standards, and expected answer ranges are in `notebooks/teacher/`.
Notebook sources are jupytext percent-format files in `notebooks/src/`; build with
`.venv/bin/jupytext --to ipynb notebooks/src/NN_name.py -o notebooks/NN_name.ipynb`.

## Data slice

`data/slice/camel-2dcc-v1.zip` (about 25 MB; contents described in `docs/slice-README.md`). The
notebooks download it from a SharePoint "Anyone with the link" share, set once in each notebook's
setup cell (`DATA_URL`). Without a link, upload the zip through Colab's Files panel.

A copy lives in OneDrive: `Funding/Awarded/2026-03-CAMEL/CAMEL-2DCC-data/`.

## Rebuilding the slice (Penn State network or VPN required)

```bash
uv venv .venv && uv pip install --python .venv/bin/python -e ~/Code/strata/core \
    -e ~/Code/strata/psu-list-adapter numpy pandas scipy matplotlib plotly ipywidgets requests \
    nbformat nbclient ipykernel jupytext numpy-stl pytest
# .env (git-ignored) holds LIST_BASE_URL and the public LIST_API_KEY
set -a; . ./.env; set +a
.venv/bin/python scripts/index_afm_files.py         # list files on every public AFM sample
.venv/bin/python scripts/build_afm_summary.py       # download + measure one scan per sample
.venv/bin/python scripts/fetch_recipes.py           # growth recipes
.venv/bin/python scripts/fetch_gallery_candidates.py  # gallery scans (picks: scripts/gallery_picks.json)
.venv/bin/python scripts/build_slice.py             # assemble data/slice/ (offline)
```

Each network stage is resumable and records failures in `data/raw/*errors.json`.

## Testing

- `PYTHONPATH=src .venv/bin/python -m pytest tests` — AFM reader (checked against the instrument's
  own 0.36 nm roughness), STL watertightness, helpers.
- `.venv/bin/python scripts/run_notebook.py notebooks/*.ipynb` — executes every notebook headlessly.
- Real Colab: `colab new -s camel-test`, `colab upload -s camel-test data/slice/camel-2dcc-v1.zip
  /content/camel-2dcc-v1.zip`, `colab exec -s camel-test -f notebooks/NN_name.ipynb`, `colab stop`.

## The public LiST key

The key reads only `Published` records. It is not a secret, but it is never written into code or
notebooks: scripts read `LIST_API_KEY` from `.env`; the teacher notebook reads a Colab Secret.
