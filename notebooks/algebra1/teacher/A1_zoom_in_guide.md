# Teacher guide — Zoom In! How Small Is a Nanometre?

**Standards:** N.Q.1–3 (units, scale), 7.RP review (ratios/proportions), A.CED.1 (one-step
equations), A.SSE.1 (interpreting scale-factor expressions).

**Time:** 30–40 minutes (Task 5 is optional; drop it if short on time).

## Goals
Students convert between metre/mm/µm/nm, use a ratio to compare sizes, and compute a scale
factor to connect a microscopic crystal scan to a human-scale object (a soccer field, 100 m
long).

## No code on screen
Every step in this notebook is a Colab **form cell**: students see a grey bar with a title, a
▶ button, and any boxes they need to fill in. The Python is hidden. To read or edit the code
for a step, double-click its grey bar; to hide it again, use Cell > Form > Hide code.

Students answer in the boxes, not in code:
- **Task 2** is a number box. Type 5000 and the step re-runs itself.
- **Tasks 3 and 4** are text boxes that take a **formula**, e.g. `hair_um / scan_um`. The
  notebook evaluates it against just those two names, so a typo gives a friendly message
  rather than a traceback. A student who does the arithmetic in their head and types `16`
  is also marked correct — if you want the formula specifically, say so out loud.
- **Task 5** is a tickbox.

**Task 1's widget is optional.** Students see a static 3D plot first and can answer from that
alone; the dropdown/slider step after it is clearly labelled optional so a stalled widget
never blocks the rest of the lesson. **Task 5's 3D-print/download step is gated** behind an
unticked box — it does not run (and does not start a download) until a student ticks it, so
Run All finishes cleanly.

## Answers (from the executed notebook)
- **Task 2** (5 µm → nm): `scan_width_nm = 5000`.
- **Task 3** (hair ÷ scan ratio): `scans_per_hair = 16` (80 µm ÷ 5 µm).
- **Task 4** (scale factor): `scale_factor = 20,000,000×` (100 m ÷ 0.000005 m) — this one is
  worked for students, since the next step (`layer_scaled_m`) is the checked task that uses it.
  Scaled layer height: `layer_scaled_m ≈ 0.013 m = 1.3 cm` — about a phone's thickness.
- **Exit ticket:**
  1. 3 µm = 3,000 nm.
  2. 80 µm hair ÷ 4 µm scan = 20 scans.
  3. Doubling the scale factor doubles the scaled layer height (thicker, ×2) — scaled
     height is a linear (proportional) function of scale factor.

## Common mistakes
1. **Converting the wrong direction.** Students multiply by 1,000 going from a smaller unit
   to a bigger one (nm → µm) instead of dividing. Point back at the conversion ladder table
   and ask "am I making the number of units bigger or smaller?"
2. **Mismatched units in the ratio/scale factor.** Task 3 and Task 4 both fail silently if a
   student mixes µm and nm, or µm and m, without converting first. Have them write the unit
   next to every number before dividing.
3. **Treating scale factor as addition.** Some students compute "field length − scan width"
  instead of a ratio. Remind them: scale factor answers "how many times bigger," which is
  always division/multiplication, never subtraction.

## If you have 10 more minutes
- Have students redo Task 4 with a different "model" size (e.g., a basketball court, 28 m)
  and compare how the scaled layer height changes.
- Ask: "If the crystal layer were twice as thick in real life, would the soccer-field
  model need a *bigger* or *smaller* scale factor to stay the same size?" (Trick question —
  scale factor doesn't depend on layer thickness at all; it's set by the scan width and the
  field length.)
