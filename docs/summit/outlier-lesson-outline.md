# Lesson outline: when is it fair to throw out data?

Draft for Wes. Revision 2, 2026-10-02. Nothing is built from this yet; the prototype at
`epistemic-demo/materials-science/student-demo.html` is on hold until Wes has reviewed this
revision.

## What changed in revision 2 (from the red team, `outlier-lesson-redteam.md`)

1. **Standards narrowed to what students actually do.** Content standards and practices are now
   only claimed where a student step requires the action the standard names. "Represent data with
   plots" (S-ID.1) is listed as exposure, not alignment. Standards that don't fit are listed under
   "Do not cite".
2. **Two student steps were added to earn the claims.** Students now compare median and IQR for
   the full and trimmed data. They also write an argument and critique the misleading report,
   instead of only choosing one.
3. **Standard codes now match the official PDF notation** (S-ID.3, S-IC.6, Practice 3). The
   website identifiers are kept in brackets as a crosswalk.
4. **Added Practice 4 (model with mathematics) and Practice 6 (attend to precision).** Statistics
   is a modeling category in the high school standards.
5. **Statistics wording fixed.**
   - "75% of films are smoother than X" now reads "the 75th percentile of these recorded scans is
     about X".
   - The 401 records are called scans, not films.
   - "27% better" is gone; the films didn't change, only the retained data did.
6. **Quartiles now use the Common Core glossary method** (Moore and McCabe), so hand work matches.
   The page discloses that software uses other methods.
7. **The outlier fence (Q3 + 1.5 × IQR) is labelled a common convention for flagging points to
   investigate.** It does not appear in Common Core.
8. **Rule names corrected.**
   - "Drop scans not made at the same size" (382) is renamed "Keep finished 5 µm scans". That
     rule is two conditions; size alone keeps 388.
   - "Broken" scans are now "incomplete" scans. The data shows they stopped early, not why.
9. **The fairness principle is softened from a slogan to criteria.** Those criteria are:
   - the question asked;
   - evidence about the measurement;
   - a rule fixed before looking at results;
   - the rule applied to every point;
   - the exclusion reported openly.

   Students also pick their rule *before* seeing its effect.
10. **The WSe₂ example is now framed as correcting a known instrument fault inside one scan,**
    with both values kept, not as permission to delete high values.
11. **An inference limit was added.** These records are not a random sample of all MoS₂ films.

## Learning objective

Students can explain why excluding outliers from a data set can make a summary look more favorable
than the evidence supports, and can judge whether an exclusion rule is justified for the question
being asked.

## Standards

Wording is verbatim from *Common Core State Standards for Mathematics* (NGA Center & CCSSO, 2010).
The codes are the PDF's own notation, with the website identifier in brackets. All cited high
school statistics standards sit under the modeling heading "Statistics and Probability★". None is
a (+) advanced standard.

**Claimed: the student steps require these**

- **S-IC.6** [HSS-IC.B.6] "Evaluate reports based on data."
  *Step 4:* students evaluate two reports drawn from the same pool of 401 scans. Each report states
  its n and its inclusion rule. Students judge the rule, the changed n, where the data came from,
  and how far the claim reaches.
- **S-ID.3** [HSS-ID.A.3] "Interpret differences in shape, center, and spread in the context of the
  data sets, accounting for possible effects of extreme data points (outliers)."
  *Step 3:* students compare two labelled distributions (all 401 scans; 353 after trimming) and
  write about shape, center and spread in context.
- **S-ID.2** [HSS-ID.A.2] "Use statistics appropriate to the shape of the data distribution to
  compare center (median, mean) and spread (interquartile range, standard deviation) of two or more
  different data sets."
  *Step 3:* students record median, mean and IQR for both distributions and explain why the median
  and IQR suit this right-skewed data better than the mean.
- **Practice 3** [MP3] "Construct viable arguments and critique the reasoning of others."
  *Step 4:* students write a claim–evidence–reasoning argument and name the flaw in the competing
  report.
- **Practice 6** [MP6] "Attend to precision." The standard's text says students "try to use clear
  definitions" and "express numerical answers with a degree of precision appropriate for the
  problem context." *Throughout:* students must keep these distinctions straight:
  - scan versus film;
  - "at or below" versus "below";
  - the 75th percentile versus a count;
  - rounded versus exact values.
