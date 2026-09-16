"""Warmup and mess-round items: notice & wonder, distributions, missingness, messy labels,
scan-size traps, and odd values. Six .js components, reused across variants via opts."""
from __future__ import annotations

import catalog_data as cd
import catalog_data_a as cda

TOP_MATERIALS = ["MoS2", "WSe2", "WS2", "In2Se3", "GaSe", "MoSe2"]


def _vals(rows, value_key, group_key=None):
    out = []
    for r in rows:
        v = r.get(value_key)
        if v is None:
            continue
        d = {"v": v}
        if group_key:
            d["g"] = r.get(group_key)
        out.append(d)
    return out


def _missing_rows(rows, group_key):
    return [{"g": r.get(group_key), "time": r.get("time"), "rough": r.get("rough")} for r in rows]


def _scan_rows(rows, group_key=None):
    out = []
    for r in rows:
        if r.get("scan") is None or r.get("rough") is None:
            continue
        d = {"scan": r["scan"], "rough": r["rough"]}
        if group_key:
            d["g"] = r.get(group_key)
        out.append(d)
    return out


def _line_share(r):
    """Fraction of the scan's expected lines that were actually recorded."""
    if r.get("pix") is None or r.get("lines") is None or r["pix"] == 0:
        return None
    return round(r["lines"] / r["pix"], 3)


def _odd_extreme_rough(threshold=5.0):
    rows = [r for r in cd.samples(clean=True) if r.get("rough") is not None and r["rough"] >= threshold]
    for r in rows:
        r["reason"] = "roughness above " + str(int(threshold)) + " nm (most films here measure under 1 nm)"
        r["share"] = _line_share(r)
    return rows


def _odd_early_stop():
    rows = [r for r in cd.samples(clean=True)
            if r.get("lines") is not None and r.get("pix") is not None and r["lines"] < r["pix"]]
    for r in rows:
        r["reason"] = "the scan stopped before it finished"
        r["share"] = _line_share(r)
    return rows


def _odd_combined(threshold=5.0):
    by_id = {}
    for r in _odd_extreme_rough(threshold):
        r = dict(r)
        by_id[r["id"]] = r
    for r in _odd_early_stop():
        if r["id"] in by_id:
            by_id[r["id"]]["reason"] = "both: roughness above " + str(int(threshold)) + \
                " nm, and the scan stopped early"
        else:
            by_id[r["id"]] = dict(r)
    return sorted(by_id.values(), key=lambda r: r["id"])


def _bg_rough(flagged_ids):
    """Roughness of every cleaned sample that is NOT in the flagged set, so an item can
    show what removing flagged rows does to the whole distribution, not just the subset."""
    return [round(r["rough"], 3) for r in cd.samples(clean=True)
            if r.get("rough") is not None and r["id"] not in flagged_ids]



def _flagged_with_bg(rows, keys):
    ids = {r["id"] for r in rows}
    return {"flagged": cd.compact(rows, keys), "bg": _bg_rough(ids)}


