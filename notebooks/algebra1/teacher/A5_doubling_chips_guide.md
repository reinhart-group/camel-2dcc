# Teacher guide — A5: Doubling Chips: The Power of 2

Source: `notebooks/algebra1/src/A5_doubling_chips.py` → `notebooks/algebra1/A5_doubling_chips.ipynb`.
All numbers below come from `scripts/run_notebook.py` against the real data slice
(`data/slice/camel-2dcc-v1.zip`, `chips_timeline.csv`) — none are typed from memory.

## Goals (student language)

- I can build and read a doubling table (repeated multiplication by 2).
- I can compare doubling growth to linear ("add the same amount") growth and find where one
  overtakes the other.
- I can compare a real dataset to two doubling-model curves and judge which fits better.
- I can use guess-and-check on a table to count doublings, without logarithms.
- I can solve a ratio problem (thin layers stacking to a everyday thickness).

## Standards per task

| Task | Standard(s) | Student action |
|---|---|---|
| 1 | F.LE.1–2, A.SSE.1 | Fill in a doubling table (repeated ×2) |
| 2 | F.LE.1–2, A.CED.2 | Compare a linear table to the doubling table; find the crossover year |
| 3 | F.IF.4–6 | Read a scatterplot against two model curves; judge fit |
| *(optional)* | F.IF.6 | Slider (rate of change) and log-axis reading — not required |
| 4 | A.SSE.1, N.Q.1 | Guess-and-check a table for "how many doublings" (no logs) |
| 5 | 7.RP (ratio review), N.Q.1 | Ratio/unit division: nm ÷ nm |

## Timing (30–40 min)

| Minutes | Section |
|---|---|
| 0–5 | Hook + setup cell |
| 5–12 | Task 1 — doubling table |
| 12–18 | Task 2 — doubling vs. adding |
| 18–26 | Task 3 — fit check (+ optional slider/log-axis extras, ~5 more min if used) |
| 26–32 | Task 4 — how many doublings to 80 billion |
| 32–37 | Task 5 — thin-layer ratio |
| 37–40 | Exit ticket |

## Expected answers (from the executed notebook)

- **Task 1:** 2,300 → 4,600 → 9,200 → 18,400 → 36,800 (years 1971, 1973, 1975, 1977, 1979). Exact
  match required — the check reports how many of the 4 blanks are correct so far.
- **Task 2:** doubling first passes adding in **1975** (doubling 9,200 vs. adding 6,900; the two
  patterns tie at 1973, 4,600 each, then doubling pulls ahead every step after).
- **Task 3:** the **2-year** doubling line tracks the real chips better than the 3-year line. This
  matches the actual best-fit doubling time for this dataset, about **2.05 years** (computed by
  `numpy.polyfit` on log2-transformed data in the Explorer edition's parallel notebook) — close
  enough to 2 that "2" is the intended answer, and no fitting is required of students here.
- **Task 4:** accept **23–27 doublings** (the check accepts this range). 25 doublings from 2,300
  gives about 77.2 billion; 26 doublings gives about 154.4 billion — the real newest chip (~80
  billion single-die, or 208 billion for the two-die B200) sits right around this crossover, so
  "about 25" is the expected read from the table.
- **Task 5:** **about 153,846 layers** (100,000 ÷ 0.65). The check accepts any guess within 10% of
  the exact value.

## Common mistakes

1. **Doubling the wrong number.** Some students double the *previous answer's previous answer*
   (skip a step) instead of the immediately preceding value — remind them each blank doubles the
   cell right before it.
2. **Reading "first year doubling is bigger" as "first year they're different."** 1971 and 1973
   are *tied*; 1975 is the first year doubling is strictly larger. Point students at the table's
   equal row before the crossover.
3. **Picking "3" in Task 3 because the curve "looks bigger."** Have students trace the line near
   the *earliest* years too — the 3-year line undershoots early data and overshoots late data; the
   2-year line stays closer across the whole range, not just at one end.

## If you have 10 more minutes

- Run the **optional slider** (Task 3's extra cell) and have students find a doubling time even
  closer than 2 years by eye.
- Try the **optional log-scale plot** and ask: "Why does the doubling line look straight here but
  curved on the normal graph?" (Equal steps on a log axis mean ×10, not +10 — a doubling curve
  becomes a straight line under a log transform.)
- Ask students to redo Task 2's table starting from a different "add" amount (e.g. +5,000 every 2
  years) and find the new crossover year.
