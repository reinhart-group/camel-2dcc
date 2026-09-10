# %% [markdown]
# # Nano Landscapes: Fly Over Crystal Surfaces Atom-Step by Atom-Step
#
# A microscope probe traces the surface of a real crystal, one scan line at a time — and you get
# to fly over the 3D result, take height profiles, and hunt for a glitch in the data.
#
# **What you'll do**
# - Rotate a real 3D height map of a crystal surface and control how tall it looks
# - Slide a line across the map and read off the height of a real atomic step
# - Turn a histogram of heights into a mean, a median, and a "which one lies?" argument
#
# **Time:** about 45–50 minutes
#
# **Materials science words**
#
# | Word | Means |
# |---|---|
# | AFM (atomic force microscope) | An instrument that scans a very sharp probe, mounted on a flexible cantilever, across a surface and uses a feedback signal to record its height at every point |
# | cantilever | The tiny flexible arm that holds the AFM's probe and bends as the probe senses the surface |
# | nanometre (nm) | One billionth of a metre (0.000000001 m) — atoms are about 0.2–0.4 nm across |
# | micrometre (µm) | One millionth of a metre = 1,000 nm |
# | terrace | A relatively flat region on a crystal surface, bounded by step edges — like the flat part of a stair step |
# | vertical exaggeration | Stretching the height axis of a 3D plot so tiny real bumps are visible |
# | RMS roughness | A single number for "how bumpy," built from the heights (more in Notebook 2) |
# | mean | The numbers added up, divided by how many there are — pulled around by extreme values |
# | median | The middle value when everything is sorted — mostly ignores extreme values |
# | scan-line artifact | A glitch from the instrument itself, not a real feature of the crystal |

# %% [markdown]
# ## 🔧 Setup (run this first)
# Click the ▶ button on the cell below. It downloads the real data (about 20 MB) and takes 10–30 seconds.
#
# *Teachers:* if your school hosts its own copy of the data, paste its link into `DATA_URL`.
# No internet link? Upload `camel-2dcc-v1.zip` with the 📁 Files panel on the left, then run this cell.

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
try:
    from google.colab import output
    output.enable_custom_widget_manager()
except ImportError:
    pass  # running outside Colab
from camel_data.classroom import *
print("✅ Data ready:", sorted(os.listdir("camel-2dcc"))[:6], "...")

# %% [markdown]
# ## How an AFM "feels" its way across a crystal
#
# An **atomic force microscope (AFM)** raster-scans a very sharp probe, mounted on a flexible
# **cantilever**, back and forth across a surface — one line at a time, the way you might feel your
# way across a textured wall with a fingertip. A feedback loop constantly adjusts the probe (or, in
# some modes, watches how the cantilever vibrates) to keep the tip–surface interaction steady, and a
# computer records how far up or down the probe moved at every point. That grid of heights is the
# whole dataset — no lens, no light, just a feedback signal.
#
# Depending on the AFM's **mode**, the probe may stay in light contact with the surface, tap it many
# times a second, or hover just above it without touching at all. Its very tip is only a few to a few
# tens of nanometres across — not literally one atom — but under the right conditions that tip apex
# is still sharp enough to pick up atom-scale height steps, which is exactly what you'll measure in
# Task 2.
#
# Heights are recorded in **nanometres (nm)**. One nanometre is one *billionth* of a metre. A human
# hair is about 80,000 nm wide — so the bumps you're about to fly over are a few hundred times
# thinner than a hair.
#
# The gallery below has 12 real AFM scans from Penn State's 2D Crystal Consortium. Some show a bulk
# crystal's surface stepping up one unit cell at a time (like the staircase you'll explore first);
# others show thin films or true 2D materials growing on top of a substrate. Careful: "two-dimensional
# material" describes how the crystal bonds, not how many atoms tall it is — a single layer can still
# be several atomic planes thick.

# %%
gallery = load_gallery()
for key, scan in gallery.items():
    print(f"{key:22s} {scan.material:8s} {scan.scan_um:g} µm scan")

