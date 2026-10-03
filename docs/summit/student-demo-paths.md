# Student demo decision paths: three gates to a transistor-channel recommendation

## Recommended bounded problem

**Mission shown to students:**

> Your team is choosing an atom-thin material for the main current-carrying channel in a prototype computer chip. Choose the material, choose an honest data-cleaning rule, then set the **strictest** available smoothness specification that at least **75%** of the measured samples pass.

The selectable specifications are **0.5 nm, 1.0 nm, and 2.0 nm RMS roughness**. “Strictest” means the smallest number. The 75% yield requirement and the three candidate specifications are scenario constraints, not claims that the dataset proves a physical transistor threshold.

This creates one checkable endpoint from real data:

- **Gate 1:** choose **MoS2**.
- **Gate 2:** choose the **purpose-built audit** rule.
- **Gate 3:** choose **1.0 nm**.
- **Report:** `313 / 403 × 100 = 77.7%` observed yield.

At 0.5 nm, MoS2 reaches only 53.8%, so 0.5 nm is too strict for the stated 75% requirement. At 1.0 nm it reaches 77.7%, so 1.0 nm is the strictest passing option. This is arithmetic and data reasoning, not a slider-to-a-hidden-target game.

## Why this is teachable in an existing 9–12 math course

| Gate | Textbook-style student skill | Exact CCSS alignment |
|---|---|---|
| 1. Choose a material | Compare distributions using **sample size, median, and IQR**; interpret “smaller is smoother” in context. | **HSS-ID.A.1** (represent data with plots), **HSS-ID.A.2** (compare center and spread of two or more data sets), **HSS-ID.A.3** (interpret differences in shape, center, and spread, accounting for outliers). |
| 2. Choose a cleaning rule | Decide which variables are relevant; distinguish a blank from zero; compare how a rule changes the numerator, denominator, and groups represented. | **HSS-ID.A.3** (possible effects of extreme points), **HSS-IC.B.6** (evaluate reports based on data). The cleaning decision is the concrete report-evaluation task. |
| 3. Set the spec and report yield | Build a pass/fail frequency table, calculate a relative frequency, compare it with 75%, and choose the smallest value satisfying an inequality. | **HSS-ID.B.5** (two-way frequencies and relative frequencies in context), **HSA-CED.A.3** (represent and interpret constraints), **HSN-Q.A.1–3** (units, appropriate quantities, and justified precision). **7.RP.A.3** is the explicit prerequisite standard for percent arithmetic commonly revisited in grades 9–12. |

The student does not need condensed-matter physics. The only context needed is: a transistor channel is the path current takes; these are possible atom-thin materials; an AFM microscope reports surface roughness in nanometres; a smaller roughness value means a flatter measured patch.

Suggested pacing is **3 minutes at Gate 1, 4 minutes at Gate 2, 4 minutes at Gate 3, and 2 minutes for the result/reveal**: 13 minutes total.

## Data population: resolve 894 versus 1,005 before building

The current slice contains three legitimate but different pools:

| Pool | Current count | Meaning |
|---|---:|---|
| `growth_summary.csv` | 1,005 | One row per sample with a growth record, whether or not AFM roughness was measured. |
| Current grown rows with `rms_roughness_nm` | 899 | The overlap between the growth-record pool and the current AFM summary. |
| `afm_summary.csv` | 1,004 | One selected usable AFM scan per measured sample, including 105 AFM samples with no row in `growth_summary.csv`. Every row has a roughness value. |

The older Kathy-facing page says **894 measured samples**. That was correct for an earlier slice snapshot but is stale for the checked-in data: the current growth-summary overlap is **899**, five more. “1,005” is not the denominator for a roughness yield; it includes 106 grown samples with no roughness measurement.

**The demo should use the 1,004-row `afm_summary.csv` pool.** The mission is explicitly about measured surface smoothness, and the material counts supplied by the lead—MoS2 401, WS2 144, MoSe2 43, WSe2 214, GaSe 51, In2Se3 33—come from this pool. This also avoids silently discarding 105 real AFM measurements merely because a separate growth record is absent.

The page must say **“1,004 AFM-measured samples”**, not “1,005 samples” or “894 measurements.” If the summit page and demo appear together, update or footnote the older 894 label so teachers do not reasonably think the two displays contradict one another.

