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
| `extras/` | Non-AFM measurements for notebook 07: FeSe resistance vs temperature (`transport_fese.csv`, `transport_summary.csv`), MoS2/WS2 Raman spectra and MoS2 peak positions (`raman_spectra.csv`, `raman_peaks.csv`), an X-ray diffraction scan (`xrd_20958.csv`, sapphire substrate), and an SEM image of MoS2 triangles with its measured scale (`sem_32096.png`, `sem_32096.json`). |
| `grains/` | Island ("grain") maps and measurements for notebook 06: three spots on one WSe2 wafer (sample 17458), a seed-stage sample (17464), and two scans for line profiles (24111, 39166). `grains.csv` has one row per detected grain; `scans.json` describes each scan. |
| `camel_data/` | Small Python helpers the notebooks import. |
| `manifest.json` | Every file with its size and SHA-256 checksum. |

## How heights were processed

AFM files were read from the instrument's raw format and converted to nanometres. Each scan line was
then levelled with a straight-line fit (the instrument software's standard first-order "Flatten"
step), and heights were shifted so the median is 0. Roughness numbers in `afm_summary.csv` come from
that levelled surface. Levelling every line can slightly shrink tall features that fill much of a
line, so treat roughness as a consistent comparison measure, not an absolute truth.

## Which scan represents each sample

Most samples have several AFM scans (centre, edge, different sizes). `afm_summary.csv` keeps one per
sample, chosen by a fixed rule: skip files an operator marked "modified", then take the largest scan
size written in the file name, breaking ties by the shortest name. This is a consistent rule, not a
scientist's pick of the best scan. Roughness depends on scan size, so compare samples with the same
`scan_size_um` when it matters. `lines` smaller than `pixels` means the scan stopped early.

## How grains were found

Each grain scan is levelled line by line using only its low (substrate) pixels. A pixel counts as
"island" when it is higher than half the typical island height (the median of pixels clearly above
the substrate noise). Each connected blob is one grain. Blobs are labelled `single`, `merged`
(touching islands joined together), `dust` (far taller than the islands), or `streak` (a thin scan
glitch); grains touching the scan border or a glitch line are flagged. This is a simple height
rule, not a scientist's hand count; the notebook draws the outlines so it can be checked by eye.
The rule is only used where islands are clearly separated; the line-profile scans have no grain table.

## Growth recipes: what blanks mean

A blank duration, temperature, or pressure means it was not recorded — never zero. After a step with
no duration, later `start_min` values are blank because the elapsed time is unknown.
`growth_summary.csv` summarises each sample's first recipe only (`n_recipes` counts how many exist);
`durations_complete` is true when every step has a duration.

## Citing

Each sample row lists its 2DCC data package and DOI. Please cite the DOI when you use a sample, and
cite the 2DCC-MIP (NSF DMR-2039351). Data are shared under CC-BY-4.0.
