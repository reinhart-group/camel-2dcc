# ---
# module: data_grain_areas
# kind: dataset
# produces: [series, groups]
# dials:
#   register: [plain, explorer]
#   messiness: [real, flagged]
# params:
#   sample_size: {default: 40, min: 10, max: 501}
#   seed: {default: 1, min: 0, max: 9999}
# minutes: 4
# ---
# %% [markdown] tags=["register:plain"]
# ## Our data: tiny triangle crystals
# Scientists grew tiny triangle-shaped crystals on a wafer (the flat disk crystals grow on)
# and measured each one's area.

# %% [markdown] tags=["register:explorer"]
# ## Data: WSe2 islands on sapphire (sample 17458)
# Areas of islands found by a height rule in three 2 µm × 2 µm AFM fields.

# %%
# Reading-level note: the Algebra 1 grade-8 gate (courseware/cli.py `_grade`) is measured on the
# COMPOSED notebook's markdown, across every module in the lesson. Running textstat on this one
# module's markdown in isolation is not comparable (a 14-word excerpt swings wildly on one long
# word) and is not how the gate is actually enforced — don't chase a phantom failure there.
_scans, _grains = load_grain_scans("camel-2dcc")
_pop = _grains[_grains["role"] == "population"]

# %% tags=["messiness:flagged"]
_pop = whole_single(_pop)   # keep only clean, whole, single triangles

# %% tags=["messiness:real"]
_pop = _pop[_pop["kind"] != "streak"]   # keep merged grains and dust: real data is messy

# %%
_pick = _pop.sample(n=min(PARAMS["sample_size"], len(_pop)), random_state=PARAMS["seed"])
series_values = _pick["area_nm2"].to_numpy(dtype=float)
series_label, series_unit = "triangle area", "nm²"
groups_table = _pick.rename(columns={"area_nm2": "value", "position": "group"})[["value", "group"]]
groups_label, groups_unit = series_label, series_unit
print(f"{len(series_values)} triangles loaded")