# %% [markdown]
# ## Fly over a real surface
#
# Pick a sample from the dropdown, then drag the **Stretch** slider. Try the **Colors** dropdown
# too — Viridis and Cividis are designed to stay readable for the most common color-vision
# differences.

# %%
explore_3d(gallery)

# %% [markdown]
# **No widgets? Here's a static view of one scan** (this always works, even without
# interactive controls):

# %%
surface_3d(gallery["atomic_staircase"], exaggeration=50).show()

# %% [markdown]
# ### 🔬 Scientist's note: that "mountain range" isn't real height
#
# Look at the numbers: the crystal above is 1 µm (1,000 nm) wide, but its actual bumps
# are only a few **nm** tall. Plotted at true scale it would look perfectly flat — so
# every 3D plot in this notebook stretches the height axis by a **vertical exaggeration**
# factor, shown right in the plot title (`heights ×50`, for example). A real AFM chip is
# nowhere near that lumpy. This is the single most common way 3D nanoscale plots mislead
# people — always check the exaggeration factor before you believe your eyes.

# %%
import numpy as np

scan = gallery["atomic_staircase"]
full_relief_nm = float(scan.z.max() - scan.z.min())
p1_nm, p99_nm = np.percentile(scan.z, [1, 99])
typical_relief_nm = float(p99_nm - p1_nm)
width_nm = scan.scan_um * 1000
print(f"Full range (every pixel, peak to valley): about {full_relief_nm:.1f} nm.")
print(f"Typical range (middle 98% of pixels, ignoring rare spikes): about {typical_relief_nm:.1f} nm.")
print(f"Scan width: {width_nm:.0f} nm.")
print(f"Relief-to-width ratio: 1 part in {width_nm / full_relief_nm:.0f} using the full range, "
      f"or 1 part in {width_nm / typical_relief_nm:.0f} using the typical range.")

# %% [markdown]
# ### Task 1 (Explore)
# Set the sample to **Atomic staircase** and try a few different **Stretch** values.
#
# 1. What stretch value makes the terraces (the stair steps) clearly visible without
#    turning them into sharp, unrealistic spikes?
# 2. What happens at a stretch of 1? Why does that match the tiny relief-to-width ratio you just
#    printed (only 1 part in a few hundred)?
#
# **Your answer:**
# _(write here)_

# %% [markdown]
# ## Take a line profile
#
# A **cross-section** is what you'd see if you sliced straight down through the crystal
# along one line and looked at the edge. Drag the red line and watch the height profile
# on the right update.

# %%
explore_cross_section(gallery["atomic_staircase"])

# %% [markdown]
# **No widgets? Here's a static cross-section of the same scan** (this always works, even without
# interactive controls) — it cuts along one row of the staircase:

# %%
import matplotlib.pyplot as plt

_demo_row = 32
_d, _h = cross_section(gallery["atomic_staircase"], _demo_row)
fig, ax = plt.subplots(figsize=(8, 3.5))
ax.plot(_d, _h, color="#4C72B0", lw=1)
ax.set(title=f"atomic_staircase — row {_demo_row} cross-section",
       xlabel="distance (nm)", ylabel="height (nm)")
ax.grid(alpha=0.3)
plt.show()

# %% [markdown]
# ### Task 2 (Core) — estimate a step height
# Move the line slider (or use the static plot above) until the profile shows a clear
# "staircase" step — a flat bit, a jump, then another flat bit. Read the jump in **nm** off the
# y-axis and enter your estimate below.
#
# SrTiO3 (the material in this scan) stacks in layers 0.39 nm tall — that's the accepted
# textbook step height. Real AFM data is noisy, so don't expect to match it exactly, and
# occasionally two step edges sit right on top of each other ("step bunching"), making a step
# look almost double that.

# %%
my_step_estimate_nm = 0.3  # <-- change me: your estimate from the profile, in nm

# %% [markdown]
# **✅ Check yourself (run the cell below — no need to change it)**

