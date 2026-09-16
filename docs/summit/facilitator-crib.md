# Facilitator crib — "Modeling the Messy", Breakout 1

For Kathy and anyone helping run the room. Written 2026-09-16 against the built page.

**The page teams use:** `notebooks/summit/modeling_the_messy.ipynb`
https://colab.research.google.com/github/reinhart-group/camel-2dcc/blob/summit-menu/notebooks/summit/modeling_the_messy.ipynb

One link, one page, four rounds in your deck's order and timings. It needs no Google
account, no sign-in and no runtime. It works on a phone in Safari in a private window.
Nothing on the page needs to be run; the run buttons are inert and teams should ignore
them.

## What the data are

Penn State's 2D Crystal Consortium grows crystal films two or three atoms thick. These
are their real records, pulled from the LiST sample database.

| | |
|---|---|
| Grown samples | 1,005 |
| Samples with a roughness measurement | 894 |
| Samples with both a growth time and a roughness | 754 |
| Distinct hand-typed spellings of the material | 35 |
| Distinct microscope scan sizes | 15 (709 of them at 5 µm) |
| Roughness range | 0.10 to 92.0 nm, median 0.74 |
| Growth methods | MOCVD and hybrid MBE |

A few activities first drop the 5 rows whose "material" field actually holds a substrate
name, so their counts read 1,000 samples and 894 measurements instead of 1,005 and 899.
Both are stated on the activity itself.

Roughness is how bumpy the surface came out, in nanometres. Smaller is flatter. It is the
one outcome measured on nearly every sample, which is why the whole session turns on it.

## Round by round

### Warm up · 5 min — three real scans in 3D

Three surfaces a team can spin with a finger: Bi2Se3 pyramids, FeSe blocks, and an
almost perfectly flat SnTe film. All three are stretched 25× vertically by the same
amount, so the comparison is fair.

**Where it goes:** teams say "the first one is rough and the last one is smooth" without
prompting. The question to ask next is the one the whole session answers: *what would you
measure to turn that word into a number?* That number is roughness, and it is the column
every later round uses.

**If it does not draw:** the still picture is real and the activity still works. The 3D
view fetches a drawing library from the internet; a blocked conference network stops it.
There can only ever be one live 3D view on the page — tapping a different scan tears the
previous one down on purpose. That is a browser limit, not a bug.

### Round 1 · 5 min — notice and wonder

**W-01, the picture.** A 2 µm AFM scan of WSe2 triangles. Teams notice the triangles.
Some notice the dark horizontal stripe about a third of the way down.

That stripe is the payoff. It is one corrupted scan line out of 512, dipping to −455 nm,
and it is an instrument fault, not the crystal. The recorded roughness for this scan is
**6.10 nm**. Drop that single line and it is **0.80 nm**. One bad line in 512 multiplied
the headline number by more than seven, and that number is sitting in a table right now.

**W-02, the numbers.** The same collection as an unlabelled histogram: a tall spike near
zero and a long thin tail. Teams reliably say "most are the same and a few are way out."
Both halves of that sentence matter later — the spike is round 3's problem and the tail
is round 2's.

**Watch for:** a team that decides the tail must be errors. Some of it is. Some of it is
a genuinely lumpy film. Nobody in the room can tell which from the histogram alone, and
that is the point of round 2.

### Round 2 · 10 min — find the mess

**M-05, one text box with thirty-five answers.** Teams switch general cleaning rules on
and off and watch a bar chart of samples per label tidy up. Nobody has to know what any
of these substances are: every rule is decided from the shape of the text, or by noticing
that two columns of the same row hold the same word.

What each rule does, in the order they appear:

| Rule | Distinct spellings | What it catches |
|---|---|---|
| none | 35 | |
| the same name typed twice | 30 | `SnSe; SnSe`, `MoS2; MoS2` |
| the same list in a different order | 28 | `FeSe; FeTe` and `FeTe; FeSe` |
| a piece that isn't a name | 27 | `MoS2; 0` |
| the value matches this row's "grown on" column | 25 | 5 rows set aside |
| fold labels under 5 samples into "rare" | 25 | hides 10 labels, changes nothing |

The last rule is deliberately the one that tidies the chart most and fixes nothing. It is
worth pointing at.

**The punchline, which the reveal button gives them:** after every rule, `MoS2` (338
samples), `2H-MoS2` (2), `MoS2-WS2` (1) and `Mo-WSe2` (18) are still four separate labels.
They look related, and no rule written from the text can tell you which of them name the
same substance. A rule that stripped everything before a dash would merge all four, would
be right about one and wrong about the others, and the chart would look equally tidy
either way.

So the mechanical mess is fixable by anyone, and the rest needs someone who knows the
field. If you do not have that person, the honest move is to report the labels as
unresolved rather than to pick a rule that looks tidy. That is the transferable lesson and
it is the one to name out loud if a team gets there.

