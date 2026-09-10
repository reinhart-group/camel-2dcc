{
  "review": {
    "scope": [
      "docs/specs/2026-09-10-composable-courseware-design.md",
      "~/Code/education/matse219/build.py",
      "~/Code/education/matse219/bin/concepts.py",
      "~/Code/education/matse219/bin/strip_live.py",
      "~/Code/education/matse219/bin/publish.py",
      "~/Code/education/matse219/modules/*.py",
      "~/Code/education/matse219/docs/build-conventions.md"
    ],
    "verdict": "Approve modules/manifests, but not five independent live dials. Use named build-time editions for structural choices; reserve runtime parameters for validated numeric choices. Prove one shared task before adding telemetry.",
    "findings": [
      {
        "rank": 1,
        "severity": "high",
        "concern": "The proposed live parameters cell cannot change variants already removed at build time.",
        "location": "design:70-78,131-133",
        "failure": "Changing `guidance` or `register` cannot restore cells stripped by the builder. Shipping all variants would expose duplicate instructions/answers. Changing data settings after later cells ran leaves stale plots, checks, and telemetry.",
        "fix": "Make `guidance`, `register`, modules, and exposed variables build-time choices. Limit runtime `PARAMS` to safe numeric choices such as sample size/seed; validate once and require Restart and Run All. Checks must derive references from immutable source data."
      },
      {
        "rank": 2,
        "severity": "high",
        "concern": "The dials are not orthogonal, so the apparent Cartesian product contains broken lessons.",
        "location": "design:43-68,80-88",
        "failure": "Examples include a bias task without `position`, an outlier task after `flagged-only` removes outliers, n=50 with only 20 rows, or open guidance without prerequisites. Successful execution does not detect pedagogical incoherence.",
        "fix": "Publish named supported profiles, not arbitrary combinations. Give each module machine-readable requirements and constraints (`requires_columns`, `min_rows`, `requires_messiness`, `assumes`, `minutes`), validate them after variant selection, and reject unsupported settings with a specific manifest error."
      },
      {
        "rank": 3,
        "severity": "high",
        "concern": "`Expects`/`Produces` names are too weak to be composition contracts.",
        "location": "design:20-39; MATSE build.py:57-64,157-180; MATSE modules/*.py:1-6",
        "failure": "MATSE strips front matter and merely warns when absent. Generic names such as `data`, `x`, and `y` collide. Finding an assignment cannot prove type, columns, units, row identity, mutability, or definition on every branch.",
        "fix": "Namespace outputs and define a small schema contract covering columns, units, type, and invariants. Reject missing inputs and duplicate producers; add runtime assertions after dataset modules. Do not promise static proof from AST assignment checks."
      },
      {
        "rank": 4,
        "severity": "medium",
        "concern": "A new `variant:` cell-marker language duplicates Jupytext metadata and conflicts with the inherited parser.",
        "location": "design:70-76,110-115; MATSE build.py:42-50,103-119",
        "failure": "The reference builder deliberately rejects unknown `# %%` titles. Adding another regex-only directive creates parsing, nesting, and code/markdown boundary rules that Jupytext already owns.",
        "fix": "Use standard Jupytext cell metadata/tags, for example namespaced tags such as `variant-guidance-scaffolded`, parsed through Jupytext/nbformat rather than regex. Require every alternative group to have exactly one selected cell. Keep stable `task_id` as explicit cell metadata, independent of notebook cell IDs."
      },
      {
        "rank": 5,
        "severity": "medium",
        "concern": "Validation scope and combinatorial testing are underspecified.",
        "location": "design:36-39,101-108,118-125; MATSE concepts.py:113-161,171-235; MATSE build.py:196-219; MATSE publish.py:207-243,486-501",
        "failure": "MATSE's finite AST registry exempts helper cells; readability checks cannot prove coherence or answer independence. Copying MATSE behavior could reduce conversion failure to a warning or permit cell errors. Testing every theoretical combination is infeasible.",
        "fix": "Build and execute every shipped manifest, fail closed on conversion or any unexpected cell error, schema-check contracts, and snapshot module order/task IDs. Test allowed profiles exhaustively; use pairwise/property tests only for runtime numeric ranges. Keep human review for prose, pacing, and answer independence."
      },
      {
        "rank": 6,
        "severity": "medium",
        "concern": "Telemetry identity and failure/privacy behavior need a contract before a hook ships.",
        "location": "design:90-99,134-135; MATSE build-conventions.md:34-67",
        "failure": "Jupytext preserves IDs by content within one destination, not across variants. Runtime edits can falsify stamped metadata. A blocking/error-leaking hook could disrupt class or unintentionally send source, answers, secrets, or identities.",
        "fix": "Defer telemetry until its event/privacy schema exists. Define semantic IDs, record build profile plus runtime-config hash, send no source/outputs/secrets, require consent, queue asynchronously with short timeouts, and contain all failures."
      },
      {
        "rank": 7,
        "severity": "medium",
        "concern": "The proposed first migration slice is still too large to isolate framework risk.",
        "location": "design:120-125",
        "failure": "Combining notebooks 02, 06, and A2 while introducing five dials, three guidance variants, compiler checks, and telemetry makes failures impossible to attribute and invites premature abstraction.",
        "fix": "Pilot one dataset module plus one task: `data_afm_summary` and `task_mean_median_by_hand`. Build exactly two named manifests (plain/scaffolded/small sample and explorer/open/larger sample), with telemetry a no-op and no live structural dials. Acceptance: deterministic outputs, contract/order validation, fail-closed execution on the real slice, independent answer checks, one Colab smoke test, and demonstrably shared task logic. Add one new dial only after this passes."
      }
    ],
    "reference_elements_to_reuse": [
      "Textual include expansion and front-matter stripping",
      "Jupytext `--update` for deterministic rebuilds",
      "Allowlisted publication and stale-artifact cleanup",
      "Concept-order checking as a limited lint, not a proof"
    ]
  }
}
