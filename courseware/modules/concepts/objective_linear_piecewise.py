# ---
# module: objective_linear_piecewise
# kind: concept
# accepts: [curve]
# dials:
#   reasoning: [notice, calculate, model, justify]
#   support: [worked, guided, partial, independent]
# minutes: 20
# ---
# %% [markdown]
# # A Recipe as a Piecewise Graph
# **Learning objective:** interpret slope and write a linear rule for one interval of a piecewise graph.

# %%
import matplotlib.pyplot as plt
plt.figure(figsize=(8,4)); plt.plot(curve_x, curve_y, marker="o", color="#0072B2")
plt.xlabel(curve_x_label); plt.ylabel(curve_y_label); plt.grid(alpha=.3); plt.show()
_slope = (curve_y[1] - curve_y[0]) / (curve_x[1] - curve_x[0])

# %% [markdown] tags=["reasoning:notice"]
# Identify an interval where the graph rises and an interval where it stays constant.

# %% [markdown] tags=["reasoning:calculate"]
# Calculate the slope of the first interval, including units.

# %% [markdown] tags=["reasoning:model"]
# Write a linear rule for the first interval and use it to estimate when the setting reaches 500 °C.

# %% [markdown] tags=["reasoning:justify"]
# Explain why one linear rule cannot honestly describe the entire recipe.

# %% [markdown] tags=["support:worked"]
# Worked form: slope = change in temperature ÷ change in time; T(t) = 25 + slope × t.

# %% [markdown] tags=["support:guided"]
# Guidance: use the endpoints (0, 25) and (17, 1000), then substitute 500 for T.

# %% [markdown] tags=["support:partial"]
# Hint: start with `m = (y2-y1)/(x2-x1)` and `y = y1 + m(x-x1)`.

# %% [markdown] tags=["support:independent"]
# State the interval and the assumed starting temperature with your model.

# %%
_time_at_500 = (500.0 - curve_y[0]) / _slope + curve_x[0]
print(f"first-interval slope = {_slope:.2f} °C/min")
print(f"model: T(t) = {curve_y[0]:g} + {_slope:.2f}t, for 0 ≤ t ≤ {curve_x[1]:g}")
print(f"the model reaches 500 °C at t = {_time_at_500:.2f} min")

# %% [markdown]
# ## Exit ticket
# What does a horizontal section of a temperature-versus-time graph say about its slope?
