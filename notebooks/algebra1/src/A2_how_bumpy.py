# %% [markdown]
# # How Bumpy Is It? Mean, Median, and Samples
#
# Computer chips only work if the crystal layers inside them are very flat. To check, Penn
# State scientists scan a surface with a microscope and get thousands of height numbers back.
# One number can't tell the whole story — so they use statistics.
#
# Today's math: mean, median, range, and how to trust a sample instead of measuring
# everything.
#
# **What you'll do**
# - Find mean, median, and range of five heights by hand.
# - Compare a smooth surface and a bumpy one.
# - See how one outlier (a speck of dust) changes the mean but not the median.
# - Pull a random sample of triangles from a real crystal and compare it to the whole group.
#
# **Time:** about 30–40 minutes.

# %% [markdown]
# ## 🔧 Setup (run this first)
# Click the ▶ button on the cell below. It downloads the real data (about 20 MB) and takes
# 10–30 seconds.
#
# *Teachers:* if your school hosts its own copy of the data, paste its link into `DATA_URL`.
# No internet link? Upload `camel-2dcc-v1.zip` with the 📁 Files panel on the left, then run
# this cell.

# %%
DATA_URL = "https://pennstateoffice365-my.sharepoint.com/:u:/g/personal/wfr5091_psu_edu/IQCkNUoFnJNJSK8lUEepTJeSAT3NukSFJzB9-9fS5GB5mp0?e=KafIFG"  # teacher: the only line you may need to change

import io, json, os, shutil, sys, zipfile, requests
def _ready():  # a complete copy has its manifest and every file it lists
    try:
        m = json.load(open("camel-2dcc/manifest.json"))
        return m["release_id"] == "camel-2dcc-v1" and all(os.path.exists("camel-2dcc/" + f["path"]) for f in m["files"])
    except (OSError, ValueError, KeyError):
        return False
if not _ready():
    shutil.rmtree("camel-2dcc", ignore_errors=True)  # clear any half-finished copy
    if os.path.exists("camel-2dcc-v1.zip"):
        zip_bytes = open("camel-2dcc-v1.zip", "rb").read()
    else:
        r = requests.get(DATA_URL + ("&" if "?" in DATA_URL else "?") + "download=1", timeout=120)
        r.raise_for_status()
        zip_bytes = r.content
    if zip_bytes[:2] != b"PK":
        raise RuntimeError("The download was not the data file. Check DATA_URL, or upload camel-2dcc-v1.zip "
                           "with the Files panel and run this cell again.")
    zipfile.ZipFile(io.BytesIO(zip_bytes)).extractall(".")
    if not _ready():
        raise RuntimeError("The data file is incomplete or the wrong version. Download camel-2dcc-v1.zip again.")
sys.path.insert(0, "camel-2dcc")
import importlib, camel_data.classroom  # reload so an updated data file never runs old helper code
importlib.reload(camel_data.classroom)
try:
    from google.colab import output
    output.enable_custom_widget_manager()
except ImportError:
    pass  # running outside Colab
from camel_data.classroom import *
print("✅ Data ready:", sorted(os.listdir("camel-2dcc"))[:6], "...")

# %% [markdown]
# ## Task 1 — Five heights, by hand
# Here are five height measurements from a crystal surface, in nanometres:
# **8, 10, 12, 9, 11**
#
# - **Mean:** add them up, divide by how many there are.
# - **Median:** sort them, pick the middle one.
# - **Range:** biggest minus smallest.

# %%
heights = [8, 10, 12, 9, 11]
my_mean = ...    # ✏️ type your answer here: the mean of heights
my_median = ...  # ✏️ type your answer here: the median of heights
my_range = ...   # ✏️ type your answer here: the range of heights

# %%
# @title Helper code (just run this)
import numpy as np
real_mean, real_median, real_range = np.mean(heights), np.median(heights), max(heights) - min(heights)
ok = [my_mean == real_mean, my_median == real_median, my_range == real_range]
if all(ok):
    print(f"✅ Nice! mean = {real_mean:g}, median = {real_median:g}, range = {real_range:g}.")
else:
    labels = ["mean", "median", "range"]
    wrong = [labels[i] for i, good in enumerate(ok) if not good]
    print(f"🔁 Check your {', '.join(wrong)}. (mean = {real_mean:g}, median = {real_median:g}, "
          f"range = {real_range:g})")

# %% [markdown]
# ## Task 2 — Two real surfaces: which is bumpier?
# `smoothest_surface` grew almost perfectly flat. `gallium_selenide_bumps` grew covered in
# little mounds. Look at both pictures, then their histograms (a bar chart of how many pixels
# had each height).

# %%
# @title Helper code (just run this) — picture + histogram, side by side
import matplotlib.pyplot as plt

def show_surface_and_histogram(scan):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5))
    size_nm = scan.scan_um * 1000
    lo, hi = np.percentile(scan.z, [1, 99])
    im = ax1.imshow(scan.z, cmap="viridis", vmin=lo, vmax=hi, extent=[0, size_nm, size_nm, 0])
    ax1.set(title=scan.title, xlabel="x (nm)", ylabel="y (nm)")
    plt.colorbar(im, ax=ax1, label="height (nm)")

    z = scan.z.ravel()
    mean, median = z.mean(), float(np.median(z))
    ax2.hist(z, bins=50, color="#0072B2", alpha=0.85)
    ax2.axvline(mean, color="#D55E00", lw=2, ls="--", label=f"mean = {mean:.2f} nm")
    ax2.axvline(median, color="black", lw=2, ls=":", label=f"median = {median:.2f} nm")
    ax2.set(title="Height histogram", xlabel="height (nm)", ylabel="pixel count")
    ax2.legend()
    plt.tight_layout()
    plt.show()
    print(f"Height range: {z.min():.1f} to {z.max():.1f} nm")

