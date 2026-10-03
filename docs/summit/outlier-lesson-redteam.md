# Red-team review: outlier lesson vs. the CCSS Mathematics PDF

Reviewed 2026-10-02 against /private/tmp/ccss.txt, the supplied extraction of
*Common Core State Standards for Mathematics*. That file is the sole authority used here for
standard wording and notation. Data checks use the lesson data source.

## Bottom line

The lesson has a defensible core, but the standards section currently overclaims. **S-IC.6 is the
best direct content match. S-ID.3 and MP3 are plausible targets after small but explicit changes to
what students must produce.** S-ID.1, S-ID.2, and 6.SP.5c are not met merely because students see a
dot plot, a quartile, an IQR-based rule, or a mean/median table.

The statistical framing also needs repair before approval:

- “75% of films are smoother than X” is not literally warranted by a pandas-interpolated Q3, and
  rows in this file are measurements/scans, not demonstrated independent films.
- The CCSS glossary defines quartiles by the Moore–McCabe method, not pandas linear interpolation.
- Q3 + 1.5 × IQR is nowhere in the supplied CCSS text.
- “27% better” confuses a lower reported cutoff caused by deletion with an improvement in films.
- The 382-row “same size” condition is actually a compound rule: finished **and** 5 µm.

Verdict labels below are deliberately strict:

- **Addresses:** the student work literally requires the named performance.
- **Touches:** students encounter the idea, but need not perform the full standard.
- **Overclaims:** the proposed evidence omits a material action in the standard.

## Verdict table

