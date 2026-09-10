{
  "review": {
    "scope": [
      "notebooks/src/01_nano_landscapes.py",
      "notebooks/teacher/01_nano_landscapes_key.md",
      "data/slice/camel-2dcc (current rebuilt payload, used for all recomputation)"
    ],
    "overall_assessment": "The notebook runs with the stated Python/Plotly/ipywidgets versions, and nearly all numeric values in the teacher key still match the current rebuilt slice. The main problems are conceptual and instructional: the step-height helper does not measure step heights, the WSe2 static surface silently omits the very artifact students are asked to find, the AFM explanation teaches contact-mode and single-atom-tip claims as universal facts, and the flattening explanation describes a different operation from the one actually applied. The core arithmetic and histogram outputs themselves are reproducible, but two self-checks/inferences can reward incorrect reasoning.",
    "finding_count": 12,
    "findings": [
      {
        "rank": 1,
        "severity": "high",
        "category": "math/data interpretation",
        "title": "The helper counts peak-to-trough excursions, not physical step edges",
        "location": "notebooks/src/01_nano_landscapes.py:159-196; notebooks/teacher/01_nano_landscapes_key.md:42-48,88-90",
        "failure_scenario": "_step_sizes smooths each row, marks local maxima and minima, and reports the absolute difference between adjacent alternating extrema. It never identifies the two flat terrace plateaus on opposite sides of an edge. On the current slice it still prints 1,470 values with quartiles 0.21-0.38 nm and 10th-90th percentiles 0.15-0.47 nm, but only about 25.6% lie within 0.34-0.44 nm of the expected 0.39 nm unit-cell step. The detector even returns values as low as 0.029 nm despite min_height=0.08, because the threshold qualifies each extremum's surrounding window rather than the reported adjacent-extrema difference. Calling all 1,470 values 'step edges' and accepting 0.15 nm as a plausible single step teaches students that broad surface undulations/noise are noisy measurements of the lattice step.",
        "suggested_fix": "Use one or more curator-validated rows and x intervals that visibly cross a terrace boundary. Estimate each step from robust plateau medians on fixed-width regions before and after the boundary, then use neighboring rows for uncertainty. If automatic detection is retained, segment terraces, cluster the same continuous boundary across rows, and validate detected edges against labeled examples; label counts as algorithmic candidates until that validation exists. Tighten the feedback around a physically justified range rather than deriving it from unrelated extrema."
      },
      {
        "rank": 2,
        "severity": "high",
        "category": "Colab/data presentation",
        "title": "The static 3D view drops the WSe2 glitch that Task 5 asks students to find",
        "location": "notebooks/src/01_nano_landscapes.py:293-326; notebooks/teacher/01_nano_landscapes_key.md:62-70,97-100",
        "failure_scenario": "The current WSe2 map is 512x512 and its extreme artifact is row 1. surface_3d's default 256-pixel limit displays z[::2, ::2], so it includes rows 0, 2, 4, ... and omits row 1 completely. The full map has a -454.98 to +221.38 nm artifact, while the static surface actually plotted spans only -1.84 to +20.58 nm. The cross-section widget defaults to row 256; its image is auto-scaled by the extreme row, and a student must move a 512-position slider to exactly row 1 near the top. Thus the advertised no-widget route cannot reveal the target at all, and even a working Colab widget makes the six-minute hunt impractical unless students run the answer-reveal cell first.",
        "suggested_fix": "For this task, render the full 512 rows (for example, call surface_3d with max_pixels=512), or downsample in a way that preserves extrema/artifact rows. Add a static full-resolution heatmap and a static profile of row 1 as the fallback, with a robust color range for the surrounding crystal plus a separate artifact-scale view. Start the exploratory slider near row 1 or give a bounded clue such as 'inspect the first ten rows.' Update the key so it does not claim the existing static surfaces cover cross-section/widget failure."
      },
      {
        "rank": 3,
        "severity": "high",
        "category": "physics",
        "title": "The AFM explanation incorrectly makes a single-atom, dragging contact probe universal",
        "location": "notebooks/src/01_nano_landscapes.py:4,18,69-74,312-313",
        "failure_scenario": "Students are told that an AFM drags a needle whose tip is one atom wide, reads the surface atom by atom, and works by touch. Commercial AFM probe radii are commonly several to tens of nanometres (Bruker lists examples around 8-20 nm), even though the final apex interaction can sometimes produce atomic resolution. AFM also has contact, intermittent-contact/tapping, and non-contact modes; Bruker describes TappingMode as an oscillating probe that lightly taps while feedback follows topography. A student could therefore give the notebook's requested 'needle dragging' explanation and leave with a false model of both spatial resolution and instrument operation.",
        "suggested_fix": "Describe AFM as raster-scanning a very sharp probe on a cantilever and using a feedback signal to map surface height. Say that the probe may remain in contact, tap intermittently, or sense forces without contact depending on mode. Replace 'single atom wide/atom by atom' with an honest distinction between a nanoscale-radius tip and atomic resolution under suitable conditions. Phrase Task 5 mechanisms in terms of probe-sample interaction or feedback on one scan line, not mandatory dragging."
      },
      {
        "rank": 4,
        "severity": "high",
        "category": "data processing",
        "title": "The median-zero explanation describes processing that was not performed",
        "location": "notebooks/src/01_nano_landscapes.py:234-241; notebooks/teacher/01_nano_landscapes_key.md:54-61,85-87",
        "failure_scenario": "The shipped flatten function fits and subtracts a separate linear polynomial from every row, then subtracts one median computed over the entire 2D result. It does not force each scan line's median or 'middle value' to zero. In addition, AFMScan.story contains only the student story and the printed gallery listing shows only key, material, and scan size, so neither place named on lines 235-236 exposes the processing string. Students and teachers are directed to verify a claim in fields they cannot see and are then given an incorrect explanation for exactly-zero global medians.",
        "suggested_fix": "Say: 'A line was fit and subtracted from each scan row to reduce row-wise offset/tilt; afterward, one global median was subtracted so the processed map's overall median is zero.' Explain that leveling can also alter real broad morphology. Either display the processing metadata explicitly from gallery.json or add it to AFMScan; do not tell students to inspect scan.story for it. Correct the same per-line-median claim in the key."
      },
      {
        "rank": 5,
        "severity": "high",
        "category": "math/self-check",
        "title": "Task 3's checker approves an incorrect micrometre-to-nanometre conversion",
        "location": "notebooks/src/01_nano_landscapes.py:199-226; notebooks/teacher/01_nano_landscapes_key.md:49-53",
        "failure_scenario": "The student is explicitly invited to change scan_nm on line 207, but expected on line 222 is calculated from that same possibly wrong scan_nm. For example, scan_nm = scan_um / 1000 followed by scans_per_hair = hair_nm / scan_nm prints an absurd 16,000,000 scans for the default sample and still receives 'Correct.' The key overstates this as checking the exact unit-conversion/formula task; it checks only whether the same scan_nm value is divided into hair_nm twice.",
        "suggested_fix": "Check the stages independently: compare scan_nm with scan_um * 1000, then compute the reference hair count directly from scan_um * 1000 rather than from the student's scan_nm. Give separate feedback for the conversion and ratio formula. Ideally make student answer variables blank/None initially instead of pre-filling both correct expressions."
      },
      {
        "rank": 6,
        "severity": "high",
        "category": "statistics",
        "title": "A mean-median gap cannot identify which scan has more or more-extreme outliers",
        "location": "notebooks/src/01_nano_landscapes.py:263-287; notebooks/teacher/01_nano_landscapes_key.md:54-61",
        "failure_scenario": "The mean-minus-median difference measures direction and degree of asymmetry in the processed values; it does not uniquely measure outlier count or extremity. Symmetric extreme tails can leave mean and median equal, and many moderate one-sided values can create a gap without isolated outliers. The key makes the unsupported inference explicit by saying GaSe has the 'more extreme/more numerous height outliers.' In the current GaSe map the middle 50% already spans about -13.08 to +15.50 nm, so the distribution is broadly spread rather than adequately summarized as a mostly ordinary surface plus a few tall points.",
        "suggested_fix": "Ask what the sign and size of the gap suggest about skew/asymmetry, not which surface has more outliers. If outliers are the target, define a rule (for example 1.5 IQR), print counts and fractions, and compare tail distances on a common scale. Reword the GaSe prompt/key so 'few tall mounds' is an image-based hypothesis to check, not a conclusion proved by mean versus median alone."
      },
      {
        "rank": 7,
        "severity": "medium",
        "category": "Colab/accessibility",
        "title": "The core line-profile task has no non-widget fallback",
        "location": "notebooks/src/01_nano_landscapes.py:134-153; notebooks/teacher/01_nano_landscapes_key.md:27-29,97-100",
        "failure_scenario": "Task 2 is core and requires moving explore_cross_section's ipywidgets slider to find and read a profile. The only static fallback is a 3D surface at lines 98-102, which cannot supply the requested line profile. The teacher key says the static fig.show() fallback cells cover unsupported browsers, but they do not cover this task. The exact Python 3.13/Plotly 5.24.1/ipywidgets 7.7.1 constructors work in a smoke test, yet a blocked or failed Colab widget frontend still removes the only route to the core measurement.",
        "suggested_fix": "Always render one curated static atomic-staircase cross-section with its row number immediately below the widget and let students use that if interaction fails. Add two labeled plateau regions or enough axis guidance for a non-AP student to subtract their heights. Make the troubleshooting text identify which static output substitutes for each core task."
      },
      {
        "rank": 8,
        "severity": "medium",
        "category": "physics/scope",
        "title": "The title and gallery description conflate atomic terraces, monolayers, and 2D crystals",
        "location": "notebooks/src/01_nano_landscapes.py:2-5,80-81",
        "failure_scenario": "The featured atomic_staircase is the surface of a bulk SrTiO3 substrate, not a crystal one atom thick. The gallery also includes an 11 nm FeSe film under a cap and several films whose layer count is not established by the notebook. Calling all 12 entries '2D crystals' and promising a flight over 'a crystal one atom thick' encourages typical students to infer that an atomic-height terrace means the entire specimen is one atom thick.",
        "suggested_fix": "Retitle around nanoscale crystal surfaces or atomic-height terraces. Describe the gallery as AFM scans of substrates and thin-film/2D-material samples, some multilayer. Explicitly distinguish a bulk crystal surface with unit-cell-high steps from a monolayer material; one structural layer can itself contain multiple atomic planes."
      },
      {
        "rank": 9,
        "severity": "medium",
        "category": "math/visualization",
        "title": "The displayed relief ratio and the plotted exaggeration do not consistently describe the visible surface",
        "location": "notebooks/src/01_nano_landscapes.py:105-128; notebooks/teacher/01_nano_landscapes_key.md:36-41",
        "failure_scenario": "The notebook's 4.3 nm relief and 1:233 ratio use the full-array min and max, but 98% of the current atomic-staircase pixels span only about 0.80 nm. The static 3D helper also strides the 528x528 map by three and sees a 3.84 nm span, not 4.29 nm. Finally, its aspect ratio is capped at z=3, so the top slider setting can say heights x1000 even though the atomic scan is effectively capped near x782. This undercuts a lesson whose central claim is that students should trust the printed exaggeration factor and relief number.",
        "suggested_fix": "Report full peak-to-peak range separately from a robust 1st-99th-percentile span and the measured terrace-step height, explaining what each means. Compute the ratio from the same displayed array/range used to set Plotly geometry. Either remove the silent aspect-ratio cap, cap the slider itself, or put the effective capped exaggeration in the title. Replace the phone-screen-protector comparison with the direct, dimensionally clear relief-to-width ratio."
      },
      {
        "rank": 10,
        "severity": "medium",
        "category": "answer key/data provenance",
        "title": "The key's 'data problem' was resolved by the rebuilt multi-material label but is still presented as current",
        "location": "notebooks/teacher/01_nano_landscapes_key.md:72-79",
        "failure_scenario": "The current gallery entry for sample 31779 is no longer material='CrSb'; it is 'CrSb + Sb2Te3,' and its story explicitly says the sample record lists both materials. afm_summary.csv has primary material='Sb2Te3' and all_materials='Sb2Te3; CrSb.' The key therefore sends a teacher to report a mismatch that the rebuild intentionally resolved and inaccurately describes the current gallery value.",
        "suggested_fix": "Remove the stale data-problem section or replace it with a short provenance note explaining that a single primary-material column and a multi-material label serve different display purposes. Regenerate or validate teacher-key diagnostics whenever the slice is rebuilt."
      },
      {
        "rank": 11,
        "severity": "low",
        "category": "accessibility",
        "title": "The absolute claim that every offered color scale is color-blind-safe is not supported",
        "location": "notebooks/src/01_nano_landscapes.py:89-95",
        "failure_scenario": "Viridis and Cividis are defensible accessibility choices, but the menu also includes Plotly's Earth and Ice scales and the notebook provides no defined color-vision condition or contrast test supporting the universal claim. A teacher may rely on the statement rather than checking the actual surface/colorbar contrast for their students and projector.",
        "suggested_fix": "Offer a smaller tested set led by Cividis/Viridis and say they are designed to remain readable for common color-vision deficiencies. Preserve height-axis and colorbar labels so color is never the only encoding; avoid claiming universal safety without a documented accessibility test."
      },
      {
        "rank": 12,
        "severity": "low",
        "category": "physics/vocabulary",
        "title": "A terrace is defined as an atom-thin ledge rather than the flat region between steps",
        "location": "notebooks/src/01_nano_landscapes.py:21",
        "failure_scenario": "A student can come away calling the vertical step edge itself a terrace and assuming every terrace boundary is exactly one atomic layer. Surface terraces are the comparatively flat regions bounded by steps; neighboring terraces can differ by one or several layers through step bunching.",
        "suggested_fix": "Define a terrace as 'a relatively flat region on a crystal surface, bounded by step edges; the height change at an edge may be one or more atomic layers.'"
      }
    ],
    "verified_matches_and_non_findings": [
      "Against the current data/slice/camel-2dcc payload, atomic_staircase has full peak-to-peak relief 4.29465 nm across 1,000 nm, so the notebook rounds to 4.3 nm and 1:233 exactly as the key says.",
      "The current _step_sizes implementation reproduces the key's printed 1,470 candidates, quartiles 0.21-0.38 nm, and 10th-90th-percentile range 0.15-0.47 nm. Finding 1 concerns what those values measure, not stale arithmetic.",
      "Task 3's default arithmetic remains 5 micrometres = 5,000 nm and 16.0 scan widths per 80,000 nm hair; 1 micrometre gives 80.0 and 2 micrometres gives 40.0.",
      "The current histogram outputs match the key: GaSe mean 1.41391 nm, median 0, min -43.88390 nm, max 56.13573 nm; WS2 mean -0.10737 nm, median 0, max 19.28536 nm.",
      "The WSe2 reveal values remain row 1 at 3.90625 nm from the top, row standard deviation 136.76039 nm versus median row standard deviation 0.55878 nm (about 244.7 times, not the key's rough 230 times), with global min/max -454.97937/+221.38452 nm. The key's rounded row, position, standard deviations, and global range are acceptable; if quoting a multiplier, update it to about 245 times.",
      "A 0.39 nm unit-cell step for SrTiO3(001)/(100) is well supported. The problem is the notebook's detector and overbroad wording, not the reference value itself.",
      "A clean-environment smoke test successfully imported and constructed surface_3d, explore_3d, and explore_cross_section under Python 3.13.14, Plotly 5.24.1, ipywidgets 7.7.1, and NumPy 2.5.3. No Python/API incompatibility was found; a CLI test cannot certify every Colab browser frontend.",
      "The rebuilt directory and data/slice/camel-2dcc-v1.zip contain the same gallery.json hash, so the recomputed directory values represent the packaged gallery metadata as well."
    ],
    "primary_sources_checked": [
      {
        "title": "Bruker, TappingMode",
        "url": "https://www.bruker.com/en/products-and-solutions/microscopes/materials-afm/afm-modes/tapping-mode.html",
        "supports": "TappingMode maps topography with an oscillating probe that lightly taps the surface and a feedback loop, contradicting a universal continuous-drag description."
      },
      {
        "title": "Bruker, AFM Probes Selection Guide",
        "url": "https://www.bruker.com/it/meta/forms/bns-form-pages/brochures/afmi/afm-probes-selection-guide/_jcr_content/root/contentpar/embedform_copy/after-content/twocolumns_copy_copy/contentpar-1/calltoaction.download-asset.pdf/primaryButton/Bruker-AFM-Probes-Guide-RevA1-BRUKER.pdf",
        "supports": "Commercial probe specifications use nanometre-scale tip radii rather than a universally single-atom-wide tip."
      },
      {
        "title": "Surface properties of atomically flat poly-crystalline SrTiO3",
        "url": "https://www.nature.com/articles/srep08822",
        "supports": "Measured/theoretical SrTiO3(100) step heights near 0.381/0.391 nm, orientation dependence, and the possibility of larger steps from step bunching."
      },
      {
        "title": "High-sensitivity of initial SrO growth on the residual resistivity in epitaxial thin films of SrRuO3 on SrTiO3(001)",
        "url": "https://www.nature.com/articles/s41598-021-95554-x",
        "supports": "A roughly 0.39 nm terrace step corresponds to one SrTiO3 unit-cell height on SrTiO3(001)."
      }
    ],
    "verification_method": [
      "Read the source notebook and teacher key line by line.",
      "Loaded every AFM gallery array from the current rebuilt data/slice/camel-2dcc payload and recomputed relief, pixel scale, step-helper output, histogram statistics, and WSe2 row statistics without modifying repository data.",
      "Inspected the shipped classroom and flatten implementations to verify downsampling, widget defaults, available AFMScan fields, and the exact leveling/median operation invoked by the notebook.",
      "Compared data/slice/camel-2dcc with the current release ZIP's gallery metadata and checked the rebuilt sample-31779 labels.",
      "Ran a temporary isolated compatibility smoke test with Python 3.13.14, Plotly 5.24.1, and ipywidgets 7.7.1; no repository files were used as outputs or edited during testing.",
      "Checked the AFM-mode, commercial-tip, and SrTiO3 step-height claims against the manufacturer and research sources listed above."
    ]
  }
}
