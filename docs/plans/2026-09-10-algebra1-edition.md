# Algebra 1 edition — conventions

Audience: a typical 9th-grade Algebra 1 student (and their teacher) with no chemistry or physics
background and no coding experience. The existing notebooks 00–07 become the **Explorer edition**
(Algebra 2 / Geometry / Statistics / stronger classes). The Algebra 1 edition reuses the same data
slice and setup cell; only the text, tasks, and amount of science change.

## Rules

1. **Math first.** Every section starts from the math idea (ratio, rate, slope, mean). The science
   is the story that makes the numbers interesting — one or two sentences, never the lesson.
2. **Reading level ≤ grade 8** (Flesch–Kincaid grade of all markdown, checked with
   `scripts/readability.py`). Sentences mostly under 15 words. Second person ("you").
3. **At most one new science word per section**, always with a picture or an everyday comparison
   ("a layer of crystal about as thin as ... "). Never use: band gap, exciton, quasiparticle, Bragg,
   epitaxy, chalcogenide, stoichiometry, Tc, cryogenic, dielectric, lattice constant.
   Allowed with a one-line meaning: atom, crystal, layer, microscope, nanometre, semiconductor,
   computer chip, superconductor, resistance.
4. **No code reading required.** Students press ▶, move sliders, or type a number where it says
   `# ✏️ type your answer here`. Helper code sits in collapsed `# @title Helper code (just run this)`
   cells. Every answer cell has a check that says "✅ Nice!" or gives a hint — never just "wrong".
5. **Short.** 30–40 minutes: a hook picture, 4–6 tasks, an exit ticket of 2–3 questions answerable
   without the computer. One idea per task.
6. **Numbers kids can hold.** Round to friendly numbers in the text; show scientific notation only
   next to the ordinary number (5,000 nm = 5 × 10³ nm). Always give units in words and symbols.
7. **Every picture is readable on its own**: big labelled axes with units, a title that is a
   sentence ("The furnace heats up for 17 minutes"), colour-blind-safe colours.
8. **Honest but light.** Real data is messy; say so in kid language ("real measurements are a little
   bumpy"). Never claim more than the data shows. No hype about AI or products.
9. **Standards:** Algebra 1 CCSS only — N.Q.1–3, A.SSE.1, A.CED.1–2, A.REI.3, F.IF.4–6, F.LE.1–2,
   S.ID.1–3 (and 7.RP ratios as review). Each teacher guide maps tasks to codes.
10. **Teacher guide** (`notebooks/algebra1/teacher/`): one page — goals, timing, answers (computed
    from the executed notebook, as ranges), 3 common mistakes, and "if you have 10 more minutes".

## Files

`notebooks/algebra1/src/A1_*.py` (jupytext percent) → `notebooks/algebra1/A1_*.ipynb`.
Verify with `scripts/run_notebook.py` and `scripts/readability.py`.
