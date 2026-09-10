# ---
# module: concept_outlier_effect
# kind: concept
# accepts: [series]
# requires:
#   messiness: [real]
# dials:
#   guidance: [worked, fill, open]
#   register: [plain, explorer]
# minutes: 8
# ---
# %% [markdown] tags=["register:plain"]
# ## One speck of dust
# Real data can have one strange, extra-large number in it — like a speck of dust landing on
# a smooth surface. Watch what one huge number does to the mean and the median.

# %% [markdown] tags=["register:explorer"]
# ## Outliers: one value far from the rest
# An **outlier** is a value far from the rest of the data — often one stray reading, not a
# true property of what you're measuring. The mean is pulled toward extreme values; the
# median usually isn't.

# %%
import numpy as np
_dust_speck = series_values.max() * 5   # one very large extra value, added on purpose
_with_dust = np.append(series_values, _dust_speck)
print(f"before: mean = {series_values.mean():.2f}, median = {float(np.median(series_values)):.2f}")
print(f"one dust speck added: {_dust_speck:.2f} {series_unit}")

# %%
my_mean_after = ...    # a placeholder until you (or the code below) fill it in
my_median_after = ...  # a placeholder until you (or the code below) fill it in

# %% tags=["guidance:worked"]
my_mean_after = _with_dust.mean()               # mean of the values, including the dust speck
my_median_after = float(np.median(_with_dust))  # median of the values, including the dust speck

# %% tags=["guidance:fill"]
my_mean_after = ...  # ✏️ recompute the mean, including the dust speck
my_median_after = float(np.median(_with_dust))

# %% [markdown] tags=["guidance:open"]
# **Your task:** Predict which will move more, the mean or the median. Then compute both,
# including the dust speck, and store them as `my_mean_after` and `my_median_after`.

# %% tags=["guidance:open"]
# your code here

# %%
_ref_dust = series_values.max() * 5
_ref_with_dust = np.append(series_values, _ref_dust)
_ref_mean_after, _ref_median_after = float(_ref_with_dust.mean()), float(np.median(_ref_with_dust))
try:
    ok_mean = my_mean_after is not ... and abs(float(my_mean_after) - _ref_mean_after) <= 0.01 * abs(_ref_mean_after)
    ok_median = my_median_after is not ... and abs(float(my_median_after) - _ref_median_after) <= 0.01 * abs(_ref_median_after)
except (NameError, TypeError):
    ok_mean = ok_median = False
print("✅ Nice! Mean and median after the dust speck are right." if ok_mean and ok_median
      else "🔁 Not yet. Hint: include the dust speck value when you recompute the mean and median.")

# %%
import matplotlib.pyplot as plt
_show_mean_after = my_mean_after if my_mean_after is not ... else _ref_mean_after      # show the right answer until yours is filled in
_show_median_after = my_median_after if my_median_after is not ... else _ref_median_after
_labels = ["mean", "median"]
_before = [series_values.mean(), float(np.median(series_values))]
_after = [_show_mean_after, _show_median_after]
_x = np.arange(len(_labels))
fig, ax = plt.subplots()
ax.bar(_x - 0.2, _before, width=0.4, color="#0072B2", label="before the dust speck")
ax.bar(_x + 0.2, _after, width=0.4, color="#D55E00", label="after the dust speck")
ax.set(xticks=_x, xticklabels=_labels, ylabel=f"{series_label} ({series_unit})",
       title="One dust speck: mean vs. median")
ax.legend()
plt.tight_layout()
plt.show()
