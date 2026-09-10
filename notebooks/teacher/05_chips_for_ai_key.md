# Teacher key — 05: Chips for AI: Exponents, Light, and Super-Cold Wires

Source: `notebooks/src/05_chips_for_ai.py` → `notebooks/05_chips_for_ai.ipynb`. All numbers below
were printed by `scripts/run_notebook.py notebooks/05_chips_for_ai.ipynb` against the real data
slice (`data/slice/camel-2dcc/`) — none are typed from memory.

## Learning targets (student language)

- I can use an exponential model N(t) = N0 · 2^((t−t0)/d) and interpret the doubling time d.
- I can fit that model to real data with `numpy.polyfit` on log-transformed data, and explain why a
  hand-picked chip list makes that fit a selection-sensitive estimate, not a proof of Moore's law.
- I can use ratio and multiplication models to compare a monolayer channel with an illustrative
  silicon channel, without claiming that figure is the thinnest ever reported.
- I can use λ = 1240/E to convert a monolayer's optical energy into a wavelength (color), and can
  say in one sentence how optical energy differs from the electronic band gap.
- I can convert between Kelvin, Celsius, and Fahrenheit with linear formulas.
- I can explain, without hype, why "more transistors" ≠ "more AI capability," why a monolayer isn't
  "one atom thick," and why superconductors don't cool anything themselves.

## Standards (CCSS) per task

| Task | Standard(s) | Student action |
|---|---|---|
| 1 | HSF.LE.A.3, HSF.IF.C.7e | Read a static d=2/d=3 comparison plot; optionally move a slider |
| 2 | HSF.LE.B.5, HSN.Q.A.2 | Fit d via `numpy.polyfit` on log2(transistors); test selection sensitivity |
| 3 | HSN.Q.A.1 | Ratio/unit reasoning (nm : nm), explicitly hypothetical |
| 4 | HSA.CED.A.2 | Multiplicative model (k layers × devices/layer) |
| 5 | HSN.Q.A.1, inverse proportion | Compute λ = 1240/E for four materials' optical energies |
| 6 | HSN.Q.A.1 | Compare photon energies at two fiber wavelengths |
| 7 | HSN.Q.A.1 (unit conversion) | Linear K↔C↔F conversion |
| 8 | HSF.IF.B.4, HSS.ID.B.6 | Read a scatterplot with a reference line and a ranged (error-bar) point |
| 9 | HSN.Q.A.1, percent change | I²R heat calc for one wire; separate percent-change/unit-rate scale exercise |
| 10–11 | HSN.Q.A.1, data cleaning | Split `;`-joined strings and count exact tokens |

## Timing (45–50 min class)

| Minutes | Section |
|---|---|
| 0–5 | Hook + setup cell |
| 5–15 | Part 1 — static d=2/d=3 comparison + optional slider (Task 1) + fit (Task 2) |
| 15–22 | Part 2 — ratio (Task 3) + stacking model (Task 4) |
| 22–32 | Part 3 — photonics (Tasks 5–6) |
| 32–42 | Part 4 — superconductors (Tasks 7–9) |
| *+5 (optional)* | *"See it happen" real-FeSe-films add-on, after Task 8's plot* |
| 42–47 | Part 5 — catalog counts (Tasks 10–11) |
| 47–50 | Exit ticket |

Core-only path (non-AP, single 45-min period): Tasks 1, 3, 4, 5, 7, 10, exit ticket — skip 2, 6, 8,
9, 11, and the "See it happen" add-on, or assign as homework/Explore. Task 1's static comparison
plot (not the slider) is what makes this path work even if Colab's interactive widgets fail to load.

## Expected answers (as ranges — real data, not brittle exact values)

- **Task 1 static plot:** the d=2 and d=3 curves visibly diverge from the real chips by different
  amounts on both axes; neither traces every point exactly, since this is a hand-fit guess, not the
  regression in Task 2.
- **Task 2 fit:** d_fit ≈ **2.0–2.1 years** (executed value: **2.05 years**; N0 back-out ≈ 2,300,
  matching the real 1971 Intel 4004 count). Any slider guess **within about ±1 year of 2.05** should
  be accepted as "close." The Intel-only sensitivity check (11 of the 18 chips) gives **2.10 years**
  — close to but not identical to the all-chips fit, illustrating that the fit is selection-sensitive.
  Students should NOT conclude this "verifies" Moore's law — see the Scientist's note.