For Gate 2 only, left-join the single `growth_time_min` field from `growth_summary.csv` by `sample_id`. This makes the “drop rows missing an unrelated field” trap visible without changing the authoritative AFM pool.

## Inputs and derived fields

Use these real fields only:

- `afm_summary.csv`: `sample_id`, `material`, `all_materials`, `scan_size_um`, `pixels`, `lines`, `rms_roughness_nm`, `height_range_nm`, `doi`.
- `growth_summary.csv`, left join only: `sample_id`, `growth_time_min`.
- `materials_reference.csv`: `material`, `name`, `family`, `why_it_matters`.
- Verified correction from the real gallery data: sample **17458** is the WSe2 scan `wse2_triangles`; the stored summary is **6.0964 nm**, while removing its one documented corrupted scan line gives **0.80 nm**. Both figures come from the checked-in dataset/audit, not from an invented example.

The raw `all_materials` field contains **35 distinct nonblank strings**. The shipped `material` field already behaves like a primary-material cleanup for semicolon entries, but it leaves `2H-MoS2` separate. The purpose-built browser rule below reproduces that cleanup transparently rather than hiding it.

## The three concrete cleaning rules

### A — Purpose-built audit (recommended)

Use only fields needed for the decision, standardize mechanically safe label cases, and repair the one artifact that has direct scan evidence.

1. Split `all_materials` on `;`, trim spaces, discard a token containing no letters (the real `MoS2; 0` case), remove exact duplicate tokens, and use the first remaining material as the primary label.
2. Map `2H-MoS2` to `MoS2`; “2H” names a stacking form, not a different chemical material.
3. Keep rows with a primary material and finite `rms_roughness_nm`. Do **not** require unrelated growth time or DOI.
4. For sample 17458 only, replace 6.0964 with the reviewed 0.80 nm value and visibly mark it “corrected from raw scan.” Do not delete all large values merely because they are large.

This reduces 35 raw nonblank strings to 26 primary labels, retains 403 MoS2 measurements after merging the two `2H-MoS2` records, and does not manufacture values for blanks.

### B — Literal labels

Keep a row only when `all_materials` exactly equals the selected label; make no correction to sample 17458. This is easy to code but treats `MoS2`, `MoS2; MoS2`, `MoS2; 0`, and `2H-MoS2` as different groups. The cost is visible: the MoS2 evidence pool falls from 403 to 391.

### C — “Complete-case” trap

Apply Rule A, then also require a nonblank `growth_time_min`, even though growth time is not used to compute smoothness yield. This is a common but indefensible “drop any row missing X” shortcut for this question. It drops MoS2 from 403 to 337 and deletes **all GaSe and all In2Se3 rows**. A blank is not a failure and is not zero; it means the separate growth table did not record that field.

### Implementable vanilla-JavaScript definitions

```js
function primaryMaterial(allMaterials) {
  if (allMaterials == null || allMaterials.trim() === "") return null;
  const parts = allMaterials.split(";")
    .map(s => s.trim())
    .filter(s => /[A-Za-z]/.test(s))
    .filter((s, i, a) => a.indexOf(s) === i);
  if (!parts.length) return null;
  return parts[0] === "2H-MoS2" ? "MoS2" : parts[0];
}

function cleanRows(rows, chosenMaterial, rule) {
  return rows.flatMap(row => {
    if (rule === "literal") {
      return row.all_materials === chosenMaterial ? [row] : [];
    }

    const material = primaryMaterial(row.all_materials);
    if (material !== chosenMaterial || !Number.isFinite(row.rms_roughness_nm)) return [];
    if (rule === "complete" && !Number.isFinite(row.growth_time_min)) return [];

    const roughness = row.sample_id === 17458 ? 0.80 : row.rms_roughness_nm;
    return [{...row, material, roughness,
             corrected: row.sample_id === 17458}];
  });
}

function yieldAt(rows, specNm) {
  const passing = rows.filter(r =>
    (r.roughness ?? r.rms_roughness_nm) <= specNm).length;
  return {passing, total: rows.length,
          percent: rows.length ? 100 * passing / rows.length : null};
}
```

