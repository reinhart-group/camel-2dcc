# ---
# module: objective_compare_groups
# kind: concept
# accepts: [groups]
# dials:
#   reasoning: [notice, calculate, model, justify]
#   support: [worked, guided, partial, independent]
# minutes: 22
# ---
# %% [markdown]
# # Compare Two Groups With Uncertainty
# **Learning objective:** compare groups using graphs, a difference in means, and a randomization test.
# The test asks whether a difference this large would be unusual if group labels did not matter.

# %%
import matplotlib.pyplot as plt
import numpy as np
_counts = groups_table["group"].value_counts()
_names = list(_counts.index[:2])
_a = groups_table.loc[groups_table["group"] == _names[0], "value"].to_numpy(float)
_b = groups_table.loc[groups_table["group"] == _names[1], "value"].to_numpy(float)
_observed = float(_a.mean() - _b.mean())
plt.figure(figsize=(7,4)); plt.boxplot([_a, _b], tick_labels=_names, showfliers=True)
plt.ylabel(f"{groups_label} ({groups_unit})"); plt.show()

# %% [markdown] tags=["reasoning:notice"]
# Compare the centers, spreads, overlap, and unusual values in the two box plots.

# %% [markdown] tags=["reasoning:calculate"]
# Calculate each group mean and their difference. Keep the sign and unit.

# %% [markdown] tags=["reasoning:model"]
# Use shuffled labels to estimate how often chance alone produces a difference at least this large.

# %% [markdown] tags=["reasoning:justify"]
# Decide what the evidence supports, while avoiding a claim that group membership caused the difference.

# %% [markdown] tags=["support:worked"]
# Worked interpretation: shuffle only the labels, recompute the difference, and compare its absolute size.

# %% [markdown] tags=["support:guided"]
# Guidance: first describe the graph, then compare the observed difference with shuffled differences.

# %% [markdown] tags=["support:partial"]
# Hint: a small randomization proportion means the observed separation is unusual under shuffled labels.

# %% [markdown] tags=["support:independent"]
# Report group sizes, centers, uncertainty evidence, and one plausible confounding variable.

# %%
_rng = np.random.default_rng(7)
_pool = np.r_[_a, _b]
_shuffled = []
for _ in range(2000):
    _p = _rng.permutation(_pool)
    _shuffled.append(_p[:len(_a)].mean() - _p[len(_a):].mean())
_p_random = (np.count_nonzero(np.abs(_shuffled) >= abs(_observed)) + 1) / 2001
print(f"{_names[0]}: n={len(_a)}, mean={_a.mean():.2f} {groups_unit}")
print(f"{_names[1]}: n={len(_b)}, mean={_b.mean():.2f} {groups_unit}")
print(f"observed difference = {_observed:.2f} {groups_unit}; randomization proportion = {_p_random:.3f}")
print("This is an observational comparison, so it does not establish cause and effect.")

# %% [markdown]
# ## Exit ticket
# Why is “the groups differ in these observations” safer than “the group label caused the difference”?