- **Practice 4** [MP4] "Model with mathematics." The standard's text says students "routinely
  interpret their mathematical results in the context of the situation and reflect on whether the
  results make sense, possibly improving the model if it has not served its purpose."
  *Steps 2 and 4:* the inclusion rule is the model. Students state the question, choose a rule,
  interpret the result, and check whether the rule still answers the question.

**Exposure only**

- **S-ID.1** [HSS-ID.A.1] "Represent data with plots on the real number line (dot plots,
  histograms, and box plots)." Students read and use a dot plot but do not build one. It becomes
  claimable only if a later version has students build the plot.

**Middle-school option, if the same steps are used in grade 6**

- **6.SP.5c** "Giving quantitative measures of center (median and/or mean) and variability
  (interquartile range and/or mean absolute deviation), as well as describing any overall pattern
  and any striking deviations from the overall pattern with reference to the context in which the
  data were gathered."
- **6.SP.5d** "Relating the choice of measures of center and variability to the shape of the data
  distribution and the context in which the data were gathered."

**Do not cite:** S-IC.3, S-IC.5, 7.SP.1–4 and 8.SP.1–4. The lesson has no study-design
classification, randomized treatment comparison, random-sample inference, two-population comparison
or bivariate data.

## Concepts, and what is left out

- **Core:** whether excluding data is justified depends on the question and on evidence about how
  each measurement was made. It does not depend on whether the result looks good.
- **Tool:** the 75th percentile (third quartile, Q3) of the recorded scans. Using it as the lab's
  headline number is this lesson's modeling choice; Common Core uses quartiles for box plots and
  the IQR.
- **Flagging convention:** Q3 + 1.5 × IQR, introduced as a widely used way to flag points for a
  closer look. It is not in Common Core and is not automatic permission to delete.
- **Out:** choosing a material, sample size, and scan-size physics. Scan size appears only as one
  reason two measurements may not be comparable.

## The data

401 recorded atomic force microscope scans of MoS₂ films from Penn State's 2DCC facility.
"Roughness" is how bumpy each scanned patch is, in nanometres; smaller is smoother.

These records are what the lab happened to measure, not a random sample of all MoS₂ films. Claims
stay about these scans.

Quartiles use the Common Core glossary method. In that method, Q3 is the median of the values
above the overall median. The numbers were checked 2026-10-02; software that interpolates gives
values differing in the third decimal place.

| Which scans count | n | Median | Q1 | Q3 (75th pct.) | IQR | Mean |
|---|---:|---:|---:|---:|---:|---:|
| All scans | 401 | 0.473 | 0.302 | 0.940 | 0.638 | 1.314 |
| Drop incomplete scans (fewer lines than pixels) | 390 | 0.477 | 0.305 | 0.938 | 0.632 | 1.330 |
| Keep finished 5 µm scans | 382 | 0.480 | 0.305 | 0.943 | 0.638 | 1.313 |
| Drop high outliers (above Q3 + 1.5 × IQR = 1.90 nm) | 353 | 0.419 | 0.283 | 0.693 | 0.410 | 0.545 |

All values are in nm. Three readings for the answer key:

- **The measurement-based rules barely move the 75th percentile,** which stays at 0.94 nm to two
  decimal places. Trimming moves it to 0.69 nm, 0.25 nm lower, after 48 high values are removed.
  The films did not change; only which scans were counted.
- **For all 401 scans, 301 are at or below Q3 (75.1%).** "Below" and "at or below" differ by one
  scan here, which is a Practice 6 talking point.
- **Trimming cuts the mean by 58%** (1.31 to 0.55 nm), the median by 11% (0.47 to 0.42 nm), and the
  IQR by 36% (0.64 to 0.41 nm). The mean reacts most because the right tail is long; the largest
  value is 92 nm.

## Teacher pre-brief (about 5 minutes)

- **The point, in two sentences:** removing data can change a conclusion as much as collecting it.
  Whether a removal is fair depends on the question and on evidence about each measurement, not on
  whether the result looks good.
