"""Model-round and dials-round catalog items: scatter fits, a sampling studio, real
growth recipes, height-map profiles, a transport curve, the complexity dials, and a
claim-checking exercise.
"""
from __future__ import annotations

import catalog_data as cd
import catalog_data_b as cdb

# Three real, complete growth recipes used by recipe_timeline. 17458 is the MOCVD WSe2
# recipe used elsewhere in the grain-scan materials, but its temperature column is a flat
# 850 C target for all six recorded steps (two blank) -- a setpoint table, not a
# measurement, and it has no shape to read. 28363 is a different MOCVD recipe (MoS2, 11
# steps, verified 2026-09-16) with real shape: 800 C anneal, a step up to 850 C, a further
# step up to 950 C for growth, then two 0 C cooldown steps. 69173 is a Hybrid MBE SnSe
# recipe with every step's duration recorded.
_MOCVD_META = {"label": "MOCVD, WSe2 on sapphire, 850 °C nucleation (sample 17458)"}
_MOCVD_SHAPE_META = {"label": "MOCVD, MoS2 on sapphire (sample 28363)"}
_MBE_META = {"label": "Hybrid MBE, SnSe (sample 69173)"}

ITEMS = [
    # ---- scatter_fit ------------------------------------------------------------
    {
        "id": "G-01",
        "round": "model",
        "title": "Does growing a film longer change how rough it is?",
        "blurb": "Scatter plot of roughness against growth time, with a least-squares "
                 "line, its slope and R-squared, and a count of how many samples could be drawn.",
        "grades": "6-12",
        "source": "1,005 samples' recipe settings joined to their AFM roughness, 2DCC LiST records",
        "item": "scatter_fit",
        "data": lambda: cd.compact(cd.samples(clean=False), ["mat", "time", "rough"]),
        "opts": {
            "question": "Penn State recorded how long each film grew and later measured how rough "
                        "it came out. Do longer growth times go with rougher films?",
            "x_key": "time", "x_label": "growth time (minutes)", "x_unit": "minute",
            "allow_color": True, "color_default": "off",
            "note": "Growth time was a recipe setting scientists chose; roughness depends on many "
                    "other things too, including which microscope scan size was used.",
        },
    },
    {
        "id": "G-02",
        "round": "model",
        "title": "Growth time and roughness, coloured by material",
        "blurb": "Same growth-time-versus-roughness plot, with a toggle to colour each point by "
                 "the material grown, so a learner can see whether one line fits every material.",
        "grades": "6-12",
        "source": "1,005 samples' recipe settings joined to their AFM roughness, 2DCC LiST records",
        "item": "scatter_fit",
        "data": lambda: cd.compact(cd.samples(clean=False), ["mat", "time", "rough"]),
        "opts": {
            "question": "Turn on colour by material. Does the growth-time trend look the same "
                        "for every material, or is it really a few materials driving the line?",
            "x_key": "time", "x_label": "growth time (minutes)", "x_unit": "minute",
            "allow_color": True, "color_default": "on",
            "note": "Material spellings are shown exactly as scientists entered them, so the same "
                    "material can appear more than once in the key.",
        },
    },
    {
        "id": "G-03",
        "round": "model",
        "title": "Does growth temperature change how rough the film is?",
        "blurb": "Scatter plot of roughness against growth temperature, with a least-squares line "
                 "and a count of how many of the 1,005 samples had both values recorded.",
        "grades": "6-12",
        "source": "1,005 samples' recipe settings joined to their AFM roughness, 2DCC LiST records",
        "item": "scatter_fit",
        "data": lambda: cd.compact(cd.samples(clean=False), ["mat", "temp", "rough"]),
        "opts": {
            "question": "Does a hotter growth temperature go with a rougher (or smoother) film?",
            "x_key": "temp", "x_label": "growth temperature (°C)", "x_unit": "°C",
            "allow_color": True, "color_default": "off",
            "note": "Temperature is recorded for fewer samples than growth time, so this graph "
                    "draws a different, smaller set of points.",
        },
    },
    {
        "id": "G-04",
        "round": "model",
        "title": "Growth temperature and roughness, coloured by material",
        "blurb": "Roughness against growth temperature, with a toggle to colour points by material.",
        "grades": "6-12",
        "source": "1,005 samples' recipe settings joined to their AFM roughness, 2DCC LiST records",
        "item": "scatter_fit",
        "data": lambda: cd.compact(cd.samples(clean=False), ["mat", "temp", "rough"]),
        "opts": {
            "question": "Colour the points by material. Is a temperature trend really one "
                        "material's recipe, or does it hold across materials?",
            "x_key": "temp", "x_label": "growth temperature (°C)", "x_unit": "°C",
            "allow_color": True, "color_default": "on",
            "note": "Material spellings are shown exactly as entered, so some materials appear "
                    "more than once in the key.",
        },
    },
    {
        "id": "G-05",
        "round": "model",
        "title": "Does chamber pressure change how rough the film is?",
        "blurb": "Roughness against growth pressure, with a least-squares line, slope, and R-squared.",
        "grades": "9-12",
        "source": "1,005 samples' recipe settings joined to their AFM roughness, 2DCC LiST records",
        "item": "scatter_fit",
        "data": lambda: cd.compact(cd.samples(clean=False), ["mat", "press", "rough"]),
        "opts": {
            "question": "Growth pressure is set in Torr. Does a higher chamber pressure go with "
                        "a rougher or smoother film?",
            "x_key": "press", "x_label": "growth pressure (Torr)", "x_unit": "Torr",
            "allow_color": False,
            "note": "Pressure spans a huge range across growth methods, so a strong-looking line "
                    "can be driven by which method used which pressure, not by pressure itself.",
        },
    },

    # ---- sampling_studio ----------------------------------------------------------
    {
        "id": "G-06",
        "round": "model",
        "title": "How much does a sample mean bounce around?",
        "blurb": "Draw random samples of n grains from a real wafer and watch the sample mean "
                 "area move around the population mean, one histogram bar at a time.",
        "grades": "6-12",
        "source": "501 real, non-touching single grains measured across 3 AFM scans on one WSe2 "
                  "wafer (sample 17458), 2DCC LiST records",
        "item": "sampling_studio",
        "data": lambda: cd.compact(cd.grains(17458), ["spot", "area"]),
        "opts": {
            "question": "Draw a small sample of grains and find its mean area. Draw again. How "
                        "much does that sample mean move around?",
            "default_spot": "all", "n_min": 3, "n_max": 60, "n_default": 8,
            "note": "Small samples bounce around more than large ones — watch how the histogram "
                    "narrows as you draw more samples or raise n.",
        },
    },
    {
        "id": "G-07",
        "round": "model",
        "title": "A convenience sample: only the center of the wafer",
        "blurb": "The same sampling studio, restricted by default to the wafer's center spot, to "
                 "show what a convenience sample can miss.",
        "grades": "6-12",
        "source": "501 real, non-touching single grains measured across 3 AFM scans on one WSe2 "
                  "wafer (sample 17458), 2DCC LiST records",
        "item": "sampling_studio",
        "data": lambda: cd.compact(cd.grains(17458), ["spot", "area"]),
        "opts": {
            "question": "If a scientist only ever scanned the center of the wafer, what would "
                        "they think the typical grain looked like? Switch to 'whole population' "
                        "to see what they'd be missing.",
            "default_spot": "center", "n_min": 3, "n_max": 40, "n_default": 8,
            "note": "The center spot's grains run smaller than the edge spot's here — a sample "
                    "from only one spot is a convenience sample, not a random one.",
        },
    },
    {
        "id": "G-08",
        "round": "model",
        "title": "A convenience sample: only the wafer's edge",
        "blurb": "The same sampling studio, restricted by default to the wafer's edge spot.",
        "grades": "6-12",
        "source": "501 real, non-touching single grains measured across 3 AFM scans on one WSe2 "
                  "wafer (sample 17458), 2DCC LiST records",
        "item": "sampling_studio",
        "data": lambda: cd.compact(cd.grains(17458), ["spot", "area"]),
        "opts": {
            "question": "Now sample only from the edge spot. Does its typical grain area match "
                        "the center spot, or the whole wafer?",
            "default_spot": "edge", "n_min": 3, "n_max": 40, "n_default": 8,
            "note": "Three scanned spots on one wafer are a measured population, not a full "
                    "wafer census — there could be other patterns a fourth spot would show.",
        },
    },

    # ---- recipe_timeline ------------------------------------------------------------
    {
        "id": "G-09",
        "round": "model",
        "title": "Read a real MOCVD growth recipe",
        "blurb": "Temperature versus elapsed time for one real growth recipe, step by step, with "
                 "each step's duration and its rate of temperature change from the step before.",
        "grades": "6-12",
        "source": "one recipe (11 steps) from growth_recipes.csv, sample 28363, 2DCC LiST records",
        "item": "recipe_timeline",
        "data": lambda: cd.recipe(28363),
        "opts": {
            "question": "This is exactly how one real MoS2 crystal was grown: temperature held "
                        "and changed step by step, from an 800 °C anneal up to 950 °C for growth "
                        "and back down. What happens right before the crystal grows?",
            "mode": "single", "a": _MOCVD_SHAPE_META,
            "note": "A blank temperature or duration means it was not recorded, not that it was zero.",
        },
    },
    {
        "id": "G-10",
        "round": "model",
        "title": "Read a real hybrid MBE growth recipe",
        "blurb": "The same kind of temperature-versus-time reading, for a longer 13-step hybrid "
                 "MBE recipe.",
        "grades": "6-12",
        "source": "one recipe (13 steps) from growth_recipes.csv, sample 69173, 2DCC LiST records",
        "item": "recipe_timeline",
        "data": lambda: cd.recipe(69173),
        "opts": {
            "question": "This recipe grew a tin selenide (SnSe) film by hybrid molecular beam "
                        "epitaxy. How many separate temperature holds can you count?",
            "mode": "single", "a": _MBE_META,
            "note": "A blank temperature or duration means it was not recorded, not that it was zero.",
        },
    },
    {
        "id": "G-11",
        "round": "model",
        "title": "Compare an MOCVD recipe to a hybrid MBE recipe",
        "blurb": "Both real recipes plotted on the same temperature-versus-time axes, so a learner "
                 "can see how differently the two growth methods run.",
        "grades": "6-12",
        "source": "two recipes from growth_recipes.csv, samples 17458 and 69173, 2DCC LiST records",
        "item": "recipe_timeline",
        "data": lambda: {"a": cd.recipe(17458), "b": cd.recipe(69173)},
        "opts": {
            "question": "One recipe finishes in under an hour, the other takes over four. What "
                        "else is different about how they hold and change temperature?",
            "mode": "compare", "a": _MOCVD_META, "b": _MBE_META,
            "note": "The two recipes run on very different timescales, so this shared axis "
                    "compresses the shorter one — read the step table below for the real numbers.",
        },
    },

    # ---- profile_reader ------------------------------------------------------------
    {
        "id": "G-12",
        "round": "model",
        "title": "Read heights off terraced triangle crystals",
        "blurb": "A real height map of a crystal surface, with a draggable line whose height "
                 "profile plots below, so a learner can read off the height of each terrace.",
        "grades": "6-12",
        "source": "one AFM scan, 2 µm across, sample 17853 (InSe), 2DCC gallery",
        "item": "profile_reader",
        # 128 pixels across natively; cd.heightmap always halves once more after its own
        # size-based stride, so any size >= 128 gives the same full-resolution 64x64 grid
        # (about 31 KB). Verified 2026-09-16: the height histogram has 7 distinct levels
        # spanning 6.7 nm, and the level spacings are uneven, clustering near 0.27 nm and
        # 0.95 nm -- not one fixed step height.
        "data": lambda: cdb.heightmap_profile("terraced_triangles", size=128),
        "opts": {
            "question": "Drag the line up and down the crystal. Each flat terrace is one step "
                        "down, but the steps are not all the same height. About how tall are the "
                        "smaller steps, and how tall are the bigger ones, in nanometers?",
            "note": "Heights are levelled per scan line and shifted so the median is 0, the "
                    "instrument's standard processing step. This scan is only 128 pixels across "
                    "(most gallery scans are about 512), so the profile is coarser than usual, "
                    "but the terrace steps still show clearly.",
        },
    },
    {
        "id": "G-13",
        "round": "model",
        "title": "Read heights off stacked triangle crystals",
        "blurb": "A real height map of stacked triangular crystals, with a draggable profile line.",
        "grades": "6-12",
        "source": "one AFM scan, 1 µm across, sample 50210 (Bi2Se3), 2DCC gallery",
        "item": "profile_reader",
        # Raised from size=96 (53x53, ~22 KB) to size=128 (66x66, ~33 KB): sharper profile,
        # still well under the ~60 KB budget.
        "data": lambda: cdb.heightmap_profile("triangle_pyramids", size=128),
        "opts": {
            "question": "These triangles stack like steps. Drag the line across a stack: how many "
                        "different height levels does it cross?",
            "note": "Heights are levelled per scan line and shifted so the median is 0, the "
                    "instrument's standard processing step.",
        },
    },

    # ---- transport_curve ------------------------------------------------------------
    {
        "id": "G-14",
        "round": "model",
        "title": "Where does the resistance drop to (almost) zero?",
        "blurb": "A real resistance-versus-temperature sweep, with a draggable threshold to "
                 "estimate the temperature where resistance falls away.",
        "grades": "9-12",
        "source": "183 real resistance measurements, 2 K to 300 K, sample 20201 (FeSe), "
                  "2DCC extras/transport_fese.csv",
        "item": "transport_curve",
        "data": lambda: cd.transport(),
        "opts": {
            "question": "This is a real iron selenide (FeSe) film cooled from room temperature "
                        "down to 2 kelvin. Drag the threshold down toward zero: about what "
                        "temperature does resistance disappear at?",
            "threshold_default": 50,
            "note": "Below its transition, FeSe carries current with (near) zero resistance — a "
                    "superconductor. This one real cooldown does not show whether every FeSe film "
                    "behaves the same way.",
        },
    },

    # ---- claim_check ------------------------------------------------------------
    {
        "id": "G-15",
        "round": "model",
        "title": "Check a claim: does growth time predict roughness?",
        "blurb": "Pick a claim about the data, see the evidence for and against it (including how "
                 "much data is missing), then rewrite the claim with a limitation.",
        "grades": "9-12",
        "source": "1,005 samples' recipe settings joined to their AFM roughness, 2DCC LiST records",
        "item": "claim_check",
        "data": lambda: cd.compact(cd.samples(clean=False), ["meth", "time", "rough"]),
        "opts": {
            "default_claim": "time_rough",
            "claims": [
                {"key": "time_rough", "claim": "Growing a film longer makes it rougher.",
                 "type": "correlation", "x_key": "time", "x_label": "growth time (min)"},
                {"key": "method_smooth", "claim": "MOCVD makes smoother films than hybrid MBE.",
                 "type": "group", "group_key": "meth", "groups": ["MOCVD", "Hybrid MBE"]},
            ],
            "note": "Both claims describe an association in observational records, never a cause.",
        },
    },
    {
        "id": "G-16",
        "round": "model",
        "title": "Check a claim: is MOCVD smoother than hybrid MBE?",
        "blurb": "The same claim-checking tool, opened on the growth-method claim first.",
        "grades": "9-12",
        "source": "1,005 samples' recipe settings joined to their AFM roughness, 2DCC LiST records",
        "item": "claim_check",
        "data": lambda: cd.compact(cd.samples(clean=False), ["meth", "time", "rough"]),
        "opts": {
            "default_claim": "method_smooth",
            "claims": [
                {"key": "time_rough", "claim": "Growing a film longer makes it rougher.",
                 "type": "correlation", "x_key": "time", "x_label": "growth time (min)"},
                {"key": "method_smooth", "claim": "MOCVD makes smoother films than hybrid MBE.",
                 "type": "group", "group_key": "meth", "groups": ["MOCVD", "Hybrid MBE"]},
            ],
            "note": "772 samples used MOCVD and 233 used hybrid MBE, and not every sample of "
                    "either was measured for roughness — a lopsided comparison, not a fair trial.",
        },
    },

    # ---- dial_panel (dials round) ------------------------------------------------
    {
        "id": "D-01",
        "round": "dials",
        "title": "Turn all three complexity dials",
        "blurb": "The full structural, provenance, and statistical dials over the sample table "
                 "and a growth-time-versus-roughness plot: the data never change, only what you "
                 "meet first.",
        "grades": "6-12",
        "source": "1,005 samples, 2DCC LiST records, every dial position shown",
        "item": "dial_panel",
        "data": lambda: cd.compact(cd.samples(clean=False),
                                   ["id", "mat", "sub", "meth", "time", "temp", "rough", "scan"]),
        "opts": {
            "question": "Penn State's 2D Crystal Consortium grew these samples and measured how "
                        "rough each film came out. Turn the dials: how does the picture change?",
            "show": ["structural", "provenance", "statistical"],
            "start": {"structural": "some", "provenance": "resolved", "statistical": "implicit"},
        },
    },
    {
        "id": "D-02",
        "round": "dials",
        "title": "A simplified two-dial version",
        "blurb": "Only the structural and statistical dials; provenance is fixed at 'resolved' so "
                 "a beginner meets one fewer decision at once.",
        "grades": "6-12",
        "source": "1,005 samples, 2DCC LiST records, resolved provenance held fixed",
        "item": "dial_panel",
        "data": lambda: cd.compact(cd.samples(clean=False),
                                   ["id", "mat", "sub", "meth", "time", "temp", "rough", "scan"]),
        "opts": {
            "question": "Two dials this time: how many variables you see, and whether noisy "
                        "measurements are filtered out. Try both.",
            "show": ["structural", "statistical"],
            "start": {"structural": "few", "provenance": "resolved", "statistical": "implicit"},
            "fixed": {"provenance": "resolved"},
            "note": "The data are already cleaned of misspelled materials and rows naming a "
                    "substrate as the material, so this version only asks about variables and noise.",
        },
    },
    {
        "id": "D-05",
        "round": "dials",
        "title": "What a grades 6-8 classroom would see",
        "blurb": "The dials start with the messier, surfaced spellings but still filtered noise.",
        "grades": "6-8",
        "source": "1,005 samples, 2DCC LiST records, 6-8 starting position",
        "item": "dial_panel",
        "data": lambda: cd.compact(cd.samples(clean=False),
                                   ["id", "mat", "sub", "meth", "time", "temp", "rough", "scan"]),
        "opts": {
            "question": "This time the material names are exactly as scientists typed them. What "
                        "do you notice?",
            "grade": "6-8", "show": ["structural", "provenance", "statistical"],
            "start": {"structural": "some", "provenance": "surfaced", "statistical": "implicit"},
        },
    },
    {
        "id": "D-06",
        "round": "dials",
        "title": "What a grades 9-12 classroom would see",
        "blurb": "The dials start at full complexity: every variable, surfaced spellings, and "
                 "every scan size and roughness value, noise and all.",
        "grades": "9-12",
        "source": "1,005 samples, 2DCC LiST records, 9-12 starting position",
        "item": "dial_panel",
        "data": lambda: cd.compact(cd.samples(clean=False),
                                   ["id", "mat", "sub", "meth", "time", "temp", "rough", "scan"]),
        "opts": {
            "question": "Full complexity: every recorded variable, every spelling, every scan "
                        "size. Why might a scientist want to see it this way?",
            "grade": "9-12", "show": ["structural", "provenance", "statistical"],
            "start": {"structural": "all", "provenance": "surfaced", "statistical": "explicit"},
        },
    },
]