| Claim in the outline | Verdict | Evidence from the supplied CCSS text | Required fix |
|---|---|---|---|
| “Quoted verbatim” standards with codes such as HSS-ID.A.3 and HSS-IC.B.6 | **Wording passes; codes drift.** The quoted content sentences are verbatim, including punctuation. The identifiers are not the notation printed in this PDF. | The PDF prints the domain heading “S-ID,” followed by numbered standards; it prints “S-IC,” then “6. Evaluate reports based on data.” It contains no HSS-, cluster-letter, or CCSS.MATH.CONTENT identifiers. | For a literal-PDF claim, cite **S-ID.3**, **S-IC.6**, **S-ID.1**, and **S-ID.2**. If district metadata requires longer registry codes, label that as a crosswalk rather than PDF notation. |
| 6.SP.B.5c and MP3 are exact PDF codes | **Code drift.** These are recognizable shorthand, but not printed that way in the PDF. | The PDF prints the domain “6.SP,” a cluster heading, then “5.” and “c.” Separately it prints “3 Construct viable arguments and critique the reasoning of others.” | Use **6.SP.5c** and **MP3 / Practice 3** as editorial shorthand, while stating that the literal PDF labels are 6.SP → 5(c) and Practice 3. |
| HSS-ID.A.3 quotation | **Verbatim wording; alignment overclaimed.** | “Interpret differences in shape, center, and spread in the context of the data sets, accounting for possible effects of extreme data points (outliers).” | Do not call this met unless students explicitly compare the original and filtered distributions and interpret **shape, center, and spread** in context. |
| Does one data set before/after deletion satisfy the plural “data sets” in S-ID.3? | **Potentially, but not as written.** Two versions with different membership can be treated as two derived data sets; the standard does not require independent sources. The lesson, however, calls them “the same data set” and asks mainly about Q3 and fairness. | S-ID.3 expressly says “the data sets” and requires differences in “shape, center, and spread.” | Name them as two derived distributions (all 401 vs. retained 353), show both, and require a contextual sentence about shape, median, and IQR. |
| HSS-IC.B.6 quotation and lesson fit | **Verbatim wording; addresses the sentence, but weakly situates its cluster.** Students do evaluate two data-based reports. | “Evaluate reports based on data.” Its cluster heading is “Make inferences and justify conclusions from sample surveys, experiments, and observational studies.” | Keep as the primary content standard, but require evaluation of inclusion rule, denominator, study/record provenance, representativeness, and the scope of any inference—not only “which would you trust?” |
| HSS-ID.A.1 quotation and “every step uses one dot plot” | **Verbatim wording; touches, not meets.** Viewing an automatically generated plot is not necessarily representing data with a plot. | “Represent data with plots on the real number line (dot plots, histograms, and box plots).” | Either say the lesson **uses** S-ID.1 representations, or require students to construct/complete a dot plot, choose a plot, or encode the filtered data themselves. |
| HSS-ID.A.2 quotation and the Q3/IQR rationale | **Verbatim wording; overclaims.** Q3 is neither a measure of center nor the IQR. The student steps do not require comparison of center and spread, do not require two or more data sets explicitly, and do not ask why the statistics are appropriate to the skewed shape. | “Use statistics appropriate to the shape of the data distribution to compare center (median, mean) and spread (interquartile range, standard deviation) of two or more different data sets.” | Have students compare median and IQR for all-data and trimmed-data distributions, explain why median/IQR are appropriate for skew/outliers, and contrast mean sensitivity. Otherwise move S-ID.2 to “possible extension.” |
| MP3 heading and continuation | **Quotation passes; activity touches.** The heading and quoted continuation are verbatim. A private one-sentence preference does not by itself establish a viable mathematical argument, response to another argument, or critique of reasoning. | “Construct viable arguments and critique the reasoning of others.” The quoted continuation also exactly matches the PDF, including the em dash. | Require claim-evidence-reasoning, exchange two responses, and have each student identify a stated assumption or flaw in the competing report. |
| 6.SP.B.5c quotation and middle-school fit | **Verbatim wording; overclaims as currently assessed.** Students are shown Q3 and a supplied fence. They need not give a median/mean or IQR/MAD, nor describe the overall pattern and striking deviations in context. | “Giving quantitative measures of center (median and/or mean) and variability (interquartile range and/or mean absolute deviation), as well as describing any overall pattern and any striking deviations from the overall pattern with reference to the context in which the data were gathered.” | For grade 6, require students to report median and IQR and describe the skew/right-tail deviations as microscope measurements. Otherwise list 6.SP.5c only as a teacher-led extension. |
| Are the cited standards marked (+)? | **No.** None of S-ID.1–3, S-IC.6, Practice 3, or 6.SP.5c carries (+). | “Additional mathematics that students should learn in order to take advanced courses … is indicated by (+).” The PDF also says all standards without (+) belong in the common college-and-career-ready curriculum. | No advanced-course caveat is needed. |
| Are S-ID and S-IC modeling standards (★)? | **Yes, through the category heading.** | The PDF heading is “Mathematics | High School—Statistics and Probability★.” It says when ★ appears on a group heading, “it should be understood to apply to all standards in that group.” | Note the modeling designation. It strengthens the case for MP4 and for interpreting assumptions/results in context; it does not waive any verbs in S-ID.2 or S-ID.3. |
| “The upper quartile (Q3) as a claim: ‘75% of films are smoother than X.’” | **Misleading.** Q3 is a statistic/threshold, not itself a claim. “Smoother than” is a strict inequality, while empirical percentile conventions involve rank and often “at or below.” Linear interpolation can place Q3 between observations without making exactly 75% of observations ≤ Q3. The unit is also a measurement/scan, not proven independent films. | The glossary defines: “Third quartile. For a data set with median M, the third quartile is the median of the data values greater than M.” | Say: “The 75th-percentile roughness of these recorded scans is about X nm.” If a frequency claim is essential, report the actual count and use “at or below.” Do not substitute “films” for “measurements” without provenance. |
| Q3 is used by CCSS as a performance claim | **No.** CCSS uses quartiles to define a box plot and IQR as variation/spread; it does not frame Q3 as a quality promise. | “A box shows the middle 50% of the data.” “Interquartile Range. A measure of variation … the distance between the first and third quartiles.” | Present the threshold interpretation as this lesson's modeling choice, not as a CCSS-defined use of quartiles. |
| “The outlier rule students meet (Q3 + 1.5 × IQR) uses the same quartiles, so no new idea is introduced.” | **False and pedagogically risky.** The rule adds IQR, multiplication by 1.5, a fence, classification, and a policy decision about deletion. | No occurrence of the Tukey 1.5 × IQR rule exists in the supplied CCSS text. The only relevant uses are “interquartile range” as variability/spread and “extreme data points (outliers).” | Teach the fence as an optional convention for flagging points for investigation. Do not present it as CCSS content or as automatic permission to delete. |
| “Key numbers (pandas quartiles)” are suitable for a CCSS-aligned hand lesson | **Convention conflict.** The rounded table happens to survive, but the exact values differ from the glossary method. | The glossary footnote says: “Many different methods for computing quartiles are in use. The method defined here is sometimes called the Moore and McCabe method.” | Either use the PDF glossary method for student hand work or explicitly teach that software conventions differ and disclose pandas linear interpolation. Never make students reproduce pandas values by a different textbook algorithm. |
| “The justified rules leave the claim at 0.94 nm.” | **Only true after rounding.** Pandas-linear Q3 values are 0.9375 (all), 0.9364 (finished), and 0.941625 nm (finished 5 µm). | CCSS emphasizes precision through Practice 6: students “express numerical answers with a degree of precision appropriate for the problem context.” | Say “all round to 0.94 nm at two decimals.” Better, show that the small changes are hidden by rounding and contrast them with the large trimmed-data change. |
| “Drop scans not made at the same size” produces n = 382 | **Mislabeled rule.** Size = 5 µm alone retains 388 scans. The reported 382 requires both lines = pixels and size = 5 µm. | This is a data/lesson claim, not a CCSS statement. Practice 6 is relevant because students “try to use clear definitions.” | Rename it “Keep finished 5 µm scans,” or isolate the size-only rule and use n = 388. State the target comparison before looking at outcomes. |
| “Makes the claim look 27% better (0.69 nm)” | **Arithmetic is approximately reproducible; interpretation is wrong.** The pandas-linear threshold falls 26.496% from 0.9375 to 0.6891 nm (26.6% using displayed 0.94 and 0.69). The films did not improve; the retained subset and reported threshold changed. | Practice 6 says students “express numerical answers with a degree of precision appropriate for the problem context.” | Replace with: “The reported 75th-percentile cutoff is 0.2484 nm lower, a 26.5% reduction, after 48 high values are excluded.” Call it more favorable/stricter, not better data or better films. |
| “It also cuts the mean by more than half while the median barely moves.” | **Numerically true but imprecise and not yet S-ID.2 evidence.** Mean falls from 1.3136 to 0.5453 nm (58.5%); median falls from 0.4730 to 0.4194 nm (11.3%). “Barely” is subjective, and no spread comparison is required. | S-ID.2 requires comparison of “center (median, mean) and spread (interquartile range, standard deviation)” using statistics appropriate to shape. | Quantify both changes, add IQR before/after, and ask why mean is more sensitive to the long right tail. |
| “Same data, two headlines” | **Misleading shorthand.** The headlines arise from the same original pool but different retained data: 401 vs. 353 measurements. The first headline hides its exclusion rule and changed denominator. | S-IC.6: “Evaluate reports based on data.” | Say “same original pool, different inclusion rules.” Put n and the inclusion rule under each report, then ask students to evaluate what is disclosed or concealed. |
| “Removing a point because the measurement was flawed is fine; removing it because of what it shows is not.” | **Useful heuristic, too absolute.** A suspected flaw needs evidence and a documented, consistently applied rule. Outcome-based trimming is misleading for a success-rate question, but a pre-specified robust procedure may be legitimate for estimating a typical value. | The statistics introduction says conclusions depend on the question and real-life action, and “The conditions under which data are collected are important in drawing conclusions from the data.” | Tie fairness to the estimand/question, provenance, pre-specification, consistent application, and transparent reporting. Prefer correcting/re-measuring a confirmed instrument fault to silently deleting it. |
| “Drop unfinished scans (measurement broken)” | **Unsupported causal label.** Lines ≠ pixels shows an incomplete rectangle, not by itself why acquisition stopped or whether the observed region's roughness is invalid. | 6.SP.5b calls for “Describing the nature of the attribute under investigation, including how it was measured and its units of measurement.” | Use “incomplete scan” unless metadata confirms an instrument failure. Explain why full-area comparability is required for the stated question. |
| The WSe₂ corrupted-line counterexample proves an outlier “deserved removal” | **Good provenance example, but use correction language.** The internal crib supports 6.10 nm before and 0.80 nm after omitting a visibly corrupted line. Still, this is correction of a known acquisition artifact within one scan, not generic deletion of a high-valued scan from a distribution. | S-ID.3 asks students to account for “possible effects of extreme data points (outliers)” in context. | Distinguish pixel/line-level repair from row-level exclusion. Preserve both the raw and corrected values, document the reason, and avoid generalizing from this case to all outliers. |

