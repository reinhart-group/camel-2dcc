# Voice pass, Modeling the Messy page (2026-10-03)

Sources applied: `style-rubric.md` (no abstraction as animate participant, including negated and attributive forms, and the capstone kicker), `prose-style-guide.md`, `style_matse219.md` section 5. Page-wide: no sentence kept only for a moral; every number and fact unchanged unless noted.

Text below is shown with HTML tags and entities stripped. `file` is relative to `tools/messy_build/`. Part A (the M-05 cards) is at the end.

## Page header and session panel

- `build.py`
  - before: Find what the mess hides, and see how the same numbers teach different lessons.
  - after: Find the mess in them, and see how one table can be taught different ways.

## Warm Up

- `build.py`
  - before: “Rough” is just a word until you measure it.
  - after: Let’s put a number on “rough”.
- `build.py`
  - before: To compare surfaces we need a number. That number is roughness, and every activity here uses it.
  - after: We compare surfaces with a number, roughness. Every activity here uses it.
- `build.py`
  - before: We cannot compare surfaces by saying one “looks rough”. A number lets two people, or two labs, agree. Schools do the same when they turn “a good week” into an attendance rate.
  - after: “Looks rough” is a judgment call. SnTe’s typical bump is 0.36 nm, a number two people can both check. Schools do the same when they turn “a good week” into an attendance rate.
- `build.py`
  - before: Let that disagreement stand; it is the reason to measure.
  - after: Let that disagreement stand.
- `build.py`
  - before: Its wafer supplies the sampling grains.
  - after: The sampling grains come from its wafer.
- `build.py`
  - before: watch tidy-up settings drop it from the data.
  - after: turn on the tidy-up settings and it drops out of the data.
- `src/w_warm.js`
  - before: by the same amount, so they compare fairly.
  - after: by the same amount, so they can be compared.

## Notice and Wonder: W-01 (one scan)

- `build.py`
  - before: Looking closely finds what a summary number hides.
  - after: Let’s look at the picture before we trust the number.
- `build.py`
  - before: A single bad scan line can quietly change a number.
  - after: One bad scan line took this film’s roughness from 0.80 nm to 6.10 nm.
- `build.py`
  - before: One bad line in 512 multiplied the roughness by more than seven. Look at the data before you trust the summary.
  - after: One bad line in 512 multiplied the roughness by more than seven (0.80 nm to 6.10 nm).
- `build.py`
  - before: A summary number is a claim about the data, and it can be wrong. Here one bad line in the scan wrecked the headline figure. A single mistyped grade, or a blank saved as 999, can do the same to a class average. Looking at the raw picture first is the cheapest check there is.
  - after: Here one bad line in the scan took the roughness from 0.80 nm to 6.10 nm. A single mistyped grade, or a blank saved as 999, moves a class average the same way.
- `build.py`
  - before: A scan is built one line at a time, so one bad line is one bad pass of the tip, not a flaw in the crystal.
  - after: A scan is built one line at a time. One bad line is one bad pass of the tip.
- `build.py`
  - before: a needle drags across the surface and feels its height.
  - after: a needle drags across the surface and records its height.
- `build.py`
  - before: The dark stripe is the instrument misbehaving, not the crystal: one scan line out of 512, dipping to −455 nm.
  - after: The dark stripe is one scan line out of 512, a bad pass of the tip that dips to −455 nm. The crystal itself is fine.

## Notice and Wonder: W-02 (histogram)

- `build.py`
  - before: Round 2 asks which of those few to trust.
  - after: In round 2 you decide which of those few to trust.
- `build.py`
  - before: A histogram draws every value instead of one average, so you can see whether “typical” even makes sense. Attendance rates, test scores and survey answers often look like this: a big pile and a thin tail. The tail is where the surprises are, and an average hides it.
  - after: Here most of the 894 films sit under 2 nm and a handful reach past 50 nm. Attendance rates and test scores often have the same shape: a big pile and a thin tail.
- `build.py`
  - before: A histogram alone cannot tell you which, and that gap is the point of the next round.
  - after: Nothing in a histogram separates the two. Round 2 starts there.
- `build.py`
  - before: They are real samples, not mistakes.
  - after: They are real samples.
