# CAMEL × 2DCC classroom data slice (release camel-2dcc-v1)

Real measurements of atomically thin crystals grown at Penn State's 2D Crystal Consortium (2DCC-MIP),
taken from the public records of its LiST sample database. Made for CAMEL high-school math lessons
(NSF award 2621173).

## What is in here

| File | What it holds |
|------|---------------|
| `samples.csv` | Every public sample: material, substrate, growth method, measurements taken, dates, data package, DOI. Entered by scientists, so spellings vary and some cells are blank — on purpose. |
| `afm_summary.csv` | One AFM (atomic force microscope) scan per sample: scan size, pixels, RMS roughness, average roughness, height range. |
| `afm_small.npz` | Every AFM scan shrunk to 64 × 64 heights (nm), keyed by sample id. |
| `afm_gallery/*.npz` | Hand-picked full-resolution height maps (`height_nm`, `x_um`, `y_um`), described in `gallery.json`. |
| `growth_recipes.csv` | Step-by-step growth recipes (MOCVD and hybrid MBE): step name, duration (min), start time, temperature (°C), pressure (Torr). |
| `growth_summary.csv` | One row per grown sample: total growth time, growth temperature and pressure, joined to its AFM roughness when measured. |
| `chips_timeline.csv`, `materials_reference.csv`, `superconductors.csv` | Curated context tables (not LiST data); see `SOURCES.md`. |
| `stl/*.stl` | 3D-printable AFM surfaces. |
| `camel_data/` | Small Python helpers the notebooks import. |
| `manifest.json` | Every file with its size and SHA-256 checksum. |

## How heights were processed

AFM files were read from the instrument's raw format, converted to nanometres, and each scan line was
levelled with a straight-line fit (the standard "flatten" step), then shifted so the median height is 0.
Roughness numbers in `afm_summary.csv` come from that levelled surface.

## Citing

Each sample row lists its 2DCC data package and DOI. Please cite the DOI when you use a sample, and
cite the 2DCC-MIP (NSF DMR-2039351). Data are shared under CC-BY-4.0.