## Quartile and numerical audit

The CCSS glossary method and pandas linear interpolation do not produce the same exact quartiles:

| Data retained | n | pandas-linear Q3 | CCSS-glossary Q3 |
|---|---:|---:|---:|
| All MoS₂ measurements | 401 | 0.9375 | 0.94025 |
| Finished scans | 390 | 0.9364 | 0.9375 |
| Finished 5 µm scans | 382 | 0.941625 | 0.9430 |
| After the stated high-outlier trim | 353 | 0.6891 | 0.6926 |

For the original 401 values, pandas gives Q1 = 0.3022 and an upper fence of 1.89045 nm.
The glossary method gives Q1 = 0.3021, Q3 = 0.94025, and a corresponding Tukey-style fence of
1.897475 nm. Both fences happen to retain the same 353 rows because no observation lies between
them. That accidental agreement does not remove the convention mismatch.

The literal frequency claim is also delicate:

- At the exact pandas Q3 for all 401 measurements, 301/401 are at or below it (75.06%) and
  300/401 are strictly below it (74.81%).
- For the 390- and 382-row data sets, an interpolated Q3 can lie between observations, so fewer
  than exactly 75% may be at or below the interpolated number.
- Rounding to 0.94 nm changes the cutoff again. For the 382-row set, 286/382 = 74.87% are below
  0.94 nm.