- `build.py`
  - before: which this chart does not show.
  - after: which is not plotted here.

## Find the Mess: lede

- `build.py`
  - before: Real data hides problems that tidy-looking rules cannot see.
  - after: Let’s apply cleaning rules to real records and see what each one does.

## M-05 (spellings)

- `build.py`
  - before: Cleaning rules can merge typos, but only an expert can say which labels mean the same thing.
  - after: Some spellings merge by rule. Others need someone who knows the field.
- `build.py`
  - before: Mechanical mess is fixable by anyone. The rest needs someone who knows the field, or an honest “unresolved”.
  - after: Four rules fix the mechanical mess. Four labels still need someone who knows the field, or the label “unresolved”.
- `build.py`
  - before: Folding labels under 5 samples into “rare” hides the small labels and fixes nothing. How many it hides depends on which other rules are on: 18 with none of them, 10 with all of them, and the count under the button tells you the number for your current choices. It makes the chart look cleanest, which is why it is worth pointing at.
  - after: Folding labels under 5 samples into “rare” hides the small labels and fixes no spelling. It hides 18 labels with no other rule on and 10 with all of them on; the count under the button shows the number for your current choices.
- `build.py`
  - before: Anything typed by hand comes out in many spellings. A rule can fix a typo, but only someone who knows the field can say whether two labels mean the same thing. Course titles, school names and student names have the same problem. A wrong merge makes the data look cleaner while making it less true.
  - after: Anything typed by hand comes out in several spellings. Course titles, school names and student names do too.
- `build.py`
  - before: a team choosing the “rare” rule because the chart looks tidiest, or one that strips everything before a dash (right for one label, wrong for others, and just as tidy). The honest answer is “unresolved, ask someone in the field”, so say that out loud if a team gets there.
  - after: a team choosing the “rare” rule because it gives the shortest chart, or one that strips everything before a dash (right for one label, wrong for others). A team that answers “unresolved, ask someone in the field” has it right, so say that out loud.
- `build.py`
  - before: Each bar counts samples with that exact spelling.
  - after: Each tile counts samples with that exact spelling.
- `build.py`
  - before: WSe2 is the orange bar.
  - after: WSe2 is the orange tile.
- `build.py`
  - before: and a bar among 35 spellings.
  - after: and a tile among 35 spellings.
- `src/w_m05.js`
  - before: Each says where it goes.
  - after: Each shows where it goes.
- `src/w_m05.js`
  - before: No rule written from the text can say which of these name the same substance. / A rule that strips everything before a dash merges all four: right about one, wrong about the others, and just as tidy. / The mechanical mess is fixable by anyone. The rest needs someone who knows the field, or an honest “unresolved”. / Fifteen samples had nothing typed in the box at all, and no rule fixes those either.
  - after: Deciding which of these name the same substance takes someone who knows the field. / Stripping everything before a dash sends Mo-WSe2 to WSe2 (219 to 237 samples), 2H-MoS2 to MoS2 and MoS2-WS2 to WS2. It is right for one of them and wrong for the others. / Fifteen samples have nothing typed in the box, and all five rules leave them as they are.

## M-02 (filter)

- `build.py`
  - before: A Reasonable Rule That Deletes a Whole Method
  - after: A Common Filter That Removes Most of One Method
- `build.py`
  - before: A sensible-sounding filter can quietly delete most of one group.
  - after: One common filter removes most of one group.
- `build.py`
  - before: Dropping incomplete rows sounds neutral, but blanks are not spread evenly. If one group has more blanks, the filter quietly removes that group. In school data, “drop students with a missing score” can drop the students who were absent on test day, and nobody sees it happen.
  - after: Hybrid MBE loses 219 of its 233 samples to this filter and MOCVD loses 32 of 772. In school data, “drop students with a missing score” has the same shape when the missing scores belong to students who were absent on test day.
- `build.py`
  - before: Two growth methods. Their records are filled in unevenly, so the same filter cuts them by very different amounts.
  - after: Two growth methods. Their records are filled in unevenly.
- `src/w_m02.js`
  - before: ' almost disappears: only groups[worst].keep + ' of groups[worst].total + ' samples ( wp + '%) survive this rule.'
  - after: ': groups[worst].keep + ' of groups[worst].total + ' samples ( wp + '%) are kept.'
