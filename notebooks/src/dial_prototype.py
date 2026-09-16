# %% [markdown]
# [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/reinhart-group/camel-2dcc/blob/dial-prototype/notebooks/dial_prototype.ipynb)

# %% [markdown]
# # Complexity dials, running in the page
#
# One real dataset from Penn State's 2D Crystal Consortium: 1,005 crystal samples, the settings
# each one was grown with, and how rough the finished film measured.
#
# The three dials below are the CAMEL complexity dials. They change **what you see first**, never
# the underlying records. Turn them and watch the row count, the missing values, and the graph
# change.
#
# This cell's output is saved in the notebook, so it works on a phone with no account and nothing
# running. Sign in and run the cells to see the Python that built it.

# %%
# @title Turn the dials { display-mode: "form" }
# (Run this cell only if you want to rebuild the widget. The saved version below already works.)
import json
import pathlib
import sys
import uuid

from IPython.display import HTML, display

ROOT = pathlib.Path.cwd()
if not (ROOT / "courseware").exists() and (ROOT.parent / "courseware").exists():
    ROOT = ROOT.parent
sys.path.insert(0, str(ROOT / "scripts"))

from build_dial_payload import build  # noqa: E402

rows = build()
payload = json.dumps(rows, separators=(",", ":"))
widget_id = "dials-" + uuid.uuid4().hex[:8]

js = (ROOT / "courseware/widgets/dials.js").read_text()
js = js.replace("__DATA__", payload).replace("__ID__", widget_id)
html = (ROOT / "courseware/widgets/dials.html").read_text()
html = html.replace("__ID__", widget_id).replace("__JS__", js)

print(f"{len(rows)} samples, {len(payload) / 1024:.0f} KB carried inside the page")
display(HTML(html))

# %% [markdown]
# ## What each dial does to this dataset
#
# **Provenance, resolved to surfaced.** Resolved removes the rows whose material field holds a
# substrate name, merges spellings such as `MoS2; MoS2` into `MoS2`, and drops samples missing the
# numbers the question needs. Surfaced puts all of that back: 228 samples never had a growth time
# recorded and 106 were never measured.
#
# **Statistical, implicit to explicit.** Implicit keeps only the common 5 micrometre scan size and
# roughness under 10 nanometres, so the spread looks tame. Explicit keeps everything, including a
# sample that measured 92 nanometres and scans taken at other sizes, which are not fair to compare.
#
# **Structural, few to all.** Two columns, six, or all sixteen, including administrative fields
# that have nothing to do with the question.
#
# Note the line above the graph: it always says how many samples the graph could actually draw.
# With provenance surfaced, the table holds 1,005 rows but the graph draws 754, because the rest
# are missing one of the two values.

# %% [markdown]
# ## For a teacher
#
# A dial setting is a decision about what students meet first, not a change to the data. A picture
# graph class and a statistics class can work from the same records. The settings you would hand
# out differ; the crystals do not.
