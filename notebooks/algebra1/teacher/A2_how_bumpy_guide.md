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
statistically; see how one outlier pulls the mean but not the median; and compare a random
sample's average to the whole group's average, including a biased ("lazy scientist") sample.

## Answers (from the executed notebook)
- **Task 1** (heights = 8, 10, 12, 9, 11): mean = 10, median = 10, range = 4.
- **Task 2:** `gallium_selenide_bumps` has a visibly wider histogram (heights more spread
  out) than `smoothest_surface` — it's the bumpier surface.
- **Task 3** (add a 90 nm dust speck): mean jumps from 10 to about 23.3 nm (+13.3); median
  moves only from 10 to 10.5 nm (+0.5). The mean is pulled hard toward the outlier; the
  median barely moves.
- **Task 4:** whole group (501 triangles, all three scanned spots) mean area ≈ 1,889 nm².
  A random sample of 10 varies run to run — typically landing within roughly ±30% of the
  whole-group mean (e.g., seeds 1–5 give sample means from about 1,875 to 2,257 nm²).
- **Task 5:** "near the edge" only mean ≈ 2,818 nm², about **+49%** above the whole group's
  true mean — a *consistent* bias, not random scatter.
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
   sample mean to equal the whole group's mean exactly. Task 4 asks for 3+ seeds precisely to
   show natural sample-to-sample variation — a single sample is an estimate, not a guarantee.

## If you have 10 more minutes
- Have students try `random_sample(whole_group, 50, seed=...)` (larger n) instead of 10 and
  discuss whether the sample mean lands closer to the whole-group mean more often.
- Revisit Task 5: ask "would scanning *more* triangles near the edge fix the problem?" (No —
  it's biased, not random; more edge-only data just repeats the same bias more precisely.)
