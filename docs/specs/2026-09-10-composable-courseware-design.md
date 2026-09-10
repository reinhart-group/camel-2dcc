# CAMEL composable courseware — design (for approval)

Date: 2026-09-10. Grounded in the CAMEL proposal (Data Translation Framework; "complexity dials";
`camel_pipeline` figure: Author → Build → Run) and the MATSE 219 build system in
`~/Code/education/matse219` (`build.py` include expansion, module contracts, `bin/concepts.py`,
`bin/strip_live.py`, `bin/publish.py`).

## Problem

Today the CAMEL material is hand-written notebooks: an "Explorer" set (00–07) and an "Algebra 1"
set (A1–A5) being written as separate copies. Two copies of the same lesson drift, and a teacher
cannot turn a dial — they can only pick a whole notebook. The proposal promises the opposite: one
set of source modules, lesson manifests that combine them, and dials that change difficulty
without removing authenticity.

## The three layers, as they will exist in this repo

### Layer 1 — Author: source modules (`modules/`)

Two kinds, each a jupytext percent-format fragment with the MATSE 219 front-matter contract
(`# Expects:` / `# Produces:` / `# Dials:` / `# ---`), so `build.py`'s stripping rule carries over:

- **Dataset components** — load one real 2DCC data product from the slice and expose named
  variables. They read dial values to choose *how much* data students see, never *which* data:
  `data_afm_summary` (roughness table), `data_grains_17458` (triangles on one wafer),
  `data_recipe` (one growth recipe), `data_fese_transport`, `data_chips`, `data_gallery`.
- **Task components** — one idea each, written once with variants per guidance level:
  `task_unit_ladder`, `task_scale_factor`, `task_mean_median_by_hand`, `task_outlier_effect`,
  `task_random_sample`, `task_bias_edge_scientist`, `task_line_profile`, `task_slope_of_ramp`,
  `task_linear_model_solve`, `task_temperature_scales`, `task_piecewise_reading`,
  `task_doubling_table`, `task_explore_3d`, `task_stl_export`, …

Content that exists now (notebooks 01–07, A1–A5) is decomposed into these modules; nothing is
thrown away.

**Compiler** (`bin/compile_modules.py`): validates every module — contract present, variables in
`# Produces:` actually defined, every variant block well-formed, reading level of each guidance
variant within its band, banned-word list for the `plain` register — and writes nothing new.
It is the gate that keeps modules "reusable structured units".

### Layer 2 — Build: lesson manifests (`lessons/*.yaml`) → build script → notebooks

A manifest is the only thing that differs between editions of a lesson:

```yaml
id: how-bumpy
title: "How Bumpy Is It? Mean, Median, and Samples"
standards: [S.ID.1, S.ID.2, S.ID.3, 7.SP.1]
minutes: 40
dials:
  guidance: scaffolded      # scaffolded | guided | open
  register: plain           # plain (≤ grade 8, story-only science) | explorer (science notes)
  sample_size: 50           # grains shown to students (population kept for the reveal)
  variables: [area_nm2]     # columns exposed; add height_nm, position for more complexity
  messiness: real           # real (keep merged/dust/missing, flagged) | flagged-only
modules:
  - setup
  - story_triangle_crystals
  - data_grains_17458
  - task_mean_median_by_hand
  - task_outlier_effect
  - task_random_sample
  - task_bias_edge_scientist
  - exit_ticket
```

`lessons/how-bumpy-explorer.yaml` would list the same modules with `guidance: open`,
`register: explorer`, `sample_size: all`, `variables: [area_nm2, height_nm, solidity, position]`.

