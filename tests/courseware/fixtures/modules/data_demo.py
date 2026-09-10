# ---
# module: data_demo
# kind: dataset
# produces: [series]
# dials:
#   messiness: [real, flagged]
# params:
#   sample_size: {default: 5, min: 3, max: 10}
# minutes: 2
# ---
# %%
import numpy as np
series_values = np.arange(1.0, PARAMS["sample_size"] + 1)
series_label, series_unit = "demo value", "nm"
