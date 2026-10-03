# Final red-team review: outlier lesson and “Modeling the Messy”

Reviewed as a skeptical grades 9–12 mathematics teacher and statistician.

Sources checked:

- `/private/tmp/student-demo.html`
- `docs/summit/outlier-lesson-outline.md` (revision 2)
- `docs/summit/outlier-lesson-redteam.md`
- `/private/tmp/investigation.html`
- `docs/summit/modeling-the-messy-polish.md`
- `docs/summit/facilitator-crib.md`
- WebKit screenshots in `/private/tmp/review-shots/` at 1280 px and 390 px

## Bottom line

I found no blocker. The outlier lesson’s displayed statistics match the revision 2 table, and its central statistical argument is sound. Its main alignment weakness is claiming Mathematical Practice 3 without requiring students to construct an argument.

“Modeling the Messy” is visually polished and implements all four meeting fixes. Its most important correction is the sampling-theory curve in G06: the simulation samples without replacement, but the displayed formula omits the finite-population correction. Several other issues weaken the lesson’s message or phone usability.

## Blockers

None found.

## Should fix

| Page and location | Finding | Evidence | Suggested fix |
|---|---|---|---|
| **B — G06, sample-size simulation** | **The theoretical sampling-spread curve is wrong for the simulation being run.** | The code shuffles a finite set of observed grains and takes the first `n`, so it samples **without replacement**. The displayed theory uses `s / sqrt(n)`, which assumes independent draws or an effectively infinite population. With 501 grains, the omitted finite-population correction is material at the larger sample sizes. | Use `s / sqrt(n) × sqrt((N - n) / (N - 1))` for each population being sampled. Make the observed simulation and theoretical curve use the same sampling design. |
| **B — G06, chart labels and explanatory text** | **“Whole-wafer mean” and “true mean” overclaim what was measured.** | The activity’s own disclosure says the 501 grains came from three scans and are “a measured population, not a full wafer census.” Three scanned regions cannot establish the whole-wafer or true population mean. | Rename these to “mean of all 501 observed grains,” “pooled observed mean,” or similarly bounded language. Reserve “whole-wafer” for a defensible wafer-wide sampling design. |
| **B — D01, “Nothing about the data changes” and silent tidying** | **The activity contradicts itself and quietly makes the kind of domain decision the lesson warns against.** | D01 says, “Nothing about the data changes. Only what a student meets first.” Yet its preparation changes the displayed subset, filters to 5 µm scans and roughness below 10 nm, and canonicalizes labels. It also silently folds `2H-MoS2` into `MoS2`, although M05 correctly teaches that a mechanical cleanup rule cannot decide whether labels denote the same material. | Say, “The source table stays fixed; the displayed subset, labels, and order change.” Remove the silent material merge, expose it as an explicit choice, or label it clearly as a domain assumption. |
| **B — Notice & Wonder, W01 and W02** | **The “Takeaway” text gives away the reveal before the student asks to see it.** | In the initial desktop and phone screenshots, W01 already says that one bad line multiplied roughness by more than seven, and W02 already summarizes the distribution, while the “Show what this is” controls remain unrevealed. The noticing task has effectively been answered for the participant. | Hide each takeaway until its reveal is opened, or replace the prereveal text with a neutral prompt. |
| **A — standards footer, Mathematical Practice 3** | **The page overclaims MP3.** | Students must select fixed answers, but the reasons and final written response are optional. That exercises recognition and critique, but it does not literally require students to “construct viable arguments.” The prior red-team review specifically recommended requiring evidence-based reasoning for this claim. | Make one brief claim-evidence-reasoning response required, add a peer-critique action, or downgrade MP3 from a claimed standard to an opportunity for discussion. |
| **A — intro scan comparison** | **“Smoother film” and “Rougher film” break the stated wording rule and encourage overgeneralization.** | The pictures are individual scanned patches, not evidence that an entire film is smoother or rougher. The statistical reports elsewhere correctly stay with “scans.” | Relabel them “smoother scanned patch” and “rougher scanned patch”; update image alt text the same way. The physical diagram may still describe the transistor film. |
| **B — G01 takeaway** | **“The line is nearly flat” is a misleading interpretation of low R².** | The reported slope is +0.059; across roughly 0–40 hours, that fitted change is about 2.36 nm, and the plotted line visibly rises. R² = 0.020 means the line explains little variation, not that its slope is nearly zero. | Say, “The line explains very little of the variation,” or “The points remain widely scattered around the fitted line.” Discuss effect size separately from fit. |
| **B — M11 at 390 px** | **The essential keep/fix/remove controls are offscreen with little indication that the table scrolls horizontally.** | The phone screenshot shows the table only through part of the roughness column; the action controls are outside the visible area. Those controls are the student action, not optional detail. | Put the action column first or make it sticky, stack each row into a card on narrow screens, or add a conspicuous horizontal-scroll cue. |
| **B — top navigation at 390 px** | **Later activities are easy to miss.** | The tab strip horizontally overflows; screenshots show only the first tabs and part of the next one. There is no clear cue that Model, Dials, and Reflect continue offscreen. | Wrap the tabs, add an explicit swipe/scroll affordance, or automatically scroll the active tab into view. Keep the five-step path indicator visible or otherwise show progress. |
| **B — page versus facilitator crib, roughness count** | **The reference materials disagree about whether 894 or 899 samples have roughness measurements.** | The page says 1,005 grown and 899 with roughness, then explains that removing five known-invalid records gives 1,000 and 894. The crib’s opening summary table labels 894 as “Samples with a roughness measurement,” while its later prose supports the page’s 899-before-cleaning / 894-after-cleaning sequence. | Correct the crib summary to 899, or explicitly label 894 as the cleaned count. Keep the before/after-cleaning distinction visible. |
| **B — page versus facilitator crib, D01 variable count** | **The crib promises “one to all nineteen” variables, while the page offers 2, 6, or all 8.** | The implemented structural dial and polish change log use eight available columns. The crib describes a materially different range. | Update the crib to 2/6/8, or expand the page only if nineteen variables are genuinely available and instructionally useful. |

