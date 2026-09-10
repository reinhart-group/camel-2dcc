# ---
# module: concept_mean_median
# kind: concept
# accepts: [series]
# dials:
#   guidance: [worked, fill, open]
#   register: [plain, explorer]
# minutes: 10
# ---
# %% [markdown] tags=["register:plain"]
# ## Mean and median
# **Mean** is the fair-share number: add up all the values, then split them evenly.
# **Median** is the middle number once you sort the list from smallest to biggest.

# %% [markdown] tags=["register:explorer"]
# ## Mean and median
# The **mean** is the arithmetic average: add every value and divide by how many there are.
# The **median** is the middle value once the data is sorted (the average of the middle two,
# if there's an even number of values).

# %%
print(f"first 10 values ({series_label}, {series_unit}):")
print(series_values[:10])

# %%
import numpy as np
my_mean = ...     # a placeholder until you (or the code below) fill it in
my_median = ...   # a placeholder until you (or the code below) fill it in

# %% tags=["guidance:worked"]
my_mean = series_values.mean()        # add every value, divide by how many there are
my_median = np.median(series_values)  # sort the values, then take the middle one

# %% tags=["guidance:fill"]
import numpy as np
my_mean = ...  # ✏️ add up the numbers and divide by how many
my_median = np.median(series_values)

# %% [markdown] tags=["guidance:open"]
# **Your task:** Find the mean and median of the data; store them as `my_mean` and `my_median`.

# %% tags=["guidance:open"]
# your code here

# %%
import numpy as np
_ref_mean, _ref_median = float(np.mean(series_values)), float(np.median(series_values))
try:
    ok_mean = my_mean is not ... and abs(float(my_mean) - _ref_mean) <= 0.01 * abs(_ref_mean)
    ok_median = my_median is not ... and abs(float(my_median) - _ref_median) <= 0.01 * abs(_ref_median)
except (NameError, TypeError):
    ok_mean = ok_median = False
print("✅ Nice! Mean and median are right." if ok_mean and ok_median
      else f"🔁 Not yet. Hint: the mean adds all {len(series_values)} values and divides by {len(series_values)}.")

# %%
import matplotlib.pyplot as plt
_show_mean = my_mean if my_mean is not ... else _ref_mean        # show the right answer until yours is filled in
_show_median = my_median if my_median is not ... else _ref_median
fig, ax = plt.subplots()
ax.hist(series_values, bins=20, color="#0072B2", alpha=0.8, edgecolor="white")
ax.axvline(_show_mean, color="#D55E00", lw=2, ls="--", label=f"mean = {_show_mean:.2f}")
ax.axvline(_show_median, color="black", lw=2, ls=":", label=f"median = {_show_median:.2f}")
ax.set(xlabel=f"{series_label} ({series_unit})", ylabel="count", title=f"{series_label}: mean and median")
ax.legend()
plt.tight_layout()
plt.show()
