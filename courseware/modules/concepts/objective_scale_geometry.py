# ---
# module: objective_scale_geometry
# kind: concept
# accepts: [map]
# dials:
#   reasoning: [notice, calculate, model, justify]
#   support: [worked, guided, partial, independent]
# minutes: 24
# ---
# %% [markdown]
# # Scale a Microscopic Surface
# **Learning objective:** use units, scale factors, and geometric measurements to connect a tiny
# height map to a visible model.

# %%
import numpy as np
import plotly.graph_objects as go
_step = max(1, int(np.ceil(map_values.shape[0] / 180)))
_z = map_values[::_step, ::_step]
_axis = np.linspace(0, map_width_nm, _z.shape[0])
go.Figure(go.Surface(x=_axis, y=_axis, z=_z, colorscale="Viridis")).update_layout(
    title="Measured surface", scene=dict(xaxis_title="x (nm)", yaxis_title="y (nm)", zaxis_title="height (nm)"),
    height=520).show()

# %% [markdown] tags=["reasoning:notice"]
# Read the axes. Which dimensions cover the greatest distance: width, depth, or height?

# %% [markdown] tags=["reasoning:calculate"]
# Scale this surface to an 80 mm model. Calculate the horizontal scale factor and the model height
# that would preserve the real aspect ratio.

# %% [markdown] tags=["reasoning:model"]
# Compare a true-scale model with a model using 10 mm of relief. Quantify the vertical exaggeration.

# %% [markdown] tags=["reasoning:justify"]
# Choose a printable vertical exaggeration and defend the tradeoff between visibility and fidelity.

# %% [markdown] tags=["support:worked"]
# Worked setup: convert nanometres to millimetres first, then divide model size by real size.

# %% [markdown] tags=["support:guided"]
# Guidance: `scale factor = model width ÷ real width`. Use the same units before dividing.

# %% [markdown] tags=["support:partial"]
# Hint: 1 nm = 0.000001 mm. Compare horizontal and vertical scale factors separately.

# %% [markdown] tags=["support:independent"]
# Record both scale factors, their units, and what a viewer could misinterpret.

# %%
_width_mm, _relief_mm = 80.0, 10.0
_horizontal_scale = _width_mm / (map_width_nm * 1e-6)
_height_nm = float(np.percentile(map_values, 99.5) - np.percentile(map_values, 0.5))
_true_height_mm = _height_nm * 1e-6 * _horizontal_scale
print(f"horizontal scale factor = {_horizontal_scale:,.0f}×")
print(f"true-scale height range = {_true_height_mm:.4f} mm; chosen printable relief = {_relief_mm:g} mm")
print(f"extra vertical exaggeration = {_relief_mm/_true_height_mm:,.0f}×")

# %%
from camel_data.classroom import AFMScan, to_stl
_export_scan = AFMScan("lesson_surface", map_values, map_width_nm / 1000, "", map_label, "", 0)
to_stl(_export_scan, "afm_surface_demo.stl", width_mm=_width_mm, relief_mm=_relief_mm)
print("Created afm_surface_demo.stl")

# %% [markdown]
# ## Exit ticket
# Why can a 3D print be mathematically accurate data but still have a deliberately exaggerated shape?