## Nice to have

| Page and location | Finding | Evidence | Suggested fix |
|---|---|---|---|
| **A — standards footer, MP6** | **The MP6 claim is defensible but lightly exercised.** | Students work with a defined percentile, exact counts, units, and “at or below,” but most precision is supplied by the interface rather than produced or checked by the student. | Keep it if the facilitator explicitly asks students to justify the boundary and wording; otherwise describe it as supported rather than central. |
| **A — sticky progress bar** | **The progress bar visually covers content in full-page captures.** | In both widths, the sticky strip appears across content partway down the composite screenshot. This may be a capture artifact, but a sticky element can also obscure a heading reached by scrolling or focus navigation. | Verify ordinary scrolling and keyboard focus in a real viewport; add suitable `scroll-margin-top` or spacing if headings land underneath it. |
| **B — G15 evidence table at 390 px** | **The For/Against comparison is cramped.** | The two evidence columns remain side by side on the narrow screenshot, producing short line lengths and slower reading. | Stack the two evidence groups vertically below a narrow breakpoint. |
| **B — M05 rule counts** | **Conditional counts can be mistaken for independent facts.** | Counts change as other cleanup switches change, so a label such as “would hide 18” may not match a facilitator’s remembered standalone number. | Add a short label such as “given your current choices” beside the live counts. |
| **B — D01 default view** | **The default “tidy quietly / typical only” state hides the mess in a lesson about exposing modeling decisions.** | The activity eventually reveals the choices, but the initial state makes the curated version feel primary and the raw structure exceptional. | Consider opening with “surface choices,” or explicitly frame the tidy view as one designed presentation rather than a neutral baseline. |

## A. Numeric and statistical audit: outlier lesson

Every value displayed from the revision 2 comparison table matches the outline:

| Rule | n | Median | Q1 | Q3 | IQR | Mean |
|---|---:|---:|---:|---:|---:|---:|
| All scans | 401 | 0.473 | 0.302 | 0.940 | 0.638 | 1.314 |
| Drop incomplete scans | 390 | 0.477 | 0.305 | 0.938 | 0.632 | 1.330 |
| Keep finished 5 µm scans | 382 | 0.480 | 0.305 | 0.943 | 0.638 | 1.313 |
| Drop flagged high outliers | 353 | 0.419 | 0.283 | 0.693 | 0.410 | 0.545 |

Additional checks also agree with the outline:

