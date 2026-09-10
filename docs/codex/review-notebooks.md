{
  "review": {
    "scope": [
      "notebooks/src/00_teacher_live_list.py",
      "notebooks/src/02_how_smooth_is_smooth.py",
      "notebooks/src/03_micrometers_to_football_field.py",
      "notebooks/src/04_build_a_crystal.py",
      "notebooks/src/05_chips_for_ai.py",
      "notebooks/teacher/02_how_smooth_is_smooth_key.md",
      "notebooks/teacher/03_micrometers_to_football_field_key.md",
      "notebooks/teacher/04_build_a_crystal_key.md",
      "notebooks/teacher/05_chips_for_ai_key.md"
    ],
    "overall_assessment": "Most default arithmetic and teacher-key values agree with the current slice, and the IEA, rounded TMD optical-energy, common superconductor, Moore-law, and Blackwell figures are defensible when kept approximate. The largest problems are architectural and conceptual: the live-LiST notebook cannot work from a hosted Colab runtime behind PSU's network gate; all five notebook sources still embed the old setup cell instead of the newly fixed shared cell; notebook 03 draws a physically incorrect MoS2 lattice and overstates a thresholded window scan as hundreds of measured step edges; and notebook 05 confuses optical transition energies with a free-carrier band gap while making a demonstrably false claim about the thinnest reported silicon research channel.",
    "finding_count": 27,
    "findings": [
      {
        "rank": 1,
        "severity": "critical",
        "category": "Colab",
        "title": "The live-LiST notebook cannot reach a PSU-network-gated host from Google Colab",
        "location": "notebooks/src/00_teacher_live_list.py:15,23-27,33-54,85-191",
        "failure_scenario": "The text implies that putting the user's browser on campus Wi-Fi or GlobalProtect makes the live calls work in Colab. A hosted Colab kernel sends requests from Google's infrastructure, not through the user's local PSU network/VPN. Under the stated network gate, a teacher can obtain and configure a key correctly and still wait up to 60 seconds for a call that cannot connect; Tasks 1-4 then skip. This contradicts the project premise that Colab cannot hit LiST directly.",
        "suggested_fix": "Label this as a local-Jupyter/Python notebook and instruct users to run the kernel itself on a PSU-connected machine or approved PSU-hosted environment. Keep a separate Colab version that demonstrates the client with cached responses only. Do not suggest that a browser-side VPN changes a remote Colab kernel's egress route."
      },
      {
        "rank": 2,
        "severity": "critical",
        "category": "Colab",
        "title": "The student sources did not receive the fixed shared setup cell",
        "location": "notebooks/src/00_teacher_live_list.py:61-82; notebooks/src/02_how_smooth_is_smooth.py:43-64; notebooks/src/03_micrometers_to_football_field.py:41-62; notebooks/src/04_build_a_crystal.py:56-77; notebooks/src/05_chips_for_ai.py:45-66",
        "failure_scenario": "Commit 5aad177 hardened notebooks/src/_setup_cell.py, but every reviewed notebook still contains the previous directory-exists/PK-magic/extractall setup. Teachers therefore do not get the new release-ID/completeness checks or HTTP raise_for_status behavior. A partial camel-2dcc directory remains permanently trusted, and a replaced ZIP can still supply the imported classroom.py. Fixing the template alone has no effect on the notebooks students run.",
        "suggested_fix": "Regenerate or mechanically synchronize every source and .ipynb from the canonical setup cell, then add a test that extracts each setup block and compares it with _setup_cell.py. Prefer a build-time include mechanism so copied setup code cannot drift again."
      },
      {
        "rank": 3,
        "severity": "high",
        "category": "physics",
        "title": "The MoS2 honeycomb drawing uses the lattice constant as a bond/hexagon side and assigns the wrong atom pattern",
        "location": "notebooks/src/03_micrometers_to_football_field.py:250-286",
        "failure_scenario": "draw_honeycomb uses a=0.316 nm as the radius/side of each drawn hexagon and alternates Mo and S around its six vertices. In real 1H-MoS2, a is the in-plane translation/Mo-Mo distance; one monolayer has a triangular Mo plane between two S planes in trigonal-prismatic coordination, not an alternating flat Mo-S honeycomb with 0.316 nm edges. The caveat says simplified, but the labels and scale still teach a false crystal structure immediately before students use a as a real lattice constant.",
        "suggested_fix": "Draw the actual projected primitive cell from fractional coordinates, with separate top/bottom S planes indicated, or make the picture purely geometric and remove atom identities and the numerical lattice constant. Keep the correct primitive-cell area formula sqrt(3)a^2/2, but explicitly define a as the translation-vector length."
      },
      {
        "rank": 4,
        "severity": "high",
        "category": "data interpretation",
        "title": "The 'whole-scan survey' is circular and counts overlapping windows, not independent step edges",
        "location": "notebooks/src/03_micrometers_to_football_field.py:200-229; notebooks/teacher/03_micrometers_to_football_field_key.md:58-64",
        "failure_scenario": "The helper scans roughly 134,000 row/window positions, preselects results whose height is already between 0.5 and 1.5 nm, and returns 392 overlapping windows. Adjacent rows and nearby columns can count the same physical boundary repeatedly. Calling these '392 clean single-layer edges' and treating their median/IQR as a real uncertainty distribution makes agreement with the expected 0.95 nm partly built into the filter and grossly overstates independent sample size. The key's claim that only about 800 candidate edges were scanned is also incorrect.",
        "suggested_fix": "Either relabel the output honestly as '392 qualifying windows under this rule' and use it only as an image-processing demonstration, or detect and cluster continuous boundaries so each physical edge is counted once, choose thresholds without using the target answer, and validate against manually labeled terraces. Do not call the resulting spread measurement uncertainty unless repeated independent measurements support that interpretation."
      },
      {
        "rank": 5,
        "severity": "high",
        "category": "math/data integrity",
        "title": "The printed vertical exaggeration does not describe the STL that was written",
        "location": "notebooks/src/03_micrometers_to_football_field.py:352-390; notebooks/teacher/03_micrometers_to_football_field_key.md:81-89",
        "failure_scenario": "The notebook computes real_relief_nm with the full peak-to-peak range, but to_stl maps the 0.5th-to-99.5th percentile span to relief_mm and clips values outside it. For the current triangle_pyramids scan, peak-to-peak is about 8.79 nm while the STL's percentile span is about 6.00 nm, so the actual vertical exaggeration is about 46% larger than the displayed value. Students are told the printed number characterizes their physical model when it does not.",
        "suggested_fix": "Use exactly the same lo/hi definition as to_stl when computing vertical_scale, ideally by returning export metadata from to_stl. Print both 'full measured range' and 'range mapped to STL relief' if the clipping lesson is useful, and update the key from the returned metadata."
      },
      {
        "rank": 6,
        "severity": "high",
        "category": "physics",
        "title": "The claim that research silicon channels have only reached roughly 5 nm is false",
        "location": "notebooks/src/05_chips_for_ai.py:155-179; notebooks/teacher/05_chips_for_ai_key.md:86-88",
        "failure_scenario": "The notebook says the thinnest reported research silicon channels are roughly 5 nm. Experimental silicon gate-all-around research has reported substantially thinner bodies, including a 0.65 nm silicon channel (Applied Physics Letters 110, 032101, 2017). The 5 nm comparison can still be a useful representative nanosheet dimension, but it cannot be described as the research lower limit.",
        "suggested_fix": "Call 5 nm a deliberately chosen illustrative silicon nanosheet thickness, not the thinnest reported value. Explain that channel thickness, gate length, process-node label, device architecture, and practical manufacturability are different quantities; keep the ratio task explicitly hypothetical."
      },
      {
        "rank": 7,
        "severity": "high",
        "category": "physics",
        "title": "The band-gap definition and the values used for color describe different physical quantities",
        "location": "notebooks/src/05_chips_for_ai.py:27-30,212-287; notebooks/teacher/05_chips_for_ai_key.md:57-63",
        "failure_scenario": "The glossary defines band gap as energy that frees an electron to carry current, but the table values near 1.55-2.0 eV are rounded optical/excitonic transition energies. In monolayer TMDs, the quasiparticle gap and optical transition differ by the exciton binding energy. The arithmetic lambda=1240/E is correct for a photon of the listed optical energy, but calling the result the color the material 'makes' or a free-carrier band gap conflates absorption, exciton emission, and electronic conduction.",
        "suggested_fix": "Rename the classroom field and section to approximate optical transition energy, define it as the energy of a prominent absorbed/emitted photon, and reserve 'electronic band gap' for the valence-to-conduction band separation. Keep the existing emission-efficiency caveat and add that substrate, strain, temperature, excitons, and dielectric environment shift the observed peak."
      },
      {
        "rank": 8,
        "severity": "high",
        "category": "math/physics",
        "title": "An unmeasured ramp start is converted into an apparently exact experimental slope",
        "location": "notebooks/src/04_build_a_crystal.py:141-217; notebooks/teacher/04_build_a_crystal_key.md:23,41-48",
        "failure_scenario": "The source records a 17-minute 'Ramp up T' endpoint/setpoint of 1000 C but no starting temperature. The notebook assumes 25 C, says furnaces start near room temperature, and then calls 57.35 C/min a good model; the key calls the 8.28-minute crossing arithmetic 'not an estimate.' A reactor may begin warm, and no data establish a linear ramp or its starting temperature. The calculation is exact only conditional on two invented assumptions.",
        "suggested_fix": "Label the entire line as a hypothetical model: 'If the ramp was linear and began at 25 C...' Report the slope and crossing as conditional estimates, not recipe measurements. Better, let students compare two assumed start temperatures or use a recipe with recorded endpoints if one exists."
      },
      {
        "rank": 9,
        "severity": "high",
        "category": "physics/context",
        "title": "The superconductor section encourages an incorrect data-center cooling/energy takeaway",
        "location": "notebooks/src/05_chips_for_ai.py:2-8,33-36,305-384,438-446; notebooks/teacher/05_chips_for_ai_key.md:82-93",
        "failure_scenario": "The I^2R example correctly gives zero DC resistive loss inside an ideal superconductor, but the surrounding narrative asks why this matters for all data-center electricity and even asks why superconductors are not 'already cooling' data centers. Superconductors do not cool equipment; they require cryogenic cooling. Real systems also have refrigeration overhead, contacts, power conversion, and AC/time-varying losses. Placing the full 415 TWh figure beside a 100 W wire example invites students to infer an unsupported system-level saving.",
        "suggested_fix": "Say superconductors might reduce selected interconnect or magnet losses in specialized future systems, not cool data centers or eliminate total energy use. Add the cryogenic energy cost and non-wire loads, and keep the IEA calculation as a separate scale exercise rather than evidence for the superconductor claim."
      },
      {
        "rank": 10,
        "severity": "high",
        "category": "pacing",
        "title": "Notebook 03's advertised core path is not credible in one 45-50 minute non-AP class",
        "location": "notebooks/src/03_micrometers_to_football_field.py:10-19,80-415; notebooks/teacher/03_micrometers_to_football_field_key.md:26-38,115-121",
        "failure_scenario": "The core path still asks students to complete nine numbered tasks spanning multistep unit conversion, feature scaling, an interactive AFM profile, layer division/rounding, crystallographic unit-cell area, scientific-notation counting, a log-log surface-area/volume graph, STL generation/download, and an exit ticket. The source is roughly 2,900 words before rendered plots and interaction. Typical Algebra/Geometry students will either rush without interpreting or fail to reach the promised 3D-print payoff.",
        "suggested_fix": "Split this into two periods ('scale and layers' and 'geometry plus 3D printing') or reduce the true 45-minute core to Tasks 1-5 plus STL export and exit ticket. Make hexagonal cells and SA:V a separate extension notebook/worksheet rather than another core strand."
      },
      {
        "rank": 11,
        "severity": "medium",
        "category": "physics",
        "title": "Monolayers are repeatedly described as one atom thick",
        "location": "notebooks/src/03_micrometers_to_football_field.py:21-30,65-68; notebooks/src/05_chips_for_ai.py:23-26,347-355",
        "failure_scenario": "A MoS2 monolayer is one structural layer but contains three atomic planes (S-Mo-S); monolayer FeSe likewise is a single formula-unit layer, not literally one atom plane. The current wording conflicts with notebook 03's later, more accurate description of a Bi2Se3 quintuple layer and can make students think 'monolayer' always means one plane of atoms.",
        "suggested_fix": "Define monolayer as one repeating structural sheet, which may contain several atomic planes. Say MoS2 is one S-Mo-S layer about 0.65 nm thick and single-layer FeSe is one FeSe unit-cell layer."
      },
      {
        "rank": 12,
        "severity": "medium",
        "category": "physics",
        "title": "The same 5 micrometer scan is described both as 20 times smaller than and about the width of a hair",
        "location": "notebooks/src/03_micrometers_to_football_field.py:4-8,65-68",
        "failure_scenario": "The opening reasonably says a few-micrometer scan is about 20 times smaller than a hair diameter, but the 'Meet your crystal' text says the 5 micrometer scan is about the width of a fine human hair. Typical hair diameters are tens of micrometers, so students receive contradictory scale anchors within a minute.",
        "suggested_fix": "Use one qualified comparison throughout: a 5 micrometer scan is roughly one-tenth to one-twentieth of a typical human-hair diameter, depending on the hair."
      },
      {
        "rank": 13,
        "severity": "medium",
        "category": "physics/data interpretation",
        "title": "The notebook asserts every triangular Bi2Se3 step is one quintuple layer",
        "location": "notebooks/src/03_micrometers_to_football_field.py:136-140",
        "failure_scenario": "Bi2Se3 commonly shows approximately 0.95 nm quintuple-layer steps, but an AFM image can contain steps of multiple quintuple layers, overlapping terraces, adsorbates, and artifacts. The notebook's own purpose is to measure and decide the layer count, so declaring every triangular step one layer tall pre-answers and overstates the observation.",
        "suggested_fix": "Say the triangular terraces often have step heights near one or several quintuple layers, and ask whether this selected edge is consistent with one quintuple layer."
      },
      {
        "rank": 14,
        "severity": "medium",
        "category": "math/visualization",
        "title": "A probability-density histogram is labeled as fraction of pixels",
        "location": "notebooks/src/02_how_smooth_is_smooth.py:131-145",
        "failure_scenario": "Matplotlib density=True normalizes total bar area to one; bar heights are probability density with units 1/nm, not the fraction of pixels in each bin. Students learning histograms can read the y-value as a direct fraction, especially when comparing scans with different bin widths or ranges.",
        "suggested_fix": "Either label the axis 'probability density (1/nm)' and explain area, or use weights=np.ones(n)/n with common bin edges and label the y-axis 'fraction of pixels per bin.'"
      },
      {
        "rank": 15,
        "severity": "medium",
        "category": "data description",
        "title": "The AFM table is described as one row per scan when it is one selected scan per sample",
        "location": "notebooks/src/02_how_smooth_is_smooth.py:176-183; notebooks/src/00_teacher_live_list.py:267-275",
        "failure_scenario": "afm_summary.csv contains one pipeline-selected primary SPM per measured sample, not every AFM scan. Calling it one row per real scan and 'almost every public sample' hides the selection step and encourages students to treat the rows as a census of measurements rather than a curated sample-level summary.",
        "suggested_fix": "Describe it as one selected AFM height scan for each sample where the pipeline found a usable calibrated SPM, and link to the documented primary-selection limitation. Include selection/error counts in the teacher note."
      },
      {
        "rank": 16,
        "severity": "medium",
        "category": "data interpretation",
        "title": "Material labels alone do not establish that rows are bare-substrate scans",
        "location": "notebooks/src/02_how_smooth_is_smooth.py:176-217; notebooks/teacher/02_how_smooth_is_smooth_key.md:41-47",
        "failure_scenario": "The cleaning helper calls Al2O3, Sapphire, GaAs, H2, and Se 'bare substrates' solely from the first material label. GaAs and Se can be intentional sample materials, and the LiST label does not by itself prove what surface the selected AFM channel imaged. Students are told they are removing non-film scans when the rule is actually a heuristic exclusion list.",
        "suggested_fix": "Rename the switch to EXCLUDE_SELECTED_MATERIAL_LABELS and explain it is a classroom heuristic, or derive bare-substrate status from reviewed sample/activity metadata. Keep the nine-row count but do not attach an unsupported physical interpretation."
      },
      {
        "rank": 17,
        "severity": "medium",
        "category": "statistics",
        "title": "Task 4b asks students to compare raw outlier counts across very unequal group sizes",
        "location": "notebooks/src/02_how_smooth_is_smooth.py:251-306; notebooks/teacher/02_how_smooth_is_smooth_key.md:48-55",
        "failure_scenario": "The printed statistic is number of 1.5-IQR points, while group sizes range from 3 MBE scans to 751 MOCVD scans. Asking which has 'more or fewer outliers' rewards the largest group and makes the n=3 boxplot appear comparable even though its quartiles and whiskers are unstable.",
        "suggested_fix": "Print and compare outlier fraction as well as count, require a minimum n for group comparison, and explicitly exclude or gray out n=3 MBE from the core inference. Emphasize that boxplot flags are rule-based unusual points, not proof of bad data."
      },
      {
        "rank": 18,
        "severity": "medium",
        "category": "physics",
        "title": "The MOCVD/Hybrid-MBE and anneal definitions are too absolute",
        "location": "notebooks/src/04_build_a_crystal.py:4-12,29-39,247-260",
        "failure_scenario": "MOCVD is described as leaving a crystal 'layer by layer,' although layer-by-layer growth is an outcome to control, not an inherent cycle-by-cycle mechanism like ALD. Hybrid MBE can combine solid-source beams with a gas/molecular precursor, so 'beams of atoms' is incomplete. Annealing can occur under a reactive flux and can change composition; it is not always simply holding without adding atoms. 'MOCVD growth runs around 1000 C' is true for the selected recipe but not a general method definition.",
        "suggested_fix": "Say gaseous metal-organic/chalcogen precursors react at a heated surface and may form mono- or few-layer films; say hybrid MBE supplies controlled atomic/molecular fluxes in high or ultrahigh vacuum, sometimes including a precursor gas. Define anneal as a heat-treatment step with no intended net deposition, and qualify 1000 C as this MoS2 recipe's setpoint."
      },
      {
        "rank": 19,
        "severity": "medium",
        "category": "causal overclaim",
        "title": "Every AFM bump is attributed to the recipe",
        "location": "notebooks/src/04_build_a_crystal.py:80-96",
        "failure_scenario": "The statement 'Every bump and terrace ... is a consequence of the recipe' excludes substrate morphology, transfer/handling, contamination, oxidation, tip convolution, feedback artifacts, and processing. It primes students for the causal overclaim the later correlation section warns against.",
        "suggested_fix": "Say the final surface reflects the recipe plus substrate, environment, handling, and measurement/processing, and that this notebook explores one possible connection rather than assigning every feature a cause."
      },
      {
        "rank": 20,
        "severity": "medium",
        "category": "Colab/usability",
        "title": "The recipe dropdown offers known failing choices and is not searchable",
        "location": "notebooks/src/04_build_a_crystal.py:300-346; notebooks/teacher/04_build_a_crystal_key.md:61-68,90-104",
        "failure_scenario": "The ipywidgets 7.7 Dropdown contains 334 IDs; despite the instruction to 'type to search,' Dropdown is not a searchable combobox. Seven current options have a ramp with missing temperature, so the provided new_slope expression prints nan; any no-ramp future row would raise IndexError. The key says any two samples are valid and only later relegates failures to troubleshooting.",
        "suggested_fix": "Pre-filter to recipes with exactly one classroom-usable ramp and complete endpoint/duration fields, or display a clear missing-data message instead of indexing iloc[0]. Use Combobox with validated options or a short curated dropdown of 6-10 contrasting recipes."
      },
      {
        "rank": 21,
        "severity": "medium",
        "category": "teacher documentation",
        "title": "The live guide names a nonexistent file and misstates the rebuild workflow",
        "location": "notebooks/src/00_teacher_live_list.py:267-287",
        "failure_scenario": "The table lists mbe_recipes.csv, but the released file is growth_recipes.csv and includes MOCVD plus Hybrid MBE. It then says PublicLiST is the route scripts/build_slice.py uses, although build_slice.py is explicitly offline and consumes already staged raw pulls. A teacher following these instructions will request the wrong file or expect build_slice.py to refresh LiST.",
        "suggested_fix": "Use growth_recipes.csv and describe the actual staged commands in order: public index/pull scripts on a PSU-connected local machine, AFM/recipe processing, then the offline build_slice.py release assembly."
      },
      {
        "rank": 22,
        "severity": "medium",
        "category": "maintenance/privacy",
        "title": "The copied live client has already drifted from the reviewed source client",
        "location": "notebooks/src/00_teacher_live_list.py:95-171",
        "failure_scenario": "The notebook says the helper is copied straight from src/camel_data/list_public.py, but it lacks the source's new empty-secret validation and any shared import/synchronization mechanism. Its statement that the key can 'only ever' see Published data also depends entirely on users supplying the intended public key; the inline client itself performs no status check before displaying live records.",
        "suggested_fix": "Generate the helper from the source module or distribute a versioned, reviewed client package rather than maintaining a second copy. Validate key configuration and assert Published status before displaying/exporting results; soften the absolute privacy claim to describe the dedicated public key's intended scope."
      },
      {
        "rank": 23,
        "severity": "medium",
        "category": "statistics/history",
        "title": "The fitted 'Moore's law' line mixes selected CPUs, GPUs, and a two-die package",
        "location": "notebooks/src/05_chips_for_ai.py:69-152; notebooks/teacher/05_chips_for_ai_key.md:47-51",
        "failure_scenario": "The 18 hand-picked records switch from single-die Intel CPUs to Apple SoCs and NVIDIA accelerators, with the final B200 count spanning two dies. This is not a consistent population or random time series, so the fitted 2.05-year doubling time is strongly shaped by curation and package definition. Calling it a proper fit to 'real chips' can make students think it independently verifies Moore's law.",
        "suggested_fix": "Call it a fit to a selected illustrative upper-envelope dataset and discuss the changing definitions. Better, use a consistent published series such as transistor density or one product class, or make selection sensitivity the statistics lesson. Keep the accurate note that Moore's law is an empirical industry trend rather than physics."
      },
      {
        "rank": 24,
        "severity": "medium",
        "category": "physics/visualization",
        "title": "A disputed/ranged FeSe transition is plotted as one exact critical temperature",
        "location": "notebooks/src/05_chips_for_ai.py:305-357; notebooks/teacher/05_chips_for_ai_key.md:57-65",
        "failure_scenario": "The prose admits that monolayer FeSe/SrTiO3 reports vary, while superconductors.csv stores 65 K and the plot shows a single exact point. The cited 65 +/- 5 K result is a superconducting signature inferred from spectroscopy under optimized annealing, whereas reported onset, gap-closing, and zero-resistance temperatures are not interchangeable. Students have just been told Tc is the boundary below which resistance is exactly zero.",
        "suggested_fix": "Use a range/error bar and label which criterion each value represents. For a non-AP lesson, either omit the contested thin-film point or say 'reported superconducting signature/onset, approximately 40-65 K' rather than treating 65 K like the bulk zero-resistance values."
      },
      {
        "rank": 25,
        "severity": "medium",
        "category": "Colab/accessibility",
        "title": "The core Moore-law slider has no static fallback",
        "location": "notebooks/src/05_chips_for_ai.py:79-127; notebooks/teacher/05_chips_for_ai_key.md:32-45,97-98",
        "failure_scenario": "Task 1 is core and depends on an ipywidgets callback that repeatedly creates Plotly figures. If the Colab widget manager fails, the key only says to rerun setup; unlike notebook 04, there is no static plot or non-widget route, so students cannot perform the first task.",
        "suggested_fix": "Render one ordinary Plotly figure at d=3 outside the widget and provide two or three static candidate curves or a numeric input fallback. Keep the slider as optional enhancement, not the only core representation."
      },
      {
        "rank": 26,
        "severity": "low",
        "category": "answer key",
        "title": "Notebook 03's teacher key no longer matches the printed terrace values",
        "location": "notebooks/src/03_micrometers_to_football_field.py:147-190; notebooks/teacher/03_micrometers_to_football_field_key.md:53-56",
        "failure_scenario": "Against the current slice, the helper prints Terrace A=0.98 nm, Terrace B=-0.07 nm, and a 1.05 nm difference. The student defaults instead use 0.99 and -0.08 to print 1.07 nm, while the key says the helper itself printed a 1.07 nm step and 1.13 layers. A student who correctly copies the current helper output gets about 1.10 layers and can appear inconsistent with the key.",
        "suggested_fix": "Populate the calculation directly from terrace_a_nm and terrace_b_nm rather than asking students to retype rounded values, or clearly make the copy step blank. Regenerate the key from the current slice and distinguish raw helper values from deliberately rounded student inputs."
      },
      {
        "rank": 27,
        "severity": "low",
        "category": "pacing/teacher key",
        "title": "Notebook 04's timing table totals more than the claimed period",
        "location": "notebooks/teacher/04_build_a_crystal_key.md:30-39",
        "failure_scenario": "The listed segments reach minute 48 and then add a final five-minute exit ticket, totaling 53 minutes before transitions or setup delays. A teacher following the plan cannot finish in a 45-50 minute period.",
        "suggested_fix": "Make Tasks 6-8 explicitly optional before the schedule, reserve minutes 43-50 for the exit ticket, and provide a true 45-minute cutoff cue."
      }
    ],
    "verified_matches_and_non_findings": [
      "Notebook 02 current outputs match its key: RMS 1.414 nm for the five-number example; gallery RMS values about 0.358 and 17.833 nm; 1,004 raw rows and 898 default-clean rows; median 0.55295 nm; In2Se3 is roughest among the top six; scan-size Pearson r is about 0.0245.",
      "Notebook 04 current default arithmetic matches its key: start times [0,17,22,27,30,40,48], conditional slope 57.3529 C/min, conditional 500 C crossing 8.2821 min, and Hybrid-MBE deposition median 4.41e-10 Torr from 15 of 26 nonmissing records.",
      "Notebook 04's corrected growth summary still gives n=331, r about 0.0242, and roughness approximately 0.01654*time + 0.7543 nm for the current MoS2 subset.",
      "Notebook 05 current numeric outputs match its key: selected-chip d=2.05394 years; wavelengths 653, 620, 752, and 800 nm from the table; 77 K=-196.15 C=-321.07 F; +128% from 415 to 945 TWh; material counts 443/203/257/43.",
      "IEA's April 2025 Energy and AI base case supports 415 TWh and about 1.5% in 2024 and approximately 945 TWh by 2030. The notebook correctly presents 945 TWh as a projection, though it should retain the base-case/uncertainty wording.",
      "The rounded monolayer TMD optical energies are plausible classroom approximations; the main issue is naming/interpretation, not the lambda=1240/E arithmetic.",
      "Intel describes the modern Moore-law shorthand as transistor count doubling about every two years and explicitly calls it an observation rather than a natural law; NVIDIA supports 208 billion transistors across Blackwell's two connected dies. The notebook's caveats are good, subject to finding 23's dataset-consistency issue.",
      "The common bulk superconductor values and 65 +/- 5 K reported superconducting signature for optimized single-layer FeSe/SrTiO3 are broadly source-supported; finding 24 concerns mixing measurement criteria and suppressing uncertainty."
    ],
    "primary_sources_checked": [
      {
        "title": "IEA, Energy and AI — Energy demand from AI",
        "url": "https://www.iea.org/reports/energy-and-ai/energy-demand-from-ai",
        "supports": "415 TWh/about 1.5% in 2024; base-case projection around 945 TWh in 2030; stated projection uncertainty"
      },
      {
        "title": "Intel, Moore's Law",
        "url": "https://www.intel.com/content/www/us/en/newsroom/resources/moores-law.html",
        "supports": "two-year modern shorthand and empirical-observation caveat"
      },
      {
        "title": "NVIDIA Blackwell announcement",
        "url": "https://nvidianews.nvidia.com/news/nvidia-blackwell-platform-arrives-to-power-a-new-era-of-computing",
        "supports": "208 billion transistors and two connected dies"
      },
      {
        "title": "Thirunavukkarasu et al., Applied Physics Letters 110, 032101",
        "url": "https://doi.org/10.1063/1.4974255",
        "supports": "experimental 0.65 nm silicon gate-all-around channel, contradicting a 5 nm reported lower limit"
      },
      {
        "title": "Roldan et al., Electronic properties of single-layer and multilayer TMDs",
        "url": "https://onlinelibrary.wiley.com/doi/10.1002/andp.201400128",
        "supports": "MoS2 lattice constant near 0.316 nm and the distinction between lattice translation, atomic planes, and layer spacing"
      },
      {
        "title": "Measurements of electrically tunable refractive index of MoS2 monolayer",
        "url": "https://www.nature.com/articles/s41699-019-0119-1",
        "supports": "approximately 1.9 eV direct optical response, approximately 0.65 nm structural-layer thickness, and multiple atomic planes"
      },
      {
        "title": "Bandgap engineering of two-dimensional semiconductor materials",
        "url": "https://www.nature.com/articles/s41699-020-00162-4",
        "supports": "optical gaps vary by material/environment and must be distinguished from quasiparticle gaps"
      },
      {
        "title": "He et al., Phase Diagram and High Temperature Superconductivity at 65 K in Single-Layer FeSe",
        "url": "https://arxiv.org/abs/1207.6823",
        "supports": "reported superconducting signature around 65 +/- 5 K under optimized annealing and criterion/sample dependence"
      },
      {
        "title": "Spatial Dimensions in Atomic Force Microscopy: Instruments, Effects, and Measurements",
        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC11404149/",
        "supports": "AFM tip/sample and roughness effects; height and lateral measurements have different limitations"
      },
      {
        "title": "U.S. EIA residential electricity use",
        "url": "https://www.eia.gov/todayinenergy/detail.php?id=65244",
        "supports": "2024 average residential-customer use about 865 kWh/month, making 10,500 kWh/year a reasonable rounded classroom assumption"
      }
    ],
    "verification_method": [
      "Read all five source notebooks and the four corresponding teacher keys line by line.",
      "Recomputed notebook outputs directly from the current data/slice/camel-2dcc payload without modifying notebook or repository files.",
      "Checked the current shared setup cell and git commit 5aad177 to identify synchronization drift.",
      "Compared time-sensitive and specialist claims with IEA, EIA, Intel, NVIDIA, and research-paper sources listed above."
    ]
  }
}