- `src/w_m02.js`
  - before: 'Both methods mostly survive. Now try requiring both.'
  - after: 'Both methods mostly stay. Try requiring both.'

## M-11 (extreme readings)

- `build.py`
  - before: An extreme value is either a real event or a mistake, and the data alone often cannot say which. Your choice changes the answer. The mean is the usual average and chases extremes. The median is the middle value and mostly ignores them. A district’s average days absent can swing on a handful of students.
  - after: Only one of the 66 readings has a known fault: sample 17458’s bad scan line. The mean is the usual average and moves with extreme values. The median is the middle value and barely moves. A district’s average days absent can shift on a handful of students.
- `build.py`
  - before: Roughness squares each gap from the average, so one extreme point counts for a lot. That is why the mean moves and the median does not.
  - after: Roughness squares each gap from the average, so one extreme point counts for a lot.
- `build.py`
  - before: So can a speck of dust the microscope tripped over.
  - after: So can a speck of dust on the surface.
- `src/w_m11.js`
  - before: Most films here measure under 1 nm. Every row is flagged for the same reason: 5 nm or more. Keep: it is a real reading, so it counts. Remove: drop it from the data. Fix: correct the value, which is only possible when you know exactly what went wrong. Here that is one row: sample 17458 (orange), whose scan has a corrupted line. Fixing it counts it at 0.80 nm instead of 6.10.
  - after: Most films measure under 1 nm. Every row here is flagged for the same reason: 5 nm or more. Keep counts it as read. Remove drops it. Fix corrects the value, and only sample 17458 (orange) has a known fault, one corrupted scan line. Fixed, it counts as 0.80 nm instead of 6.10.

## G-01 (trend line)

- `build.py`
  - before: A model summarizes a pattern. Ask how much it explains and what it leaves out.
  - after: Let’s fit lines to the records and check how much each one explains.
- `build.py`
  - before: The line rises about 0.06 nm per minute, yet explains only 2% of the variation (R² = 0.020). How steep it is and how well it fits are separate questions.
  - after: The line rises about 0.06 nm per minute, and growth time accounts for 2% of the variation in roughness (R² = 0.020).
- `build.py`
  - before: A line can be fitted to any cloud of dots, even a shapeless one, and it will always have a slope. R² says how much of the ups and downs the line actually accounts for. The same check applies to “more study time means higher scores” or “more absences means lower grades”.
  - after: R² is the share of the ups and downs in roughness that the line accounts for. Claims like “more study time means higher scores” or “more absences means lower grades” get the same check.
- `build.py`
  - before: because roughness is so skewed. That is a good advanced conversation, not the headline.
  - after: because roughness is so skewed. That is an advanced conversation.

## G-15 (check a claim)

- `build.py`
  - before: Claims in reports and in the news arrive as one tidy sentence. Checking one means asking what supports it, what cuts against it, and who was actually measured. Rewriting it is practice at saying only as much as the data can carry.
  - after: “Growing a film longer makes it rougher” is one sentence. Behind it are 754 samples, a slope of 0.06 nm per minute and R² = 0.020.
- `build.py`
  - before: The line runs through every film at once, so anything else that changes with growth time rides along with it.
  - after: The line runs through every film at once, so anything else that changes with growth time is mixed into the slope.
- `build.py`
  - before: Each box averages over whatever else differs between the groups, growth time included.
  - after: Each box pools films that differ in other ways, growth time included.
- `build.py`
  - before: The trend line lumps in everything that changes with growth time. Of the 754 samples on it, 740 are MOCVD, and the slope is about the same with MOCVD alone (about 0.06 nm per minute either way). So this line hardly mixes in method. It does mix in which material, which substrate and which project.
  - after: Of the 754 samples on the trend line, 740 are MOCVD, and the slope is about the same with MOCVD alone (about 0.06 nm per minute either way). Method barely varies along it. Material, substrate and project all vary.
