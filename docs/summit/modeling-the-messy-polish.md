# Modeling the Messy: polish pass (investigation.html)

File changed: `epistemic-demo/materials-science/investigation.html` only (branch summit-fixes, not committed).
Build sources and test scripts: `/private/tmp/claude-501/-Users-giraffe-Code-camel/c2c16920-5a2f-406e-b581-7b4dc311830d/scratchpad/messy/` (`build.py`, `src/`, `verify.py`, `numbers.py`, screenshots).

## Page-wide changes
- Every tab opens with a point-first card: one plain sentence on what the round shows, then "Your job".
- Every activity: one-sentence point, one-line task, the demo, a blue "Takeaway" box. Longer detail moved into collapsible "More" disclosures.
- Inline-SVG icon sprite (no new dependencies): logo, tab icons, one icon per activity, icons on takeaways, claims and reflections. A clickable five-step session path on Warm Up replaces the timing table.
- One shared chart/control library replaces nine duplicate copies of the old one (page went from about 1.0 MB to 0.86 MB). Charts now draw at the container's real pixel width, so 12px labels stay 12px on a phone.
- No rotated labels anywhere: categorical charts are horizontal bars with labels on the left. Notes moved out of the SVG into captions. Text is truncated with an ellipsis rather than clipped.
- Controls are now big segmented buttons (or shortcuts) that redraw immediately. American spelling throughout (the old page mixed in none; I kept it consistent).
- All real data strings (9 embedded datasets plus the 3D scan items) are copied byte-for-byte from the old page; verified by substring match.

## Per tab
- **Warm Up.** Point: "Rough" is a word until you measure it. 3D surface picker restyled; live 3D now gets room to be 600px tall instead of overflowing. Stat tiles (1,005 / 899 / 1 nm) replace three paragraphs. The 1,000 vs 894 explanation is a disclosure. New "Follow one film: sample 17458" card (see item 2).
- **1 Notice & Wonder.** W-01: after reveal, a red box marks the bad scan line on the image, and a two-bar chart shows 6.10 nm vs 0.80 nm. W-02: reveal relabels the x axis "roughness (nm)" and writes "most films: under 2 nm" and "a long, thin tail" on the chart. Reveal text cut to short bullets.
- **2 Find the Mess.** M-05: rules are now per-rule segmented controls defaulting to "keep as typed", with a live "would remove N spellings" per rule, a big spelling counter, and one-click "Keep everything as typed" / "Turn on all five rules". The reveal shows four chips (MoS2 338, 2H-MoS2 2, MoS2-WS2 1, Mo-WSe2 18). M-02: segmented required / not required, horizontal bars with the pale total behind and "740 of 772 (96%)" written on the bar, axis fixed at 772, a live one-line verdict. M-11: the old box plot (rotated labels, 340px wide) became a before/after dot chart for mean and median on a fixed 0-2 nm axis, plus number cards; shortcuts "Remove all 66", "Remove the 10 roughest", "Clear"; table sorted roughest first; the repeated "why flagged" column is now one caption.
- **3 Model It.** G-01: show/hide line, three color modes, slope in plain words, an R-squared meter ("explains about 2%"), and a note that sample 17458 is one of the 251 undrawn samples. G-15: claims are two big buttons, evidence is two side-by-side For / Against boxes, drafts persist per claim, a model rewrite sits in a disclosure. G-06: see item 3.
- **4 Turn the Dials.** Dials are three labelled segmented controls in plain words ("show the mess" / "tidy it quietly"). New step chart shows samples left after each step (1,005 to 752 to 650). Scatter axes frozen so settings compare. Live line tracks sample 17458.
- **Reflect.** Questions shortened with icons. New "Our Film's Journey" recap. Careful-claims list shortened.

