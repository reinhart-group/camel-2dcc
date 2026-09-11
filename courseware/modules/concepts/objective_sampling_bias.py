# ---
# module: objective_sampling_bias
# kind: concept
# accepts: [series, groups]
# dials:
#   reasoning: [notice, calculate, model, justify]
#   support: [worked, guided, partial, independent]
# minutes: 20
# ---
# %% [markdown]
# # Fair Samples
# **Goal:** tell apart chance changes in a random sample and bias from the way a sample was picked.

# %%
import matplotlib.pyplot as plt
import numpy as np
_rng = np.random.default_rng(11)
_sizes = [10, 50]
_sample_means = {n: np.array([_rng.choice(series_values, n, replace=False).mean() for _ in range(200)])
                 for n in _sizes if n <= len(series_values)}
for _n, _means in _sample_means.items():
    plt.hist(_means, bins=18, alpha=.55, label=f"n={_n}")
plt.axvline(np.mean(series_values), color="black", ls="--", label="population mean")
plt.xlabel(f"sample mean ({series_unit})"); plt.ylabel("repeated samples"); plt.legend(); plt.show()

# %% [markdown] tags=["reasoning:notice"]
# Which sample size produces the tighter cluster of sample means?

# %% [markdown] tags=["reasoning:calculate"]
# Compare the range of the repeated means for n=10 and n=50.

# %% [markdown] tags=["reasoning:model"]
# Explain why means from a larger sample tend to spread less. One large sample can still miss the true mean.

# %% [markdown] tags=["reasoning:justify"]
# Make a rule that samples from every image area. Explain why your rule is more fair.

# %% [markdown] tags=["support:worked"]
# Worked result: larger random samples tend to vary less. Each mean uses more values.

# %% [markdown] tags=["support:guided"]
# Guidance: compare the widths of the two graphs. Then tell chance apart from an unfair way to pick.

# %% [markdown] tags=["support:partial"]
# Hint: random does not mean perfect. It means the method does not favor one item.

# %% [markdown] tags=["support:independent"]
# Use the graph as proof. Then give a fair way to pick the sample.

# %%
for _n, _means in _sample_means.items():
    print(f"n={_n}: middle 90% of sample means = {np.percentile(_means,5):.1f} to {np.percentile(_means,95):.1f} {series_unit}")

# %% [markdown]
# ## Exit ticket
# A person always measures the easiest edge to reach. Is the main problem chance or bias?
