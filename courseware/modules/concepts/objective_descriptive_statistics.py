# ---
# module: objective_descriptive_statistics
# kind: concept
# accepts: [series]
# dials:
#   reasoning: [notice, calculate, model, justify]
#   support: [worked, guided, partial, independent]
# minutes: 18
# ---
# %% [markdown]
# # Describe a Distribution
# **Learning objective:** describe a numerical distribution using its shape, center, and spread.

# %%
import matplotlib.pyplot as plt
import numpy as np
_mean = float(np.mean(series_values))
_median = float(np.median(series_values))
_q1, _q3 = np.percentile(series_values, [25, 75])
_sd = float(np.std(series_values))
plt.figure(figsize=(8, 4)); plt.hist(series_values, bins=20, color="#0072B2", edgecolor="white")
plt.axvline(_mean, color="#D55E00", label="mean"); plt.axvline(_median, color="black", ls="--", label="median")
plt.xlabel(f"{series_label} ({series_unit})"); plt.ylabel("count"); plt.legend(); plt.show()

# %% [markdown] tags=["reasoning:notice"]
# Describe where most values sit and whether the histogram has a longer tail on one side.

# %% [markdown] tags=["reasoning:calculate"]
# Calculate the mean, median, range, and interquartile range. Include the measurement unit.

# %% [markdown] tags=["reasoning:model"]
# Compare standard deviation with interquartile range. Explain which reacts more to extreme values.

# %% [markdown] tags=["reasoning:justify"]
# Choose the better measure of a typical value for this distribution and defend your choice from the graph.

# %% [markdown] tags=["support:worked"]
# Worked result: the code below reports every statistic and names the calculation.

# %% [markdown] tags=["support:guided"]
# Guidance: mean uses every value; median is the middle; range is maximum minus minimum; IQR is Q3 − Q1.

# %% [markdown] tags=["support:partial"]
# Hints: use `np.mean`, `np.median`, `np.ptp`, and `np.percentile`.

# %% [markdown] tags=["support:independent"]
# Show your calculations and support your interpretation with at least two statistics.

# %%
print(f"mean = {_mean:.2f} {series_unit}; median = {_median:.2f} {series_unit}")
print(f"range = {np.ptp(series_values):.2f} {series_unit}; IQR = {_q3-_q1:.2f} {series_unit}; SD = {_sd:.2f} {series_unit}")

# %% [markdown]
# ## Exit ticket
# If one extremely large measurement were added, which would usually move more: mean or median? Why?