## The four meeting items, and how I read them
1. **Misspellings cleaning-rule controls default to "keep".** Read as the five M-05 rules. Each is now an explicit "keep as typed" | "merge" choice that starts on keep (the old toggles started off but never said so). I did not change D-01's Provenance dial default ("tidy it quietly", the original starting point); if Kathy meant that dial too, it is one line (`st.provenance`) in the D-01 script.
2. **Thread the material through the exercises.** Read as: one continuing story. I found that the W-01 scan, the M-11 row 17458 (6.096 nm, 2 um scan), and the G-06 wafer are all sample 17458, a WSe2 film (confirmed against the data and `student-demo-paths.md`). It is introduced on Warm Up, then appears in every round: W-01 reveal, WSe2 in orange in M-05, a note in M-11, "not drawn" in G-01, the G-06 wafer, a live tracker in D-01, and the Reflect recap. The Warm Up 3D scans stay three other materials, as in the original.
3. **Sampling visuals: frozen x axis.** Read as G-06's histogram. It already froze the axis per spot; now one fixed range (0 to 5,000 nm squared) is used for every spot and every n, so any redraw is comparable, and the caption says so. It also marks the whole-wafer mean always, plus the spot mean when you sample a single spot. I also froze axes in D-01 and M-02/M-11 for the same reason. The y axis of the histogram still rescales.
4. **One color when few variables.** Read as: color only encodes something when there is something to encode. All charts are single blue. D-01 colors by material only when material is one of the variables shown (6 or 8 variables); with the 2-variable setting everything is blue and a note says why. G-01 defaults to one color, with optional "WSe2 highlighted" (orange vs light blue) and "by material". Orange is reserved for the thread (WSe2 / sample 17458) and red for the fit line and the bad scan line.

## Numbers
All data and fact-checked numbers unchanged. Re-derived live and matched to the crib: 754 plotted / 251 left out, slope +0.059, R-squared 0.020, 740/772 and 14/233, MOCVD median 0.62 vs hybrid MBE 1.47 (756 vs 143 measured), mean 1.83 to 1.01 and median 0.74 to 0.66 when all 66 are removed, 35 to 25 spellings, sampling theory 592 at n=3.
Possible issues, not changed:
- The facilitator crib says D-01's structural dial runs "from one to all nineteen" variables; the widget only has 2 / 6 / 8 columns (I labelled it that way).
- D-01's "tidy it quietly" merges `2H-MoS2` into `MoS2` (and takes the first name before a semicolon), which is exactly the domain judgement M-05's reveal says rules cannot make. It is in the original; left as is.
- The old M-11 chart note read "36 of 1854 samples", counting the same samples in several groups. Gone with the redesign.

## Verification (WebKit via Playwright, 1280px and 390px, all 6 tabs)
- Console/page errors: 0 at both widths. Horizontal page overflow: 0. Overlapping or clipped chart text: 0 after clicking every control (218 clicks on Find the Mess, including each of the 66 x 3 table buttons, every select option, slider min/mid/max, both reveals).
- Method: the CLAUDE.md overlap detector, i.e. pairwise `getBoundingClientRect()` of every SVG `<text>` plus a check against the SVG bounds and the viewport.
- Earlier runs found and I fixed: bars missing in the new horizontal bar chart (array reassignment bug), clipped labels at 390px (long bar labels, an axis title, median and mean marker labels), a truncated W-01 bar label.
- Main-path paragraphs: all at or under about 25 words except the closing "Go further" line (28).
- The 3D warm-up draws live in WebKit (network was available).
- Not verified: real iPhone Safari; the old page's WebGL one-at-a-time behavior is unchanged.

## Unsure / left alone
- "Thread the material" is my interpretation. A different reading is "use one material for every chart"; the data do not allow that (M-02 and G-15 compare methods, not materials).
- The headline "most important" badge on M-02 comes from the old page's text and the crib.
- I did not touch `student-demo.html` or any other file.

---

# Second pass: context primer, live 3D only

Wes's feedback: not enough context for high school math teachers, and the 3D still images must go. Same constraints: only `investigation.html`, no data changes, nothing committed.

## 1. 3D warm-up is live only
- The still PNGs and the "Spin it in 3D" button are gone, and the three base64 3D placeholder images were deleted from the page (about 12 KB). The 3D scan surfaces themselves are unchanged (z arrays checked byte-for-byte). The W-01 microscope image is a real data image, not a placeholder, so it stays.
- One Plotly viewer draws as soon as Warm Up is shown. The pyramids / city blocks / almost flat buttons purge the old surface and draw the next. Exactly one canvas exists at any time (checked at 1280 and 390).
- The loader fetches Plotly on page load. If it fails, one line replaces the box: "The 3D viewer could not load (it needs an internet connection). Everything else on this page still works." (tested by blocking the CDN). A lost WebGL context shows a one-line "tap a surface button to redraw" message.
- Colors: the saturated yellow came only from the old still images. The live surfaces already carried a 1st to 99th percentile color range. I kept that range, so the bumps show on a viridis scale. The vertical stretch (25x) is the same for all three, as before. I added fewer z-axis ticks (they crowded each other) and a two-line, smaller title on phones (it was clipped at 390px).