- `build.py`
  - before: The group comparison lumps in growth time. Only 24 of the 233 hybrid MBE samples have a growth time recorded, and only 14 have both a time and a roughness. So you cannot check whether the method gap is really a growth-time gap. Among the 24 that were recorded, hybrid MBE growths were shorter (median 7 min vs 15 min for MOCVD), which if anything points the other way.
  - after: In the group comparison, growth time varies inside each box. Only 24 of the 233 hybrid MBE samples have a growth time recorded, and only 14 have both a time and a roughness. With 14, you can’t check whether the method gap is really a growth-time gap. Among the 24 that were recorded, hybrid MBE growths were shorter (median 7 min vs 15 min for MOCVD), which if anything runs the other way.
- `build.py`
  - before: Whichever comparison you choose, name what it lumps together. The honest fix is to compare like with like: same material, same time range. These records mostly do not allow it.
  - after: Whichever comparison you choose, say what it lumps together. Comparing like with like (same material, same time range) is the fix, and these records mostly have too few matching samples.

## G-06 (sampling)

- `build.py`
  - before: Bigger samples wander less, but an easy-to-take sample can be off target for good.
  - after: Bigger samples vary less. A sample of the easy-to-reach grains stays off target at any size.
- `build.py`
  - before: A sample is a small piece used to stand in for the whole. A bigger one gives steadier answers, but only if it is picked fairly. Surveying only the students who are easy to reach, such as those who answer email, can give a confident answer that is wrong.
  - after: Grains at the center have a median area of 1,526 nm² and grains toward the edge 2,792 nm², so a center-only sample is off target at any size. A survey of only the students who answer email has the same problem.
- `build.py`
  - before: The center’s median grain is 1,526 nm² and the edge’s is 2,792 nm².
  - after: *(removed)*
- `build.py`
  - before: Center-only and edge-only samples stay off target at any size; they just get more confident about the wrong answer.
  - after: Center-only and edge-only samples stay off target at any size, and their spread keeps shrinking around the wrong value.
- `build.py`
  - before: How Much Does One Sample Tell You?
  - after: How Close Is One Sample to the Whole?

## D-01 (dials)

- `build.py`
  - before: The same data can be taught simply or honestly. Each dial trades one for the other.
  - after: The same table can be taught simply or in full. Turning a dial changes what students see first.
- `build.py`
  - before: The simplest setting is easy to teach but promises what the data cannot keep. The full setting is honest but hard to start with.
  - after: The simplest setting shows 2 variables and a clean graph. The fullest shows all 8 variables with the mess and the noise left in, and is harder to start from.
- `build.py`
  - before: The same table can be shown in many ways, and each way hides something. Choosing what students see first is a teaching choice and a data choice at once. The dials make that trade visible: easier to start with, or more honest about the mess.
  - after: With the Provenance dial on “tidy it up”, sample 17458 leaves the table because it has no growth time. On “show the mess” and “show the noise”, it stays.
- `build.py`
  - before: whether missing values and odd spellings are shown or quietly resolved.
  - after: whether missing values and odd spellings are shown or resolved.
- `src/w_d01.js`
  - before: is a domain assumption no text rule can make, so it is your choice and starts off.
  - after: is a domain assumption, so it is your choice and starts off.
- `src/w_d01.js`
  - before: The source table stays fixed. The dials change which rows, columns and labels you meet first. This starting view is one designed presentation, not a neutral baseline.
  - after: The starting view is one designed presentation.
- `src/w_d01.js`
  - before: Typical-only hides everything above 10 nm.
  - after: Typical-only leaves out everything above 10 nm.
- `src/w_d01.js`
  - before: tidy it quietly (button label)
  - after: tidy it up

## Reflect

- `build.py`
  - before: There are no right answers. Disagreement is where the data literacy is.
  - after: There are no right answers.
- `build.py`
  - before: whether a line means anything. Those calls are the data literacy.
  - after: whether a line means anything.
- `build.py`
  - before: Dials: tidy settings quietly removed it.
  - after: Dials: tidy settings removed it.

## Primer cards

- `primer.py`
  - before: An atomic force microscope (AFM) does not use light. A very sharp tip on a tiny flexible arm is dragged across the surface, line by line, like a record-player needle.
  - after: An atomic force microscope (AFM) drags a very sharp tip on a tiny flexible arm across the surface, line by line, like a record-player needle.