Therefore, “the 75th percentile is about X” is defensible; “75% of films are smoother than X” is
not a safe literal translation.

## Standards considered but not currently earned

| Candidate | Verbatim PDF text | Red-team judgment |
|---|---|---|
| S-IC.3 | “Recognize the purposes of and differences among sample surveys, experiments, and observational studies; explain how randomization relates to each.” | Potentially valuable for naming what the 2DCC records are and what can be inferred, but the lesson never classifies the data source or discusses randomization. Not currently addressed. |
| S-IC.5 | “Use data from a randomized experiment to compare two treatments; use simulations to decide if differences between parameters are significant.” | Not applicable. There is no randomized experiment, two treatments, simulation, or significance decision. Filtering one data set does not create treatments. |
| 7.SP.1 | “Understand that statistics can be used to gain information about a population by examining a sample of the population; generalizations about a population from a sample are valid only if the sample is representative of that population. Understand that random sampling tends to produce representative samples and support valid inferences.” | A strong missing caution if the lesson makes claims beyond these 401 records. The outline explicitly leaves sampling out and does not establish a random or representative sample, so it cannot claim this standard now. |
| 7.SP.3 | “Informally assess the degree of visual overlap of two numerical data distributions with similar variabilities, measuring the difference between the centers by expressing it as a multiple of a measure of variability.” | Not applicable without two population distributions, similar-variability reasoning, and a standardized center difference. Before/after deletion is not naturally two populations. |
| 7.SP.4 | “Use measures of center and measures of variability for numerical data from random samples to draw informal comparative inferences about two populations.” | Not applicable: neither random sampling nor two populations is established. |
| 8.SP.1 | “Construct and interpret scatter plots for bivariate measurement data to investigate patterns of association between two quantities. Describe patterns such as clustering, outliers, positive or negative association, linear association, and nonlinear association.” | The word “outliers” is not enough. This lesson is univariate and uses a dot plot, not paired bivariate data or a scatter plot. Do not cite 8.SP. |
| 6.SP.5d | “Relating the choice of measures of center and variability to the shape of the data distribution and the context in which the data were gathered.” | Better than 6.SP.5c **if** students decide why median/IQR are preferable to mean for the long right tail. The current outline leaves that contrast optional, so this is a revision target, not present evidence. |

