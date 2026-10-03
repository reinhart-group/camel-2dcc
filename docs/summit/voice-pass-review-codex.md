# Codex review: Modeling the Messy voice pass

Scope: the complete built page, including primer cards, teacher notes, dynamically generated widget copy, and reflection. I checked the built page against the current generator and confirmed they are byte-for-byte identical. I also recomputed the fixed counts and statistics from the embedded data.

No fixed numeric mismatch was found. Verified values include 1,005/899/894/754/251; M-02’s 740 of 772 and 14 of 233; M-11’s 66, 1.83/1.01, and 0.74/0.66; G-01’s slope 0.059, R² 0.0196, and Spearman 0.287; G-15’s 756/143 and 0.622/1.471; and G-06’s 501, 1,526, and 2,792. Findings 4–6 concern what the numbers are said to mean, not their arithmetic.

1. **Clear — W-01 and W-02 answer the notice-and-wonder prompt before the output can teach.**

   - **Quote:** “One bad scan line took this film’s roughness from 0.80 nm to 6.10 nm.” / “Here most of the 894 films sit under 2 nm and a handful reach past 50 nm.” These appear above the interactive notice-and-wonder widgets.
   - **Rule broken:** The workshop guide says not to explain what an output is about to show and to let the output teach. The prose also undercuts the page’s own instruction to notice first and reveal later.
   - **Suggested rewrite:** Before W-01: “Start with the image. Write what you notice before opening the measurement.” Before W-02: “Start with the shape. Write what you notice before revealing the variable and unit.” Move the numerical observations after the reveal.

2. **Clear — several Takeaway boxes merely repeat a labeled chart or readout.**

   - **Quote:** “Only complete rows keeps 740 of 772 MOCVD samples but only 14 of 233 hybrid MBE.” / “Removing all 66 moves the mean from 1.83 to 1.01 nm but the median only from 0.74 to 0.66.” / “The line rises about 0.06 nm per minute, and growth time accounts for 2%...”
   - **Rule broken:** “Let the output teach” and “Don’t re-explain what the output already shows.” These are end-of-card mini-summaries of values already printed directly beside the visualization.
   - **Suggested rewrite:** Remove the duplicate Takeaway text. If a post-output sentence is needed, add only an interpretation absent from the labels, such as “The same missing-value rule affects the two methods differently.”

3. **Clear — the recurring W-01 sentence makes a scan line the actor and lands as a mini-moral.**

   - **Quote:** “One bad line in 512 multiplied the roughness by more than seven.” The same construction also appears as “One bad scan line took this film’s roughness from...”
   - **Rule broken:** The MATSE 219 rubric rejects an abstraction staged as the agent, especially in the final takeaway clause. A line does not perform arithmetic or take a value somewhere; including it changes the calculation.
   - **Suggested rewrite:** “With the bad line included, the computed roughness is 6.10 nm; without it, the result is 0.80 nm.”

4. **Clear — M-11 conflates two different calculations.**

   - **Quote:** “Roughness squares each gap from the average, so one extreme point counts for a lot.” It sits in a card about the mean and median of 894 already-computed roughness values.
   - **Rule broken:** This is statistically misleading. RMS roughness squares within-scan height deviations. The mean across scans does not square deviations; it is sensitive because every scan-level value contributes directly. The sentence invites teachers to infer the wrong reason for the mean/median contrast.
   - **Suggested rewrite:** “The mean uses every roughness value, so a few large readings pull it upward. The median depends on rank and changes much less.” Keep the RMS formula in the primer only.

5. **Clear — M-11 turns a roughness statistic into the height of one bump.**

   - **Quote:** “A real bump can be 92 nm tall. So can a speck of dust on the surface.”
   - **Rule broken:** The 92.025 nm value is RMS roughness for an entire scan, not the recorded height of one bump. The displayed number is real, but the prose changes its statistical meaning.
   - **Suggested rewrite:** “A scan can have RMS roughness near 92 nm because of real topography or contamination. The number alone does not distinguish them.”

6. **Clear — G-06 motivates a mean-based simulation with subgroup medians.**

   - **Quote:** “Grains at the center have a median area of 1,526 nm² and grains toward the edge 2,792 nm², so a center-only sample is off target at any size.” The widget then samples and compares **average** grain area against the all-grains **mean**.
   - **Rule broken:** The numbers are correct, but medians do not establish where the sampling distribution of the mean is centered. This mixes estimands while teaching sampling bias.
   - **Suggested rewrite:** Use the matching means: “Mean grain area is 1,469 nm² at the center, 2,818 nm² toward the edge, and 1,889 nm² across all 501 observed grains.” Alternatively, change the simulation to sample medians.