- **Task 3 ratio (hypothetical):** with the default si_channel_nm = 5.0, ratio ≈ **7.5–8.0×**
  (executed: **7.7×**). Accept any answer consistent with whatever si_channel_nm the student tried.
  Push back on any answer that treats "~5 nm" as the record-thinnest silicon channel — it's an
  illustrative figure only; research channels well under 1 nm have been reported.
- **Task 4 stacking:** purely arithmetic — accept any internally consistent k × one_layer_devices
  (default in the notebook: 4 × 500,000 = 2,000,000). There is no "correct" real-world value; grade
  on whether the multiplication is right, not the made-up inputs.
- **Task 5 wavelengths (optical energies, not electronic band gaps):** MoS2 ≈ **650–655 nm (red)**,
  WS2 ≈ **618–622 nm (orange)**, WSe2 ≈ **750–755 nm (near-infrared)**, MoSe2 = **800 nm
  (near-infrared)**. (Executed: 653, 620, 752, 800.) Graphene is correctly excluded (its
  `optical_energy_monolayer_eV` is blank, along with several other materials with no single
  classroom value) — watch for students who don't filter it and get a `ZeroDivisionError`/`NaN`.
- **Task 6:** 1310 nm ≈ **0.94–0.95 eV**; 1550 nm ≈ **0.79–0.80 eV**. Both are lower energy than
  every monolayer optical energy in Task 5 (smallest is MoSe2 at 1.55 eV) — students should notice
  fiber light is *lower* energy than any of these materials' visible-light optical energies.
- **Task 7:** 77 K = **−196.15 °C** = **−321.07 °F** (also acceptable: **−321.1 °F**, or −320.5 to
  −321.5 °F band for rounding).
- **Task 8 table/plot:** solid materials (mercury, lead, niobium, FeSe bulk crystal, MgB2, YBCO,
  HgBa2Ca2Cu3O8) each have one `critical_temp_K` value plotted as an orange circle. Single-layer
  FeSe on SrTiO3 has **no single `critical_temp_K`** (it prints as blank/NaN in the table) and is
  plotted separately as a pink diamond with an error bar spanning `tc_low_K`=40 K to
  `tc_high_K`=65 K — a *reported superconducting signature*, not a zero-resistance measurement like
  the other rows.
- **"See it happen" real-FeSe-films add-on (Explore, ~5 min, optional):** from `transport_summary.csv`,
  `T_zero_1pct_K` — sample **20198 ≈ 4.99 K**, **20200 ≈ 14.00 K**, **20201 ≈ 22.87 K**; sample
  **20199 never reaches ~zero resistance** in its measured range (down to 4 K, the lowest
  temperature it was measured at — `T_zero_1pct_K` is blank/NaN). Two films (20200, 20201) reach
  zero resistance at a higher temperature than bulk FeSe's 8 K; one (20198) reaches it lower;
  20199 doesn't reach it at all here — the point is real thin-film samples disagree with each
  other and with the bulk value, which is exactly what motivates further study, not a mechanism
  claim. Ohm's-law check on sample 20198 (I = 1 µA): at **19.54 K, R ≈ 1015.6 Ω → V ≈ 1.016 mV**;
  at **3.00 K, R ≈ −0.004 Ω → V ≈ −0.004 µV** — the near-zero-K voltage is thousands of times
  smaller and its slight negative sign is measurement noise (the instrument's noise floor), not
  negative resistance.
- **Task 9 heat (single wire):** default 100 A through 0.01 Ω → **100 W** wasted as heat (I²R);
  accept any internally-consistent I²R for whatever current the student tries. This is a toy
  single-wire example — it is explicitly NOT evidence about data-center-scale savings.
- **Task 9 IEA figures (separate scale exercise):** percent change 415 → 945 TWh ≈ **+127% to
  +128%** (executed: **+128%**, rounded). Homes: 2024 ≈ **39–40 million** homes (executed: 40M),
  2030 ≈ **90 million** homes exactly (945e9 / 10,500 = 90,000,000 — a nice round check value).
  These numbers describe the *scale* of data-center electricity use in general; they are not tied
  to the I²R wire example above, and students should not present one as causing or explaining the
  other.
- **Task 10/11 catalog counts** (exact-token match on the `;`-split `materials` column, from the
  real slice): **MoS2 = 443, WS2 = 203, WSe2 = 257, MoSe2 = 43**. A naive `.str.contains("WSe2")`
  substring search over-counts because of the alloy `Mo-WSe2` — this is a deliberate "messy data"
  trap; the provided `count_material()` helper splits on `;` and does exact-token matching to avoid
  it.

## Common misconceptions / troubleshooting

- **"Moore's law is a guarantee."** It's a fitted trend from 1971–2024 data, not a physical law;
  the Scientist's note after Task 2 addresses this directly — press students to restate it in their
  own words if their exit-ticket answer treats it as inevitable.
- **"The Task 2 fit proves Moore's law."** `chips_timeline.csv` is a hand-picked selection — single-
  die Intel CPUs, then Apple phone/laptop chips, then NVIDIA AI accelerators, with the 2024 row
  (B200) packaging two dies. The Intel-only sensitivity check gives a different d (2.10 vs. 2.05
  years) from the same underlying data source, which is the point: this is a selection-sensitive
  estimate, not independent verification.
- **"More transistors = smarter AI."** These are different variables (density, memory movement,
  energy, heat are also relevant) — this is the point of exit-ticket question 3.
- **Confusing photon energy and wavelength direction.** Higher energy → *shorter* wavelength. If a
  student says "800 nm has more energy than 650 nm," have them recompute 1240/800 vs 1240/650.
- **Treating the "~5 nm" silicon figure as the thinnest ever made.** It's flagged in two places (Part
  2 intro and the Scientist's note after Task 3) as a deliberately chosen illustrative figure, not a
  record — research silicon channels well under 1 nm have been reported. Real silicon transistors
  are 3D fin/GAA shapes with no single "channel thickness," and this ratio task stays hypothetical.
- **"Channel thickness," "gate length," and the marketing "node name" are the same thing.** They are
  not — Part 2's intro now separates all four (channel thickness, gate length, node name,
  manufacturability) in one short list before Task 3.