**Build script** (`build.py`, adapted from MATSE 219's): for each manifest,
1. writes a parameters cell holding the dial values (students can see them; teachers can change
   them and re-run — the dial is live, not only a build-time switch);
2. expands `# %% include:` modules in order (MATSE 219 rule: course-local then shared);
3. keeps only the variant blocks matching the dials, marked in modules as
   `# %% [markdown] variant: guidance=scaffolded` / `# %% variant: register=explorer` (a new
   directive the build consumes, like `teaches:`, so it never reaches students);
4. inlines sketches (`# %% sketch:`) as MATSE 219 does;
5. converts with `jupytext --update`, executes, and runs the checks below.

**Dials, concretely** (the proposal's three plus the two this work showed are needed):

| Dial | Values | What changes | What never changes |
|---|---|---|---|
| sample size | e.g. 20 / 100 / all | rows or grains students see | data stay real, unsmoothed |
| number of variables | column list | which measurements are exposed | units, provenance |
| guidance | scaffolded / guided / open | worked example → fill-in-one-number → blank cell with a goal | the task's math idea |
| register | plain / explorer | reading level and how much science is explained | correctness of every claim |
| messiness | real / flagged-only | whether glitches, dust, blanks are left in or flagged-and-filtered | blanks are never zero |

### Layer 3 — Run: telemetry hook slot

Every built notebook includes `module: telemetry_hook` right after setup. By default it is a
no-op that prints nothing. When Becca's collector is configured (an env var / Colab Secret with
the FastAPI endpoint), it registers IPython `pre_run_cell` / `post_run_cell` handlers and ships
revision, error, and idle events as JSONL. Notebook cells carry stable IDs (jupytext `--update`)
and each task module stamps a `task_id` and the dial settings, so every telemetry event can be
tied to *which module at which dial setting* — the unit the learning-analytics questions (RQ1/RQ2)
need. This repo only defines the slot and the event metadata; the collector and dashboard are
Becca's framework.

## Checks the build runs (the "validation checklists")

- execute top to bottom with the real slice (existing `scripts/run_notebook.py`);
- reading level per register (`scripts/readability.py`: plain ≤ 8.0, explorer reported);
- concept ordering (`# %% teaches:` / `# %% assumes:`, adapted from `bin/concepts.py`) — e.g. a
  plain lesson cannot use slope before a module that teaches it;
- every answer check is independent of the student's own input (a review finding we hit twice);
- every widget has a static fallback.

## Reuse vs. new

- Reuse from MATSE 219 (copy, not import, so CAMEL stays self-contained for partner teachers):
  include expansion, front-matter stripping, sketch inlining, `--update` stable cell IDs, the
  concept-checker idea, publish-by-allowlist.
- New: manifests, the `variant:` directive, the parameters cell, the compiler, the telemetry slot.
- Unchanged: the data slice, SharePoint delivery, `camel_data` helpers, tests.

## Migration plan (after approval)

1. Scaffold `modules/`, `lessons/`, `build.py`, `bin/compile_modules.py` with tests.
2. Decompose one lesson end to end ("How Bumpy?", from notebooks 02 + 06 + A2) into modules with
   plain/explorer and scaffolded/guided/open variants; build two manifests; verify both.
3. Decompose the rest; the old hand-written notebooks move to `archive/` once their manifests
   build and pass.
4. Codex reviews the framework and one built lesson; Colab run of every built notebook.

## Revisions after Codex design review (docs/codex/review-composable-design.md)

All seven points accepted; they supersede the sections above where they conflict.

1. **Build-time vs. run-time.** `guidance`, `register`, the module list, and exposed `variables`
   are structural and fixed at build time. The notebook's runtime `PARAMS` holds only validated
   numeric choices (`sample_size`, `seed`); changing them requires Restart & Run All. Answer checks
   recompute references from immutable source data, never from student-edited objects.
2. **Named editions, not free combinations.** Each lesson ships a small set of supported profiles
   (e.g. `algebra1`, `explorer`). Modules declare machine-readable requirements
   (`requires_columns`, `min_rows`, `requires_messiness`, `assumes`, `minutes`); the builder
   rejects a manifest whose dial settings break a module, with a specific error.
3. **Real contracts.** Outputs are namespaced (`roughness_table`, `grains_table`), and each dataset
   module's contract (type, required columns, units, invariants) lives in YAML and is asserted at
   runtime right after the module runs. The builder checks manifest order for missing inputs and
   duplicate producers. No claim of static proof.
4. **Variants via Jupytext cell tags** (`variant-guidance-scaffolded`, `variant-register-plain`),
   parsed with Jupytext/nbformat; every alternative group must resolve to exactly one cell.
   `task_id` is explicit cell metadata, independent of notebook cell IDs.
5. **Testing.** Build and execute every shipped manifest, fail closed on conversion or any
   unexpected cell error, snapshot module order/task IDs; exhaustive over shipped profiles,
   property tests only for runtime numeric ranges; human review stays for prose and pacing.
6. **Telemetry deferred.** The slot ships as a no-op. Before it activates: deterministic semantic IDs
   (`lesson/module/task/cell_role`), build profile + runtime-config hash on every event, no source,
   outputs, or secrets sent, consent, async queue with short timeouts, silent bounded failures.
7. **Smaller pilot.** One dataset module (`data_afm_summary`) + one task
   (`task_mean_median_by_hand`), two named manifests (`algebra1`: plain/scaffolded/small sample;
   `explorer`: explorer/open/larger sample). Acceptance: deterministic outputs, contract and order
   validation, fail-closed execution on the real slice, independent answer checks, one Colab smoke
   test, and visibly shared task logic. Add a dial only after the pilot passes.

## Open questions for Wes

1. Copy MATSE 219's build code into CAMEL, or factor a shared tiny package both repos import?
   (Recommend: copy now, factor later if a third course appears.)
2. Teachers pick an edition (build-time) and may change only numeric data dials such as sample size
   and seed in Colab (revision 1). Is that enough control for the partner teachers, or do they need
   more editions per lesson?
3. Does Becca's telemetry framework already define an event schema (xAPI/Caliper per the proposal)
   that the hook should emit?