Rule C must not be labeled simply “clean.” Call it **“require growth time too”** so the student can see the extra condition they chose. The result screen should explain why it was irrelevant to the stated decision.

## All 54 material × cleaning-rule × specification paths

Pass means `roughness <= specification`; the boundary is inclusive. `A`, `B`, and `C` refer to the rules above. Each cell is `passing / carried rows = yield`.

| Material | Cleaning rule | 0.5 nm | 1.0 nm | 2.0 nm |
|---|---|---:|---:|---:|
| MoS2 | A · purpose-built audit | 217/403 = **53.8%** | 313/403 = **77.7%** | 356/403 = **88.3%** |
| MoS2 | B · literal labels | 212/391 = **54.2%** | 302/391 = **77.2%** | 344/391 = **88.0%** |
| MoS2 | C · require growth time | 201/337 = **59.6%** | 260/337 = **77.2%** | 294/337 = **87.2%** |
| WS2 | A · purpose-built audit | 66/144 = **45.8%** | 106/144 = **73.6%** | 124/144 = **86.1%** |
| WS2 | B · literal labels | 66/144 = **45.8%** | 106/144 = **73.6%** | 124/144 = **86.1%** |
| WS2 | C · require growth time | 64/133 = **48.1%** | 96/133 = **72.2%** | 113/133 = **85.0%** |
| MoSe2 | A · purpose-built audit | 12/43 = **27.9%** | 31/43 = **72.1%** | 39/43 = **90.7%** |
| MoSe2 | B · literal labels | 12/43 = **27.9%** | 31/43 = **72.1%** | 39/43 = **90.7%** |
| MoSe2 | C · require growth time | 12/43 = **27.9%** | 31/43 = **72.1%** | 39/43 = **90.7%** |
| WSe2 | A · purpose-built audit | 21/214 = **9.8%** | 110/214 = **51.4%** | 163/214 = **76.2%** |
| WSe2 | B · literal labels | 21/214 = **9.8%** | 109/214 = **50.9%** | 162/214 = **75.7%** |
| WSe2 | C · require growth time | 21/205 = **10.2%** | 105/205 = **51.2%** | 154/205 = **75.1%** |
| GaSe | A · purpose-built audit | 1/51 = **2.0%** | 15/51 = **29.4%** | 34/51 = **66.7%** |
| GaSe | B · literal labels | 0/48 = **0.0%** | 14/48 = **29.2%** | 32/48 = **66.7%** |
| GaSe | C · require growth time | **no rows** | **no rows** | **no rows** |
| In2Se3 | A · purpose-built audit | 0/33 = **0.0%** | 2/33 = **6.1%** | 7/33 = **21.2%** |
| In2Se3 | B · literal labels | 0/29 = **0.0%** | 1/29 = **3.4%** | 4/29 = **13.8%** |
| In2Se3 | C · require growth time | **no rows** | **no rows** | **no rows** |

## Is there one defensible best path?

Yes, **for this bounded dashboard decision and this checked-in dataset**:

1. **MoS2 fits the stated job.** `materials_reference.csv` explicitly describes it as an “ultra-thin transistor channel.” WSe2 is also transistor-relevant, as the p-type partner in logic, but its observed roughness distribution is much higher. The other four cards explicitly describe light emission, optics, heterostructures, or memory rather than the main channel job.
2. **Rule A is the most defensible cleaning rule.** It resolves only text patterns the data make explicit, uses only variables needed for the question, and corrects one instrument artifact supported by the underlying scan. It neither throws out legitimate large measurements merely for being large nor discards groups for missing irrelevant growth fields.
3. **1.0 nm is the strictest offered specification meeting 75% yield.** Under Rule A, MoS2 is 313/403 = 77.7% at 1.0 nm; 0.5 nm is only 53.8%.

The numerical margin at the decisive 1.0 nm specification is visible:

- MoS2: **77.7%**, 2.7 percentage points above the required 75%.
- WS2, the next-highest observed yield among all six: **73.6%**, 1.4 points below the requirement.
- The gap between them is **4.1 percentage points**.
- WSe2, the other explicitly transistor-relevant card: **51.4%**, 26.3 points below MoS2.

This is a descriptive winner, not proof that MoS2 is universally superior. The task must say “best choice **from these records under this contract**.” A confidence-interval or causal claim would exceed the 10–15 minute brief and is not supported by this observational, nonrandom collection.

