# Menu review, round 1 (operator feedback 2026-09-16)

The operator reviewed the warmup and "find the mess" notebooks item by item. This records what
they said, the confirmed cause of each problem, and the fix. It also records an audit of the two
notebooks they have not reviewed yet, so the same classes of problem get fixed before they see
them.

## The standard to build to

The operator's stated principle, which now governs every item:

> "the best exercises are the interactive ones that result in obvious changes to a chart or table"

Every item should have at least one control whose movement produces a visible change in a chart,
and the readout should name what changed and out of how many rows.

## Fixed: axis limits everywhere (the operator's main complaint)

The operator reported this on W-02, W-05, M-08, M-09 and M-10, and said "yes that is a problem
throughout, the roughness really doesn't have any values above ~30 but the limit of 80 makes the
charts ugly."

Confirmed cause. Roughness is extremely right-skewed: of 894 samples with a roughness on record,
the median is 0.75 nm and the 98th percentile is 10.9 nm, but the maximum is 92.0 nm. Only four
samples measure above 30 nm. Auto-scaling to the full extent therefore spent most of the axis on
empty space.

Fix, in `courseware/widgets/core.js`, so it lands on every chart at once. A new `autoDomain`
helper stops the axis at a round number near the 98th percentile whenever the maximum is more
than 1.5 times that percentile, and reports how many samples fall beyond. Nothing is hidden:

- `hist` draws the off-scale samples as their own grey bar past the limit, labelled "15+".
- `scatter` pins off-scale points to the edge and draws them hollow and dashed, so they never read
  as a real position.
- `box` clamps its dots and whiskers to the limit.
- Every clipped chart carries a caption naming the count, for example "12 of 894 samples measure
  above 15 and are drawn at the edge".
- `line` is never clipped, because a trace's shape is the content.

What the rule chooses on real data, and why it is safe:

| variable | n | max | axis stops at | off-scale |
|---|---|---|---|---|
| roughness (nm) | 894 | 92.0 | 15 | 12 |
| growth time (min) | 775 | 90 | 40 | 9 |
| scan size (µm) | 894 | 70 | 10 | 10 |
| grain area (nm²) | 501 | 7217 | 5000 | 5 |
| resistance (ohm) | 183 | 1705 | not clipped | 0 |
| temperature (K) | 183 | 299 | not clipped | 0 |

The rule fires only on skewed variables and leaves the superconductor transport curve alone, which
is the case that would have been ruined by a blanket clip.

The axis stops at 15 nm rather than the 30 the operator suggested. 30 still leaves 75% of samples
in the first bar; 15 shows 98.7% of them with visible structure. The number is derived from the
data rather than chosen, so it adapts per chart.

Also added `CAMEL.bars`, a categorical bar chart with an optional pale "total" bar behind each
value, so "kept out of total" reads as one shape. It exists to give the table-only items a chart
that moves.

## Fixed: individual items

- **W-01, the image was very low resolution and had no explanation.** The 512×512 source array was
  downsampled to 96 pixels, rendered small, then re-encoded as JPEG at quality 78. Now rendered
  from the full-resolution source as a PNG with a scale bar in micrometres and a colourbar labelled
  in nanometres.
- **W-03, the line was flat at 1000 from 0 to 40.** The recipe table's temperature column holds the
  *target* temperature for each step, not a measurement. Sample 23451 records 1000 for every step,
  including the one named "Ramp up T", so the flat line was the data. The reveal text claimed a
  17-minute ramp that does not exist; I had invented it from the step name. The item now uses
  sample 17403, which holds 850 for five steps, steps up to 1000, then records 0 for both cooldown
  steps. The zero is the lesson: it is a placeholder, not a temperature.
- **M-02, buttons did not show their state.** The requirement buttons are now filled when on and
  outlined when off, and a bar chart of rows surviving per group redraws on every toggle.
- **M-05, "some are clearly 2 categories not just 1".** The item fed all 35 raw spellings to a list
  of single-material buckets, but 13 of those spellings name two materials separated by a
  semicolon, so the task was self-contradictory. M-05 now covers only the 22 single-token
  spellings; the semicolon rows belong to M-07.
- **M-06, "only 3 entries".** The filter looked for `Al2O3`, `GaAs`, `0` and `Se`, but a bare `0`
  never appears as a material value; it occurs only inside `MoS2; 0`. Its note also claimed seven
  rows across four entries, where the truth is six rows across three. The item is removed and its
  lesson folded into M-05 as a "not a crystal" bucket.