- **The data** in the two sentences above, plus one 3D picture each of a smooth and a rough scan.
- **The misconception to listen for:** "outliers are mistakes, so you should remove them." The
  lesson's answer: an outlier is a reason to look closer, not a reason to delete.
- **Vocabulary:**
  - dot plot;
  - median;
  - quartile and 75th percentile;
  - IQR;
  - outlier;
  - "at or below".
- **Answer key** (the table above), the quartile method used, and the timing below.

## Student part (about 15–20 minutes)

1. **Find the 75th percentile.** One dot plot of 401 scans. Students drag a cutoff until it sits at
   the 75th percentile. The page then reports the value and the count at or below it (301 of 401).
   Students write the result as a precise sentence about scans, not films.
2. **Choose a rule before seeing its effect.** Three rules are shown as pictures. Students pick one
   and write a reason *before* the page shows what it removes:
   - Drop incomplete scans.
   - Keep finished 5 µm scans.
   - Drop high outliers (above the flagging fence).
3. **Compare two distributions.** The page shows "all 401 scans" and "353 after trimming" side by
   side. Students fill in median, mean and IQR for each and answer two questions:
   - How do shape, center and spread differ, and why?
   - Which summary would you trust to describe typical roughness, and why?
4. **Evaluate two reports.** The reports draw on the same pool of 401 scans, each with its n and
   rule printed underneath:
   - Report A: "The 75th-percentile roughness of our scans is 0.69 nm (n = 353, values above
     1.90 nm excluded)."
   - Report B: "The 75th-percentile roughness of our scans is 0.94 nm (n = 382, finished 5 µm
     scans only)."

   Students write a short claim–evidence–reasoning argument for which report better answers "How
   smooth are the scans this lab records?" They then name the flaw in the other report.

There is no single scripted path. The page records each student's rule, reason and written answers
for the debrief.

## Debrief (whole class, about 10 minutes)

- **Reveal:** Report A removed rough scans because they were rough, so its summary describes the
  smoother scans, not the lab's results.
- **Why the rule matters more than the arithmetic:** a removal is defensible when all of these
  hold:
  - it fits the question;
  - it rests on evidence about the measurement;
  - it was chosen before seeing the results;
  - it is applied to every point;
  - it is reported openly.

  Report B meets all five; Report A meets none of the first three.
- **A case where something should be fixed.** In one WSe₂ scan, a single corrupted line out of
  512 pushed the recorded roughness from 0.80 nm to 6.10 nm. After investigation, that line is an
  instrument fault inside the scan. Correcting it, with both values kept and the reason written
  down, is different from deleting a whole scan for being rough. (Source: the facilitator crib.)
- **Transfer:** dropping a student's lowest test score, a drug trial leaving out patients who got
  worse, a fitness app ignoring "bad" days. For each: which question is being answered, and is the
  removal disclosed?
- **Exit ticket:** "Give one justified and one unjustified reason to remove a data point, and say
  what makes the difference."

## What changes from the current prototype (when building is approved)

- **Cut:** material choice (old Gate 1) and the fixed 0.5/0.8/1.0 nm tiers (old Gate 3); both were
  look-ups.
- **Kept:**
  - the intro;
  - the real 3D smooth/rough pair;
  - the dot plot;
  - the picture-first rule cards. These get renamed as above, and students choose before the
    preview.
- **New:**
  - the drag-to-75th-percentile step;
  - the side-by-side distribution comparison with student-entered statistics;
  - the written report evaluation;
  - a teacher pre-brief and debrief.
- **Self-check:** rebuilt around the table above, using the glossary quartile method.

## Open questions for Wes

1. **Step 1:** should students drag the cutoff to find the 75th percentile, or see it computed?
   Dragging builds more understanding but takes more time.
2. **Step 3:** should students type the median, mean and IQR themselves, or read them off and
   interpret? Typing earns S-ID.2 more firmly; reading is faster for a summit demo.
3. **Teacher material:** should the pre-brief and debrief live on the same page behind a teacher
   toggle, or on a separate teacher page?
4. **Time:** 15–20 student minutes plus about 15 for teachers is longer than the earlier design. Is
   that acceptable for the summit slot?