## 2. Context primer ("What am I looking at?")
- Five cards at the top of Warm Up, each with a numbered badge and a simple inline-SVG diagram, written for someone with no science background:
  1. **What the materials are:** 2D materials, graphene, formulas as labels, a bulk-vs-2D-vs-graphene atom diagram, and a collapsible table of all 11 formulas (MoS2, WSe2, WS2, MoSe2, GaSe, InSe, In2Se3, SnSe, SnTe, Bi2Se3, FeSe) with plain name and "why anyone cares". Reassurance line: "You don't need the chemistry. Treat each formula as a label."
  2. **Why grow them, why smooth matters:** substrate, vacuum chamber, MOCVD (gas, "frost on a window") vs MBE (beams) vs hybrid MBE, growth time. Diagram of both methods.
  3. **How the microscope works:** AFM as a sharp tip on a flexible arm dragged line by line like a record-player needle; color means height; scan size. Diagram of tip, arm and surface, plus a scale strip (hair about 70 um, then scan patch 2 to 5 um, then bumps about 1 to 10 nm; marked not to scale).
  4. **What roughness is:** RMS roughness = standard deviation of the heights in the scan, with the formula and a height-profile diagram (dashed average, red gaps). Notes that squaring lets one extreme point count a lot.
  5. **What one row is:** three real rows pulled from the embedded data (samples 17207, 17458, 23056) with each of the 8 columns explained in plain words; "blank" marks missing values.
- The same cards open in a drawer from a floating "What am I looking at?" button that is on every tab. The drawer closes with a Close button, a click outside, or Esc. Links such as "MOCVD or hybrid MBE" or "AFM" inside activities open the drawer at the matching card.

## 3. "What you're looking at" captions
Every activity has a one-to-two-sentence caption under its point, with first-use definitions and primer links: 3D scans, W-01, W-02, M-05, M-02, M-11, G-01, G-15, G-06, D-01. Examples:
- W-01: "An AFM height map of a WSe2 (tungsten diselenide) film: each bright triangle is a tiny crystal island. Color shows height."
- W-02: "Each bar counts films by roughness, the typical bump height. The unit stays hidden until you reveal it."
- I also replaced the old word "disc" with "substrate (the flat base)" everywhere, and wrote WSe2 as WSe<sub>2</sub> in prose.

## Verification (WebKit, 1280px and 390px)
- Full pass on all six tabs, every control clicked: 0 console errors, 0 page overflow, 0 overlapping or clipped chart text. The same overlap detector also ran over the open drawer on every tab at both widths: 0 issues. The drawer opens, closes via Close and via Esc, and an in-page link opens it scrolled to the right card.
- Numbers re-derived from the data after the change still match: 754 / 251, +0.059, 0.020, 740 of 772 vs 14 of 233, medians 0.62 vs 1.47, mean 1.83 to 1.01 and median 0.74 to 0.66, 35 to 25 spellings.
- All nine embedded datasets are still byte-identical to the original page.

## Judgment calls and open points
- **W-01 caption:** Wes's example included "the dark horizontal stripe is one bad scan line". W-01 is a "look first" activity, so the caption does not name the stripe up front; the reveal does (with the red box). Easy to add if he wants it given away.
- **"Bumpy layer makes a worse device":** I wrote "a smooth layer is easier to build devices on, so labs track roughness", plus a note that smoother is not automatically better. The facilitator crib and the Reflect tab both say not to claim smoother means a working device.
- **Primer "why anyone cares" lines** are from general knowledge, not the data (for example, SnSe turns heat into electricity; Bi2Se3 conducts on its surface). Worth a quick check by Reinhart group before the summit. The hair width (about 70 um) is the coordinator's figure.
- Primer diagrams use small text; on a phone they sit in a side-scrolling figure so the text stays readable (the page itself never scrolls sideways).
- Main-path captions run about 25 to 28 words, a little over the earlier 25-word rule.

