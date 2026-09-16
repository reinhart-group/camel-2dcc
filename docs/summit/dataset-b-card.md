# Replacement text for the Dataset B card (slide 15)

The card in the received deck promises "growth sequence, element ratio, and measured grain
area for each sample". That was drafted before anyone saw our files. Grain areas exist for
two wafers, not for the collection, so the measurement that works across every sample is
surface roughness. Everything below was checked against the files on 2026-09-16.

---

## Dataset B — Growing tiny crystals

**Penn State 2D Crystal Consortium · 1,005 samples · real, uncleaned records**

**The question:** these films are grown two or three atoms thick as candidates for future
electronics. Do the settings the scientists chose have anything to do with how smooth the
film came out?

**What is in the file:** one row per grown sample. Each row holds the recipe settings —
material, substrate, growth method, how long it grew, at what temperature and pressure —
and, where the sample was later put under a microscope, one measurement of surface
roughness in nanometres.

**What to watch for:**

- 106 samples were never measured, and 228 have no growth time recorded. The missing
  values are not missing at random: requiring both leaves 740 of 772 samples from one
  growth method and only 14 of 233 from the other.
- The material name was typed by hand. There are 35 different spellings, a few of which
  name the disc the crystal was grown on rather than the crystal, and thirteen of which
  name two materials at once.
- Roughness runs from 0.10 to 92 nanometres with a median of 0.74, so the average and the
  middle tell very different stories.
- Roughness depends on how large an area the microscope scanned, and 15 different scan
  sizes appear in the file.

**What the data cannot tell you:** whether any of these samples became a computer chip,
and whether a smoother film makes a better device. Every pattern in the file is an
association in records of experiments that were never designed to be compared.

---

## Suggested wording for the slide 14 link

> **Everything you need is one link. No account, no sign-in, no installation.**
> Works on a phone.

Link and QR target:
https://colab.research.google.com/github/reinhart-group/camel-2dcc/blob/summit-menu/notebooks/summit/modeling_the_messy.ipynb