- `primer.py`
  - before: Squaring means one extreme point counts for a lot. Round 1 shows exactly that.
  - after: Squaring makes one extreme point count for a lot. Round 1 shows an example.

## Cut list (sentences or clauses removed outright)

- **Warm up**: "it is the reason to measure" (teacher note tail)
- **W-01**: "Look at the data before you trust the summary." (takeaway kicker)
- **W-01**: "A summary number is a claim about the data, and it can be wrong." and "Looking at the raw picture first is the cheapest check there is."
- **W-01**: "not a flaw in the crystal" (figure caption); "the instrument misbehaving" (reveal line)
- **W-02**: "The tail is where the surprises are, and an average hides it."; "so you can see whether typical even makes sense"
- **W-02**: "not mistakes" (reveal line; the teacher note says some of the tail may be errors)
- **M-05**: "It makes the chart look cleanest, which is why it is worth pointing at." (rare-rule detail; the 18 and 10 stay)
- **M-05**: "A wrong merge makes the data look cleaner while making it less true."; "only someone who knows the field can say..." (the cards now show it)
- **M-05**: Reveal bullet "The mechanical mess is fixable by anyone. The rest needs someone who knows the field, or an honest unresolved" (duplicated the takeaway)
- **M-05**: "and just as tidy" (teacher note and reveal)
- **M-02**: "and nobody sees it happen"; "the filter quietly removes that group"; "Dropping incomplete rows sounds neutral"
- **M-02**: "so the same filter cuts them by very different amounts" (caption restated the chart)
- **M-11**: "That is why the mean moves and the median does not." (figure caption); "Your choice changes the answer."
- **G-01**: "How steep it is and how well it fits are separate questions." (takeaway kicker); "not the headline"
- **G-01**: "A line can be fitted to any cloud of dots..." in the why block (it repeated the point line)
- **G-15**: "Claims in reports and in the news arrive as one tidy sentence..." (replaced by the 754 / 0.06 / 0.020 instance)
- **G-06**: "A bigger one gives steadier answers, but only if it is picked fairly."; the median-area sentence moved from the detail into the why block
- **D-01**: "The dials make that trade visible: easier to start with, or more honest about the mess."; "The source table stays fixed..." caption (repeats the point line)
- **Reflect**: "Disagreement is where the data literacy is."; "Those calls are the data literacy."
- **Primer 3**: "An AFM does not use light." (negated opener; the schematic itself shows a laser)

## Part A: the M-05 cards

Six cards sit at the top of the M-05 panel, before the widget. Each shows one raw value as stored and its sample count, then one consequence with a number. All numbers are computed in `build.py` (`M05_CARDS`) by summing column 2 of `DATA["m05"]` rows that match the stated text; an assertion checks 334, 338, 5 and 34.