# %%
# @title Helper code (just run this) — measures the step from curated terrace regions
import numpy as np

staircase = gallery["atomic_staircase"]

# Chosen by inspecting the map: rows 30-34 all cross the same clean, sharp step edge, with a
# flat terrace on each side well clear of the jump itself.
curated_rows = [30, 31, 32, 33, 34]
before_nm = (460, 538)   # flat terrace just above the step
after_nm = (553, 630)    # flat terrace just below the step

def _plateau_median(row, nm_lo, nm_hi):
    px_lo = int(round(nm_lo / staircase.pixel_nm))
    px_hi = int(round(nm_hi / staircase.pixel_nm))
    return float(np.median(staircase.z[row, px_lo:px_hi]))

row_steps = []
print(f"Rows {curated_rows[0]}-{curated_rows[-1]}, terrace medians at x = {before_nm} nm vs {after_nm} nm:")
for row in curated_rows:
    before_h = _plateau_median(row, *before_nm)
    after_h = _plateau_median(row, *after_nm)
    row_steps.append(before_h - after_h)
    print(f"  row {row}: {before_h:.2f} nm -> {after_h:.2f} nm, step = {before_h - after_h:.2f} nm")

step_mean = float(np.mean(row_steps))
step_lo, step_hi = min(row_steps), max(row_steps)
print(f"\nMeasured step height ≈ {step_mean:.2f} nm (row-to-row range {step_lo:.2f}-{step_hi:.2f} nm).")
print("Textbook SrTiO3 unit cell: 0.39 nm — steps can look doubled if two edges bunch together.")

if step_lo - 0.05 <= my_step_estimate_nm <= step_hi + 0.05:
    print("\n🎯 Right in the range our curated rows measured — nice reading!")
elif 0.2 <= my_step_estimate_nm <= 0.6:
    print("\n👍 Reasonable — a plausible single-step reading; real AFM data is noisy row to row.")
elif 0.6 < my_step_estimate_nm <= 1.0:
    print("\n🤔 That's close to double the measured step — you may have read across two step edges "
          "bunched together (it happens on real crystals).")
else:
    print("\n🔁 Try again: find a clean flat-jump-flat pattern on the profile (or the static plot "
          "above) and re-read the y-axis in nm.")

# %% [markdown]
# ## From micrometres to nanometres
#
# Every scan above is labelled in **micrometres (µm)**, but heights are in **nanometres
# (nm)**. 1 µm = 1,000 nm — so converting is always "multiply by 1,000."

# %%
scan_key = "tin_selenide_grains"  # <-- change me: try any key printed in the gallery list above
scan_um = gallery[scan_key].scan_um
scan_nm = scan_um * 1000  # <-- change me: is this the right conversion?
print(f"{scan_key}: {scan_um:g} µm = {scan_nm:g} nm wide")

# %% [markdown]
# ### Task 3 (Core) — how many scans fit across a hair?
# A human hair is about 80,000 nm wide. Using the scan width you just converted, how many
# copies of that scan, laid edge to edge, would it take to span one hair's width?

# %%
hair_nm = 80000
scans_per_hair = hair_nm / scan_nm  # <-- change me: write the formula
print(f"About {scans_per_hair:.1f} copies of the {scan_key} scan span one hair's width.")

# %%
# @title Helper code (just run this) — checks your conversion and your formula separately
expected_scan_nm = scan_um * 1000  # computed straight from scan_um, not from your scan_nm
if abs(scan_nm - expected_scan_nm) > 0.5:
    print(f"🔁 Check your µm→nm conversion first: {scan_um:g} µm should be {expected_scan_nm:.0f} nm, "
          f"not the {scan_nm:.0f} nm you have.")
else:
    expected_ratio = hair_nm / scan_nm
    if abs(scans_per_hair - expected_ratio) > 0.05:
        print(f"🔁 The conversion looks right, but the formula doesn't — hair_nm / scan_nm gives "
              f"{expected_ratio:.1f}. Check your formula above.")
    else:
        print(f"✅ Correct: {expected_ratio:.1f} scans span one hair's width.")