- **M-12, "not interactive and it's sort of silly that the dropdown includes specific numbers".**
  The reason string embedded each row's line counts, producing 14 distinct reasons and a dropdown
  full of numbers. Reasons are now generic, the numbers live in sortable columns, the filter only
  appears when there are few reasons, and marking a row "remove" now redraws a chart so the reader
  watches their own cleaning decisions move the median.

## Audit of the model and dials notebooks, before review

Three problems of the same kinds are already present and confirmed against the data.

**G-03, G-04 and G-05 fit a line through a handful of discrete values.** Growth temperature has
13 distinct values across 710 rows, and the two commonest account for 87% of them. Chamber
pressure has 8 distinct values across 767 rows, with 90% in the top two. A scatter plot of either
against roughness is a set of vertical stripes, and a least-squares line through it invites a
conclusion the data cannot support. Growth time is fine by contrast: 47 distinct values with only
28% in the top two, so G-01 and G-02 stand. Recommendation: rebuild G-03, G-04 and G-05 as box
plots by level, which is the honest display for a discrete predictor and still interactive.

**G-09 plots another flat recipe.** Recipe 17458 records a single temperature, 850, for all six
steps, with two steps blank. It is the same failure as W-03. Recipe 69173, used by G-10, holds six
distinct temperatures and is fine. Recommendation: pick a different MOCVD recipe with real shape,
or reframe G-09 the way W-03 was reframed.

**G-12 asks the reader to measure a staircase that the processed data no longer contains.** The
`atomic_staircase` scan was processed with a per-line linear flatten and each line's median set to
zero, which removes exactly the height differences between terraces. The array now spans 0.89 nm
between its 0.5th and 99.5th percentiles, less than one 0.39 nm terrace step, and its height
histogram is a single unimodal blob. Averaging 64 rows does not recover the steps. Recommendation:
use `terraced_triangles` (InSe) instead, whose height histogram has seven distinct levels over
6.7 nm and whose averaged line profile spans 3.9 nm. Do not assert a fixed layer height for it —
the observed level spacings are uneven, clustering near 0.27 nm and 0.95 nm.

G-13 is unaffected: `triangle_pyramids` spans 6.0 nm with a 4.9 nm line profile.

G-12 and G-13 also share W-01's downsampling: `heightmap_profile` is called with `size=96`.

## Still open

The dials notebook (D-01 to D-06) has not been audited item by item.

## Added while verifying the fixes

**W-01's glitch is the strongest provenance lesson in the catalog, and the item was wasting it.**
The scan's recorded roughness is 6.10 nm. Exactly one scan line out of 512 is corrupted, dipping
to −455 nm, and it is plainly visible in the rebuilt image. Drop that one line and the roughness is
0.80 nm, so a single bad line inflates the headline number by a factor of 7.6. The colourbar
independently shows the crystals are only about 2 nm tall, which is what makes the artifact
obvious. W-01's reveal now says this. It also gives M-11, which asks which extreme roughness
readings to trust, a worked answer.

**M-11 and M-13 now chart the whole dataset, not just the flagged rows.** Marking rows "remove"
originally moved only the median of the flagged subset, which barely budges. The items now carry
the roughness of all 828 unflagged samples alongside the flagged ones, so the chart and readout
show what the reader's removals do to all 894 measured samples. Removing all 66 extreme rows moves
the mean from 1.829 to 1.014 nm while the median only moves from 0.743 to 0.661 — the mean is
sensitive to outliers and the median is not, which is exactly the lesson, and now it is visible
rather than asserted.

## Verification of this round

- `scripts/build_catalog.py` succeeds: warmup 326 KB (8 items), mess 560 KB (12), model 724 KB
  (16), dials 554 KB (6); 42 items, 2.1 MB total.
- `pytest -q`: 56 passed.
- Every item JS file parses under `node --check`, and none contains `fetch`, `XMLHttpRequest` or
  `<script src`.
- 17 assertions on the new axis code pass against the real arrays, including that a histogram's
  bars plus its overflow bar still account for all 894 samples.
- The M-11 widget was executed headlessly against its real payload: it reports mean 1.829 and
  median 0.743 across 894 samples, matching the same figures computed independently in Python, and
  its payload carries 66 flagged rows plus 828 background values.
