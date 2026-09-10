{
  "1_notebook_lineup": {
    "top_recommendation": "Launch with five independent 45–50 minute notebooks, led by the AFM terrain notebook; every notebook should reach its main visualization within the first 10 minutes and use preprocessed data rather than asking students to parse instrument files.",
    "notebooks": [
      {
        "title": "Nano Landscapes: Explore a 2D Crystal in 3D",
        "math_standard_or_concept": [
          "CCSS HSS.ID.A.1–3: distributions, center, spread, and outliers",
          "CCSS HSF.IF.B.4–6: interpreting graphs and average rate of change"
        ],
        "data_slice": "Six to eight representative, pre-leveled AFM height maps from MoS2, WSe2, and SnSe, plus per-map roughness and scan metadata; include one visibly artifact-prone map for critique.",
        "wow_moment": "Students rotate a real 3D nanoscale surface, move a line-profile slider across it, and watch the height profile update.",
        "student_tasks": [
          "Set vertical exaggeration and color-range controls to reveal terraces without hiding outliers.",
          "Read the scan width and height range, converting micrometers to nanometers.",
          "Estimate a terrace step from a line profile and compare it with the map's reported roughness.",
          "Compare mean, median, range, and IQR and explain which statistic best describes a surface with a tall particle.",
          "Identify one likely scan artifact and distinguish it from a plausible sample feature."
        ],
        "timing_minutes": "5 hook, 10 controls/tutorial, 22 analysis, 8 explanation, 5 exit ticket"
      },
      {
        "title": "Recipe Showdown: Which SnSe Growth Order Makes Bigger Grains?",
        "math_standard_or_concept": [
          "CCSS HSS.ID.A.1–3: boxplots, median, IQR, overlap, and outliers",
          "CCSS HSS.IC.B.6: evaluating conclusions from an experiment"
        ],
        "data_slice": "The afm-stats SnSe table with grain areas, deposition order, Se:Sn ratio, sample identifier, repeat/group identifier, and DOI-backed package provenance.",
        "wow_moment": "A one-click regrouping changes the boxplots from deposition order to Se:Sn ratio, showing how the apparent winner depends on the comparison.",
        "student_tasks": [
          "Predict which recipe group has the largest typical grain area.",
          "Calculate or read the median and IQR for each group.",
          "Compare overlap and outliers without claiming that a boxplot alone proves causation.",
          "Write a recommendation to a crystal grower and name one limitation or possible confounder."
        ],
        "timing_minutes": "5 context, 8 prediction/tutorial, 22 group analysis, 10 claim-evidence-reasoning, 5 share-out"
      },
      {
        "title": "From Five Micrometers to a Football Field",
        "math_standard_or_concept": [
          "CCSS HSN.Q.A.1–3: units, scale, and appropriate precision",
          "CCSS HSG.MG.A.1–3: geometric modeling",
          "CCSS HSA.CED.A.1–4: equations and rearranging formulas"
        ],
        "data_slice": "Three AFM maps with scan dimensions and height calibration, a small table of approximate monolayer step heights, and one downsampled surface prepared for STL export.",
        "wow_moment": "Students scale a real 5 micrometer scan to field size, then download an STL whose touchable relief comes from that same AFM map.",
        "student_tasks": [
          "Compute the scale factor from the nanoscale scan to a 100 m field and scale a feature width.",
          "Estimate layer count from a measured step using thickness divided by an approximate monolayer step height, then round and report uncertainty.",
          "Compare horizontal and vertical scale factors and explain why a printable model needs labeled vertical exaggeration.",
          "Choose an STL base thickness and model width that are printable while preserving relative surface shape."
        ],
        "timing_minutes": "6 scale hook, 15 proportional reasoning, 12 layer estimate, 12 STL controls/export, 5 reflection"
      },
      {
        "title": "Build a Crystal: Graph an MBE Recipe",
        "math_standard_or_concept": [
          "CCSS HSF.IF.B.4–6: interpreting piecewise graphs and rates of change",
          "CCSS HSA.CED.A.1–4: variables, constraints, and formulas"
        ],
        "data_slice": "Four short, de-identified but provenance-linked MBE recipe step tables for FeSe, SnSe, or related materials, containing duration, substrate temperature, source temperatures, pressure, and flux where available; blank fields remain explicitly missing.",
        "wow_moment": "A step table becomes an animated temperature-and-pressure timeline showing the sequence used to grow an atomically thin material.",
        "student_tasks": [
          "Convert step durations to cumulative time and place boundaries on a timeline.",
          "Interpret the piecewise temperature graph and find an average heating or cooling rate where a ramp is documented.",
          "Compare pressure using scientific notation and multiplicative factors rather than inappropriate additive differences.",
          "Change one permitted recipe parameter with a slider and check whether it remains inside stated constraints.",
          "Explain why missing flux or ramp details must not be silently treated as zero."
        ],
        "timing_minutes": "6 growth video/context, 12 timeline construction, 17 calculations, 10 scenario slider, 5 exit ticket"
      },
      {
        "title": "How Thin Materials Help Chips See, Switch, and Scale",
        "math_standard_or_concept": [
          "CCSS HSF.LE.A.1–3 and HSF.LE.B.5: exponential models and interpreting parameters",
          "CCSS HSS.ID.B.6: scatterplots, trends, and residual thinking",
          "CCSS HSN.Q.A.1–3: units and quantitative reasoning"
        ],
        "data_slice": "A curated package-level table linking MOCVD TMD films, WSe2 or MoS2 FETs, SRAM/monolithic-3D work, memtransistor arrays, and a photonics example to material, device role, year, area or density metrics when actually reported, and DOI; add a clearly labeled contextual transistor-count table from an authoritative external source rather than inventing missing LiST values.",
        "wow_moment": "Students toggle between a linear and log view of transistor counts, then connect scaling limits to real wafer-scale 2D material and stacked-device research packages.",
        "student_tasks": [
          "Classify examples as primarily sensing/light, switching/logic, memory, or integration, allowing justified overlaps.",
          "Fit or inspect an exponential transistor-count model and interpret its doubling time as a historical trend, not a law of nature.",
          "Use device density times area to estimate a count for a stated hypothetical chip area.",
          "Compare planar and stacked layouts with the same footprint using a simple multiplicative model.",
          "Write a two-sentence explanation of why AI data centers care about computing density, memory movement, energy, and heat—not transistor count alone."
        ],
        "timing_minutes": "7 device hook, 12 classification/data provenance, 16 exponential model, 10 scaling scenario, 5 explanation"
      }
    ]
  },
  "2_algebra_and_geometry_hooks": {
    "top_recommendation": "Center the math on measurements students can manipulate—unit conversion, proportional scale, profiles, area, and simple exponential models—while labeling approximations and separating measured quantities from idealized models.",
    "hooks": [
      {
        "hook": "Layer count from AFM step height",
        "student_math": "estimated layers = measured step height / approximate monolayer step height; for MoS2, about 0.65 nm is a useful classroom approximation.",
        "physics_guardrail": "AFM step height depends on substrate, adsorbates, water, calibration, and material; students should report an estimate with uncertainty and should not force a non-integer measurement into certainty. Use material-specific values instead of applying 0.65 nm to every compound."
      },
      {
        "hook": "Scale a 5 micrometer AFM scan to a 100 meter field",
        "student_math": "scale factor = 100 m / 5 micrometers = 20,000,000; a 100 nm feature would become 2 m wide at that scale.",
        "physics_guardrail": "Convert all lengths to the same unit before dividing, and state that vertical exaggeration may use a different scale in a 3D model."
      },
      {
        "hook": "Hexagonal lattice geometry",
        "student_math": "Use 60 degree geometry, tessellation, and either the regular-hexagon area 3√3 s²/2 or the 2D primitive-cell area √3 a²/2, with a diagram defining s or lattice constant a.",
        "physics_guardrail": "A TMD is not simply a sheet of identical hexagons: metal and chalcogen atoms occupy different sites and layers. Never equate bond length, hexagon side, and lattice constant without defining the model."
      },
      {
        "hook": "Feature or transistor density",
        "student_math": "count = density × area; compare equal footprints with one versus several stacked device layers and use percent change or multiplicative factors.",
        "physics_guardrail": "Do not infer transistor counts from AFM features or equate material sample area with usable circuit area; use actual reported device metrics or label the calculation hypothetical."
      },
      {
        "hook": "Surface-area-to-volume ratio",
        "student_math": "For similar prisms, area scales with length squared and volume with length cubed, so surface-area-to-volume scales as 1/length.",
        "physics_guardrail": "A monolayer's electronic behavior is not explained by surface-area-to-volume ratio alone; quantum confinement, screening, bonding, and interfaces also matter."
      },
      {
        "hook": "Moore-style exponential growth",
        "student_math": "N(t) = N0 × 2^(t/d), compare linear and logarithmic plots, and solve or estimate doubling time d.",
        "physics_guardrail": "Moore's law is an empirical historical trend, not a physical law or a guarantee; transistor count, performance, energy use, and AI capability are different variables."
      },
      {
        "hook": "Photon energy and semiconductor response",
        "student_math": "Use E = hc/λ as inverse proportionality with a provided constant or compare wavelength ratios; connect shorter wavelength with greater photon energy.",
        "physics_guardrail": "Do not claim every photon above a tabulated band gap is efficiently detected or emitted; thickness, defects, contacts, selection rules, and device design matter."
      },
      {
        "hook": "Recipe timelines and pressure ratios",
        "student_math": "Build cumulative time from durations, calculate slopes only during documented ramps, and compare vacuum pressures using powers of ten and multiplicative factors.",
        "physics_guardrail": "A setpoint is not necessarily the measured sample temperature, missing values are not zeros, and correlation between a recipe variable and outcome does not isolate causation."
      }
    ]
  },
  "3_dataset_slice_design": {
    "top_recommendation": "Publish small, versioned, per-notebook ZIP bundles plus one machine-readable release manifest; keep original vendor files out of the student path, retain DOI-level provenance, and put the replaceable SharePoint URL in a single configuration file rather than notebook cells.",
    "release_layout": [
      "One bundle per notebook so a class downloads only what it needs; also offer one all-in-one teacher bundle for offline preparation.",
      "CSV for tidy sample metadata, AFM summary statistics, recipe steps, device/package context, and spectra when used; use UTF-8, explicit headers, ISO dates, and empty cells for missing values.",
      "Compressed NPZ for AFM arrays, with float32 height_nm plus x_um and y_um coordinate vectors or documented pixel spacing; include masks where invalid pixels exist. Avoid standalone NPY because it separates arrays from their coordinate metadata.",
      "PNG thumbnails for previews and low-bandwidth fallbacks; do not use PNG pixel values as quantitative height data.",
      "Optional pre-generated STL only as a fallback. The normal notebook should generate STL from a downsampled map and record lateral scale, base thickness, vertical exaggeration, and units.",
      "Include LICENSE/TERMS, README, CHANGELOG, CITATION.cff or citation text, manifest.json, and checksums.sha256 in each release."
    ],
    "size_targets": [
      "Notebook bundle: preferably 5–20 MB and no more than about 50 MB.",
      "AFM quantitative map: usually downsample to 128×128 or 256×256 float32 for interaction; retain a small number of 512×512 maps only when the detail supports a task.",
      "Thumbnail: roughly 512 px on the long side and typically below 250 KB.",
      "All-in-one teacher bundle: target below 200 MB, with every included map explicitly used or offered as an extension."
    ],
    "manifest_schema": {
      "release_fields": [
        "schema_version",
        "release_id",
        "title",
        "created_utc",
        "license_or_terms",
        "source_system",
        "public_sample_count_at_extract",
        "processing_software_version",
        "bundle_files"
      ],
      "per_asset_fields": [
        "asset_id",
        "sample_public_id",
        "material_normalized",
        "growth_method_normalized",
        "measurement_type",
        "source_filename_or_record_id",
        "source_package_title",
        "source_doi",
        "source_accessed_utc",
        "file_path",
        "media_type",
        "byte_size",
        "sha256",
        "shape",
        "dtype",
        "x_unit",
        "y_unit",
        "z_unit",
        "pixel_size_x",
        "pixel_size_y",
        "processing_state",
        "processing_steps",
        "quality_flags",
        "student_safe_label",
        "notes"
      ],
      "controlled_values": "Version material names, growth methods, measurement types, processing states, and quality flags in a small data dictionary; preserve the original LiST text in separate raw_label fields when normalization changes it."
    },
    "url_strategy": [
      "Store logical bundle IDs, expected byte sizes, and SHA-256 hashes in the release manifest.",
      "Store the SharePoint anonymous download URL only in one small data_sources.json configuration file distributed with the notebooks; notebook cells refer to a bundle ID, not a tenant URL.",
      "Put one clearly labeled Teacher Setup cell at the top that can load an alternate configuration file or uploaded local bundle, so a district can replace hosting without editing analysis cells.",
      "Pin notebooks to a release ID rather than a mutable latest file; teachers can deliberately change one release setting after reading the changelog.",
      "Cache the downloaded bundle in the Colab session, verify hash and file signature before extraction, and show a plain-language error with manual-upload instructions if retrieval fails."
    ]
  },
  "4_pitfalls": {
    "top_recommendation": "Preprocess once with a documented, reviewable pipeline, ship both quality flags and provenance, and make every notebook fail with a useful manual-upload fallback instead of silently correcting data or trusting a successful HTTP status.",
    "items": [
      {
        "pitfall": "AFM plane leveling",
        "risk": "A fitted plane can remove real large-scale slope or curvature and materially change roughness and volume measurements.",
        "mitigation": "Preserve an unmodified cropped array, state the fit order and mask, show before/after previews, and calculate classroom metrics from a named processing state."
      },
      {
        "pitfall": "Scan-line artifacts and overprocessing",
        "risk": "Line offsets, streaks, feedback errors, scars, and tip convolution can be mistaken for grains; aggressive row flattening can create or erase features.",
        "mitigation": "Include quality flags and one artifact-identification activity; exclude flagged maps from inferential comparisons unless the artifact itself is the lesson. Avoid claiming that thresholded AFM regions are grains without validation."
      },
      {
        "pitfall": "Units and aspect ratios",
        "risk": "Nanometers, micrometers, pixels, seconds, Celsius, kelvin, torr, and scientific notation are easily mixed; 3D plots and STL models can imply a false physical aspect ratio.",
        "mitigation": "Encode units in column names and manifest fields, convert explicitly, label axes, show dimensional checks, and display the vertical exaggeration factor on every 3D view and exported model."
      },
      {
        "pitfall": "Colab widgets",
        "risk": "Plotly FigureWidget and ipywidgets may render blank or lose state unless the custom widget manager is enabled, and package-version changes can break callbacks.",
        "mitigation": "Call google.colab.output.enable_custom_widget_manager() before widget creation, pin tested major versions, keep a non-widget Plotly fallback, add a Restart and run all note, and test in a fresh anonymous Colab session."
      },
      {
        "pitfall": "SharePoint anonymous downloads",
        "risk": "Sharing links may redirect, expire, be revoked, require tenant cookies, append an existing query string, return an HTML login page with status 200, or be blocked by a school network.",
        "mitigation": "Create an actual anyone-with-link file-download share, form the download URL correctly when query parameters already exist, follow redirects with timeouts and limited retries, validate content type or archive signature plus size and SHA-256, and provide manual upload and offline ZIP paths. Re-test links before each workshop."
      },
      {
        "pitfall": "Rate limits and repeated downloads",
        "risk": "A classroom starting simultaneously can trigger throttling, and rerunning cells can redownload large assets.",
        "mitigation": "Use one small bundle per notebook, cache it once per runtime, apply bounded exponential backoff for transient responses, avoid parallel file-by-file fetching, and distribute an offline copy to teachers in advance."
      },
      {
        "pitfall": "Selection bias and causal claims",
        "risk": "Published samples and curated visually interesting maps are not a random sample of all growth attempts, while recipe variables may be confounded.",
        "mitigation": "Label the population represented, publish inclusion rules, keep failed or messy examples when permission allows, and frame results as evidence from the slice rather than universal causal conclusions."
      },
      {
        "pitfall": "Public-key and provenance leakage",
        "risk": "Notebooks can accidentally expose an API key, internal hostnames, unpublished records, or restricted metadata even if the intended slice is public.",
        "mitigation": "Put no LiST key in any notebook or bundle, export only Published records after an allowlist review, scan archives for secrets and internal URLs, and retain public DOI citations instead of private links."
      }
    ]
  },
  "5_teacher_support": {
    "top_recommendation": "Ship every notebook as a three-part classroom kit: a student notebook, a fully worked teacher copy, and a two-page lesson guide with timing, standards, expected answers, misconceptions, troubleshooting, and complexity dials.",
    "include": [
      "Answer keys with expected numeric ranges, not brittle single values, plus sample claim-evidence-reasoning responses and a short interpretation rubric.",
      "A standards alignment table mapping each task—not merely each notebook—to CCSS code, student action, and evidence of learning; add editable state-standard crosswalk space rather than claiming universal alignment.",
      "Three visible complexity dials: Core changes numbers or selects from menus; Explore adds formulas, comparisons, or a second dataset; Extend exposes optional code, uncertainty, or a design challenge. Default to Core for a 45-minute non-AP class.",
      "A minute-by-minute plan, prerequisite check, vocabulary list, learning targets in student language, materials list, and an exit ticket that can be completed without code.",
      "Teacher notes on common misconceptions: AFM color is encoded height rather than natural color; a 3D plot is vertically exaggerated; correlation is not causation; missing is not zero; monolayer thickness is approximate; Moore's law is not a guarantee.",
      "A data story card for each selected sample: material, growth method, why researchers care, what was measured, package title, DOI, and one honest limitation. Include pronunciation help and define semiconductor, transistor, photonics, wafer, and data center without hype.",
      "A technology connection that distinguishes electronics, photonics, logic, memory, and integration, and explains AI-data-center relevance through compute density, memory bandwidth or movement, energy, and cooling while avoiding claims that a sample is already deployed commercially.",
      "Accessibility: colorblind-safe scales, redundant labels or patterns, alt text, keyboard-accessible controls where possible, readable contrast, captions/transcripts for media, and a static table/plot alternative to every interactive view.",
      "Operational fallbacks: pre-run screenshots, printable worksheet, local CSV/ZIP download, manual-upload directions, tested browser list, expected download size, and a one-page Colab/SharePoint troubleshooting flow.",
      "Reproducibility and trust: release ID displayed in the notebook, DOI citations, data-processing summary, definition of each derived metric, inclusion/exclusion rules, checksum validation, and a contact/report-an-issue route.",
      "Classroom safety note for STL: the notebook creates a digital model only; any physical printing follows the school's normal printer, ventilation, heat, and supervision rules.",
      "A five-minute teacher rehearsal checklist and a fresh-runtime test checklist, including widget rendering, anonymous download, manual fallback, answer-key values, and total runtime on a school-managed Chromebook."
    ]
  }
}