- **Treating `one_layer_devices` as measured data.** It's explicitly made up for Task 4's
  multiplication model — watch for answers that cite the 2,000,000 figure as if it were a real chip
  spec.
- **"Optical energy" and "electronic band gap" are the same number.** They're close but not
  identical — the Part 3 intro and the Task 5 Scientist's note both explain the difference (exciton
  binding) in one or two sentences; watch for students who call the Task 5 table "the band gap."
- **"A monolayer is one atom thick."** It isn't — the glossary and Part 3 both now define a
  monolayer as one *repeating layer* of structure, which can hold several atomic planes (MoS2's
  monolayer is a three-plane S–Mo–S sandwich, ~0.65 nm). Watch for students carrying over "one atom"
  language from earlier notebooks.
- **"Superconductors cool data centers" / "superconductors are already cooling AI chips."** Wrong
  direction of cause and effect: a superconductor must *be* cooled (cryogenically, at real energy
  cost) before it works — it doesn't cool anything itself. The Part 4 intro, the Task 8 Scientist's
  note, and exit-ticket question 3 all address this; if a student's answer says superconductors
  "keep things cold," redirect them to the glossary definition.
- **Treating the IEA 415→945 TWh numbers as proof of superconductor savings.** They aren't connected
  — Task 9 is split into "one wire" (I²R) and a clearly separated "scale of data-center electricity"
  exercise with its own heading, and the Scientist's note after the I²R calculation says so directly.
- **Assuming a higher-Tc thin film "explains" why (mechanism).** The "See it happen" add-on
  deliberately does not explain *why* films 20200/20201 reach zero resistance above bulk FeSe's
  8 K — that's an open research question this notebook doesn't answer. Watch for students
  inventing a mechanism (e.g., "because it's thinner") that the data doesn't support.
- **Reading the slightly negative near-zero resistance as "negative resistance."** It's instrument
  noise floor, not a real physical effect — the Scientist's note after the Ohm's-law check says so.
- **Treating single-layer FeSe's 65 K as an exact zero-resistance value.** It's plotted with an
  error bar (40–65 K) using a different marker (pink diamond vs. orange circle) specifically because
  it's a reported signature under specific lab conditions, not a zero-resistance measurement like
  the other superconductors in the table.
- **`ZeroDivisionError` / `NaN` in Part 3.** Happens if a student re-implements the wavelength
  calculation without excluding rows where `optical_energy_monolayer_eV` is blank (several materials
  have no single classroom value, including graphene, a semimetal with no gap). The provided code
  already filters `> 0`, which also excludes blanks.
- **Widget doesn't render.** Task 1's static d=2/d=3 comparison plot works without widgets, so this
  should never block the core task. For the optional slider, confirm
  `output.enable_custom_widget_manager()` ran in the setup cell (only fires inside real Colab) and
  that the student didn't skip the setup cell.

## Complexity dials

- **Core:** Tasks 1, 3, 4, 5, 7, 10.
- **Explore:** Tasks 2, 6, 8, 9, plus the optional "See it happen" real-FeSe-films add-on (~5 min).
- **Extend:** Task 11.