## Where early mistakes visibly cost the student

### Wrong material at Gate 1

- WS2 and MoSe2 miss the 75% goal at 1.0 nm and must relax to 2.0 nm.
- WSe2 also must relax to 2.0 nm, despite being transistor-relevant.
- GaSe and In2Se3 cannot reach 75% even at the loosest 2.0 nm option.
- The result panel should preserve the student's route: “Your earlier WS2 choice means the 1.0 nm contract now fails: 106 of 144 = 73.6%.” Do not silently reset the material.

### Weak cleaning at Gate 2

- Literal-label matching loses 12 MoS2 measurements: 403 becomes 391. The headline percentage barely moves, which is itself useful—similar percentages can hide different denominators.
- Requiring growth time loses 66 MoS2 measurements: 403 becomes 337. For GaSe and In2Se3 it deletes the entire selected group, so Gate 3 has **no denominator and no yield**, not 0% yield.
- Keeping sample 17458's known glitch makes WSe2 appear slightly worse at 1.0 nm: 109/214 = 50.9% rather than the reviewed 110/214 = 51.4%. The small aggregate change does not make the glitch harmless; it shows why provenance matters even when a median or percentage is robust.

### Wrong interpretation at Gate 3

- Picking 0.5 nm because it “sounds best” violates the 75% yield constraint.
- Picking 2.0 nm for MoS2 meets yield but is not the **strictest** passing option.
- Dividing by the original 1,004 instead of the rows carried through the chosen material and cleaning gates produces the wrong conditional percentage. The denominator must remain visible throughout.

## Sample-size traps

Gate 1 should display `n` as prominently as the median. The raw six-card summaries are:

| Material | n | Median roughness | IQR | Share at or below 1.0 nm before Gate 2 |
|---|---:|---:|---:|---:|
| MoS2 | 401 | 0.473 nm | 0.635 nm | 311/401 = 77.6% |
| WS2 | 144 | 0.534 nm | 0.705 nm | 106/144 = 73.6% |
| MoSe2 | 43 | 0.662 nm | 0.587 nm | 31/43 = 72.1% |
| WSe2 | 214 | 0.983 nm | 1.271 nm | 109/214 = 50.9% |
| GaSe | 51 | 1.320 nm | 1.711 nm | 15/51 = 29.4% |
| In2Se3 | 33 | 3.409 nm | 5.470 nm | 2/33 = 6.1% |

MoSe2 and In2Se3 should carry a **“small evidence pool”** badge because `n < 50`; GaSe at 51 should remain visibly close to that boundary. Do not ban those choices—the consequence is part of the lesson—but show that one sample changes MoSe2's yield by about 2.3 percentage points and In2Se3's by about 3.0 points, versus about 0.25 points for MoS2.

The apparent 90.7% MoSe2 yield at the loose 2.0 nm spec is based on only 43 scans. It should not outrank MoS2 for the stated primary-channel job merely because a small group's percentage is larger at a different, looser specification.

No `n = 0` path may display “0%.” It must display **“No result—your cleaning rule removed the whole group.”** Zero successes from observed rows and no observed rows are different mathematical statements.

## Minimal information panel at each gate

### Gate 1 · Pick a material (about 3 minutes)

Show exactly six cards. Each card needs only:

- plain name and formula;
- one job tag copied/paraphrased from `why_it_matters` (“main transistor channel,” “partner transistor,” “light,” “optics,” or “memory”);
- `n`, median, and IQR;
- a tiny common-scale box/dot strip; and
- the sentence **“smaller roughness = flatter measured patch.”**

Prompt: **“Which material fits the job and has the strongest smoothness evidence?”** No band gaps, lattice constants, growth methods, or atom diagrams are needed.

### Gate 2 · Pick a cleaning rule (about 4 minutes)

Show the same three rule cards A/B/C for whichever material survived Gate 1. Each card needs:

