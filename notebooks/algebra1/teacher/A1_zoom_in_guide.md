# Teacher guide — Zoom In! How Small Is a Nanometre?

**Standards:** N.Q.1–3 (units, scale), 7.RP review (ratios/proportions), A.CED.1 (one-step
equations), A.SSE.1 (interpreting scale-factor expressions).

**Time:** 30–40 minutes (Task 5 is optional; drop it if short on time).

## Goals
Students convert between metre/mm/µm/nm, use a ratio to compare sizes, and compute a scale
factor to connect a microscopic crystal scan to a human-scale object (a football field).

## Answers (from the executed notebook)
- **Task 2** (5 µm → nm): `scan_width_nm = 5000`.
- **Task 3** (hair ÷ scan ratio): `scans_per_hair = 16` (80 µm ÷ 5 µm).
- **Task 4** (scale factor): `scale_factor = 20,000,000×` (100 m ÷ 0.000005 m).
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
- Ask: "If the crystal layer were twice as thick in real life, would the football-field
  model need a *bigger* or *smaller* scale factor to stay the same size?" (Trick question —
  scale factor doesn't depend on layer thickness at all; it's set by the scan width and the
  field length.)