# %% [markdown]
# ## Reading the heights: histogram, mean, and median
#
# Every pixel in a scan has a height. Plot all of them as a histogram and you get the
# **distribution** of heights across the whole crystal.
#
# ### 🔬 Scientist's note: why is the median so often exactly 0.00 nm?
# Every scan here went through the same two-step correction before you ever saw it: first a
# straight line was fit and subtracted from **each scan row** (removing tilt/drift so a tilted
# microscope doesn't get mistaken for a tilted crystal), then **one global median** — computed
# across the whole corrected map — was subtracted so the processed map's overall median lands at
# exactly 0.00 nm. That's a deliberate instrument-correction step, not a coincidence — you can see
# the exact recipe recorded for every scan below. Keep in mind that leveling can also shrink real
# broad features that fill most of a line, so treat "median = 0" as a processing choice, not proof
# that "nothing is happening" — that's why you compare **mean vs. median**, not just read either
# number alone.

# %%
# The exact processing recipe is recorded for every gallery scan — no need to guess at it.
gallery_meta = json.loads(open("camel-2dcc/afm_gallery/gallery.json").read())
_demo_key = "gallium_selenide_bumps"
_processing = next(m["processing"] for m in gallery_meta if m["key"] == _demo_key)
print(f"{_demo_key} processing: {_processing}")

# %%
# @title Helper code (just run this) — histogram with mean and median marked
import matplotlib.pyplot as plt

def plot_height_histogram(scan):
    z = scan.z.ravel()
    mean, median = float(z.mean()), float(np.median(z))
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.hist(z, bins=60, color="#4C72B0", alpha=0.85)
    ax.axvline(mean, color="#DD8452", lw=2, linestyle="--", label=f"mean = {mean:.2f} nm")
    ax.axvline(median, color="#2B2B2B", lw=2, linestyle=":", label=f"median = {median:.2f} nm")
    ax.set(title=f"{scan.title} — height distribution", xlabel="height (nm)", ylabel="pixel count")
    ax.legend()
    plt.show()
    return mean, median

# %%
mean1, median1 = plot_height_histogram(gallery["gallium_selenide_bumps"])
print(f"mean = {mean1:.2f} nm, median = {median1:.2f} nm")

# %% [markdown]
# ### Task 4 (Core) — mean vs. median
# The gallium selenide scan grew as rounded mounds, not a flat sheet — a few of those
# mounds are much taller than the rest of the surface.
#
# 1. Which is bigger here, the mean or the median? By about how much?
# 2. A few extra-tall mounds are like one heavy dust particle sitting on a scale next to
#    a pile of pebbles — which statistic does the "dust particle" drag around more, the
#    mean or the median? Explain in one or two sentences.
#
# **Your answer:**
# _(write here)_

# %% [markdown]
# **Explore:** now compare a much flatter sample — WS2 grown as small islands, with the
# bare sapphire substrate showing through as gaps.

# %%
mean2, median2 = plot_height_histogram(gallery["ws2_islands"])
print(f"mean = {mean2:.2f} nm, median = {median2:.2f} nm")

# %%
# @title Helper code (just run this) — counts outliers with a real rule (1.5 × IQR)
def outlier_summary(scan, label):
    z = scan.z.ravel()
    q1, q3 = np.percentile(z, [25, 75])
    iqr = q3 - q1
    lo, hi = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    outliers = (z < lo) | (z > hi)
    print(f"{label}: IQR = {iqr:.2f} nm, 1.5×IQR fence = [{lo:.1f}, {hi:.1f}] nm -> "
          f"{outliers.sum():,} outlier pixels ({outliers.mean() * 100:.1f}% of the scan)")

outlier_summary(gallery["gallium_selenide_bumps"], "GaSe")
outlier_summary(gallery["ws2_islands"], "WS2")