| card | raw value, samples | consequence | computation |
|---|---|---|---|
| same name twice | `SnSe; SnSe`, 12 | exact text SnSe gives 20; with repeats 34 | 20 (SnSe) + 12 (`SnSe; SnSe`) + 2 (`SnSe` x5) |
| same pair, two orders | `FeSe; FeTe` 2, `FeTe; FeSe` 1 | one order gives 2, both give 3 | 2 + 1 |
| a piece that isn't a name | `MoS2; 0`, 1 | exact MoS2 gives 334; with 3 repeated and this 1, 338 | 311 + 16 (C-Al2O3) + 2 (Scored c-Al2O3) + 5 (substrate typed twice) = 334; + 3 (`MoS2; MoS2`: 2 + 1) + 1 = 338 |
| substrate typed as the material | `Al2O3` 3, `GaAs` 2 | 5 samples sit under substrate names | rows whose material equals the substrate column exactly: 3 + 2 (matches the page's existing 1,000 vs 1,005) |
| 2H-MoS2 | `2H-MoS2`, 2 | the 338 MoS2 samples leave out these 2; inclusion is a field-expert call | 2 |
| Mo-WSe2 | `Mo-WSe2`, 18 | cutting before the dash moves 18 into WSe2, 219 to 237; right-or-wrong is a field-expert call | 17 + 1 (hexagonal BN substrate); WSe2 exact = 214 + 4 + 1 = 219 |

The 5 samples under 'substrate typed as the material' come from the same rows the existing page copy cites (1,000 vs 1,005). The M-05 reveal now states what a cut-before-the-dash rule does (Mo-WSe2 to WSe2, 2H-MoS2 to MoS2, MoS2-WS2 to WS2) instead of asserting that no rule can decide.

## Judgment calls and open points

- M-05 and the warm-up thread said "bar" for what is now a tile wall; changed to "tile" (counts unchanged).
- Titles changed because they broke the rule: "A Reasonable Rule That Deletes a Whole Method" (stance adjective, and 14 of 233 hybrid MBE samples remain, so "whole" was inaccurate) became "A Common Filter That Removes Most of One Method"; "How Much Does One Sample Tell You?" became "How Close Is One Sample to the Whole?". Button label "tidy it quietly" became "tidy it up".
- Kept as-is: "wander" (page term for sample-to-sample spread, used in chart labels), "Tidying" (a rule name), and the Ask-the-room questions.
- The G-15 "honest fix" and the teacher-note "honest answer" are gone. The new teacher line says a team that answers "unresolved, ask someone in the field" has it right.
- The W-02 reveal no longer says the tail values are not mistakes; the page says elsewhere that some may be.

## Applied after Codex review

Review: `voice-pass-review-codex.md`. Text shown with tags and entities stripped. G-06 means computed from the embedded data: center 1,469 (191 grains), edge 2,818 (104), all 501 = 1,889 nm² (Codex's figures confirmed). G-15: 756 + 143 = 899 measured MOCVD + hybrid MBE samples (confirmed); MOCVD median roughness 0.622 < hybrid MBE 1.471.

1. W-01 point: "Start with the image. Write what you notice before opening the measurement." W-01 why: "One roughness number summarizes the whole scan. Looking at the picture first is how we check what that number rests on. A teacher does the same with a class average: look at the grades before trusting it." W-02 task: "Start with the shape. Write what you notice before revealing the variable and unit." W-02 why: "A histogram shows every value at once, so we can check the shape before we summarize it. Attendance rates and test scores deserve the same look." Also (extension): W-01 figure caption now "A scan is built one line at a time, one pass of the tip per line." so it no longer foreshadows the bad line.
2. Takeaways kept, rewritten as interpretation. W-01: "The 6.10 nm comes mostly from one faulty line out of 512. The other 511 lines are still usable." W-02: "One typical value describes the big pile and leaves the far-out readings out. In round 2 you decide which of those readings to trust." M-02: "The same missing-value rule affects the two methods differently, because their records are filled in unevenly." M-11: "Removing the 66 readings changes the mean a lot and the median little, so the keep-or-remove decision matters most if you report the mean." G-01: "Growth time alone leaves most of the variation in roughness unexplained."
3. W-01 reveal line: "With the bad line included, the computed roughness is 6.10 nm; without it, the result is 0.80 nm." Reflection recap: "Notice: with one bad scan line included it reads 6.10 nm; without it, 0.80 nm."
4. M-11 why: "The mean is the usual average. It uses every value, so a few large readings pull it up. The median is the middle value and depends on rank, so extreme values change it much less." Panel point now "Removing extreme values changes the mean far more than the median." The RMS-squaring figure and caption were removed from M-11 (it explained the wrong calculation); the primer's roughness card keeps it, and its line "Round 1 shows an example" became "Squaring makes large gaps count for more."
5. M-11 more: "A scan can have RMS roughness near 92 nm because of real topography or contamination. The number alone does not distinguish them. Record your reasons, not just your tally."
6. G-06 why: "Mean grain area is 1,469 nm² at the center, 2,818 nm² toward the edge, and 1,889 nm² across all 501 observed grains, so a center-only sample is centered away from the all-grains mean at any size. A survey of only the students who answer email has the same problem." Teacher note: "...their spread keeps narrowing around the center mean or the edge mean, not the all-grains mean." (The `more()` details held no medians.)
7. Dial name "Statistical" kept. Dial question: "Which scans are included?" Buttons: "all recorded scans" / "5 µm scans under 10 nm" (the widget rule is scan size = 5 µm and roughness < 10 nm). Funnel step: "5 µm scans under 10 nm". Plot note: "This setting leaves out scans that are not 5 µm and readings of 10 nm or more." Dial help: "Statistical: which scans are included. One setting keeps every recorded scan. The other keeps only 5 µm scans under 10 nm." Takeaway: "The fullest shows all 8 variables, the mess, and every recorded scan, and is harder to start from." Why: "...With the Statistical dial on '5 µm scans under 10 nm', it leaves because it was scanned at 2 µm. On 'show the mess' and 'all recorded scans', it stays." Thread text: "Gone. The '5 µm scans under 10 nm' setting removed it: it was scanned at 2 µm." Provenance dial question "Mess shown or hidden?" became "Mess shown or tidied up?".
8. G-01 more: "Spearman's rank correlation is +0.29. Ranking reduces the influence of the largest roughness values, so it measures something different from the fitted line." Summary: "A rank-based measure, and who is missing".
9. G-01 teacher note: ""This fitted line explains about 2% of the variation in roughness" is a good sentence to write. If you mention Spearman, add that the rank-based association is modestly positive." Same overclaim in the Model lede fixed: ""The line explains about 2% of the variation" is a real finding."
10. G-01 more: "Missingness is not random: 251 samples lack growth time, roughness, or both. See M-02." Teacher note: "The other 251 lack a growth time or a roughness, and the gaps are not random; see M-02."
11. G-06 point: "Sampling variation decreases as n increases. A sample of only the easy-to-reach grains stays off target at any size." Takeaway: "As n increases, sample means narrow around the mean of the grains being sampled. For a center-only sample, that is not the all-grains mean." Verdicts: "Sampling variation decreases as n increases: the pile narrows around the mean of all 501 grains..." and "...Increasing n does not remove selection bias." Teacher: "watch the spread of sample averages narrow as n goes up."
12. "Sampling: the 501 measured grains came from three scans across its wafer."
13. M-05 rule note: "A real choice. It combines small groups under 'rare'." Details: "...combines the small labels into one category and fixes no spelling. It combines 18 labels with no other rule on and 10 with all of them on..." Widget: "would combine N small labels into one displayed category, and fixes 0 spellings".
14. "Deciding whether 2H-MoS2 belongs with MoS2 requires domain knowledge." / "Deciding whether Mo-WSe2 should count as WSe2 requires domain knowledge."
15. "Hand-entered labels often appear in several spellings." Takeaway: "Four rules fix the mechanical mess. Four labels still require domain knowledge. Until then, leave them unresolved."
16. W-01 reveal: "The stripe records a bad pass of the tip rather than a −455 nm surface feature. The remaining scan lines are still usable." Teacher note: "The fault is one line; the rest of the scan is usable."
17. Warm-up details: "A very sharp tip moves across the surface of a real film and records its height 250,000 times." W-01 reveal: "...a very sharp tip moves across the surface and records its height." Primer card 3: "moves a very sharp tip on a tiny flexible arm across the surface, line by line, like a record-player needle." Animation unchanged.
18. "The triangles are WSe2 crystal islands. WSe2 is studied for atomically thin transistor channels."
19. "These observational comparisons support associations, not causal conclusions. A good rewrite names who was measured and under what conditions."
20. "Among the 24 recorded hybrid MBE times, the median is 7 min, against 15 min for MOCVD. That points the opposite way from a growth-time explanation of the method gap, and 14 pairs are too few to say more."
21. "The page embeds the source records unchanged. Each activity states the filters or grouping rules it applies."
22. "A single layer is a semiconductor." / "Sample 17458 is WSe2."
23. Folded into 4 (M-11 why): "...it uses every value, so a few large readings pull it up... extreme values change it much less."
24. "Among the 899 MOCVD and hybrid MBE samples with roughness measurements, MOCVD films had the lower median roughness, but the groups were not grown or measured under comparable conditions."
25. "Model: no growth time was recorded, so the plot excludes sample 17458." D-01 in-table text: "Still in the table, but no growth time was recorded, so it is not plotted."

## Moral/hedge cut (2026-10-03)

Generator: `tools/messy_build/` (`build.py`, `primer.py`, `src/w_g15.js`). Rebuilt `investigation.html`.

### School analogies and morals (deleted)
- W-02 why: "...before we summarize it. Attendance rates and test scores deserve the same look." -> sentence cut.
- W-01 why: "One roughness number summarizes the whole scan. Looking at the picture first is how we check what that number rests on. A teacher does the same with a class average..." -> "One roughness number summarizes 512 scan lines."
- Warm-up why: "Schools do the same when they turn 'a good week' into an attendance rate." -> cut.
- M-05 why: "Course titles, school names and student names do too." -> cut.
- M-02 why: "In school data, 'drop students with a missing score' has the same shape..." -> cut.
- M-11 why: "A district's average days absent can shift on a handful of students." -> cut.
- G-01 why: "Claims like 'more study time means higher scores'... get the same check." -> cut.
- G-06 why: "A survey of only the students who answer email has the same problem." -> cut.

### Duplicated caveats (kept once, in the Reflect claims panel)
- Primer card 2: "Smoother is not automatically better: roughness is one quality measure among many." -> cut.
- Reflect: student panel "Three Claims We Are Careful Not to Make" / tag "keep these limits explicit" -> "Three claims these records don't support", no tag; one factual sentence per claim (device: "Nothing in these records connects roughness to device performance."; chips: "Nothing in these records shows that any sample became a chip."; cause: unchanged). Teacher "claims to correct" details deleted, including "Say so kindly..." and "which is still exciting".
- Session panel: "Before you start: the Reflect tab ends with three wrong claims..." -> cut.
- G-15 rewrite example: "A good rewrite names the population and the limit." -> cut (example kept). G-15 lede: "A good rewrite names who was measured and under what conditions." -> cut. "These are records, not a controlled experiment, so 'makes' is the wrong verb." kept.
- G-15 discussion: "Whichever comparison you choose, say what it lumps together. Comparing like with like... is the fix..." -> "Few samples share both material and time range, so a like-for-like comparison is not possible here."
- G-15 discussion: "...and 14 pairs are too few to say more" -> cut; "That points the opposite way from a growth-time explanation of the method gap" -> "That is the opposite direction from a growth-time explanation."

### Hedges, approval, reassurance
- "Record your reasons, not just your tally." -> cut.
- Reflect lede "There are no right answers." -> cut (lede now has no job line).
- Notice lede: "Let's look at the picture before we trust the number." -> "Let's look at the picture, then the number."
- Reflect Q1: "which extremes to trust, whether a line means anything" -> "which extremes to keep, how much a line explains".
- M-05 lede: "Others need someone who knows the field." -> "Four labels stay separate."
- Mo-WSe2 card: second sentence "Deciding whether Mo-WSe2 should count as WSe2 requires domain knowledge." -> cut (2H-MoS2 card keeps its sentence).
- Teacher notes cut: "A team that answers 'unresolved, ask someone in the field' has it right..."; "A team that can say what each setting costs has got the point of the session."; "Let that disagreement stand."; "Protect time for this one; ..."; "If you mention Spearman, add that the rank-based association is modestly positive."; "'This fitted line explains about 2%...' is a good sentence to write."
- W-02 teacher: "Some of it may be, and some is a genuinely lumpy film. Nothing in a histogram separates the two." -> "A histogram doesn't separate errors from rough films."
- G-01 teacher: "are let down by how loose the cloud is" -> "find a loose cloud".
- G-15 teacher: "rewrites that only soften the wording ('might make'). A good rewrite names who was measured..." -> "rewrites that only change 'makes' to 'might make'."

### Sweep (extra cuts)
- W-01 lede: "Spotting something the reveal skips counts as a win." -> cut.
- W-02 takeaway: "which of those readings to trust" -> "to keep"; M-11 title "Would You Trust?" -> "Would You Keep?".
- M-05: "No chemistry needed." (lede), "Nobody needs to know the chemistry." (teacher) -> cut. Takeaway: "Until then, leave them unresolved." -> cut.
- Primer card 1: "You don't need the chemistry. Treat each formula as a label." -> "Treat each formula as a label."
- M-11: summary "There is no answer key" -> "Why 92 nm is ambiguous".
- Session panel: "Teams can ignore them." -> cut.
- Left as is: G-15 takeaway "These observational comparisons support associations, not causal conclusions." (statement of what the method supports).