ITEMS = [
    # ---------------------------------------------------------------- notice_and_wonder (warmup)
    {
        "id": "W-01",
        "round": "warmup",
        "title": "What do you see in this picture?",
        "blurb": "One microscope height map, no labels yet. Notice, wonder, then reveal what it is.",
        "grades": "6-12",
        "source": "one AFM height map, 2DCC gallery",
        "item": "notice_and_wonder",
        "data": lambda: {"kind": "image", **cda.small_heightmap("wse2_triangles")},
        "opts": {
            "kind": "image",
            "question": "This is a real picture from a scientific instrument. What do you notice? "
                        "What do you wonder?",
            "reveal_title": "Tiny triangles of tungsten diselenide (WSe2), with a glitch.",
            "reveal_lines": [
                "This is an atomic force microscope (AFM) scan: a needle drags across the surface "
                "and feels its height, atom by atom.",
                "The triangles are crystals of WSe2, a material thin enough that it could make "
                "transistors thinner than any made of silicon.",
                "This scan also has a glitch — a line where the instrument itself misbehaved, "
                "not the crystal. Did you notice it?",
                "The recorded roughness for this scan is 6.10 nm over a 2 µm × 2 µm patch — but "
                "the colour scale shows the crystals themselves are only about 2 nm tall. Exactly "
                "one scan line out of 512 is the glitch, and it dips to −455 nm. Leave that single "
                "line out and the roughness is 0.80 nm.",
                "So one bad line in 512 multiplied the headline number by more than seven. This is "
                "the kind of thing worth finding before anyone puts the number in a table.",
            ],
        },
    },
    {
        "id": "W-02",
        "round": "warmup",
        "title": "What is this pile of numbers?",
        "blurb": "A histogram with no labels yet. Notice the shape, then reveal what was measured.",
        "grades": "6-12",
        "source": "894 AFM roughness measurements, 2DCC LiST records",
        "item": "notice_and_wonder",
        "data": lambda: {"kind": "hist", "values": [r["rough"] for r in cd.samples(clean=True)
                                                     if r["rough"] is not None]},
        "opts": {
            "kind": "hist", "xlab": "value", "bins": 24,
            "question": "Here are 894 real measurements, with no label yet. What do you notice about "
                        "their shape? What do you wonder?",
            "reveal_title": "Roughness (in nanometers) of 894 real crystal films grown at Penn State.",
            "reveal_lines": [
                "Roughness measures how bumpy a film's surface is: a flatter film has a smaller number.",
                "Most films here are very flat — under 2 nanometers bumpy, which is just a few "
                "atoms tall.",
                "A handful measure far rougher, over 50 nanometers. Those long bars on the right are "
                "real samples, not mistakes — though roughness also depends on how big an area was "
                "scanned, which this chart does not show.",
            ],
        },
    },
    {
        "id": "W-03",
        "round": "warmup",
        "title": "What happened during this recipe?",
        "blurb": "A temperature trace from a real growth recipe, with no labels yet. Notice, wonder, "
                 "then reveal what was cooking.",
        "grades": "6-12",
        "source": "one growth recipe, 2DCC LiST records, sample 17403",
        "item": "notice_and_wonder",
        "data": lambda: {"kind": "line", **{k: v for k, v in cda.recipe_trace(17403).items() if k == "points"}},
        "opts": {
            "kind": "line", "xlab": "minutes since the recipe started", "ylab": "temperature (°C)",
            "question": "This is the temperature log of a real recipe run inside a furnace. What do "
                        "you notice? What do you wonder? Does anything in this line look physically "
                        "impossible for a real furnace to do?",
            "reveal_title": "Growing tungsten disulfide (WS2) on sapphire, by MOCVD.",
            "reveal_lines": [
                "This log records a target temperature for each step, not a continuous measurement. "
                "The flat stretches and the instant jump from 850°C to 1000°C at 45.5 minutes are "
                "artifacts of how the table was written — a real furnace takes time to change "
                "temperature, and that ramp simply is not in this data.",
                "The last two steps ('Cooldown 1' and 'Cooldown 2') are both recorded as 0°C. No "
                "furnace drops from 1000°C to freezing in nine minutes, so 0 is not a real "
                "temperature here — we read it as a placeholder for 'no target was set while "
                "cooling,' though the log does not say so directly.",
            ],
        },
    },
    {
        "id": "W-04",
        "round": "warmup",
        "title": "What is happening to this material as it warms up?",
        "blurb": "A resistance-vs-temperature curve with no labels yet. Notice, wonder, then reveal "
                 "what was measured.",
        "grades": "6-12",
        "source": "183 resistance measurements on one FeSe sample, 2DCC extras",
        "item": "notice_and_wonder",
        "data": lambda: {"kind": "line", "points": cda.transport_points()},
        "opts": {
            "kind": "line", "xlab": "temperature (kelvin)", "ylab": "resistance (ohms)",
            "question": "This is a real measurement taken as a sample slowly warmed up from near "
                        "absolute zero to room temperature. What do you notice? What do you wonder?",
            "reveal_title": "Iron selenide (FeSe), a superconductor, warming up.",
            "reveal_lines": [
                "A superconductor carries electricity with zero resistance below some temperature, "
                "then acts like an ordinary material above it.",
                "Here, resistance stays near zero below about 17 kelvin (−256°C), then rises "
                "as the sample warms — the transition this material is known for.",
                "This is one sample's measurement, not a claim about every FeSe film ever grown.",
            ],
        },
    },
    # ---------------------------------------------------------------- distribution_explorer (warmup)
    {
        "id": "W-05",
        "round": "warmup",
        "title": "How rough are these films, really?",
        "blurb": "A histogram of roughness for every measured sample. Change the number of bins and "
                 "toggle the mean and median.",
        "grades": "6-12",
        "source": "894 samples with AFM roughness, 2DCC LiST records",
        "item": "distribution_explorer",
        "data": lambda: cd.compact(_vals(cd.samples(clean=True), "rough"), ["v"]),
        "opts": {
            "question": "Slide to change how finely the data is binned. Turn the mean and median "
                        "lines on and off. Does the shape surprise you?",
            "value_label": "roughness", "unit": "nm", "bins_default": 20, "bins_max": 45,
            "note": "Roughness depends on how big an area the microscope scanned, so this mixes scans "
                    "of many different sizes together.",
        },
    },
    {
        "id": "W-06",
        "round": "warmup",
        "title": "Does roughness look different for one material?",
        "blurb": "The same roughness histogram, but pick a single material to look at.",
        "grades": "6-12",
        "source": "894 samples with AFM roughness, 2DCC LiST records",
        "item": "distribution_explorer",
        "data": lambda: cd.compact(
            _vals([r for r in cd.samples(clean=True) if r["mat"] in TOP_MATERIALS], "rough", "mat"),
            ["v", "g"]),
        "opts": {
            "question": "Pick a material. Slide the bins, toggle the mean and median. Does one "
                        "material's shape look different from the rest?",
            "value_label": "roughness", "unit": "nm", "bins_default": 16, "bins_max": 40,
            "group_label": "material",
            "group_options": [{"v": m, "t": m} for m in TOP_MATERIALS],
            "note": "Only the six most-measured materials are offered here. Roughness also depends "
                    "on scan size, which this chart does not control for.",
        },
    },
    {
        "id": "W-07",
        "round": "warmup",
        "title": "How big are the islands on one wafer?",
        "blurb": "A histogram of measured island (grain) areas from one real AFM scan.",
        "grades": "6-12",
        "source": "501 detected grains, one WSe2 scan, sample 17458 (2DCC grains dataset)",
        "item": "distribution_explorer",
        "data": lambda: cd.compact(_vals(cd.grains(17458), "area"), ["v"]),
        "opts": {
            "question": "Each of these numbers is the measured area of one island on a single wafer. "
                        "Slide the bins, toggle the mean and median.",
            "value_label": "island area", "unit": "nm²", "bins_default": 22, "bins_max": 45,
            "note": "This is every usable island found on one scan of one sample — not every "
                    "island ever grown at Penn State.",
        },
    },
    {
        "id": "W-08",
        "round": "warmup",
        "title": "How long do these growths take?",
        "blurb": "A histogram of total recorded growth time across every sample with a time on record.",
        "grades": "6-12",
        "source": "775 samples with a recorded growth time, 2DCC LiST records",
        "item": "distribution_explorer",
        "data": lambda: cd.compact(_vals(cd.samples(clean=True), "time"), ["v"]),
        "opts": {
            "question": "Each number is one sample's total time in the furnace, start to finish. "
                        "Slide the bins, toggle the mean and median.",
            "value_label": "growth time", "unit": "min", "bins_default": 20, "bins_max": 40,
            "note": "1,000 samples exist in this slice; only 775 have a recorded growth time. The "
                    "other 225 are simply left out here — not zero.",
        },
    },
    # ---------------------------------------------------------------- missingness_gate (mess)
    {
        "id": "M-02",
        "round": "mess",
        "title": "If you need both time and roughness recorded, who survives — by growth method?",
        "blurb": "Toggle two requirements and watch how many rows survive, overall and for each "
                 "growth method.",
        "grades": "6-12",
        "source": "1,005 samples, 2DCC LiST records (uncleaned)",
        "item": "missingness_gate",
        "data": lambda: cd.compact(_missing_rows(cd.samples(clean=False), "meth"), ["g", "time", "rough"]),
        "opts": {
            "question": "Turn each requirement on or off. How many samples are left — and does it "
                        "depend on how the crystal was grown?",
            "group_label": "growth method",
            "note": "With both requirements on: 740 of 772 MOCVD rows survive, but only 14 of 233 "
                    "Hybrid MBE rows do. A method-only comparison built from “complete” rows "
                    "would barely see Hybrid MBE at all.",
        },
    },
    {
        "id": "M-03",
        "round": "mess",
        "title": "If you need both time and roughness recorded, who survives — by material?",
        "blurb": "The same two requirements, broken down by material instead of growth method.",
        "grades": "6-12",
        "source": "1,000 cleaned samples, 2DCC LiST records",
        "item": "missingness_gate",
        "data": lambda: cd.compact(_missing_rows(cd.samples(clean=True), "mat"), ["g", "time", "rough"]),
        "opts": {
            "question": "Turn each requirement on or off. Some materials nearly disappear — which "
                        "ones, and why might that be?",
            "group_label": "material",
            "note": "In2Se3 and GaSe have roughness on record for many samples but growth time for "
                    "none of them, so requiring both erases them from view entirely.",
        },
    },
    {
        "id": "M-04",
        "round": "mess",
        "title": "If you need both time and roughness recorded, who survives — by year?",
        "blurb": "The same two requirements, broken down by the year the sample was grown.",
        "grades": "6-12",
        "source": "1,000 cleaned samples, 2DCC LiST records",
        "item": "missingness_gate",
        "data": lambda: cd.compact(_missing_rows(cd.samples(clean=True), "year"), ["g", "time", "rough"]),
        "opts": {
            "question": "Turn each requirement on or off. Does record-keeping look different in some "
                        "years than others?",
            "group_label": "year",
            "note": "Record-keeping habits changed over time — this is not a judgment about the "
                    "science done in any year, only about what got written down.",
        },
    },
    # ---------------------------------------------------------------- label_rules (mess)
    {
        "id": "M-05",
        "round": "mess",
        "title": "How many ways can one box be filled in?",
        "blurb": "One text box, typed into by hand for years, holds 35 different spellings. Switch "
                 "general cleaning rules on and off and watch the count fall and the bar chart "
                 "tidy up. No chemistry required: every rule is decided from the text itself.",
        "grades": "6-12",
        "source": "1,005 samples, raw “material” text field beside the “grown on” field",
        "item": "label_rules",
        "data": cda.label_pairs,
        "opts": {
            "question": "This chart counts samples by whatever someone typed into the material "
                        "box. You do not need to know what any of these substances are. Turn on "
                        "a rule and watch what happens to the chart and to the count.",
            "top": 12,
            "rare_below": 5,
            "reveal_title": "All five rules together take 35 spellings down to 25. Here is what "
                            "no rule written from the text can fix:",
            "reveal_lines": [
                "MoS2 has 338 samples, 2H-MoS2 has 2, MoS2-WS2 has 1 and Mo-WSe2 has 18. They "
                "look related and they are four separate labels. Deciding which of them are the "
                "same substance is not something you can read off the text.",
                "A rule that stripped everything before a dash would merge all four. It would be "
                "right about one of them and wrong about the others, and the chart would look "
                "just as tidy either way.",
                "So the mechanical mess — repeats, orderings, a stray 0, the disc typed into the "
                "crystal box — is fixable by anyone. The rest needs someone who knows the field, "
                "and if you do not have that person, the honest move is to say the labels are "
                "unresolved rather than to pick a rule that looks tidy.",
                "Fifteen samples had nothing typed in the box at all. No rule fixes those either.",
            ],
            "note": "Nothing here was invented for the workshop. These are the spellings in the "
                    "records as they stand today.",
        },
    },
    {
        "id": "M-07",
        "round": "mess",
        "title": "One sample, two materials — which one counts?",
        "blurb": "Some rows list two materials separated by a semicolon. Sort each one; then see "
                 "which half a cleanup script keeps.",
        "grades": "6-12",
        "source": "39 of 1,005 samples, raw “material” text field, 2DCC LiST records",
        "item": "clean_labels",
        "data": lambda: [d for d in cda.material_labels() if ";" in d["raw"]],
        "opts": {
            "question": "Each of these rows names two materials for one sample. Tap a spelling, then "
                        "pick which material you think should represent that row.",
            "targets": ["MoS2", "SnSe", "MnSe2", "In2Se3", "GaSe", "FeSe", "FeTe", "Bi2Se3",
                        "not sure / other"],
            "reveal_button": "Which one does an automatic cleanup script keep?",
            "reveal_lines": [
                "A simple rule keeps only the text before the first semicolon and throws the rest away.",
                "For “SnSe; SnSe” that is harmless — both sides agree. For "
                "“MnSe2; In2Se3” it silently keeps MnSe2 and erases In2Se3 from the record, "
                "even though both were really there.",
                "Did every one of your picks match what that rule would have chosen?",
            ],
            "note": "39 of the 1,005 rows (13 distinct spellings) list more than one material this way.",
        },
    },
    # ---------------------------------------------------------------- scan_size_trap (mess)
    {
        "id": "M-08",
        "round": "mess",
        "title": "Which material's film measures roughest — and does that hold up?",
        "blurb": "Compare roughness across six materials, then lock the comparison to one scan "
                 "size and watch the sample count (n) for each material, not just the medians.",
        "grades": "6-12",
        "source": "samples with AFM roughness, restricted to the six most-measured materials",
        "item": "scan_size_trap",
        "data": lambda: cd.compact(
            _scan_rows([r for r in cd.samples(clean=True) if r["mat"] in TOP_MATERIALS], "mat"),
            ["g", "scan", "rough"]),
        "opts": {
            "mode": "compare", "low_n": 10,
            "question": "An atomic force microscope measures roughness by scanning a small patch "
                        "of the film; “scan size” is how wide that patch is, in "
                        "micrometers (µm — millionths of a meter). A bigger patch is more "
                        "likely to catch one unusually tall bump, which can push a material's "
                        "roughness number up for a reason that has nothing to do with the crystal "
                        "itself. These six materials were not all scanned at the same size. "
                        "Compare them as measured, then lock the comparison to one scan size and "
                        "see what changes — and what that costs you.",
            "compare_key": "mat", "compare_label": "material",
            "note": "Locking to one scan size is supposed to make the comparison fairer, and mostly "
                    "the ranking barely moves. The one material whose number moves a lot, In2Se3, "
                    "moves because its sample shrinks from 32 films down to 2 once you require the "
                    "same scan size — not because controlling revealed some hidden truth. A median "
                    "from 2 samples is not more trustworthy than one from 32; it is just smaller. "
                    "Watch n for every material in both views before you trust any of these medians.",
        },
    },
    {
        "id": "M-09",
        "round": "mess",
        "title": "Does growth method change roughness, even after controlling for scan size?",
        "blurb": "Compare roughness between two ways of growing these crystals, then check the gap "
                 "at specific scan sizes to see whether it survives.",
        "grades": "6-12",
        "source": "samples with AFM roughness, both growth methods",
        "item": "scan_size_trap",
        "data": lambda: cd.compact(_scan_rows(cd.samples(clean=True), "meth"), ["g", "scan", "rough"]),
        "opts": {
            "mode": "compare", "low_n": 10,
            "question": "These crystals were grown two different ways: MOCVD (metal-organic "
                        "chemical vapor deposition — gas-phase chemicals react and build up the "
                        "film) and Hybrid MBE (molecular beam epitaxy — atoms are deposited more "
                        "slowly, layer by layer). “Scan size” is how wide a patch of film "
                        "the microscope measured, in micrometers (µm); it can affect the "
                        "roughness number on its own, regardless of growth method. Compare the two "
                        "methods as measured, then lock to one scan size at a time and see whether "
                        "the gap between them survives.",
            "compare_key": "meth", "compare_label": "growth method",
            "note": "The gap does not close at any scan size with enough samples to check: Hybrid "
                    "MBE films measure rougher than MOCVD films whether you look at every scan "
                    "together or lock to one size. That is a real pattern that held up under a "
                    "plausible check — even though the group sizes shift a lot as you lock to "
                    "different scan sizes. These are observational records, not a controlled "
                    "experiment, so the most this shows is that growth method is associated with "
                    "rougher films here, not that it causes the difference.",
        },
    },
    {
        "id": "M-10",
        "round": "mess",
        "title": "Does scan size alone change the roughness number, even for one material?",
        "blurb": "Every sample here is the same material, WSe2. Step through scan sizes and watch "
                 "the distribution, its median, and its sample count (n) move together.",
        "grades": "6-12",
        "source": "WSe2 samples with AFM roughness, 2DCC LiST records",
        "item": "scan_size_trap",
        "data": lambda: cd.compact(_scan_rows([r for r in cd.samples(clean=True) if r["mat"] == "WSe2"]),
                                    ["scan", "rough"]),
        "opts": {
            "mode": "step", "low_n": 4,
            "question": "Nothing about the crystal changes in this data — every scan below is the "
                        "same material, WSe2 (tungsten diselenide). Only the “scan size” "
                        "changes: how wide a patch of the film the microscope measured, in "
                        "micrometers (µm, millionths of a meter). Step through the scan sizes "
                        "and watch what happens to the measured roughness — and to how many "
                        "samples back up each step.",
            "note": "Roughness tends to rise as the scan window grows, at least across the three "
                    "sizes with enough samples to trust: 1 µm (4 samples), 2 µm (28 "
                    "samples), and 5 µm (171 samples). The larger scan sizes shown, from 10 "
                    "µm up, have only one to three samples each — not enough to know whether "
                    "they continue that trend or are just noise from a couple of unusual scans. "
                    "Both facts are on screen at once so neither one hides the other.",
        },
    },
    # ---------------------------------------------------------------- odd_values (mess)
    {
        "id": "M-11",
        "round": "mess",
        "title": "Which extreme roughness readings would you trust?",
        "blurb": "A sortable table of the roughest measured samples. Mark each keep, fix, or remove.",
        "grades": "6-12",
        "source": "66 of 1,000 cleaned samples, roughness 5 nm or higher",
        "item": "odd_values",
        "data": lambda: _flagged_with_bg(_odd_extreme_rough(),
                                         ["id", "mat", "meth", "scan", "rough", "reason"]),
        "opts": {
            "question": "Most films here measure under 1 nm rough. These 66 measure 5 nm or rougher, "
                        "up to 92 nm. Sort through them: keep, fix, or remove?",
            "columns": [{"key": "mat", "label": "material"}, {"key": "meth", "label": "method"},
                        {"key": "scan", "label": "scan size (µm)"}, {"key": "rough", "label": "roughness (nm)"}],
            "chart": {"key": "rough", "label": "roughness (nm)", "what": "flagged samples"},
            "note": "There is no answer key here. A real bump can be 92 nm tall; so can a speck of "
                    "dust the microscope tripped over. Record your reasons, not just your tally.",
        },
    },
    {
        "id": "M-12",
        "round": "mess",
        "title": "Which scans stopped before they finished?",
        "blurb": "A sortable table of scans where the recorded lines are fewer than the pixels across "
                 "— meaning the scan stopped early. Mark each keep, fix, or remove and watch the "
                 "chart of lines-recorded move.",
        "grades": "6-12",
        "source": "110 of 1,000 cleaned samples, scan lines fewer than pixels",
        "item": "odd_values",
        "data": lambda: cd.compact(_odd_early_stop(),
                                    ["id", "mat", "meth", "scan", "pix", "lines", "share", "reason"]),
        "opts": {
            "question": "For each of these, the microscope recorded fewer lines than the scan's own "
                        "pixel width — the scan stopped partway through. Sort through them.",
            "columns": [{"key": "mat", "label": "material"}, {"key": "meth", "label": "method"},
                        {"key": "pix", "label": "pixels across"}, {"key": "lines", "label": "lines recorded"},
                        {"key": "share", "label": "share of lines recorded"}],
            "chart": {"key": "share", "label": "share of lines recorded", "what": "flagged samples"},
            "note": "A short scan is not automatically wrong — it may still show a real, if "
                    "smaller, patch of the sample. Decide what you would do with each one.",
        },
    },
    {
        "id": "M-13",
        "round": "mess",
        "title": "All the odd-looking rows in one table",
        "blurb": "Every sample flagged for extreme roughness or an early-stopped scan, filterable by "
                 "reason. Mark each keep, fix, or remove.",
        "grades": "6-12",
        "source": "174 of 1,000 cleaned samples, flagged for one or both reasons",
        "item": "odd_values",
        "data": lambda: _flagged_with_bg(
            _odd_combined(),
            ["id", "mat", "meth", "scan", "rough", "pix", "lines", "share", "reason"]),
        "opts": {
            "question": "These 174 rows were flagged for at least one reason. Filter by reason, sort "
                        "by any column, and sort through them: keep, fix, or remove?",
            "columns": [{"key": "mat", "label": "material"}, {"key": "meth", "label": "method"},
                        {"key": "scan", "label": "scan (µm)"}, {"key": "rough", "label": "roughness (nm)"},
                        {"key": "pix", "label": "pixels"}, {"key": "lines", "label": "lines"},
                        {"key": "share", "label": "share of lines recorded"}],
            "chart": {"key": "rough", "label": "roughness (nm)", "what": "flagged samples"},
            "note": "Only 2 rows are flagged for both reasons at once — most odd rows are odd in "
                    "only one way.",
        },
    },
]
