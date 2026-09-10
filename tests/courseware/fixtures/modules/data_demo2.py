# ---
# module: data_demo2
# kind: dataset
# produces: [groups]
# dials:
#   messiness: [real, flagged]
# params:
#   sample_size: {default: 100, min: 50, max: 200}
# minutes: 2
# ---
# %%
import numpy as np
groups_values = np.arange(1.0, PARAMS["sample_size"] + 1)
groups_label, groups_unit = "demo groups", "nm"
