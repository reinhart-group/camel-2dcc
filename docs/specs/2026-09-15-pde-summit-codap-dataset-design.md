# PDE Data Literacy Summit: dataset and materials for "Modeling the Messy"

Design for what the CAMEL 2DCC side owes Kathy Hill's Breakout 1 session at the Pennsylvania
Department of Education Data Literacy Summit. Written 2026-09-15.

## Context

Kathy's deck (`Modeling_the_Messy_Breakout1.pptx`, received 2026-09-15) already fixes the session
design. Our job is to supply the dataset and supporting materials, not to design the activity or
the tool.

- 70 minutes: 5 min warm-up, 15 min framing, 35 min hands-on, 15 min reflect and Q&A.
- Audience: PDE staff, K-12 teachers, curriculum coordinators, administrators, IU staff. Teams of
  3-4. Devices may be iPads.
- Tool: CODAP (`codap.concord.org`), free, browser-based, no account. Slide 14.
- Four rounds: notice and wonder (5 min), find the mess (10 min), model it (12 min), turn the
  dials (8 min). Slide 16.
- Two datasets offered: A is Wangda Zuo's cooling data, B is ours ("Growing tiny crystals").
- Kathy's three complexity dials (slide 12): structural (how many variables), provenance (whether
  missing values and anomalies are surfaced or resolved), statistical (whether noise is made
  explicit).
- Two placeholders in the deck are ours to fill: the dataset link or QR code on slide 14, and the
  Dataset B card on slide 15 ("Confirm the final variable lists with Rebecca before the session").

The deck's Dataset B card was drafted before anyone saw our files. It promises "growth sequence,
element ratio, and measured grain area for each sample". We have grain measurements for two
samples only, so the card is rewritten to match the data we actually have. Kathy edits the slide.

## Decisions

1. **CODAP is the floor; Colab is the ceiling.** Teams do all four rounds in CODAP, which needs no
   account. CODAP's FAQ says tablet support is still in progress, so "works on any device" is a
   claim to test, not to promise, and the fallback is a preloaded CODAP document or a laptop per
   table. A parallel Colab notebook serves teachers who want code and
   supports Kathy's slide 14 line about where high school goes next. The session does not depend
   on it.
2. **We do not build a web tool for this summit.** A purpose-built dial widget would beat CODAP on
   our dataset and lose on everything a teacher does next week with their own data. If CAMEL later
   wants dials and reasoning telemetry inside the tool, the path is a CODAP plugin, not a
   competing application. That is a separate project and needs its own feasibility check.
3. **The outcome variable is surface roughness, not grain area.** Roughness exists for 899 of the
   1,005 grown samples; grain areas exist for 2. The investigative question becomes: how do the
   recorded recipe settings relate to the one roughness measurement kept per sample? That is an
   association question about observational records, not a test of whether a recipe produces
   quality, and the file summarizes only each sample's first recipe.
4. **The mess is real and stays in.** No synthetic errors are added. Every messy feature listed
   below was verified in the files on 2026-09-15.

## What the device test changed (2026-09-15, evening)

A notebook of ten labelled probes (`notebooks/mobile_js_test.ipynb`, branch `mobile-js-test`) was
opened on a phone in Safari, in a private window, with no Google session and no runtime attached.
Saved HTML and JavaScript outputs render **and respond**: tap handlers, a slider filtering 740 rows
carried inside the page, a library loaded from a CDN, touch drawing on a canvas, and an external
page in an iframe. What fails is anything that needs Python: `ipywidgets` is dead, a Colab form cell
renders and accepts taps but never updates, and a Plotly figure shown with `fig.show()` saves a mime
bundle that displays as nothing.

So the no-account constraint no longer forces CODAP. A published notebook can be an interactive page
for anyone who opens the link and a Python environment for anyone who signs in. Decision 2 below
stands for the summit, but it is now a choice about what serves teachers afterwards, not a technical
limit.

Consequence for this repo: shipping a notebook that a phone can read means shipping it **with
outputs executed**. The tracked notebooks currently carry none, so a reader who does not run them
sees only text. `camel_data.classroom.surface_3d` now returns a wrapper whose `.show()` writes
self-contained HTML, so an executed copy stays interactive for a reader without a kernel.

