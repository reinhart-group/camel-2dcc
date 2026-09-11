# ---
# module: data_chip_timeline
# kind: dataset
# produces: [curve]
# dials:
#   realism: [clean, curated, annotated, research]
# minutes: 4
# ---
# %% [markdown]
# ## The data: transistor counts over time
# A transistor is a tiny switch. Modern computer chips contain billions of them. This table lists
# announced counts for a hand-picked set of well-known chips; it is not every chip ever made.

# %%
_chips = load_table("chips_timeline").sort_values("year")

# %% tags=["realism:clean"]
_chosen = _chips[_chips["maker"] == "Intel"]

# %% tags=["realism:curated"]
_chosen = _chips.copy()

# %% tags=["realism:annotated"]
_chosen = _chips.copy()
print("The final chip packages two dies, and the list mixes several kinds of processors.")

# %% tags=["realism:research"]
_chosen = _chips.copy()
print(_chosen[["year", "chip", "maker", "transistors", "dies_in_package"]])

# %%
curve_x = _chosen["year"].to_numpy(float)
curve_y = _chosen["transistors"].to_numpy(float)
curve_x_label, curve_y_label = "year", "transistor count"
