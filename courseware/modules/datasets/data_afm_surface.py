# ---
# module: data_afm_surface
# kind: dataset
# produces: [map]
# dials:
#   realism: [clean, curated, annotated, research]
# minutes: 4
# ---
# %% [markdown]
# ## The data: one surface measured atom by atom
# An atomic force microscope traces a tiny tip across a surface. The result is a grid of height
# measurements. The colors and 3D shape below come from those measurements, not an artist's model.

# %%
import numpy as np

# %% tags=["realism:clean"]
_scan = load_gallery()["triangle_pyramids"]
_lo, _hi = np.percentile(_scan.z, [2, 98])
map_values = np.clip(_scan.z, _lo, _hi)

# %% tags=["realism:curated"]
_scan = load_gallery()["triangle_pyramids"]
map_values = _scan.z.copy()

# %% tags=["realism:annotated"]
_scan = load_gallery()["triangle_pyramids"]
map_values = _scan.z.copy()
print("Annotation: unusually high and low pixels remain visible; check them before interpreting a step.")

# %% tags=["realism:research"]
_scan = load_gallery()["triangle_pyramids"]
map_values = _scan.z.copy()
print("Research view: full-resolution values with no clipping or smoothing.")

# %%
map_width_nm = float(_scan.scan_um * 1000)
map_label, map_unit = "crystal surface height", "nm"
print(f"Loaded a {map_values.shape[0]} × {map_values.shape[1]} height map covering "
      f"{map_width_nm:g} nm × {map_width_nm:g} nm.")
