# ---
# module: data_afm_roughness
# kind: dataset
# produces: [series, groups]
# dials:
#   register: [plain, explorer]
#   messiness: [real, flagged]
# params:
#   sample_size: {default: 60, min: 10, max: 1004}
#   seed: {default: 1, min: 0, max: 9999}
# minutes: 4
# ---
# %% [markdown] tags=["register:plain"]
# ## Our data: bumpy or smooth films
# Scientists scan a surface with a microscope and measure how bumpy it is.

# %% [markdown] tags=["register:explorer"]
# ## Data: AFM roughness across the 2DCC sample library
# RMS roughness (nm) from one representative AFM scan per public sample.

# %%
_afm = load_table("afm_summary")

# %% tags=["messiness:flagged"]
_afm = _afm[_afm["growth_method"].notna() & ~_afm["material"].isin(["Al2O3", "Sapphire"])]

# %% tags=["messiness:real"]
_afm = _afm.copy()
_afm["growth_method"] = _afm["growth_method"].fillna("not recorded")   # missing is not zero

# %% tags=["register:plain"]
series_label, series_unit = "bumpiness", "nm"

# %% tags=["register:explorer"]
series_label, series_unit = "bumpiness (RMS roughness)", "nm"

# %%
_pick = _afm.sample(n=min(PARAMS["sample_size"], len(_afm)), random_state=PARAMS["seed"])
series_values = _pick["rms_roughness_nm"].to_numpy(dtype=float)
groups_table = _pick.rename(columns={"rms_roughness_nm": "value", "growth_method": "group"})[["value", "group"]]
groups_label, groups_unit = series_label, series_unit
print(f"{len(series_values)} scans loaded")
