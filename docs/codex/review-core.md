{
  "review": {
    "scope": [
      "src/camel_data/spm.py",
      "src/camel_data/classroom.py",
      "src/camel_data/list_public.py",
      "scripts/build_afm_summary.py",
      "scripts/build_slice.py",
      "notebooks/src/_setup_cell.py",
      "data/slice/camel-2dcc-v1.zip and its data/slice/camel-2dcc payload"
    ],
    "overall_assessment": "The reference RMS conversion and watertight-STL tests pass, including under Python 3.13 with plotly 5.24.1 and ipywidgets 7.7.1. The release archive is clean of the requested secrets and internal hostname. However, the pipeline is not yet safe to treat as a reproducible public classroom release: it does not independently enforce Published status, primary-scan selection is usually arbitrary, 64x64 map generation can discard a large fraction of a scan, and recipe summaries can manufacture apparently valid times by combining recipes or treating unknown durations as zero.",
    "findings": [
      {
        "rank": 1,
        "severity": "critical",
        "title": "The 'public' client fails open when given a more privileged API key",
        "location": "src/camel_data/list_public.py:44-48,64-75; scripts/build_slice.py:200-206,232-238",
        "failure_scenario": "PublicLiST accepts any key from an argument, environment variable, or Colab Secret, then sends an empty sample search and exports every record the key can see. If a researcher rebuilds with a staff or otherwise privileged key, unpublished samples can enter samples.csv and the derived files while manifest.json still asserts that the release contains 'public Published records only.' The current raw pull happens to contain 1,413/1,413 Published rows, but that is an observation, not an enforced invariant.",
        "suggested_fix": "Use the API's explicit Published-status filter if available and also validate every returned row client-side. Abort the pull/build if status is missing or anything is not exactly Published. Require a dedicated public read-only key for release builds, record the filter in the manifest, and add a release test proving all exported sample IDs came from Published rows."
      },
      {
        "rank": 2,
        "severity": "high",
        "title": "Primary AFM selection is arbitrary for most multi-scan samples",
        "location": "scripts/build_afm_summary.py:38-51",
        "failure_scenario": "pick_primary claims to prefer the largest scan, but it can infer scan size only from filenames matching a narrow '<number> by/x <number> um' pattern. In the current inputs, 940 samples have multiple SPM files, yet only 47 of the 1,004 selected files (4.7%) have a parsed size hint. For almost all tied files, max() therefore chooses the shortest filename rather than a scientifically defined primary scan. Roughness comparisons can silently mix edge/center scans, different scan areas, channels, or acquisition variants.",
        "suggested_fix": "Select from parsed SPM metadata rather than filenames: inspect each candidate's calibrated height channel, scan dimensions, resolution, line direction, and acquisition metadata. Define and document a deterministic scientific rule, retain every candidate and rejection reason in provenance, recognize all processed/modified naming variants, and require curator selection when candidates remain tied."
      },
      {
        "rank": 3,
        "severity": "high",
        "title": "The 64x64 downsampler silently crops up to nearly half a real scan",
        "location": "scripts/build_afm_summary.py:54-58,70-72; src/camel_data/classroom.py:68-71",
        "failure_scenario": "downsample truncates each dimension to a multiple of 64 before averaging. In the current measured set, 76 scans lose more than 5% of their pixels, 50 lose more than 10%, and one 125x512 scan loses 48.8%. The returned afm_small.npz arrays carry no crop bounds or x/y coordinates, so a teacher or student cannot know that the bottom or right of the image was removed. Non-square scans are also forced into visually square 64x64 arrays without physical aspect metadata.",
        "suggested_fix": "Resample the complete extent with area-weighted bins or a tested resize method instead of top-left cropping. Store original rows/columns, scan_x_um, scan_y_um, crop/resampling method, and coordinate vectors or pixel spacing. If a thumbnail is deliberately cropped, center it and label the crop bounds; do not present it as the full quantitative map."
      },
      {
        "rank": 4,
        "severity": "high",
        "title": "Growth summaries combine distinct recipes into one fictitious run",
        "location": "scripts/build_slice.py:110-137,150-161",
        "failure_scenario": "build_recipes assigns recipe_number, but build_growth_summary drops that key and groups only by sample_id. The current slice has 22 samples with two or three recipes. Their total time is the sum of separate recipes, while maximum temperature and median pressure may come from different recipes; the resulting row looks like one internally consistent growth run when it is not.",
        "suggested_fix": "Keep a stable source recipe ID and aggregate by sample_id plus recipe ID/number. If the classroom table requires one row per sample, choose one canonical recipe using an explicit rule and expose that rule and the number of alternatives. Never sum revisions or separate runs unless the source explicitly says they are sequential parts of one process."
      },
      {
        "rank": 5,
        "severity": "high",
        "title": "Unknown recipe durations become false start times and zero totals",
        "location": "scripts/build_slice.py:119-136,150-159",
        "failure_scenario": "elapsed += dur or 0.0 advances by zero when a duration is missing, so every later start_min is presented as known even though elapsed time is indeterminate. Pandas groupby sum also returns zero for all-missing groups by default. The current slice has 873 missing-duration rows across 166 samples; at least seven samples report growth_time_min=0 even though their identified growth/deposition-step durations are unknown, and mixed known/missing groups are silently undercounted. Students can interpret missing measurements as genuine instantaneous steps.",
        "suggested_fix": "Propagate unknown elapsed time after the first missing duration, use sum(min_count=1), and add completeness flags. Calculate totals and rates only for complete sequences, or publish explicit lower bounds when partial sums are educationally useful. Tests should cover a missing first, middle, and final duration."
      },
      {
        "rank": 6,
        "severity": "high",
        "title": "Pregrowth anneals are misclassified as growth",
        "location": "scripts/build_slice.py:140-155",
        "failure_scenario": "The exclusion regex recognizes 'pre-growth' but not the real label 'Pregrowth'. Five current 'Pregrowth Annealing 1' rows—samples 23428, 23433, 23435, 23436, and 23437—are counted as growth. For example, sample 23428 receives 10 minutes of growth instead of 5, and its summarized temperature, pressure, and growth-step count can also include the anneal.",
        "suggested_fix": "Normalize case, punctuation, and whitespace before classification, or cover variants such as pre[ -]?growth and post[ -]?growth plus robust P.G. forms. Prefer an explicit source step category when available, retain the classification rule/version, and add regression tests using the real labels above."
      },
      {
        "rank": 7,
        "severity": "high",
        "title": "The Colab setup accepts any ZIP and trusts any existing data directory",
        "location": "notebooks/src/_setup_cell.py:12-22",
        "failure_scenario": "A directory named camel-2dcc causes all download and validation logic to be skipped, even if it is partial, stale, or from another release. A downloaded or uploaded file is accepted solely because its first two bytes are PK; HTTP status, release ID, expected size, per-file hashes, and archive paths are not checked. The cell then imports camel_data.classroom from that archive, so a replaced SharePoint target or malicious/wrong teacher URL can execute attacker-supplied Python in Colab. An interrupted prior extraction can make every rerun fail or load a silently mixed release.",
        "suggested_fix": "Pin an expected release ID and archive SHA-256 in the setup cell or a trusted small config. Call raise_for_status(), stream with a size limit, validate a strict member allowlist/root and reject absolute or '..' paths, extract to a temporary directory, verify manifest hashes and required files, then atomically install it. Prefer keeping executable helper code in the trusted notebook/package rather than the remotely downloaded data ZIP. On every run validate an existing directory before reusing it and give teachers a clear repair/manual-upload path."
      },
      {
        "rank": 8,
        "severity": "high",
        "title": "Universal per-row flattening can remove genuine morphology and bias comparisons",
        "location": "src/camel_data/spm.py:140-151; scripts/build_afm_summary.py:69-80; scripts/build_slice.py:172-185",
        "failure_scenario": "Every row is independently fit with a line using all pixels, including islands, steps, particles, and other real features. A large feature occupying much of a row pulls the fit and is partly subtracted; different morphologies are altered by different amounts. The successful 0.358 nm versus 0.36 nm reference validates one smooth scan, but not the heterogeneous scans used for classroom roughness, range, profiles, and 3D surfaces.",
        "suggested_fix": "Retain and publish raw calibrated heights alongside each processed map. Use a documented global plane correction and apply line correction only with masks/robust fitting where justified. Add before/after quality metrics and validate representative smooth, stepped, islanded, and artifact-heavy scans against instrument software or reviewed exports. Make every downstream metric name its processing state."
      },
      {
        "rank": 9,
        "severity": "medium",
        "title": "A truncated cached SPM file is never downloaded again",
        "location": "scripts/build_afm_summary.py:65-70",
        "failure_scenario": "Downloads are written directly to the final path, and any existing path is trusted. If a process dies during write, a gateway returns an error body, or a prior run leaves a truncated file, read_spm fails but future resumptions see the path and continually reuse the bad bytes. The sample remains in the error file even after network conditions recover.",
        "suggested_fix": "Download to a sibling temporary file, validate minimum length, Nanoscope header marker, parsed data bounds, and expected server size or checksum when available, then atomically rename. If validation of an existing cache fails, quarantine or replace it. Record the download checksum in afm_measurements.json, and write checkpoint/error JSON through temporary files plus atomic replace as well."
      },
      {
        "rank": 10,
        "severity": "medium",
        "title": "An uncalibrated height-looking channel can be relabeled as nanometers",
        "location": "src/camel_data/spm.py:105-115,128-136; scripts/build_afm_summary.py:69-80",
        "failure_scenario": "When the Z-scale syntax is not recognized, read_spm returns raw integer values with unit='raw'. height_channel first looks for calibrated exact names but then returns any channel containing 'height' regardless of unit. The builders subsequently call the data z/height_nm and write nm-labelled roughness and ranges. All 1,004 currently measured primaries resolve to nm, but one new file variant can silently contaminate a rebuild.",
        "suggested_fix": "Fail closed unless the selected topography channel has a recognized physical length unit and successful calibration. Expand the scale parser only from validated Nanoscope variants, normalize convertible units explicitly, and add negative tests proving raw/a.u. channels cannot enter nm outputs."
      },
      {
        "rank": 11,
        "severity": "medium",
        "title": "max_pixels is not actually a maximum, and rendering/export assumes square arrays",
        "location": "src/camel_data/classroom.py:22-41,77-96,154-185",
        "failure_scenario": "Both functions compute step with floor division. A shipped 528x528 map therefore renders at 264x264 despite max_pixels=256 and exports at 176x176 despite max_pixels=150; each pre-generated 528-source STL is about 13.9 MB uncompressed. For a rectangular AFMScan, surface_3d builds both axes from the row count, while to_stl uses the row count for both dimensions and can ignore columns or index past them. This causes inaccurate coordinates, oversized browser work, or an exception.",
        "suggested_fix": "Use ceil(max(rows, cols) / max_pixels) or explicit target-grid resampling, create x from columns and y from rows, and either carry separate scan_x_um/scan_y_um values through AFMScan or reject non-square inputs with a clear error. Add tests for 528x528, rows<cols, rows>cols, NaN, and constant-height inputs."
      },
      {
        "rank": 12,
        "severity": "medium",
        "title": "Bulk retrieval has no throttling/retry policy and shares one requests Session across workers",
        "location": "src/camel_data/list_public.py:47-61; scripts/build_afm_summary.py:92-105",
        "failure_scenario": "Four worker threads share one Session and issue downloads without bounded retries or backoff. A classroom-release rebuild that encounters 429, timeout, or transient 5xx responses records omissions and continues; unless the operator audits the error file and expected counts, build_slice will publish the smaller measurements set. Requests does not promise that arbitrary Session use is thread-safe.",
        "suggested_fix": "Use one client/session per worker or serialize the shared session, configure bounded exponential backoff honoring Retry-After for 429/5xx, and make timeout errors as actionable as connection errors. Gate release creation on an explicit completeness policy and carry missing/error counts into the manifest. Preserve or merge prior error history rather than replacing it without review."
      },
      {
        "rank": 13,
        "severity": "medium",
        "title": "The build uses broad copy rules that can regress the currently clean secret boundary",
        "location": "scripts/build_slice.py:212-213,227-229",
        "failure_scenario": "Every entry under data/curated is copied, and nearly the entire camel_data source directory is copied with only list_public.py and __pycache__ excluded. The current archive is clean, but a future maintainer can add a scratch credential file, internal-URL helper, or new API client and ship it automatically without changing build_slice.py.",
        "suggested_fix": "Replace both broad copies with explicit release allowlists, fail on unexpected files, and add a CI/release check that inspects archive entries and decompressed text for forbidden modules, exact configured secret values, credential/private-key markers, and internal host patterns."
      },
      {
        "rank": 14,
        "severity": "low",
        "title": "Invalid secret and base-URL configurations fail with misleading errors",
        "location": "src/camel_data/list_public.py:25-38,44-48",
        "failure_scenario": "Colab userdata.get can return an empty/None value, which escapes _api_key and later produces a requests InvalidHeader rather than the documented 'No LiST key found' message. LIST_BASE_URL also always receives '/api/v2'; a teacher who supplies an already complete API base gets a duplicated path and 404s.",
        "suggested_fix": "Strip and validate the retrieved key before returning it. Define LIST_BASE_URL unambiguously as either an origin/root or a complete API URL, normalize it once, and test both documented forms."
      },
      {
        "rank": 15,
        "severity": "low",
        "title": "The setup placeholder bypasses the intended friendly error",
        "location": "notebooks/src/_setup_cell.py:9,13-20",
        "failure_scenario": "With no uploaded ZIP and the shipped PASTE-SHAREPOINT-LINK-HERE value unchanged, requests raises MissingSchema before the cell reaches its plain-language 'not the data file' RuntimeError. A generic school-hosted or already signed URL can also be broken by blindly appending another download query parameter.",
        "suggested_fix": "Detect the placeholder before calling requests and raise the documented teacher-facing message. Parse and update the query only for recognized SharePoint links; allow an explicitly supplied direct-download URL to remain unchanged."
      }
    ],
    "artifact_audit": {
      "status": "pass",
      "archive": "data/slice/camel-2dcc-v1.zip",
      "checks": [
        "The ZIP is structurally valid and all 27 manifest-listed payload files match their recorded byte sizes and SHA-256 hashes.",
        "The archive contains 28 entries: 27 manifest-listed payload files plus manifest.json itself.",
        "list_public.py is absent from both the archive entry list and the packaged camel_data source directory; only classroom.py and spm.py are packaged there.",
        "The internal hostname m4-2dcc.vmhost.psu.edu, its vmhost.psu.edu suffix, LIST_API_KEY, X-API-KEY, private-key markers, and common inline credential markers were not found in decompressed archive members.",
        "No exact nontrivial value read from the local .env file was found in any decompressed archive member.",
        "No .env, secret/credential-named file, list_public.py, __pycache__, or .pyc entry is present in the ZIP; all entries are unique regular files with no absolute or '..' paths or symlinks.",
        "The archive contains no HTTP(S) URL or email address, and the current staged-tree-only __pycache__ is not archived.",
        "No CSV cell in the current payload starts with a common spreadsheet-formula trigger (=, +, -, @, tab, or carriage return)."
      ],
      "qualification": "This is a targeted static scan, not a proof that arbitrary high-entropy binary data can never contain sensitive information. The explicit allowlist and automated release checks recommended in finding 12 should make the boundary durable."
    },
    "verification": {
      "tests": [
        "PYTHONPATH=src pytest: 6 passed in the repository environment.",
        "Isolated Python 3.13.14 environment with plotly 5.24.1 and ipywidgets 7.7.1: 6 passed; an additional setup/gallery smoke test loaded all 12 gallery scans and 1,004 small maps and created the Plotly surface.",
        "Reference test confirms 256x256 Height Sensor data, 2,000 nm scan size, and flattened RMS within 0.01 nm of the 0.36 nm reference.",
        "STL test confirms matched directed edges and positive bounded volume."
      ],
      "limitations": [
        "The existing tests do not exercise Colab front-end widget rendering, SharePoint redirects/authentication/throttling, interrupted extraction, API pagination with live responses, missing recipe values, multiple recipes per sample, uncalibrated SPM variants, or non-square/odd-sized arrays.",
        "The default repository test command fails collection unless src is installed or PYTHONPATH=src is set; this does not affect the packaged Colab import path but should be addressed in normal project packaging/test configuration."
      ]
    }
  }
}