7. **Clear — D-01 calls real, unexplained observations “noise.”**

   - **Quote:** “The fullest shows all 8 variables with the mess and the noise left in...” / dial labels “show the noise” and “typical samples only.”
   - **Rule broken:** M-11 explicitly establishes that only one extreme reading has a known fault. D-01 then treats non-5 µm scans and values at or above 10 nm as “noise” without evidence. This is an unsupported statistical judgment disguised as a display choice.
   - **Suggested rewrite:** Rename the dial “Scope” with choices such as “all recorded scans” and “5 µm scans below 10 nm.” Say exactly what the restricted view excludes without calling those observations noise.

8. **Clear — the explanation for the larger Spearman coefficient is too strong.**

   - **Quote:** “The rank correlation is stronger (Spearman +0.29) because roughness is so skewed.”
   - **Rule broken:** Skew alone does not imply that Spearman correlation will exceed Pearson correlation. Ranking reduces the influence of extreme values and captures monotonic association; the observed difference cannot be attributed to skew alone from these two coefficients.
   - **Suggested rewrite:** “Spearman’s rank correlation is +0.29. Ranking reduces the influence of the largest roughness values, so it answers a different question from the fitted line.”

9. **Clear — the teacher note overstates the G-01 result.**

   - **Quote:** “We found almost no relationship” is offered as “a good sentence to write.”
   - **Rule broken:** R² = 0.020 supports “the fitted line explains little variation,” not the broader claim that almost no relationship exists. The same card reports Spearman +0.29, which is evidence of a modest monotonic association.
   - **Suggested rewrite:** “This fitted line explains about 2% of the variation in roughness.” If mentioning Spearman, add that the rank-based association is modestly positive.

10. **Clear — G-01 uses the exact negated animate-abstraction form the rubric warns about.**

   - **Quote:** “The 251 left-out samples did not leave at random.”
   - **Rule broken:** Samples are staged as actors that left. The rubric specifically says negated forms and animate motion are easy-to-miss violations.
   - **Suggested rewrite:** “Missingness is not random: 251 samples lack growth time, roughness, or both. See M-02.”

11. **Clear — G-06 retains several abstraction-as-agent capstones.**

   - **Quote:** “More grains shrink the wander.” / “A bigger n squeezes the pile toward the mean...” / “a bigger n will not fix that.”
   - **Rule broken:** Grains and `n` are made to shrink, squeeze, and fix the result. These short final clauses are the capstone rhythm identified as the rubric’s highest-priority failure.
   - **Suggested rewrite:** “Sampling variation decreases as n increases.” / “As n increases, the sampling distribution narrows around the relevant population mean.” / “Increasing n does not remove selection bias.”

12. **Clear — the reflection recap gives the wafer a social-transfer verb.**

   - **Quote:** “Sampling: its wafer gave the 501 grains.”
   - **Rule broken:** This is the rubric’s “object hands you something” pattern. The real action is measurement across three scans.
   - **Suggested rewrite:** “Sampling: the 501 measured grains came from three scans across its wafer.”

13. **Clear — M-05 repeatedly makes a rule “hide” groups.**

   - **Quote:** “A real choice, and it hides small groups.” / “would hide 18 small labels...” / “Folding labels under 5 samples into ‘rare’ hides the small labels...”
   - **Rule broken:** “Hides” is explicitly in the rubric’s adversarial verb class. Here the operation combines categories in the displayed chart; it has no intent toward the learner.
   - **Suggested rewrite:** “This combines small groups under ‘rare’.” / “would combine 18 small labels into one displayed category.”

14. **Clear — both field-knowledge card endings are grammatically indirect and hard to parse.**

   - **Quote:** “Whether they belong in it is a call for someone who knows the field.” / “Whether that is right is a call for someone who knows the field.”
   - **Rule broken:** MATSE 219 voice names the decision plainly. Here “they,” “it,” and “that” force the reader to reconstruct the referents, while “is a call for someone” is awkward idiom.
   - **Suggested rewrite:** “Deciding whether `2H-MoS2` belongs with `MoS2` requires domain knowledge.” / “Deciding whether `Mo-WSe2` should count as `WSe2` requires domain knowledge.”

15. **Clear — the M-05 generalization is absolute, and its takeaway has a broken parallel structure.**

   - **Quote:** “Anything typed by hand comes out in several spellings.” / “Four labels still need someone who knows the field, or the label ‘unresolved’.”
   - **Rule broken:** The first claim is needlessly universal. The second coordinates a person with a label and makes “labels need someone” the actor. Neither is the short, plain declarative voice in section 5.
   - **Suggested rewrite:** “Hand-entered labels often appear in several spellings.” / “Four labels still require domain knowledge. Until then, leave them unresolved.”

16. **Clear — W-01 claims more about the specimen than the evidence supports.**

   - **Quote:** “The dark stripe is one scan line out of 512, a bad pass of the tip that dips to −455 nm. The crystal itself is fine.”
   - **Rule broken:** Identifying the stripe as an acquisition artifact does not establish that the entire crystal is “fine.” The final reassurance is a mini-moral and an evidentiary overclaim.
   - **Suggested rewrite:** “The stripe records a bad pass of the tip rather than a −455 nm surface feature. The remaining scan lines are still usable.”