# %%
gallery = load_gallery()
show_surface_and_histogram(gallery["smoothest_surface"])

# %%
show_surface_and_histogram(gallery["gallium_selenide_bumps"])

# %% [markdown]
# **Your answer:** Which surface's histogram is wider — meaning its heights are more spread
# out? Which surface is bumpier: `smoothest_surface` or `gallium_selenide_bumps`?
#
# _(write here)_

# %% [markdown]
# ## Task 3 — One speck of dust
# A speck of dust lands on the surface while it's being scanned. It's just one pixel, but
# it's very tall. Watch what it does to your Task 1 numbers.

# %%
heights_with_dust = heights + [90]   # one dust speck: a single very tall reading, in nm
mean_with_dust = ...    # ✏️ type your answer here: the mean of heights_with_dust
median_with_dust = ...  # ✏️ type your answer here: the median of heights_with_dust

# %%
# @title Helper code (just run this)
real_mean2 = np.mean(heights_with_dust)
real_median2 = np.median(heights_with_dust)
ok2 = [mean_with_dust == real_mean2, median_with_dust == real_median2]
if all(ok2):
    print(f"✅ Nice! mean = {real_mean2:g} nm (was {real_mean:g}), "
          f"median = {real_median2:g} nm (was {real_median:g}).")
    print("One tall number dragged the mean way up — the median barely moved.")
else:
    print(f"🔁 Try again. mean should be {real_mean2:g}, median should be {real_median2:g}.")

# %% [markdown]
# **Your answer:** By how much did the mean change? By how much did the median change? Why
# does one tall number move the mean more than the median?
#
# _(write here)_

# %% [markdown]
# ## Task 4 — Sampling real triangles
# `wse2_17458_center` is a real scan of a wafer covered in tiny triangle-shaped crystals. The
# green outlines below are triangles the computer found and measured.

# %%
scans, table = load_grain_scans()
scan = scans["wse2_17458_center"]

fig, ax = plt.subplots(figsize=(6, 6))
show_grains(scan, table, ax=ax, kinds=("single",))
ax.plot([], [], color="#2ca02c", lw=3, label="green = one triangle")
ax.legend(loc="upper right")
plt.show()

# %% [markdown]
# Across the whole wafer (three scanned spots), there are **501** whole, clean triangles —
# that's our whole group. Each one has an area, in nm². Below is the whole group's mean area.

# %%
population = whole_single(table)
population = population[population["scan"].isin(["wse2_17458_center", "wse2_17458_flat", "wse2_17458_edge"])]
whole_group = population["area_nm2"].to_numpy()
group_mean = whole_group.mean()
print(f"Whole group: {len(whole_group)} triangles, mean area = {group_mean:.0f} nm²")

# %% [markdown]
# Now pull a **random sample** of just 10 triangles — like drawing 10 names out of a hat —
# and compare its mean to the whole group's mean.

# %%
seed = 1   # <-- change me: try a few different whole numbers
my_sample = random_sample(whole_group, 10, seed=seed)
sample_mean = my_sample.mean()
print(f"My sample (n=10): mean area = {sample_mean:.0f} nm²")
print(f"Whole group:       mean area = {group_mean:.0f} nm²")
print(f"Difference: {sample_mean - group_mean:+.0f} nm²")

# %% [markdown]
# **Your answer:** Try at least 3 different seed numbers. Does the sample mean land exactly
# on the whole group's mean? Does it get closer if you imagine using more than 10 triangles?
#
# _(write here)_

# %% [markdown]
# ## Task 5 — Is the lazy scientist being fair?
# Imagine a scientist who is always in a hurry and only ever scans **near the edge** of the
# wafer, because it's the closest spot to reach.

# %%
edge_group = population.loc[population["scan"] == "wse2_17458_edge", "area_nm2"]
edge_mean = edge_group.mean()
percent_off = 100 * (edge_mean - group_mean) / group_mean
print(f"'Near the edge' only: mean area = {edge_mean:.0f} nm²")
print(f"Whole group:          mean area = {group_mean:.0f} nm²")
print(f"That's {percent_off:+.0f}% off the whole group's true mean.")

# %% [markdown]
# **Your answer:** Compare this to Task 4. A random sample of 10 landed a little above or
# below the whole group's mean by chance — but the "near the edge" number is off by the same
# amount *every single time*. Is always scanning near the edge a fair way to describe the
# whole wafer? Why or why not?
#
# _(write here)_

# %% [markdown]
# ## Exit ticket
# Answer these without running any code.
#
# 1. A list of heights is 4, 5, 5, 6, 30. Is the mean bigger or smaller than the median? Why?
# 2. A scientist wants to know the typical triangle size on a wafer, but only has time to
#    measure 10 triangles. What should they do to pick a fair sample of 10?
# 3. Two surfaces have the exact same median height. Does that mean they look the same?
#    What else would you want to know before deciding?

# %% [markdown]
# **Nice work!** You used mean, median, and range to describe bumpy surfaces, and you saw why
# scientists trust a random sample more than a convenient one.
