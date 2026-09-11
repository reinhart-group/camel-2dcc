# ---
# module: data_grain_population
# kind: dataset
# produces: [series, groups]
# dials:
#   realism: [clean, curated, annotated, research]
# params:
#   sample_size: {default: 80, min: 20, max: 501}
#   seed: {default: 3, min: 0, max: 9999}
# minutes: 4
# ---
# %% [markdown]
# ## The data: tiny triangles
# A computer found triangle-like shapes in three small images. We use the shapes that passed its
# rules as our whole group. The computer can still miss a shape or give it the wrong label.

# %%
_scans, _all_grains = load_grain_scans("camel-2dcc")
_population = _all_grains[_all_grains["role"] == "population"]

# %% tags=["realism:clean"]
_population = whole_single(_population)

# %% tags=["realism:curated"]
_population = whole_single(_population)

# %% tags=["realism:annotated"]
_population = _population[_population["kind"] != "streak"]
print(_population["kind"].value_counts())

# %% tags=["realism:research"]
_population = _population.copy()
print(_population[["scan", "position", "kind", "touches_edge", "area_nm2"]].head(12))

# %%
_pick = _population.sample(n=min(PARAMS["sample_size"], len(_population)),
                           random_state=PARAMS["seed"])
series_values = _pick["area_nm2"].to_numpy(float)
series_label, series_unit = "triangle area", "nm²"
groups_table = _pick.rename(columns={"area_nm2": "value", "position": "group"})[["value", "group"]]
groups_label, groups_unit = series_label, series_unit