17. **Clear — the AFM primer overstates tip geometry and one imaging mode.**

   - **Quote:** “A needle sharpened to a single atom was dragged across a real film...” / “An atomic force microscope (AFM) drags a very sharp tip...”
   - **Rule broken:** AFM tips have nanoscale apex radii; “sharpened to a single atom” is not supported for these scans. AFM may operate in contact, tapping, or non-contact modes, so “drags” should not be presented as the generic definition unless the acquisition mode is known.
   - **Suggested rewrite:** “An AFM moves a nanoscale tip across the surface and records a grid of heights.” If these records document contact mode, name that mode explicitly.

18. **Clear — the WSe2 reveal makes an unsupported product comparison.**

   - **Quote:** “The triangles are WSe2 crystals, thin enough to make transistors thinner than any silicon one.”
   - **Rule broken:** The scan establishes crystal topography, not the thickness of a completed transistor. “Any silicon one” is also grammatically loose and stronger than the page’s careful “studied as candidates” language elsewhere.
   - **Suggested rewrite:** “The triangles are WSe2 crystal islands. WSe2 is studied for atomically thin transistor channels.”

19. **Clear — the G-15 takeaway assigns the wrong grammatical category to the claims.**

   - **Quote:** “Both claims are associations in observational records, never causes.”
   - **Rule broken:** The claims use causal verbs (“makes”), so the claims themselves are not associations. “Never causes” is also an abrupt mini-moral rather than a statement about what the study design supports.
   - **Suggested rewrite:** “These observational comparisons support associations, not causal conclusions.”

20. **Clear — G-15 retains a prohibited hedge.**

   - **Quote:** “Among the 24 that were recorded, hybrid MBE growths were shorter ... which if anything runs the other way.”
   - **Rule broken:** The workshop guide says not to hedge. “If anything” weakens a result that can be stated with its actual limit.
   - **Suggested rewrite:** “Among the 24 recorded hybrid MBE times, the median was 7 minutes, versus 15 minutes for MOCVD. This difference points opposite the proposed growth-time explanation, but only 14 hybrid MBE samples have both measurements.”

21. **Clear — the source-data disclosure contradicts the filtering described immediately before it.**

   - **Quote:** “A few activities first set aside five rows...” followed by “Nothing was cleaned up, simplified or invented for this page.”
   - **Rule broken:** The absolute sentence is imprecise and rhetorically defensive. The page does filter, canonicalize, and aggregate records for particular activities, even though the embedded source rows remain unchanged.
   - **Suggested rewrite:** “The page embeds the source records unchanged. Each activity states the filters or grouping rules it applies.”

22. **Clear — the primer contains two small grammar/clarity slips.**

   - **Quote:** “As one layer it is a semiconductor.” / “Our film is this.”
   - **Rule broken:** Section 5 favors short declaratives, but they still need natural syntax and an explicit referent.
   - **Suggested rewrite:** “A single layer is a semiconductor.” / “Sample 17458 is WSe2.”

23. **Borderline — “mean moves” is functional in context but still uses the rubric’s animate-fate pattern.**

   - **Quote:** “The mean is the usual average and moves with extreme values. The median is the middle value and barely moves.”
   - **Rule broken:** “Moves” is common statistical shorthand, so this is not as clear as “chases extremes.” Still, the paired sentence stages both statistics as moving characters and supplies the card’s concluding contrast.
   - **Suggested rewrite:** “Extreme values change the mean substantially. They usually change the median much less.”

24. **Borderline — the “good rewrite” uses casual uncertainty where the population can be named exactly.**

   - **Quote:** “Among the samples 2DCC happened to measure...”
   - **Rule broken:** “Happened to” is conversational but functions as a hedge. The page knows the relevant observed population and can state it directly.
   - **Suggested rewrite:** “Among the 899 MOCVD and hybrid MBE samples with roughness measurements, MOCVD films had the lower median roughness, but the groups were not grown or measured under comparable conditions.”

25. **Borderline — the final recap compresses a missing value into a dramatic punchline.**

   - **Quote:** “Model: no growth time, so it was never a dot.”
   - **Rule broken:** The sentence is memorable, but “never a dot” is an end-weighted reveal rather than the direct MATSE 219 voice.
   - **Suggested rewrite:** “Model: no growth time was recorded, so the plot excludes sample 17458.”

## Overall assessment

The pass removed many obvious morals and several strong animate abstractions, but the page still uses the same pattern in short takeaways and widget verdicts. The most consequential revisions are not cosmetic: correct M-11’s explanation of mean sensitivity, align G-06’s motivating statistic with its mean-based simulation, and stop calling unexplained observations “noise.” After those, the highest-value voice change is to remove prereveal answers and duplicate Takeaway text so the interactive output can do the teaching.