**M-02, the rule that deletes a method.** This is the strongest single finding in the
dataset and the one to protect time for.

"Only use samples where both the growth time and the roughness were recorded" sounds like
basic hygiene. Applied here it keeps **740 of 772 MOCVD samples and 14 of 233 hybrid MBE
samples**. A comparison of the two methods built from "complete" rows would barely contain
the second method at all, and nothing in the resulting chart says so.

**The question to ask:** what does your own student information system do when a field is
blank, and is it blank at random?

**M-11, extreme values (optional).** The 66 samples measuring 5 nm or rougher. Teams mark
each keep, fix or remove and watch the whole dataset's mean and median move. Removing all
66 moves the **mean from 1.83 to 1.01 nm** and the **median only from 0.74 to 0.66**.
That contrast is the lesson and it is visible on the chart, not asserted.

If a team saw the glitch line in W-01, point out that they have already met one of these
rows.

### Round 3 · 12 min — model it

**G-01, growth time against roughness.** 754 points, and the honest result is a
disappointment: the least-squares line has a slope of **+0.059 nm per minute** and an
**R² of 0.020**. Growth time explains about 2% of the variation in roughness.

The rank correlation is stronger (Spearman +0.29) because the roughness values are so
skewed, which is a good advanced conversation but not the headline. The headline is that
a team can fit a line to anything and the line means almost nothing here.

**Watch for:** teams reading the fitted line as a result. Ask how many of the 1,005
samples are in the picture. The answer is 754, and the 251 that left did not leave at
random — see M-02.

**G-15, check a claim.** Two claims, both of which teams tend to believe. The tool shows
the evidence on both sides, including how much data is missing, and asks for a rewrite.

- *"Growing a film longer makes it rougher."* The association is real and tiny, and
  "makes" is the wrong verb for observational records.
- *"MOCVD makes smoother films than hybrid MBE."* MOCVD's median roughness is 0.62 nm
  against hybrid MBE's 1.47 nm, so the gap is real in these records. But the two groups
  were grown for different projects, on different substrates, measured at different scan
  sizes, and the hybrid MBE group has 143 measured samples against MOCVD's 756. It is a
  lopsided observation, not a trial.

A good rewrite names the population and the limit: *"Among the samples 2DCC happened to
measure, MOCVD films were typically smoother, but the two groups were not grown or
measured under comparable conditions."*

**G-06, sampling (optional).** Draw samples of n crystals from one wafer and watch the
spread of sample means narrow as n rises. Observed spreads track the theory closely: 592,
470, 315, 219, 154 and 122 nm² at n = 3, 5, 10, 20, 40 and 60. It also offers sampling
from only the wafer's center or only its edge, which is what a convenient sample costs —
the center's median grain is 1,526 nm² and the edge's is 2,792 nm².

### Round 4 · 8 min — turn the dials

**D-01** puts your three dials over the same table and the same graph. Nothing about the
data changes; only what a student meets first.

- **Structural** — how many variables are in front of them, from one to all nineteen.
- **Provenance** — whether the missing values and the odd spellings are shown or quietly
  resolved.
- **Statistical** — whether the noise and the outliers are left in.

**The question that lands:** what did you give up at the setting you chose? The simplest
version is easy to teach and makes a promise the data cannot keep. The full version is
honest and hard to start with. Teams who can name the trade rather than pick a side have
got the session.

## Claims to correct if you hear them

Teams reach for these, and all three are wrong.

1. **"So these are the chips in AI data centers."** No. Nothing in these records shows
   these samples became chips. 2D materials are *researched* as candidates for future
   electronics. That is the accurate sentence and it is still exciting.
2. **"Smoother is better."** Roughness is one quality measurement among many. Nothing
   here connects it to whether a device works.
3. **"Longer growth causes rougher films."** Every relationship on the page is an
   association in observational records of experiments never designed to be compared.

## Practical notes

- **Devices.** One phone or iPad per team is enough. The page is about 1 MB; if the venue
  network is slow, ask teams to open it during the 15-minute framing section rather than
  at the start of the hands-on block.
- **Run buttons.** A signed-in Google user who taps one will be asked to connect a
  runtime, and if they do, the activity below that cell will be replaced by nothing. Tell
  the room once: nothing on this page needs to be run.
- **Offline.** Everything except the 3D view works with no internet once the page has
  loaded.
- **Teachers who want the code.** `notebooks/python_demo.ipynb` rebuilds several of these
  activities in about a dozen lines of Python each, and is the honest answer to "where
  does this go in a high school CS class". It needs a Google sign-in.
- **The full menu.** `notebooks/catalog/` holds all forty items across the four rounds,
  including the ones not chosen for this page.