## Missing Practices that fit the lesson

**MP4 — “Model with mathematics.”** The most relevant verbatim sentence is: “They routinely
interpret their mathematical results in the context of the situation and reflect on whether the
results make sense, possibly improving the model if it has not served its purpose.” This fits a
lesson about how an inclusion rule changes a real-world conclusion. To claim MP4, students should
state the question/target population, choose an inclusion rule, interpret the changed statistic,
and revisit whether the model answers the original question.

**MP6 — “Attend to precision.”** The PDF says students “try to use clear definitions,” “are careful
about specifying units of measure,” and “express numerical answers with a degree of precision
appropriate for the problem context.” It adds that high-school students “have learned to examine
claims and make explicit use of definitions.” This lesson should require precision about:

- measurement/scan versus film;
- below versus at or below;
- Q3 versus a 75% empirical count;
- exact versus rounded values;
- the quartile algorithm;
- “incomplete” versus proven “broken”; and
- the population to which a report applies.

## Recommended standards list

### Claim now, after tightening the assessment prompts

1. **S-IC.6** — “Evaluate reports based on data.”
   - Strongest direct match. Require an evidence-based evaluation that addresses the inclusion
     rule, changed n, provenance, and scope—not a preference alone.
2. **MP3 / Practice 3** — “Construct viable arguments and critique the reasoning of others.”
   - Require each student to make an argument, inspect another argument, and name a valid
     assumption or flaw.
3. **MP6 / Practice 6** — “Attend to precision.”
   - Make the distinctions listed above explicit scoring criteria.
4. **MP4 / Practice 4** — “Model with mathematics.”
   - Require students to connect the mathematical inclusion model to the lab question and assess
     whether the result still answers that question.

### Claim only after adding explicit statistical comparison

5. **S-ID.3** — “Interpret differences in shape, center, and spread in the context of the data
   sets, accounting for possible effects of extreme data points (outliers).”
   - Show full and filtered distributions and require contextual interpretation of all three:
     shape, center, and spread.
6. **S-ID.2** — “Use statistics appropriate to the shape of the data distribution to compare
   center (median, mean) and spread (interquartile range, standard deviation) of two or more
   different data sets.”
   - Require median and IQR comparison and an explanation of why those statistics suit the skewed
     distributions. A teacher note about means is insufficient.

### Describe as exposure unless students construct the representation

7. **S-ID.1** — “Represent data with plots on the real number line (dot plots, histograms, and box
   plots).”
   - “Uses a dot plot” is accurate now. “Meets S-ID.1” needs student construction or an equivalent
     act of representation.

### Middle-school option after revision

8. **6.SP.5c** — “Giving quantitative measures of center (median and/or mean) and variability
   (interquartile range and/or mean absolute deviation), as well as describing any overall pattern
   and any striking deviations from the overall pattern with reference to the context in which the
   data were gathered.”
   - Require students to give the measures and contextual description. Pair with **6.SP.5d** if
     students choose median/IQR in response to skew and outliers.

### Do not cite for the current lesson

- **S-IC.3, S-IC.5, 7.SP.1–4, and 8.SP.1–4.** The current task contains no study-design
  classification, randomized treatment comparison, random-sample inference, two-population
  comparison, or bivariate association.

## Minimum rewrite needed for defensible alignment

1. Replace the headline claim with “The 75th-percentile roughness of these 401 recorded scans is
   about 0.94 nm,” and always show n and the inclusion rule.
2. Treat all-data and trimmed-data results as two explicitly labeled derived distributions.
3. Require students to compare their shape, median, and IQR in context.
4. Require a written argument and a critique of a peer/report, not only a choice.
5. Disclose the quartile convention. For literal CCSS consistency, use the glossary's method; if
   pandas remains, show that different conventions give slightly different exact values.
6. Describe 1.5 × IQR as a convention for flagging observations, absent from CCSS and not an
   automatic deletion rule.
7. Rename the n = 382 rule “finished 5 µm scans.”
8. State the inference boundary: these records do not establish a random, representative sample of
   all MoS₂ films.
