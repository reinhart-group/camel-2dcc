# Teacher guide — How Bumpy Is It? Mean, Median, and Samples

**Standards:** S.ID.1–3 (mean, median, range, shape of distributions), 7.SP review (random
samples vs. the whole group).

**Time:** 30–40 minutes.

**Note:** the words "standard deviation," "RMS," and "sampling distribution" are intentionally
absent from the student text (kept as mean/median/range/spread only). You may introduce those
terms verbally for advanced students — the *Explorer* edition (`02_how_smooth_is_smooth.py`,
`06_counting_crystals.py`) covers them in depth.

## Goals
Students compute mean, median, and range by hand; compare two real surfaces visually and
statistically; see how one outlier pulls the mean but not the median; and compare random
samples of different sizes to the whole group's average, including a one-spot ("lazy
scientist") sample.

**On the 501 triangles:** these are every triangle a simple computer rule kept in three small
2 µm × 2 µm scanned patches of one wafer — not the whole wafer. The notebook calls them "all
the triangles we measured" and their average the "whole group's average," never the wafer's
true mean, and it tells students the green outlines are blobs that *passed the computer's
checks*, not confirmed triangles. Task 5's edge comparison is framed as a question ("could a
one-spot answer miss the whole group?"), not a proven bias — it's a single scan.

## Answers (from the executed notebook)
- **Task 1** (heights = 8, 10, 12, 9, 11): mean = 10, median = 10, range = 4.
- **Task 2:** the mounded surface (material name hidden from students) has a visibly wider
  histogram (heights more spread out) than the flat surface — it's the bumpier one.
- **Task 3** (add a 90 nm dust speck): mean jumps from 10 to about 23.3 nm (+13.3); median
  moves only from 10 to 10.5 nm (+0.5). The mean is pulled hard toward the outlier; the
  median barely moves.
- **Task 4:** whole group (501 triangles, all three scanned patches) mean area ≈ 1,889 nm².
  Sample means vary run to run and shrink toward the whole-group mean as `sample_size` grows
  (seeds 1–5): n=10 lands about −0.7% to +19.5% off (means ≈1,875–2,257 nm²); n=80 lands
  about −5.4% to +10.0% off (means ≈1,788–2,077 nm²) — a visibly tighter spread.
- **Task 5:** the one "near the edge" scan mean ≈ 2,818 nm², about **+49%** above the whole
  group's average — worth discussing as a *possible* one-spot problem, not a proven bias
  (we only have one edge scan).
- **Exit ticket:**
  1. Mean (4,5,5,6,30) = 10, median = 5 — mean is bigger; the 30 drags it up.
  2. Pick the 10 triangles at random (e.g., number them all and draw 10 numbers), not just
     the easiest-to-reach ones.
  3. No — same median doesn't guarantee the same shape or spread; compare histograms/range
     too.

## Common mistakes
1. **Confusing mean and median formulas.** Some students average the min/max instead of
   sorting for the median. Have them physically write the sorted list first.
2. **Thinking the outlier "doesn't count."** Some students want to drop the dust speck before
   computing anything — that's a real modeling decision scientists make, but here the point is
   to *see* its effect first, so make sure they compute both mean and median *with* it in Task 3.
3. **Random sample = perfectly matches the whole group.** Students may expect their n=10
   sample mean to equal the whole group's mean exactly. Task 4 asks them to compare several
   seeds at n=10 *and* n=80 precisely to show natural sample-to-sample variation and that
   bigger samples tend (not guaranteed) to land closer — a single sample is an estimate, not a
   guarantee.

## If you have 10 more minutes
- Have students try `sample_size = 200` and discuss whether the sample mean lands closer to
  the whole-group mean even more often.
- Revisit Task 5: ask "would scanning *more* triangles near this same edge spot settle the
  question?" (No — it's still one location; we'd need scans from several different edge spots
  to know whether edges really run bigger.)