That fix is not live yet, and the reason is worth recording: the notebooks do not import
`src/camel_data`. They import the copy of it that ships inside the data slice, which the setup cell
downloads from SharePoint. Trying to call the new helper from a notebook fails with
`NameError: name 'show' is not defined`, because the deployed copy predates it. Making the fix
reach a classroom takes three steps: rebuild `data/slice/` so `camel_data/` is refreshed, rebuild
`camel-2dcc-v1.zip`, and re-upload that zip to the SharePoint link the notebooks point at. Until
then, notebook sources must keep calling `fig.show()`.

## Verified data facts

From `data/slice/camel-2dcc/` (`growth_summary.csv` joined to `samples.csv` and `afm_summary.csv`):

| Feature | Count | Dial |
|---|---|---|
| Grown samples (rows) | 1,005 | - |
| Rows with both growth time and roughness | 754 | provenance |
| Missing growth time / temperature / pressure | 228 / 295 / 238 | provenance |
| Missing roughness (sample never AFM-scanned) | 106 | provenance |
| Missing DOI | 480 | provenance |
| Distinct material spellings (nonblank, grown samples) | 35 | provenance |
| Material values containing ";" (e.g. `MoS2; MoS2`, `MoS2; 0`) | 39 | provenance |
| Material field equal to the substrate (e.g. `Al2O3`) | 5 | provenance |
| Scans that stopped early (lines < pixels), grown samples | 112 | provenance |
| Roughness range (nm) | 0.10 to 92.03 | statistical |
| Samples rougher than 10 nm | 21 | statistical |
| Distinct scan sizes among grown samples, 709 of them at the common 5 um | 17 values | statistical |
| Usable columns after the join | 19 | structural |
| Spearman correlation, growth time vs roughness (754 rows) | +0.29 | model |
| Same correlation within WS2 (133 rows) | -0.11 | model |
| Growth methods: MOCVD / Hybrid MBE | 772 / 233 | model |
| Hybrid MBE rows keeping both time and roughness | 14 of 233 | provenance |

The last two rows are the strongest round-3 finding available: requiring both values to be
recorded silently removes almost one entire growth method.

## Deliverables

### D1. `crystal_growth.csv` - the full messy file

One row per grown sample, 1,005 rows, 19 columns, every value as recorded. This is a classroom
subset of the join, not every source field: `measurements`, `date_created`, `durations_complete`,
`n_growth_steps`, `n_recipes` and the instrument fields are left out, and the file ships with a
field dictionary saying so. Columns:
`sample_id`, `sample_label`, `material`, `substrate`, `growth_method`, `n_steps`,
`total_recipe_min`, `growth_time_min`, `growth_temperature_C`, `growth_pressure_torr`,
`rms_roughness_nm`, `avg_roughness_nm`, `height_range_nm`, `scan_size_um`, `pixels`, `lines`,
`growth_date`, `data_package`, `doi`. Missing values stay blank. Nothing is renamed to hide its
origin.

### D2. Dial variants

Four files, one per grade band, mirroring the table on slide 17 so Kathy can copy its layout for
Dataset B.

| File | Rows | Columns | Structural | Provenance | Statistical |
|---|---|---|---|---|---|
| `crystals_k2.csv` | ~24 | 2 | one variable | resolved | implicit |
| `crystals_35.csv` | ~60 | 3 | few | resolved | implicit |
| `crystals_68.csv` | ~300 | 6 | some | one issue surfaced | discussed |
| `crystals_912.csv` | 1,005 | 19 | all | nothing resolved | explicit |

Concretely:
- **Resolved** means material spellings normalized, rows whose material is really a substrate
  removed, rows missing the columns the task needs removed, and one scan size (5 um) kept.
- **Surfaced** means those rows stay and the student meets them.
- **Implicit** means outliers above 10 nm are gone and scan size is constant, so the spread is
  narrow. **Explicit** means all values stay and `scan_size_um` is present so the class can reason
  about why a comparison across scan sizes is unfair.
- The K-2 file is a hand-checked 24-row extract with a crystal name and a smooth/bumpy label, for
  a picture graph. Young students can unhide columns in CODAP, which is why it is a separate file.