- one plain-language rule sentence;
- rows before → rows after;
- one real example (`MoS2; MoS2`, sample 17458's bad line, or blank growth time); and
- a bar that visibly changes the carried denominator.

Prompt: **“Which rule fixes documented problems without deleting rows for information this decision never uses?”** Define blank as “not recorded,” not zero. Do not ask students to recognize chemical names; every text rule is explained mechanically.

### Gate 3 · Set the spec and calculate yield (about 4 minutes)

Show three large buttons: **0.5 nm**, **1.0 nm**, **2.0 nm**. Each updates:

- a fixed-scale roughness dot/histogram with pass/fail shading;
- the integer fraction `passing / total`;
- the calculation `passing ÷ total × 100` rounded to one decimal place; and
- a 75% contract line marked pass/fail.

Prompt: **“Choose the smallest specification that reaches at least 75%. Then report the yield.”** Keep the material and cleaning choices pinned above the chart so the causal chain of the student's own decisions is visible.

### Result panel (about 2 minutes)

Use one sentence with all three choices:

> With **MoS2**, the **purpose-built audit**, and a **1.0 nm** limit, **313 of 403 scans pass: 77.7% yield**.

Then show one comparison sentence: **“0.5 nm fails at 53.8%; 2.0 nm passes but is not the strictest passing option.”** If the student took another path, show its actual result first, then a “compare with the contract-winning path” button. Early choices must never be silently overwritten.

## Implementation and interpretation guardrails

- Embed the needed real rows locally in the static page; no account, CDN, or fetch is necessary.
- Freeze the demo to a named slice/version and put the count/date in a small source note. Otherwise a future slice rebuild can move the single correct answer.
- Use one decimal place for yield and three decimals for Gate 1 medians. The pass/fail calculation must use unrounded roughness values.
- Do not describe yield as manufacturing yield. It is **“share of measured scans meeting this classroom contract.”** These public research samples were not a random production lot.
- Do not claim smoothness alone determines transistor performance. The scenario deliberately holds the decision to one measured quantity so the math problem is bounded.
- Do not call every extreme value an error. Rule A corrects sample 17458 because the underlying image documents one corrupted line; it keeps the real 92 nm MoS2 measurement.
- Preserve the real-data provenance: 2DCC data are CC BY 4.0; cite the dataset/slice and 2DCC-MIP as already requested in `data/slice/camel-2dcc/README.md`.

## Bottom line for the lead's merge

The cleanest student-facing story is not “guess the scientifically perfect material.” It is **satisfy a written data contract**: right job, relevant cleaning, at least 75% observed yield, smallest offered roughness limit. That framing makes every gate ordinary high-school statistics/algebra, keeps the physics to four plain-language sentences, and produces one answer with visible consequences for every wrong turn.

## Revision: making Gate 2 matter

This revision responds to two weaknesses in the first design. It is the recommended version to implement; the earlier analysis remains above as an audit trail.

### Revised contract

Remove the material job tags entirely. Give students this data-only contract:

> Choose a material backed by at least **100 comparable scans**. At least **75%** of those scans must meet the final roughness specification. Choose the strictest available specification: **0.5 nm, 0.8 nm, or 1.0 nm**.

The three Gate 2 rules now address measurement comparability and outcome-based deletion. None patches an individual sample.

1. **Q · Complete scans, mixed window sizes:** keep rows with `lines === pixels`, but mix all AFM scan sizes.
2. **T · Trim high outliers:** within the selected material, compute `Q3 + 1.5 × IQR` on all its roughness values and delete every row above that upper fence. This is a recognizable textbook rule but a bad production-yield rule: it removes samples precisely because their measured outcome is high.
3. **W · Comparable measurements (best):** keep only completed **5 µm × 5 µm** scans: `lines === pixels && scan_size_um === 5`. Five micrometres is the common measurement window in this dataset. The slice documentation explicitly warns that roughness depends on scan size and says to compare samples at the same `scan_size_um` when it matters.

Rule W is best for a reason other than retaining the most data. For MoS2 it keeps **382** rows, fewer than Rule Q's 390 but more than Rule T's 353. It wins because it applies a measurement-design rule before looking at pass/fail outcomes: every retained roughness value came from the same-sized, completed scan. Rule T instead selects on the response variable and makes yield look better by deleting failures.

The 0.8 nm option is a scenario contract tier, not a physical transistor threshold. It is useful mathematically because the real MoS2 distribution has many observations on both sides of it; the cleaning rule therefore produces a visible change rather than a cosmetic denominator change.

### Implementable revised rules

```js
function revisedClean(rows, chosenMaterial, rule) {
  const selected = rows.filter(r =>
    r.material === chosenMaterial && Number.isFinite(r.rms_roughness_nm));

  if (rule === "complete") {
    return selected.filter(r => r.lines === r.pixels);
  }

  if (rule === "comparable") {
    return selected.filter(r =>
      r.lines === r.pixels && r.scan_size_um === 5);
  }

  if (rule === "trimHigh") {
    const values = selected.map(r => r.rms_roughness_nm).sort((a, b) => a - b);
    const q1 = quantile(values, 0.25); // use one documented quantile convention
    const q3 = quantile(values, 0.75);
    const upperFence = q3 + 1.5 * (q3 - q1);
    return selected.filter(r => r.rms_roughness_nm <= upperFence);
  }

  throw new Error("unknown cleaning rule");
}
```

The static site must use the same quantile convention used to generate the checked values below (pandas linear interpolation). To avoid cross-browser ambiguity, it can embed each material's computed upper fence alongside the raw rows: MoS2 1.89045, WS2 2.1156125, MoSe2 1.947475, WSe2 3.826875, GaSe 5.2613, and In2Se3 15.8519 nm.

### All 54 revised paths

Each cell is `passing / rows carried by Gate 2 = observed yield`. A numerical yield is not sufficient unless the carried denominator is at least 100.

| Material | Gate 2 rule | 0.5 nm | 0.8 nm | 1.0 nm |
|---|---|---:|---:|---:|
| MoS2 | Q · complete, mixed sizes | 207/390 = **53.1%** | 273/390 = **70.0%** | 303/390 = **77.7%** |
| MoS2 | T · trim high outliers | 215/353 = **60.9%** | 281/353 = **79.6%** | 311/353 = **88.1%** |
| MoS2 | W · complete 5 µm scans | 201/382 = **52.6%** | 266/382 = **69.6%** | 296/382 = **77.5%** |
| WS2 | Q · complete, mixed sizes | 65/141 = **46.1%** | 92/141 = **65.2%** | 105/141 = **74.5%** |
| WS2 | T · trim high outliers | 66/125 = **52.8%** | 93/125 = **74.4%** | 106/125 = **84.8%** |
| WS2 | W · complete 5 µm scans | 63/136 = **46.3%** | 87/136 = **64.0%** | 100/136 = **73.5%** |
| MoSe2 | Q · complete, mixed sizes | 9/22 = **40.9%** | 15/22 = **68.2%** | 17/22 = **77.3%** |
| MoSe2 | T · trim high outliers | 12/39 = **30.8%** | 26/39 = **66.7%** | 31/39 = **79.5%** |
| MoSe2 | W · complete 5 µm scans | 9/19 = **47.4%** | 15/19 = **78.9%** | 17/19 = **89.5%** |
| WSe2 | Q · complete, mixed sizes | 7/158 = **4.4%** | 55/158 = **34.8%** | 78/158 = **49.4%** |
| WSe2 | T · trim high outliers | 21/184 = **11.4%** | 80/184 = **43.5%** | 109/184 = **59.2%** |
| WSe2 | W · complete 5 µm scans | 7/145 = **4.8%** | 54/145 = **37.2%** | 74/145 = **51.0%** |
| GaSe | Q · complete, mixed sizes | 1/51 = **2.0%** | 3/51 = **5.9%** | 15/51 = **29.4%** |
| GaSe | T · trim high outliers | 1/46 = **2.2%** | 3/46 = **6.5%** | 15/46 = **32.6%** |
| GaSe | W · complete 5 µm scans | 0/16 = **0.0%** | 0/16 = **0.0%** | 3/16 = **18.8%** |
| In2Se3 | Q · complete, mixed sizes | 0/33 = **0.0%** | 2/33 = **6.1%** | 2/33 = **6.1%** |
| In2Se3 | T · trim high outliers | 0/30 = **0.0%** | 2/30 = **6.7%** | 2/30 = **6.7%** |
| In2Se3 | W · complete 5 µm scans | 0/2 = **0.0%** | 0/2 = **0.0%** | 0/2 = **0.0%** |

### Gate 2 now changes the correct material's final answer

For MoS2, the revised Gate 2 creates a consequential fork:

- **Best rule W:** 0.8 nm gives 266/382 = **69.6%**, missing the contract by **5.4 percentage points**. The correct Gate 3 answer is therefore **1.0 nm**, at 296/382 = **77.5%**.
- **Rule Q:** 0.8 nm gives 273/390 = **70.0%**; it also correctly requires **1.0 nm**. It is usable but less comparable because it mixes scan-window sizes.
- **Biased rule T:** deleting high outcomes changes 0.8 nm to 281/353 = **79.6%**, exceeding the contract by **4.6 points**. It produces the wrong final answer, **0.8 nm**.

The same dataset therefore swings **10.0 percentage points at the decisive 0.8 nm tier** solely because Rule T removed 48 high-roughness MoS2 scans. This is not knife-edge: the honest comparable result is 5.4 points below 75%, while the trimmed result is 4.6 points above it.

The teachable reveal is: **an outlier rule can be mathematically correct and still answer the wrong question.** Tukey fences are useful for flagging unusual observations; they are not automatic permission to delete the units that failed a quality requirement. If the job is to report the observed share passing, high but valid measurements belong in the denominator.

### Does Gate 1 work from scan data alone?

Yes, if the requirement is stated before students choose:

> Select a material that has at least **100 measured scans** and at least **75% at or below 1.0 nm roughness**. Prefer the lower median if more than one qualifies.

No `materials_reference.csv` job tag is needed. On the raw AFM cards:

| Material | Raw n | At or below 1.0 nm | Meets n ≥ 100 and yield ≥ 75%? |
|---|---:|---:|---|
| MoS2 | 401 | 311/401 = **77.6%** | **Yes** |
| WS2 | 144 | 106/144 = **73.6%** | No: yield is 1.4 points short. |
| MoSe2 | 43 | 31/43 = **72.1%** | No: both n and yield fail. |
| WSe2 | 214 | 109/214 = **50.9%** | No: yield fails. |
| GaSe | 51 | 15/51 = **29.4%** | No: both fail. |
| In2Se3 | 33 | 2/33 = **6.1%** | No: both fail. |

MoS2 is the only raw-data choice meeting both conditions. Crucially, the result survives the best Gate 2 rule: on completed 5 µm scans, MoS2 remains at 296/382 = **77.5%**, while WS2 is 100/136 = **73.5%** and WSe2 is 74/145 = **51.0%**. The minimum-n rule prevents MoSe2's 17/19 = 89.5% from masquerading as stronger evidence after the 5 µm restriction.

The observed MoS2–WS2 separation at 1.0 nm is **4.0 percentage points raw** and **4.0 points after Rule W**. Both groups have fair descriptive sample sizes (401 versus 144 raw; 382 versus 136 comparable). That is enough for one bounded answer about these records, but not enough to claim a universal population difference: the site should continue to say “best in this dataset under this contract,” not “scientifically proven best material.”

Without a stated minimum n, Gate 1 does **not** work: the 19 comparable MoSe2 scans show 89.5% at 1.0 nm and would win on percentage alone. Without the stated 1.0 nm/75% requirement, “choose from the scan data” is also open-ended; median, IQR, yield, and sample count can rank materials differently. The two-part contract is what makes the answer unique.

### Revised three-gate path to hand to the implementer

1. **Gate 1 — Evidence screen:** from scan data only, choose the material meeting `n >= 100` and `yield at 1.0 nm >= 75%`. Answer: **MoS2**.
2. **Gate 2 — Fair comparison rule:** choose completed 5 µm scans, not mixed windows and not deletion based on roughness outcome. Answer: **Rule W**.
3. **Gate 3 — Strictest contract tier:** test 0.5, 0.8, and 1.0 nm against 75%. Answer: **1.0 nm**, with `296 / 382 = 77.5%`.

Gate 2's chart should explicitly animate the 48 MoS2 high outliers disappearing under Rule T and show the denominator changing from 401 to 353. The accompanying sentence should say **“The rule removed failures because they failed”**. Under Rule W, it should instead highlight the `scan_size_um` and `lines/pixels` columns before showing 382 retained rows. This makes the distinction visible without requiring any materials-science knowledge.
