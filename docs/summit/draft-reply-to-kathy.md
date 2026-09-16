# Draft reply to Kathy Hill (not sent)

Subject: Re: Data Literacy Summit — here is the session page, built

Kathy,

Glad you said that about CODAP, because we would rather build it. Here is the page, built
against your deck and ready to try on your phone right now:

**https://colab.research.google.com/github/reinhart-group/camel-2dcc/blob/summit-menu/notebooks/summit/modeling_the_messy.ipynb**

That is the whole thing teams need. No Google account, no sign-in, no installation, nothing to
run. It works on a phone in Safari in a private window with nothing signed in. One link and one
QR code for slide 14.

It follows your session design as written: a 5-minute warm-up, then your four rounds at 5, 10, 12
and 8 minutes, in your order, with your language. What is in each round:

- **Warm up.** Three real microscope scans a team can spin with a finger — a field of crystal
  pyramids, a superconductor that grew in rectangular blocks, and a film so flat that its typical
  bump is two atoms wide. All stretched vertically by the same amount, so the comparison is fair.
  It ends on the question the rest of the session answers: what would you measure to turn "rough"
  into a number?
- **Round 1, notice and wonder.** An unlabelled microscope picture, then the same collection as an
  unlabelled pile of 894 numbers. The picture has a real instrument glitch in it, and teams find
  it. That glitch inflated the recorded roughness for that sample from 0.80 nm to 6.10 nm, and the
  wrong number is still in the table.
- **Round 2, find the mess.** Thirty-five hand-typed spellings of the material name to sort (no
  chemistry needed — every spelling has a plain-English gloss); then the one we would protect time
  for, where a reasonable-sounding rule, "only use samples where both values were recorded", keeps
  740 of 772 samples from one growth method and 14 of 233 from the other; then the extreme
  readings, where marking rows for removal moves the mean from 1.83 to 1.01 nm and the median
  barely at all.
- **Round 3, model it.** Fit a line and read its slope and R², which is 0.020 — growth time
  explains about 2% of the variation, and a team that reports "we found almost nothing" has got it
  right. Then a claim-checking tool that shows the evidence on both sides and asks for a rewrite.
- **Round 4, turn the dials.** Your three dials — structural, provenance, statistical — over the
  same table and the same graph, so the room sees that nothing about the data changed and only the
  entry point did.

Two things to go with it:

- **A facilitator crib** (`docs/summit/facilitator-crib.md`): what teams typically find in each
  round, every number they will see on screen, and the three claims to correct if you hear them.
- **Replacement text for the Dataset B card** on slide 15 (`docs/summit/dataset-b-card.md`). The
  drafted card promises measured grain area for each sample; we have grain measurements for two
  wafers, not the collection. The measurement that works across everything is surface roughness.
  The replacement says what is really in the file and what to watch for. It is yours to edit.

Nothing here is precious. The session page was chosen from a menu of forty activities, which is
still there at `notebooks/catalog/` if you want to swap any of them — every item has an ID, and
telling us "drop M-11, use G-16 instead" is a five-minute change. Tell us what is wrong with it
and we will rebuild it.

A few notes on the data, so the slides stay accurate:

- The mess is real and we added none of it. There are 35 different spellings of the material
  names, including a few where a substrate name was typed into the material field; 228 samples
  have no growth time recorded and 106 were never measured; roughness runs from 0.10 to 92
  nanometres; and some scans stopped early.
- One honest caution for the framing: nothing in these records shows that these samples became
  chips, or that a smoother film makes a better device. The accurate line is that 2D materials are
  being researched as candidates for future electronics.

Two things we still need from you:

1. The date of the summit and your deadline for the deck.
2. Whether we may replace the Dataset B card as above.

Wes and Becca