Counts along the resolved path, in the order the rules apply: 665 rows have growth time, roughness,
and a 5 um scan; removing the 2 rows whose material equals its substrate leaves 663; keeping only
roughness under 10 nm leaves 650. Of those, 314 read exactly `MoS2` before spellings are
normalized. Each variant ships with one deterministic rule list, its exact column list, its
expected row count, and a checksum, so the file can be rebuilt and checked.

### D3. `crystals_one_wafer.csv` - optional zoom-in

501 crystal candidates the detector kept whole from three 2 um fields on one WSe2 wafer
(sample 17458): of 643 detected blobs, those labelled `single` that touch neither the scan border
nor a glitch line. Columns give area, side length, height, the spot, and the detector flags. These
are automated measurements from three fields, not a census of the crystals on the wafer. Median area is 1,526 nm2 at the center and 2,792 nm2 toward
the edge. Offered to teams that finish early or want to see crystals rather than summary rows.

### D4. Dataset card and facilitator crib

- Replacement text for the slide 15 Dataset B card: the question, what is in the file, and what to
  watch for, all matching D1.
- A crib sheet for Kathy and any helpers: what teams typically find in round 2, what a defensible
  round 3 model looks like, the three findings above, and the claims we must not make.

### D5. Link and QR for slide 14

Files published in the public GitHub repo so a raw link needs no account, plus a QR image. CODAP
imports a CSV by drag-and-drop or from a URL; the QR should point at a short landing page listing
the files rather than at one raw CSV, so teams can pick their grade band.

### D6. Colab dial notebook

One notebook whose first cell is three form dropdowns, `structural`, `provenance`, `statistical`,
matching Kathy's dial names. Running it rebuilds the dataframe from `crystal_growth.csv` and
redraws one graph, so the audience sees that the data never changed and only the entry point did.
Uses the form-cell pattern already in `notebooks/algebra1/`. Includes one step that asks an AI
assistant to modify a cell, then asks whether its cleaning choice was defensible.

## Two cautions for the crib sheet

CODAP's correlation is Pearson, so the Spearman values above are facilitator and Colab numbers, not
something a team reproduces by dragging. The crib gives the least-squares line and R squared a team
will actually see.

A graph of growth time against roughness uses the 754 rows that have both, so 251 rows leave the
picture without saying so. Every graph instruction names its denominator.

## Claims we must not make

Nothing in these files shows that 2DCC materials are on a commercial AI-chip roadmap, that these
samples became chips, or that smoother films make better devices. The honest framing is that 2D
materials are researched as candidates for future electronics, and that roughness is one quality
measurement among many. Correlations in this observational, unbalanced dataset are associations,
never causes.

## Build order

Codex reviewed this spec on 2026-09-15 and recommended cutting scope until the core is tested.
First: D1, the 9-12 variant, D4, and D5, each verified in CODAP. The 6-8 variant follows if Kathy
wants it. The K-2 and 3-5 files, D3, and the Colab notebook wait until the core passes. The K-2
file also needs a written rule for its smooth-or-bumpy label and its 24 rows, which does not exist
yet, and a two-column file has nothing for a student to unhide.

## Non-goals

- A CAMEL-built web tool for this summit.
- Grain measurements for more than the two wafers already processed.
- The Moore's law and transistor-count material, which is not our data.

## Open questions for Kathy

1. The date of the summit, and her deadline for the deck.
2. Approval to rewrite the Dataset B card, since the drafted variable list does not match our data.
3. Whether attendees can sign in to Google, which decides how prominent the Colab track can be.
4. Whether she wants the K-2 and 3-5 files at all, given that her session is billed as high school.

## Testing

- Import every file into CODAP in a browser and on a real iPad, and record the result as a device
  and browser matrix rather than a guarantee. CODAP's own FAQ says tablet support is still in
  progress, so the iPad path is the risk to test first: the file picker, whether a URL import works
  in Safari, and how 1,005 rows respond. Keep a fallback ready, such as a CODAP document with the
  data already loaded, or facilitator laptops at each table.
- Check that blank cells stay blank rather than reading as zero, and that `growth_date` is
  recognized as a date.
- Check file sizes: the full file should stay comfortably under a megabyte.
- Execute the Colab notebook headlessly with `scripts/run_notebook.py`, then once in real Colab.
- Have one person outside the project follow the round-by-round crib with only the files and the
  slides.