---

# Third pass: fixes from the Codex review (section B)

Same constraints (only `investigation.html` plus the two crib edits; no data changes; nothing committed).

| # | Finding | Status | What changed |
|---|---|---|---|
| 1 | G06 theory ignores sampling without replacement | Fixed | Theory is now sigma/sqrt(n) x sqrt((N-n)/(N-1)), with sigma the standard deviation of the N grains actually sampled (501, or the center/edge/flat subset). The readout ("theory says") and the spread-vs-n curve both use it, and a caption says why. At n = 3, 5, 10, 20, 40, 60 theory is 590, 456, 321, 225, 155, 124 for all grains; the simulated spreads sit on it. |
| 2 | G06 "whole-wafer" / "true mean" | Fixed | Now "all 501 grains" for the sample-from choice, "all-grains mean" on the chart, "mean of all 501 grains" in the verdict; spot marks read "center-spot mean" and so on. Takeaway says "stays away from the all-grains mean". |
| 3a | D01 "Nothing about the data changes" | Fixed | Point and footer now say the source table stays fixed while rows, columns and labels change, and the default view is framed as a designed presentation, not a neutral baseline. |
| 3b | D01 silent 2H-MoS2 merge | Fixed | The old "keep the first name before a semicolon, and fold 2H-MoS2 into MoS2" is gone. "Tidy" now uses only Find the Mess's mechanical rules (drop a non-name piece, collapse a repeated name, sort a list). A fourth control, "A judgment call: is 2H-MoS2 the same as MoS2? keep separate / treat as MoS2", starts on keep separate, with a caption pointing to M-05. G-01's "color by material" had the same hidden merge and now uses the same mechanical rules. Counts (1,005 / 752 / 650) are unaffected. |
| 4 | W01/W02 takeaways visible before reveal | Fixed | Both takeaways are hidden until "Show what this is" is clicked (checked: hidden before, shown after). |
| 5 | G01 "nearly flat" | Fixed | Now: "The line rises about 0.06 nm per minute, yet explains only 2% of the variation (R2 = 0.020). How steep it is and how well it fits are separate questions." |
| 6 | M11 controls off-screen on phones | Fixed | The keep/fix/remove column is now first, and below 520px each row becomes a labeled card with the buttons on top (plus a "Sort by" menu, since card rows have no header). |
| 7 | Tab strip on phones | Fixed | Below 600px the tabs wrap into a 2-column grid, so all six are visible at once; the active one is tinted. |
| 8 | G15 For/Against | Fixed | Boxes stack below 520px (they only wrapped by accident before). |
| 9 | M05 live counts | Fixed | "given your current choices" now sits on the big counter and on every per-rule count. |
| 10 | Crib | Fixed | `facilitator-crib.md`: roughness count reads "899 (894 after the 5 invalid records are set aside)"; the D01 structural dial reads "2, 6 or all 8 columns". |

Also: the floating "What am I looking at?" button is now an icon-only circle on phones (it was covering table buttons).

Interpretation note on #1: I used Codex's formula with sigma as the standard deviation of the N grains (divide by N), which is the exact finite-population result; using the n-1 standard deviation would be slightly off.

Verification (WebKit, 1280px and 390px): all six tabs, every control clicked (223 clicks on Find the Mess at 390px, including the new cards, Sort menu and judgment-call dial): 0 console errors, 0 page overflow, 0 overlapping or clipped chart text. Drawer: opens, closes with Close and Esc, deep links work, 0 overlap on every tab. Live 3D: one canvas, swaps cleanly, one-line message when the CDN is blocked. All 9 datasets still byte-identical; the previously checked numbers (754/251, +0.059, 0.020, 740/772 vs 14/233, 0.62 vs 1.47, 1.83 to 1.01 and 0.74 to 0.66, 35 to 25, 1,005 to 752 to 650) still hold. One overlap found along the way (long G06 marker label on 390px) was fixed and re-checked.
Not done: the "open D01 on surface choices by default" suggestion (listed as nice-to-have); I framed the default view instead. Real-device Safari is still untested.