- Q3 is 0.940 nm by the stated CCSS-glossary/Moore–McCabe method.
- 301 of 401 scans are at or below Q3, displayed correctly as 75.1%.
- The exact upper fence is 1.8975 nm and is appropriately rounded to 1.90 nm for the student-facing cutoff.
- Rule effects are consistent: 11 removed for incomplete scans, 19 removed for finished 5 µm scans, and 48 removed by the high-outlier rule.
- Reports A and B preserve the outline’s wording and avoid the rejected “27% better” claim.
- The teacher material correctly describes 1.5×IQR as a flagging convention rather than an automatic deletion rule. The rule card intentionally lets the student test deletion, and the later comparison exposes the consequence.
- I found no accidental claim that the trimmed distribution describes all MoS2 films. The statistical conclusion is bounded to the lab’s recorded scans.

### Standards audit

| Footer claim | Verdict | Student action on the page |
|---|---|---|
| **S-IC.6** | **Addresses** | Students evaluate two reports based on data and identify why removing inconvenient results makes one conclusion misleading. |
| **S-ID.3** | **Addresses** | Students compare before/after distributions and answer questions about shape, center, spread, and outliers in context. Treating a derived subset as the second data set is reasonable here because the comparison itself is the lesson’s object. |
| **S-ID.2** | **Addresses** | Students use displayed mean, median, quartiles, and IQR to compare distributions and choose resistant summaries for skewed data. The standard says “use,” not “calculate.” |
| **MP4** | **Addresses** | Students choose an inclusion model before seeing its effect, then evaluate whether the resulting mathematical conclusion fits the scientific question. |
| **MP6** | **Touches / modestly addresses** | The page emphasizes exact boundary language, units, and counts, but the interface performs most precision work. |
| **MP3** | **Overclaims** | Fixed-choice critique is required; constructing an argument is not. Optional prose is insufficient for a literal alignment claim. |
| **S-ID.1, labeled “exposure”** | **Accurate label** | Students read dot plots and distribution displays, but do not construct those plots. |

No cited content standard is marked (+). The footer’s use of PDF notation (`S-ID.2`, `S-ID.3`, `S-IC.6`) is correct. Modeling is chiefly represented through MP4; the footer does not falsely attach a modeling star to these content-standard codes.

## B. Numeric and meeting-fix audit: “Modeling the Messy”

The page agrees with the crib on the central fixed values:

- W01: 6.10 nm versus 0.80 nm; 1 acquired line out of 512.
- W02: 894 cleaned roughness observations.
- M05: 35 raw material labels; reveal counts 338 `MoS2`, 2 `2H-MoS2`, 1 `MoS2-WS2`, and 18 `Mo-WSe2`.
- M02: 740 and 772 before rounding; 14 and 233 after rounding; 754 combined.
- M11: mean 1.83 → 1.01 and median 0.74 → 0.66 after removing 66 flagged rows.
- G01: 754 plotted and 251 omitted; slope +0.059; R² = 0.020.
- G15: medians 0.62 and 1.47; counts 756 and 143.
- G06: 501 observed grains; center median 1,526 and edge median 2,792.
- Dials: 1,005 → 752 → 650.

The only fixed-count conflicts found are the 899/894 labeling and the D01 nineteen/eight-variable mismatch listed above. G06’s random sample spread necessarily varies by run; the concern there is the theoretical comparator, not the random values themselves.

### Four meeting fixes

| Requested fix | Verdict | Evidence |
|---|---|---|
| M05 misspelling rules default to “keep as typed” | **Implemented** | All rule controls open in the keep state, with bulk controls available. |
| Carry sample 17458 through the experience | **Implemented** | It appears through the warmup, W01, M05, M11, G01 note, G06, D01, and reflection; G01 explicitly explains why it is absent from that plot. |
| Freeze the G06 x-axis | **Implemented** | The sampling-spread chart uses a consistent 0–5,000 scale across position and sample size. |
| Use one color when color is not encoding a variable | **Implemented** | G01 and the reduced-variable D01 views use a single series color; additional colors are used where they encode material, position, or the threaded sample. |

## Recommended disposition

The outlier lesson is ready for summit use after the MP3/footer correction and scan-label cleanup. “Modeling the Messy” is also close, but I would correct G06’s finite-population theory and population language before presenting it to mathematics teachers. The phone navigation and M11 controls deserve a real-device pass because they affect whether participants can find and perform the intended actions.
