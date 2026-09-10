# CAMEL × 2DCC: public data route, classroom data slice, and HS math Colab demos

Date: 2026-09-10. Owner: Wes Reinhart (for Becca Napolitano, CAMEL PI, NSF 2621173).

## Goal

Give Grades 9–12 math classes (typical Algebra 1/2, Geometry, intro Statistics — not AP) a set of
Google Colab notebooks built on real, published 2D-materials data from the 2DCC-MIP LiST database,
with AFM (atomic force microscopy) as the centerpiece. Owed to Becca today (action item 2026-09-10):
sample AFMs, a Colab Plotly 3D rendering, and a 3D-printable model.

## What we learned (evidence)

- **LiST public key works.** `X-API-KEY` header against `https://m4-2dcc.vmhost.psu.edu/list/api/v2`
  sees 1,413 samples, all `Published`. AFM is on 1,068 of them; MoS2 (452), WSe2 (257), WS2 (203)
  dominate; MOCVD (775) and hybrid MBE (246) are the main growth methods. Samples link to citable
  data packages with DOIs (`10.26207/...`).
- **LiST is Penn State-network-gated.** Colab VMs cannot reach it. So students get a pre-built slice.
- **AFM raw files are Bruker Nanoscope `.spm`.** Our reader (`src/camel_data/spm.py`) converts them to
  nanometres and matches the instrument's own number: 0.358 nm RMS roughness vs. 0.36 nm in the file
  name (sample 24906, SnTe).
- **MBE samples carry recipe tables** (step durations, pressure, substrate and source temperatures).
- **Existing CAMEL figure** (`afm-stats.pdf`): SnSe grain-area box plots by deposition order and Se:Sn
  ratio — a ready-made statistics story.

## Architecture

```
LiST (PSU network, public key)                      Google Colab (student)
   │  scripts/*.py (runs on Wes's Mac / VPN)            ▲
   ▼                                                    │ requests.get(SHARE_URL + download=1)
data/slice/  ──copy──►  OneDrive: Funding/Awarded/2026-03-CAMEL/CAMEL-2DCC-data/  ──"Anyone" link──┘
```

1. **Public-data route** — `camel_data.list_public.PublicLiST`: small `requests` client. Key comes from
   the `LIST_API_KEY` env var (repo `.env`, git-ignored) or a Colab Secret; never hard-coded. Friendly
   errors for off-network and bad-key cases. Teachers on campus/VPN can use it directly; a teacher
   notebook demonstrates it.
2. **Slice builder** — `scripts/` stages, each resumable and writing to disk:
   index AFM files → download one primary height scan per sample → compute stats → write slice.
3. **Classroom data slice** (`camel-2dcc-v1`), one zip plus loose files:
   - `samples.csv` — the full public catalog, one row per sample (material, substrate, growth method,
     techniques, date, data package, DOI). Messy on purpose: blanks, duplicates of material spellings.
   - `afm_summary.csv` — one row per AFM scan: sample, material, growth method, scan size, pixels,
     RMS roughness, average roughness, height range, date. Real noise and missing values retained.
   - `afm_gallery/*.npz` — ~15 curated full-resolution height maps (nm, float32) with metadata:
     atomic terraces on sapphire, MoS2/WSe2/WS2 films, SnSe grains, a superconductor (FeSe), a
     topological insulator (Bi2Se3), In2Se3. Chosen for visual drama and a clear math story.
   - `afm_small/*.npz` — every AFM scan downsampled to 64×64, for "compare many" activities.
   - `mbe_recipes.csv` — flattened MBE growth steps where available.
   - `manifest.json` — file list, sizes, SHA-256, data-package DOIs, build date, licence/citation.
   - `stl/*.stl` — two print-ready AFM surfaces.
4. **Colab notebooks** (`notebooks/`), one class period each, sliders and fill-in-a-number cells, a
   single "setup" cell that downloads the slice from the SharePoint link. Teacher answer keys.
5. **Helper module** `camel_data` shipped inside the zip, so notebook cells stay short.

## Notebook lineup (draft; refined with Codex brainstorm)

| # | Title | Math | Data | Wow moment |
|---|-------|------|------|-----------|
| 1 | Flying Over Flatland | Geometry: scale, ratios, cross-sections | AFM gallery | Plotly 3D surface with material dropdown and height-exaggeration slider; export an STL to 3D-print |
| 2 | How Smooth Is Smooth? | Statistics: histograms, mean/median, SD = RMS roughness, outliers | gallery + `afm_summary.csv` | A dust speck flips the mean but not the median |
| 3 | Stacking Atoms | Algebra: linear functions, unit conversion, scientific notation, hexagon area | gallery step heights, MoS2 layer 0.65 nm | Count atomic layers from a step height; how many atoms fit on a fingernail |
| 4 | Chips for AI | Exponential functions, inverse relationships | curated table + catalog | Moore's law, 2D-material transistors, light colour from band gap (λ = 1240/E), superconductors and data-centre energy |
| 5 | Messy Data Detective | Statistics: comparing groups, scatter plots, line of best fit, missing data | `samples.csv`, `afm_summary.csv`, recipes | MOCVD vs MBE roughness; does hotter growth mean smoother films? |
| 0 | Teacher: live LiST access | — | LiST via public key | Pull a fresh record yourself (PSU network) |

## Error handling

- Build scripts record every failed sample/file to an errors JSON with the exception; nothing is
  silently dropped. Downloads retry nothing blindly; files LiST 500s on are logged and skipped.
- Notebooks: if the download fails, the setup cell prints the URL it tried and how to fix it.

## Testing

- Unit tests for the `.spm` reader against the 0.36 nm reference file and for slice loaders.
- Execute every notebook headlessly with `nbclient` locally, then in a real Colab VM with the Colab CLI
  (`colab new` → upload → run → `colab stop`).
- Codex reviews code and notebooks; findings are verified before being applied.

## Open items for Wes (non-blocking)

- Create one "Anyone with the link can view" share on the OneDrive folder or zip (PSU tenant may
  restrict this; fallback is a Penn State–only link or a GitHub release).
- Confirm licence text for the slice (2DCC data packages are published; default CC-BY-4.0 citation).
