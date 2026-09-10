{
  "review": {
    "scope": [
      "notebooks/src/06_counting_crystals.py",
      "notebooks/teacher/06_counting_crystals_key.md",
      "src/camel_data/grains.py",
      "scripts/build_grains.py",
      "data/slice/camel-2dcc/grains/"
    ],
    "overall_assessment": "The notebook's arithmetic, equilateral-triangle formula, current printed counts, and finite-population resampling code are mostly sound. Its central statistical story is not: 501 algorithm-selected blobs in three purposively chosen 2 µm × 2 µm fields are presented as every eligible triangle anywhere on a wafer, and the single field at each nominal position cannot establish wafer-position bias. The optional growth comparison also rests on incorrect sample provenance: the packaged recipe says 17464 received a 10-minute ripening step, while 17458 is the no-ripening sample. The grain finder is useful as an intentionally simple classroom segmentation, but its labels and threshold are described with substantially more physical certainty than the code supports. Sixteen prioritized findings follow.",
    "finding_count": 16,
    "findings": [
      {
        "rank": 1,
        "severity": "critical",
        "category": "statistics / data integrity",
        "title": "The 501 detected grains are not the wafer population",
        "location": "notebooks/src/06_counting_crystals.py:19-20,29-34,304-329; notebooks/teacher/06_counting_crystals_key.md:25-30,71-85",
        "failure_scenario": "Students are explicitly taught that the data contain every whole, cleanly separated triangle anywhere on the wafer and that 1,889 nm² is the true wafer mean. In fact, the 501 rows are the detector's retained components in only three selected 2 µm × 2 µm AFM fields (12 µm² total), after excluding edge-touching, glitch-touching, merged, tall, and elongated objects. Unsampled wafer locations and eligible grains missed or rejected by the algorithm are outside this frame. This confuses a census of a constructed finite data set with the scientific target population and undermines the lesson's main learning objective.",
        "suggested_fix": "Define three levels explicitly: target population = all eligible WSe2 domains on wafer 17458; observed sampling frame = detector-eligible domains in the three imaged fields; classroom pseudo-population = the 501 retained rows used for the resampling demonstration. Call 1,889 nm² the pooled three-field mean, not the true wafer mean, and state that wafer-wide inference would require a probability sample of many fields plus a validated detector. It is fine to treat the 501 values as a finite pseudo-population solely for demonstrating sampling distributions."
      },
      {
        "rank": 2,
        "severity": "critical",
        "category": "materials science / provenance",
        "title": "The optional 'seed-only, no-growth-step' comparison reverses the recorded recipes",
        "location": "notebooks/src/06_counting_crystals.py:443-465; notebooks/teacher/06_counting_crystals_key.md:86-90; scripts/build_grains.py:27-42",
        "failure_scenario": "The notebook says 17464 contains only seeds formed before growth and uses that premise to explain its lower detected fraction and density. The packaged growth recipe records 17458 at 850 °C with a 0.5-minute nucleation step followed by cooldown/no ripening, whereas 17464 was run at 875 °C and received a 10-minute Ripening 1 step. Thus 17464 is not the no-growth counterpart claimed, the comparison changes temperature and date as well as recipe, and the key's causal conclusion ('fewer seeds') is unsupported. The metadata for scan 24111 also says '20 min growth', while the packaged recipe records two 10-minute ripening stages plus a 23-minute growth stage.",
        "suggested_fix": "Regenerate growth notes directly from the recipe records. Remove the seed-only causal exercise unless the intended sample can be identified and its recipe verified; otherwise make Task 7 a descriptive comparison between two differently processed samples and list the confounders. Correct 24111 to the recorded stage durations or avoid summarizing its growth time."
      },
      {
        "rank": 3,
        "severity": "high",
        "category": "statistics",
        "title": "One AFM field per position cannot demonstrate wafer-position bias",
        "location": "notebooks/src/06_counting_crystals.py:386-429,489-494; notebooks/teacher/06_counting_crystals_key.md:80-85,112-114",
        "failure_scenario": "The 104 edge grains are treated as 104 independent spatial replicates and the +49% pooled difference is said to reflect real wafer-position dependence because n is already large. All 104 are clustered in one field. The contrast may be a peculiarity of that field, spatial correlation, selection/classification effects, or position; more grains inside the same field do not supply replication of wafer position. A teacher would be led to present an unreplicated observational contrast as established sampling bias.",
        "suggested_fix": "Describe this as a hypothetical illustration conditional on the three observed fields: choosing the observed edge field produces a different pooled-frame estimate. Do not claim a real wafer-position effect. For empirical inference, acquire several independently and preferably randomly located fields within each position, treat field rather than grain as the replicate, and compare field-level estimates or use a cluster-aware analysis."
      },
      {
        "rank": 4,
        "severity": "high",
        "category": "grain-finding logic",
        "title": "The classifier never establishes that a blob is one clean triangle",
        "location": "notebooks/src/06_counting_crystals.py:81-107,154-160,306-318; notebooks/teacher/06_counting_crystals_key.md:11-14; src/camel_data/grains.py:40-43,128-179",
        "failure_scenario": "A component is labeled `single` merely when it is not extremely elongated, not more than 2.5 times the median component height, and not below 0.8 solidity. There is no triangularity, corner-count, concavity decomposition, or supervised validation. `merged` is only a low-solidity heuristic, so convex overlaps can be called single and irregular isolated objects can pass. Nevertheless the prose equates `single` with 'one clean triangle' and treats all 501 as real triangles. This can bias counts, sizes, and every downstream statistic while hiding model uncertainty from students.",
        "suggested_fix": "Rename the categories to honest operational labels such as `candidate_single`, `low_solidity`, `tall_blob`, and `elongated_blob`. Say `whole_single()` selects components that pass these heuristics, not confirmed triangles. Hand-label a stratified subset, report confusion/error rates, and optionally add an explicit triangularity criterion before using counts scientifically."
      },
      {
        "rank": 5,
        "severity": "high",
        "category": "grain-finding logic / data integrity",
        "title": "The documented substrate leveling and halfway threshold do not match the implementation",
        "location": "src/camel_data/grains.py:1-13,105-119,128-151; notebooks/src/06_counting_crystals.py:97-107",
        "failure_scenario": "The documentation says each line is fit using substrate pixels and a pixel becomes island above the midpoint between substrate zero and a typical top. The code fits pixels below one global median, which are not proven substrate, then subtracts the median of the lower half rather than the substrate level. In the shipped maps the overall medians remain about 0.14-0.16 nm, not zero. It then sets threshold to `0.5 * top` rather than `substrate + 0.5 * (top - substrate)`. Each scan gets a different data-dependent threshold (currently about 0.94-1.07 nm for 17458), so segmentation and between-field comparisons can shift with coverage and background distribution.",
        "suggested_fix": "Either change the prose to describe the exact lower-half leveling and `0.5 * top` heuristic, or implement a defensible background estimate and use `background + 0.5 * (top - background)`. Save and display the estimated background, threshold, and sensitivity of counts/means to plausible common thresholds. Avoid calling low pixels substrate without validating that assumption on each scan."
      },
      {
        "rank": 6,
        "severity": "high",
        "category": "measurement / terminology",
        "title": "`covered_fraction` is not wafer coverage and includes rejected artifacts",
        "location": "scripts/build_grains.py:70-86; notebooks/src/06_counting_crystals.py:449-465; notebooks/teacher/06_counting_crystals_key.md:86-96",
        "failure_scenario": "The displayed 10.4% and 4.3% values are the fractions of pixels in one AFM frame belonging to any retained connected component in `labels`, including merged, dust, streak, edge, and glitch-adjacent components. They represent only pixels above an adaptive mid-height threshold, not the full physical footprint, and are then called 'wafer coverage'. In the current center field, 10.4% total labeled fraction falls to about 7.0% for whole-single candidates alone; the analogous 17464 value is about 3.3%. Students can draw a physical wafer-coverage conclusion from a detector-mask statistic.",
        "suggested_fix": "Rename it `above_threshold_pixel_fraction_in_this_field`, state exactly which labels it includes, and show a category breakdown. If physical surface coverage is desired, validate a consistent segmentation rule at matched resolution and report estimates across sampled fields; never generalize one frame's fraction to the wafer."
      },
      {
        "rank": 7,
        "severity": "high",
        "category": "AFM physics / measurement",
        "title": "The notebook reports absolute leveled z as step height and incorrectly implicates tip shape in vertical inflation",
        "location": "notebooks/src/06_counting_crystals.py:227-260; notebooks/teacher/06_counting_crystals_key.md:61-65,106-108; src/camel_data/grains.py:130-135,157-175",
        "failure_scenario": "`h.max()` is printed as the grain's peak height without subtracting nearby substrate, and `height_nm` is the component's mean absolute leveled z despite its 'above substrate' documentation. For grain 217 the printed maximum is about 1.94 nm, but the nearby profile baseline is about 0.23 nm, so the local rise is about 1.72 nm. The key compares the uncorrected maximum with a monolayer step and says tip shape inflates AFM height. Finite tip radius chiefly broadens lateral shape; it does not ordinarily add directly to a vertical step height. The explanation therefore mixes a baseline bug with an inaccurate AFM artifact claim.",
        "suggested_fix": "Estimate local substrate from profile segments outside the component and report `plateau/peak minus local substrate`; similarly compute component height relative to a surrounding annulus. Explain that adsorbates/interfacial water, feedback/setpoint effects, leveling, and z calibration can affect apparent step height, while tip geometry mainly affects lateral dimensions. Keep the appropriately cautious conclusion that these data alone do not determine layer count."
      },
      {
        "rank": 8,
        "severity": "high",
        "category": "pacing / pedagogy",
        "title": "The advertised 45-minute core is materially overfilled",
        "location": "notebooks/src/06_counting_crystals.py:12-22,95-440,489-499; notebooks/teacher/06_counting_crystals_key.md:32-43",
        "failure_scenario": "A non-AP class is expected to download and inspect data, interpret a segmentation failure, manually measure and calculate triangle area, interpret three separate line profiles, learn population/sample notation, try three seeds, interpret three sampling distributions, compare boxplots, reason about bias, and answer a three-part exit ticket. The key allocates only three minutes to load and interpret the three-position boxplot plus Task 6 and only two minutes to the exit ticket. Normal Colab startup/download delay or student discussion makes completion implausible.",
        "suggested_fix": "Make one coherent 45-minute path: setup and segmentation check; geometry plus one WSe2 profile; then the finite-pseudo-population simulation and exit ticket. Move the SnSe profile, second WSe2 profile, spatial comparison, and recipe comparison to extensions or a second lesson. Budget at least 7-10 minutes for the sampling-versus-bias discussion and 4-5 minutes for the exit ticket."
      },
      {
        "rank": 9,
        "severity": "medium",
        "category": "statistics",
        "title": "The code's simple random sample of grains does not model scanning a smaller wafer area",
        "location": "notebooks/src/06_counting_crystals.py:332-361",
        "failure_scenario": "The text says a scientist scans a smaller area, but `rng.choice(population, replace=False)` samples individual already-known grains with equal probability from the pooled list. An area scan samples spatial clusters, may exclude boundary-crossing grains, and gives grains unequal inclusion behavior through field placement and detectability. Students can leave believing that scanning one small patch is a simple random sample of individual grains.",
        "suggested_fix": "Present the code explicitly as an urn-style SRS from the constructed 501-value classroom frame. Contrast it with the actual two-stage process: randomly choose fields/locations, then observe grains within fields. If the aim is to model AFM sampling, resample spatial windows or whole fields rather than individual grains."
      },
      {
        "rank": 10,
        "severity": "medium",
        "category": "statistics / answer-key mismatch",
        "title": "The key's theoretical sampling SD omits the finite-population correction",
        "location": "notebooks/teacher/06_counting_crystals_key.md:71-79",
        "failure_scenario": "The simulation samples without replacement from N=501 on every draw, but the key compares its SDs only with sigma/sqrt(n) and attributes differences vaguely to finite sampling. Using the notebook's population SD of 1,023.87 nm², the exact SD is `sigma/sqrt(n) * sqrt((N-n)/(N-1))`: approximately 456.1, 224.5, and 137.5 nm² for n=5, 20, and 50. The key instead predicts 458, 229, and 145; the discrepancy is noticeable at n=50 and is systematic, not simulation noise.",
        "suggested_fix": "Either teach the finite-population correction and give the corrected predictions, or say sigma/sqrt(n) is a large-population approximation whose overestimate grows as the sampling fraction increases. Keep the current simulated values (about 465, 221, 134), which are consistent with Monte Carlo variation around the corrected values."
      },
      {
        "rank": 11,
        "severity": "medium",
        "category": "statistics / pedagogy",
        "title": "Bias is defined as every realized estimate missing in the same direction",
        "location": "notebooks/src/06_counting_crystals.py:413-429; notebooks/teacher/06_counting_crystals_key.md:29-30,80-85,112-114",
        "failure_scenario": "The notebook says the edge-only estimate is +49% 'every single time, no matter how many grains' and that bias is a predictable same-direction error every time. Bias is a property of an estimator's expectation under a sampling process, not a guarantee about every realized sample. Small random samples from an edge stratum still vary and could fall on either side of the pooled mean; increasing within-edge n reduces random error while retaining the design's expected offset. The printed +49% is constant only because the code repeatedly uses the same complete observed field.",
        "suggested_fix": "Define bias as the long-run/expected difference caused by the selection procedure. Say repeated edge-only samples would still show random variation but would tend to center on the edge-field or edge-region mean rather than the target mean. Change 'every single time' to 'systematically, on average' and distinguish adding grains within one field from sampling more independent fields."
      },
      {
        "rank": 12,
        "severity": "medium",
        "category": "measurement comparability",
        "title": "A pixel-count cutoff makes the 17458-versus-17464 density comparison non-comparable",
        "location": "src/camel_data/grains.py:128-167; notebooks/src/06_counting_crystals.py:451-465; notebooks/teacher/06_counting_crystals_key.md:86-90,119-123",
        "failure_scenario": "Both scans require at least 12 pixels, but 17458 has about 3.906 nm pixels while 17464 has about 9.766 nm pixels. The minimum accepted physical area is therefore about 183 nm² versus 1,144 nm², 6.25 times larger for 17464. Shape rules such as a 2.5-pixel minor-axis cutoff also change physical meaning. The notebook mentions that coarse sampling may miss tiny seeds, but the key still concludes that the lower density means fewer seeds; this detector alone cannot support that conclusion.",
        "suggested_fix": "Resample both maps to a common physical pixel size or impose the same physical-area and physical-width cutoffs, then rerun sensitivity checks. Until then, describe the result only as fewer detected qualifying components per area at the native resolutions, with no claim about seed density."
      },
      {
        "rank": 13,
        "severity": "medium",
        "category": "materials science",
        "title": "Hexagonal atomic symmetry alone does not explain triangular grains",
        "location": "notebooks/src/06_counting_crystals.py:163-177",
        "failure_scenario": "The prose says the hexagonal bonding pattern makes grains triangular and that even growth in every direction makes hexagons. Crystal symmetry constrains allowed edge orientations, but triangular versus hexagonal morphology depends on relative edge terminations and growth/etch kinetics, precursor flux, and conditions. Truly isotropic growth would tend toward a circle; a hexagon results when six crystallographically allowed edges have comparable rates. Students receive an over-simple structure-to-shape causal rule.",
        "suggested_fix": "Say that WSe2's lattice permits equivalent edge directions separated by 60 degrees, while growth kinetics and the relative stability/rate of different edge terminations determine whether three or six edges dominate. Replace 'evenly in every direction' with 'at comparable rates along the six allowed edge directions.'"
      },
      {
        "rank": 14,
        "severity": "medium",
        "category": "geometry / measurement",
        "title": "The two area checks share data and calibration, and a factor-of-two pass rule is too loose",
        "location": "notebooks/src/06_counting_crystals.py:15-16,172-213; notebooks/teacher/06_counting_crystals_key.md:20-22,55-60,103-105",
        "failure_scenario": "The formula A = sqrt(3)s²/4 and current arithmetic are correct, but the methods are called 'genuinely independent'. Both derive from the same thresholded AFM image and the same x-y calibration; the student's endpoints also follow the algorithm's visible boundary. Shared segmentation/calibration errors can make them agree. The accepted area ratio 0.5-2.0 corresponds to roughly 40.5-81.0 nm for this grain around an equivalent side of 57.2 nm, so a visibly poor length estimate can pass and be labeled reasonable.",
        "suggested_fix": "Call them two differently derived, correlated estimates. Ask students to mark three vertices and measure all three sides, average them, and discuss non-equilateral shape and boundary uncertainty. Tighten the feedback to a pedagogically useful range (for example about 20-30% in area after testing classroom readability), or grade the reasoning rather than returning a binary factor-of-two success."
      },
      {
        "rank": 15,
        "severity": "medium",
        "category": "usability / correctness",
        "title": "Students are told to choose a displayed grain ID, but neither map displays IDs",
        "location": "notebooks/src/06_counting_crystals.py:117-142,179-196; notebooks/teacher/06_counting_crystals_key.md:132-135; src/camel_data/grains.py:46-69",
        "failure_scenario": "Both `show_grains` calls use the default `number=False`, yet Task 2 says to read another ID off the Part 1 map. A student who guesses an ID classified as merged/dust/streak can also trigger `IndexError` at `.iloc[0]`, because the lookup is not restricted or validated even though the key claims any whole-single ID is acceptable. In a live class this creates avoidable confusion and code failures.",
        "suggested_fix": "Show numbers for eligible candidates (`number=True` with only whole-single labels), provide a printed/dropdown list, or keep grain 217 fixed. Validate the chosen ID and print a friendly message with valid choices instead of indexing an empty result."
      },
      {
        "rank": 16,
        "severity": "low",
        "category": "Colab robustness",
        "title": "The notebook relies on an unverified scikit-image installation",
        "location": "notebooks/src/06_counting_crystals.py:47-90; src/camel_data/grains.py:46-50,72-83",
        "failure_scenario": "The setup verifies only downloaded files. Task 1 imports `skimage.segmentation.find_boundaries`, and the first line-profile task imports `skimage.measure.profile_line`. If a classroom's Python 3.13 Colab image changes or omits scikit-image, execution fails after the data download with `ModuleNotFoundError`, without a teacher-friendly remedy. The notebook otherwise avoids the Plotly/ipywidgets failure modes because it uses static Matplotlib figures and has no file-download interaction.",
        "suggested_fix": "At setup, import-check the exact runtime dependencies and either install a tested scikit-image version with `%pip` or raise a concise instruction that names the missing package. Pin/test a Python-3.13-compatible release in the notebook build environment."
      }
    ],
    "verified_matches_and_non_findings": [
      "The equilateral-triangle formula is correct. For current grain 217, area 1,419.067 nm² gives equivalent side 57.247 nm; a 55 nm manual estimate predicts 1,310 nm² and the printed ratio 0.92 is correct.",
      "Current pooled-frame outputs match the teacher key: N=501, mean=1,888.618 nm², population SD=1,023.872 nm²; center/flat/edge means are about 1,469/1,809/2,818 nm², and the edge-versus-pooled arithmetic is +49%.",
      "The sampling code correctly draws without replacement within each simulated sample and creates 1,000 independent samples. Current simulated SDs are about 464.6, 221.0, and 133.8 nm² for n=5,20,50.",
      "The qualitative claim that sampling distributions of the mean narrow as n grows is correct for this finite classroom frame.",
      "The WSe2 monolayer description as a Se-W-Se trilayer is appropriate. Published AFM examples commonly report an apparent monolayer step around 0.7-0.8 nm, so the notebook's order-of-magnitude reference is reasonable, subject to measurement conditions.",
      "The current line choices produce interpretable plots: grain 217 has a local rise near 1.7 nm after baseline subtraction; scan 24111 shows an approximately 1-1.5 nm feature; and the SnSe profile plausibly supports a qualitative count of roughly 3-5 treads.",
      "The packaged `camel_data/grains.py` is byte-identical to `src/camel_data/grains.py`, so the reviewed implementation is the one students load from the slice.",
      "No ipywidgets or Plotly widget is required by this notebook, and it does not initiate a browser file download. Static Matplotlib is a sensible Colab choice here."
    ],
    "primary_sources_checked": [
      {
        "title": "Origin of ultrafast growth of monolayer WSe2 via chemical vapor deposition",
        "url": "https://www.nature.com/articles/s41524-019-0167-2",
        "supports": "WSe2 domain morphology depends on edge attachment/diffusion kinetics and precursor conditions; lattice symmetry alone is not a complete triangle-versus-hexagon explanation."
      },
      {
        "title": "Growth of 2H stacked WSe2 bilayers on sapphire",
        "url": "https://pubs.rsc.org/en/content/articlehtml/2019/nh/c9nh00260j",
        "supports": "An AFM monolayer height near 0.8 nm is a reasonable experimental reference on sapphire."
      },
      {
        "title": "Layer-dependent mechanical properties and enhanced plasticity in the van der Waals chromium trihalide magnets",
        "url": "https://pubs.rsc.org/en/content/articlehtml/2019/nr/c9nr04270a",
        "supports": "The methods report AFM identification of monolayer WSe2 at approximately 0.75 nm, supporting the notebook's general reference range rather than an exact universal value."
      },
      {
        "title": "NIST: Atomic Force Microscopy",
        "url": "https://www.nist.gov/programs-projects/atomic-force-microscopy",
        "supports": "Probe geometry affects lateral nanoparticle dimensions, while height is the directly measured dimension; this does not support listing tip shape as a generic additive vertical-height inflation."
      }
    ],
    "verification_method": [
      "Inspected the complete student source, teacher key, grain library, build script, tests, packaged metadata, recipe records, and current CSV/NPZ arrays with line-numbered source references.",
      "Recomputed all counts, means, population SDs, current simulation SDs, finite-population theoretical SDs, area/side conversions, category-specific mask fractions, pixel-area detection limits, and selected line profiles from `data/slice/camel-2dcc/grains/`.",
      "Compared the 17458, 17464, 24111, and 39166 scan metadata with the packaged growth-recipe records and checked the packaged-versus-source grain module hashes.",
      "Reviewed primary research and NIST material for WSe2 morphology, monolayer AFM height, and AFM tip-geometry interpretation. No repository files other than this requested review artifact were edited."
    ]
  }
}
