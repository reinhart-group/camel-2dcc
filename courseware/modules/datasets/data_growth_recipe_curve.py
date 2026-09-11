# ---
# module: data_growth_recipe_curve
# kind: dataset
# produces: [curve]
# dials:
#   realism: [clean, curated, annotated, research]
# minutes: 4
# ---
# %% [markdown]
# ## The data: time and temperature from a real growth recipe
# A growth recipe is a timed list of furnace settings. We only need to know that the machine heats,
# holds, and cools; learning how the material grows is not part of this math lesson.

# %%
import numpy as np
_recipe = (load_table("growth_recipes")
           .query("sample_id == 23451 and recipe_number == 1")
           .sort_values("step_number").reset_index(drop=True))

# %% tags=["realism:clean"]
curve_x = np.array([0.0, 17.0, 40.0])
curve_y = np.array([25.0, 1000.0, 1000.0])

# %% tags=["realism:curated"]
curve_x = np.r_[0.0, (_recipe["start_min"] + _recipe["duration_min"]).iloc[:5].to_numpy(float)]
curve_y = np.r_[25.0, _recipe["temperature_C"].iloc[:5].to_numpy(float)]

# %% tags=["realism:annotated"]
curve_x = np.r_[0.0, (_recipe["start_min"] + _recipe["duration_min"]).iloc[:5].to_numpy(float)]
curve_y = np.r_[25.0, _recipe["temperature_C"].iloc[:5].to_numpy(float)]
print("The 25 °C starting point is a classroom assumption; the recipe did not record it.")

# %% tags=["realism:research"]
curve_x = np.r_[0.0, (_recipe["start_min"] + _recipe["duration_min"]).iloc[:5].to_numpy(float)]
curve_y = np.r_[25.0, _recipe["temperature_C"].iloc[:5].to_numpy(float)]
print(_recipe[["step", "duration_min", "start_min", "temperature_C"]])
print("The cooldown temperatures are missing, so they are not invented as zeros.")

# %%
curve_x_label, curve_y_label = "elapsed time (min)", "furnace setting (°C)"
