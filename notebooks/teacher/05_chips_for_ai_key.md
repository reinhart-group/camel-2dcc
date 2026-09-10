# Teacher key — 05: Chips for AI: Exponents, Light, and Super-Cold Wires

Source: `notebooks/src/05_chips_for_ai.py` → `notebooks/05_chips_for_ai.ipynb`. All numbers below
were printed by `scripts/run_notebook.py notebooks/05_chips_for_ai.ipynb` against the real data
slice (`data/slice/camel-2dcc/`) — none are typed from memory.

## Learning targets (student language)

- I can use an exponential model N(t) = N0 · 2^((t−t0)/d) and interpret the doubling time d.
- I can fit that model to real data with `numpy.polyfit` on log-transformed data.
- I can use ratio and multiplication models to compare a monolayer channel with a silicon one.
- I can use λ = 1240/E to convert between a photon's energy and its wavelength (color).
- I can convert between Kelvin, Celsius, and Fahrenheit with linear formulas.
- I can explain, without hype, why "more transistors" ≠ "more AI capability" and why superconductors
  aren't already cooling data centers.

## Standards (CCSS) per task

| Task | Standard(s) | Student action |
|---|---|---|
| 1 | HSF.LE.A.3, HSF.IF.C.7e | Compare linear vs. log-axis views of exponential data; move a parameter slider |
| 2 | HSF.LE.B.5, HSN.Q.A.2 | Fit d via `numpy.polyfit` on log2(transistors); interpret the parameter |
| 3 | HSN.Q.A.1 | Ratio/unit reasoning (nm : nm) |
| 4 | HSA.CED.A.2 | Multiplicative model (k layers × devices/layer) |
| 5 | HSN.Q.A.1, inverse proportion | Compute λ = 1240/E for four materials |
| 6 | HSN.Q.A.1 | Compare photon energies at two fiber wavelengths |
| 7 | HSN.Q.A.1 (unit conversion) | Linear K↔C↔F conversion |
| 8 | HSF.IF.B.4, HSS.ID.B.6 | Read a scatterplot with a reference line |
| 9 | HSN.Q.A.1, percent change | I²R heat calc; percent change; unit-rate "homes" estimate |
| 10–11 | HSN.Q.A.1, data cleaning | Split `;`-joined strings and count exact tokens |

## Timing (45–50 min class)

| Minutes | Section |
|---|---|
| 0–5 | Hook + setup cell |
| 5–15 | Part 1 — doubling-time slider (Task 1) + fit (Task 2) |
| 15–22 | Part 2 — ratio (Task 3) + stacking model (Task 4) |
| 22–32 | Part 3 — photonics (Tasks 5–6) |
| 32–42 | Part 4 — superconductors (Tasks 7–9) |
| 42–47 | Part 5 — catalog counts (Tasks 10–11) |
| 47–50 | Exit ticket |

Core-only path (non-AP, single 45-min period): Tasks 1, 3, 4, 5, 7, 10, exit ticket — skip 2, 6, 8,
9, 11 or assign as homework/Explore.

## Expected answers (as ranges — real data, not brittle exact values)

- **Task 2 fit:** d_fit ≈ **2.0–2.1 years** (executed value: **2.05 years**; N0 back-out ≈ 2,300,
  matching the real 1971 Intel 4004 count). Any slider guess **within about ±1 year of 2.05** should
  be accepted as "close."
- **Task 3 ratio:** with the default si_channel_nm = 5.0, ratio ≈ **7.5–8.0×** (executed: **7.7×**).
  Accept any answer consistent with whatever si_channel_nm the student tried.
- **Task 4 stacking:** purely arithmetic — accept any internally consistent k × one_layer_devices
  (default in the notebook: 4 × 500,000 = 2,000,000). There is no "correct" real-world value; grade
  on whether the multiplication is right, not the made-up inputs.
- **Task 5 wavelengths:** MoS2 ≈ **650–655 nm (red)**, WS2 ≈ **618–622 nm (orange)**,
  WSe2 ≈ **750–755 nm (near-infrared)**, MoSe2 = **800 nm (near-infrared)**. (Executed: 653, 620,
  752, 800.) Graphene (0 eV gap) is correctly excluded — watch for students who don't filter it and
  get a `ZeroDivisionError`/`inf`.
- **Task 6:** 1310 nm ≈ **0.94–0.95 eV**; 1550 nm ≈ **0.79–0.80 eV**. Both are lower energy than
  every monolayer gap in Task 5 (smallest is MoSe2 at 1.55 eV) — students should notice fiber light
  is *lower* energy than any of these materials' visible-light gaps.
- **Task 7:** 77 K = **−196.15 °C** = **−321.07 °F** (also acceptable: **−321.1 °F**, or −320.5 to
  −321.5 °F band for rounding).
- **Task 9 heat:** default 100 A through 0.01 Ω → **100 W** wasted as heat (I²R); accept any
  internally-consistent I²R for whatever current the student tries.
- **Task 9 IEA figures:** percent change 415 → 945 TWh ≈ **+127% to +128%** (executed: **+128%**,
  rounded). Homes: 2024 ≈ **39–40 million** homes (executed: 40M), 2030 ≈ **90 million** homes
  exactly (945e9 / 10,500 = 90,000,000 — a nice round check value).
- **Task 10/11 catalog counts** (exact-token match on the `;`-split `materials` column, from the
  real slice): **MoS2 = 443, WS2 = 203, WSe2 = 257, MoSe2 = 43**. A naive `.str.contains("WSe2")`
  substring search over-counts because of the alloy `Mo-WSe2` — this is a deliberate "messy data"
  trap; the provided `count_material()` helper splits on `;` and does exact-token matching to avoid
  it.

## Common misconceptions / troubleshooting

- **"Moore's law is a guarantee."** It's a fitted trend from 1971–2024 data, not a physical law;
  the Scientist's note after Task 2 addresses this directly — press students to restate it in their
  own words if their exit-ticket answer treats it as inevitable.
- **"More transistors = smarter AI."** These are different variables (density, memory movement,
  energy, heat are also relevant) — this is the point of exit-ticket question 3.
- **Confusing photon energy and wavelength direction.** Higher energy → *shorter* wavelength. If a
  student says "800 nm has more energy than 650 nm," have them recompute 1240/800 vs 1240/650.
- **Treating the "~5 nm" silicon figure as precise.** It's flagged as an order-of-magnitude,
  illustrative teaching figure in a Scientist's note — real silicon transistors are 3D fin/GAA
  shapes with no single "channel thickness."
- **Treating `one_layer_devices` as measured data.** It's explicitly made up for Task 4's
  multiplication model — watch for answers that cite the 2,000,000 figure as if it were a real chip
  spec.
- **Assuming superconductors already cool AI data centers today.** They don't, per the Scientist's
  note in Part 4 — this is a live research direction, not current infrastructure.
- **`ZeroDivisionError` / `inf` in Part 3.** Happens if a student re-implements the wavelength
  calculation without excluding graphene's `band_gap_monolayer_eV == 0` row (a real value, not a
  missing one — a semimetal has no gap). The provided code already filters `> 0`.
- **Widget doesn't render.** Confirm `output.enable_custom_widget_manager()` ran in the setup cell
  (only fires inside real Colab) and that the student didn't skip the setup cell.

## Complexity dials

- **Core:** Tasks 1, 3, 4, 5, 7, 10.
- **Explore:** Tasks 2, 6, 8, 9.
- **Extend:** Task 11.