- Counts re-verified from the data, not taken from the subagents' reports: 42 items with M-06 gone;
  M-05 covers 22 spellings over 951 rows; M-07 covers 13 spellings over 39 rows; 15 rows have a
  blank material field and appear in neither; the non-crystal entries Al2O3, GaAs and Se account
  for 6 rows, not the 7 the old note claimed; M-11 66 rows, M-12 110, M-13 174.

## Round 2 of operator review

- **W-01's image** was rendered from a 96-pixel downsample and palette-quantised to 64 colours,
  which banded a continuous colour map. The operator saw both faults: "weird color effect in the
  reproduction; low resolution still."
- **M-01 needed its outliers back.** The automatic axis clipping suits the warmup histograms but
  works against a group comparison where the spread is the point. It now defaults to the full range
  and offers a zoomed view, stating in both cases how many samples sit off the chart.
- **M-05 required chemistry nobody in the room has.** "i guarantee high school math teachers won't
  know what FeTe is or that Al2O3 is a substrate." It now sorts by the *kind of problem a label
  has* rather than by which chemical it names, every spelling carries a plain-English gloss, and
  the cleanup script's choices appear as a mapping table with the reader's disagreements marked
  rather than as three sentences of prose.
- **M-08, M-09 and M-10** promised changes the data does not deliver. Controlling for scan size
  barely moves the material ranking, and the one material that does move, In2Se3, moves because
  its sample collapses from 32 rows to 2. The MOCVD versus hybrid MBE gap survives every scan size
  that has enough samples to check. M-10 had no control at all. All three were rebuilt around what
  the numbers actually show.
- **G-06, G-07 and G-08 were broken.** The sample-size slider fired on every drag tick and the draw
  function cleared the accumulated sample means each time, so the histogram could never hold more
  than one bar. Changing n now redraws a batch of 300 sample means at once, and the horizontal axis
  is pinned so raising n visibly narrows the distribution instead of an auto-scaling axis hiding
  it. Observed spreads track the standard errors: 592, 470, 315, 219, 154 and 122 nm² at n of 3, 5,
  10, 20, 40 and 60, against a theoretical 592, 458, 324, 229, 162 and 132.
- **G-09 plotted another setpoint table.** Recipe 17458 records 850 °C for all six steps. It now
  uses sample 28363, an MOCVD MoS2 growth whose eleven steps run 800 → 850 → 950 with both
  cooldowns recorded as 0.
- **G-12 measured a staircase that processing had removed**, and its drag line was nearly the same
  colour as the heat map beneath it. It now uses the InSe `terraced_triangles` scan, whose height
  histogram has seven distinct levels over 6.7 nm, and the drag line is a black and white striped
  bar with arrowheads, so the cue survives desaturation on a projector.
- **The K-2 and grades 3-5 dial variants are gone.** The operator: "are you seriously suggesting
  1st graders are looking at 2D material nanometer scale roughness measurements?" They are right,
  and Kathy's own email puts this session at the high-school level, so the bands were outside the
  brief as well as implausible. Grade labels of "3-8" and "3-12" elsewhere were corrected to
  "6-12". The menu is 40 items.
- **D-01 is the one the operator called excellent**, and it is the model the rest should follow.

## Two defects in how the notebooks are delivered

**The code cells do not run.** Every catalog cell contains a single comment,
`# M-01: the working version is saved below.` Connecting a runtime and pressing run does nothing.
The saved-output floor works exactly as designed, but the "Colab ceiling" — a teacher signing in to
see how the thing was built — was never built. Making it real means packaging the item definitions
so a cell can rebuild its own widget, or writing each cell as the underlying analysis in plain
pandas. That decision is still open.

**Helper code shipped inside the data zip.** The notebooks imported `camel_data` from the 31 MB
slice rather than from `src/`, so a fix to `src/camel_data/classroom.py` could not reach any reader
until someone re-uploaded that zip by hand, and notebooks silently ran the stale copy. `pyproject`
now declares a build backend and src layout, so a runtime installs the helper code from the public
repo and the zip carries data only. Verified by installing into a clean virtualenv.

## A process failure worth recording

Commit `a5627ae`, whose message describes only the plotly fix, actually contains thirteen files of
three subagents' in-progress work. The cause was a blanket `git add -A` run in a working tree
shared with running agents. Anyone reverting that commit expecting a plotly-only change would also
delete the M-01, M-05, M-08, M-09, M-10, G-06, G-07, G-08 and G-12 rebuilds. The content is
verified and correct; only the message is wrong. Do not use blanket staging while agents share the
tree.