# %% [markdown]
# ### Task 4b (Explore)
# Look at the mean–median gap for each scan again.
#
# 1. Which surface has the bigger gap, and what does a bigger gap tell you about the **shape**
#    (skew) of that surface's height distribution — not how many outliers it has?
# 2. Now look at the outlier counts printed above, using a standard rule (any pixel more than
#    1.5×IQR beyond the 25th/75th percentile). Does the surface with the bigger mean–median gap
#    also have more outlier pixels? What does that tell you about using "mean vs. median" as an
#    outlier detector, compared to a proper outlier rule?
#
# **Your answer:**
# _(write here)_

# %% [markdown]
# ## Spot the glitch
#
# Not every unusual-looking line in a scan is a real crystal feature. Instruments have
# bad moments too: a spike of static, a skipped line, the probe briefly losing a steady signal.
#
# Fly over the WSe2 triangles below and look for something that doesn't look like a
# crystal feature at all.

# %%
explore_cross_section(gallery["wse2_triangles"])

# %% [markdown]
# **No widgets? Here's a full-resolution static view** (this always works) — a slider only shows
# 256 lines at a time, but a flat image shows every row at once, so a scan-line glitch can't hide
# off-screen:

# %%
_wse2 = gallery["wse2_triangles"]
_lo, _hi = np.percentile(_wse2.z, [1, 99])  # robust colour limits: one bad row won't wash out the crystal
fig, ax = plt.subplots(figsize=(6, 6))
im = ax.imshow(_wse2.z, cmap="viridis", vmin=_lo, vmax=_hi,
               extent=[0, _wse2.scan_um * 1000, _wse2.scan_um * 1000, 0])
ax.set(title=_wse2.title, xlabel="x (nm)", ylabel="y (nm)")
plt.colorbar(im, label="height (nm)")
plt.show()

# %%
surface_3d(gallery["wse2_triangles"], exaggeration=5, max_pixels=512).show()

# %% [markdown]
# ### Task 5 (Explore) — real feature or scan artifact?
# Hint: look closely in the first ten rows of the scan (drag the line slider near the top, or
# look at the full-resolution image above).
#
# 1. Describe what you noticed that looks out of place.
# 2. Real WSe2 triangles are small, three-sided, and only a few nm tall (see the story text for
#    this sample). Why doesn't the odd feature you found fit that description?
# 3. Name one thing about *how* an AFM works — its feedback loop, or the probe briefly losing a
#    steady signal mid-line — that could cause a single line to glitch like this.
#
# **Your answer:**
# _(write here)_

# %%
# @title Helper code (just run this) — reveals exactly where the glitch is
wse2 = gallery["wse2_triangles"]
row_std = wse2.z.std(axis=1)
glitch_row = int(np.argmax(row_std))
typical_std = float(np.median(row_std))
print(f"The noisiest row is row {glitch_row} "
      f"(std ≈ {row_std[glitch_row]:.1f} nm, vs ≈ {typical_std:.1f} nm for a typical row — "
      f"about {row_std[glitch_row] / typical_std:.0f}× noisier).")
print(f"That's about {glitch_row * wse2.pixel_nm:.1f} nm down from the top of the scan — "
      "a single scan-line artifact, not a crystal feature.")
print(f"Whole-scan height range: {wse2.z.min():.0f} to {wse2.z.max():.0f} nm — far beyond "
      "anything a few-nm-tall WSe2 triangle could produce.")

_gd, _gh = cross_section(wse2, glitch_row)
fig, ax = plt.subplots(figsize=(8, 3.5))
ax.plot(_gd, _gh, color="#C44E52", lw=1)
ax.set(title=f"Height along the glitch row (row {glitch_row})", xlabel="distance (nm)", ylabel="height (nm)")
ax.grid(alpha=0.3)
plt.show()

# %% [markdown]
# ## Exit ticket
# Answer these without running any code.
#
# 1. A scan is 2 µm wide. How many nanometres is that?
# 2. Two AFM scans of the same material have the same median height but very different
#    means. What does that difference tell you about the surface?
# 3. A friend says, "the 3D plot proves this crystal has huge mountains on it." What
#    question would you ask them before agreeing?
