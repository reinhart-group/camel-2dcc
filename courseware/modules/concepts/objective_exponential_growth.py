# ---
# module: objective_exponential_growth
# kind: concept
# accepts: [curve]
# dials:
#   reasoning: [notice, calculate, model, justify]
#   support: [worked, guided, partial, independent]
# minutes: 20
# ---
# %% [markdown]
# # Doubling Over Time
# **Learning objective:** distinguish additive from multiplicative change and interpret an exponential model.

# %%
import matplotlib.pyplot as plt
import numpy as np
_years = curve_x - curve_x[0]
_log_slope, _log_intercept = np.polyfit(_years, np.log2(curve_y), 1)
_doubling_time = 1 / _log_slope
_model = 2 ** (_log_intercept + _log_slope * _years)
plt.figure(figsize=(8,4)); plt.scatter(curve_x, curve_y, color="#D55E00", label="listed chips")
plt.plot(curve_x, _model, color="#0072B2", label="exponential model")
plt.yscale("log"); plt.xlabel(curve_x_label); plt.ylabel(curve_y_label + " (log scale)"); plt.legend(); plt.show()

# %% [markdown] tags=["reasoning:notice"]
# Describe how repeated multiplication differs from adding the same number each year.

# %% [markdown] tags=["reasoning:calculate"]
# Starting at 2,300, build four rows of a table that doubles each step.

# %% [markdown] tags=["reasoning:model"]
# Interpret the fitted doubling time and compare selected data points with the model.

# %% [markdown] tags=["reasoning:justify"]
# Decide whether the model should be called a prediction or a summary of the past, and defend your wording.

# %% [markdown] tags=["support:worked"]
# Worked rule: after n doublings, N = 2,300 × 2ⁿ.

# %% [markdown] tags=["support:guided"]
# Guidance: each new row is the previous row multiplied by 2; equal time intervals give equal factors.

# %% [markdown] tags=["support:partial"]
# Hint: use `2300 * 2**n`, then interpret n as elapsed time divided by doubling time.

# %% [markdown] tags=["support:independent"]
# State the model, interpret its parameters, and name one limitation of the selected data.

# %%
print("doubling table:", [2300 * 2**n for n in range(5)])
print(f"fitted historical doubling time ≈ {_doubling_time:.2f} years")
print("Caution: this hand-picked timeline summarizes history; it does not guarantee future growth.")

# %% [markdown]
# ## Exit ticket
# In one sentence, explain how you can recognize exponential rather than linear growth in a table.
