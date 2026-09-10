# ---
# module: concept_demo
# kind: concept
# accepts: [series]
# dials:
#   guidance: [worked, fill, open]
#   register: [plain, explorer]
# minutes: 8
# ---
# %% [markdown]
# ## Mean and median

# %% [markdown] tags=["register:plain"]
# The **mean** is the fair-share number.

# %% [markdown] tags=["register:explorer"]
# The mean is the arithmetic average of all values.

# %% tags=["guidance:worked"]
answer = float(sum(series_values) / len(series_values))

# %% tags=["guidance:fill", "guidance:open"]
answer = ...  # ✏️ type your answer here
