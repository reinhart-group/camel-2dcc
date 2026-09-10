# %% [markdown]
# # Nano Landscapes: Fly Over a Crystal One Atom Thick
#
# A microscope needle traces the surface of a real crystal, atom by atom — and you get to
# fly over the 3D result, take height profiles, and hunt for a glitch in the data.
#
# **What you'll do**
# - Rotate a real 3D height map of a crystal surface and control how tall it looks
# - Slide a line across the map and read off the height of a single atomic step
# - Turn a histogram of heights into a mean, a median, and a "which one lies?" argument
#
# **Time:** about 45–50 minutes
#
# **Materials science words**
#
# | Word | Means |
# |---|---|
# | AFM (atomic force microscope) | An instrument that drags a tiny needle over a surface and records how far up or down it moves |
# | nanometre (nm) | One billionth of a metre (0.000000001 m) — atoms are about 0.2–0.4 nm across |
# | micrometre (µm) | One millionth of a metre = 1,000 nm |
# | terrace | A flat, atom-thin ledge on a crystal surface, like a stair step |
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
DATA_URL = "PASTE-SHAREPOINT-LINK-HERE"  # teacher: the only line you may need to change

import io, os, sys, zipfile, requests
if not os.path.isdir("camel-2dcc"):
    if os.path.exists("camel-2dcc-v1.zip"):
        zip_bytes = open("camel-2dcc-v1.zip", "rb").read()
    else:
        link = DATA_URL + ("&" if "?" in DATA_URL else "?") + "download=1"
        zip_bytes = requests.get(link, timeout=120).content
    if zip_bytes[:2] != b"PK":
        raise RuntimeError("The download was not the data file. Check DATA_URL, or upload camel-2dcc-v1.zip "
                           "with the Files panel and run this cell again.")
    zipfile.ZipFile(io.BytesIO(zip_bytes)).extractall(".")
sys.path.insert(0, "camel-2dcc")
try:
    from google.colab import output
    output.enable_custom_widget_manager()
except ImportError:
    pass  # running outside Colab
from camel_data.classroom import *
print("✅ Data ready:", sorted(os.listdir("camel-2dcc"))[:6], "...")

# %% [markdown]
# ## A needle that reads a crystal like Braille
#
# An **atomic force microscope (AFM)** drags a needle so sharp its tip is a single atom
# wide, back and forth across a surface, the way a fingertip reads Braille. Wherever the
# surface rises, the needle rises with it. A computer records that height at every point,
# and that grid of heights is the whole dataset — no lens, no light, just touch.
#
# Heights are recorded in **nanometres (nm)**. One nanometre is one *billionth* of a
# metre. A human hair is about 80,000 nm wide — so the bumps you're about to fly over are
# a few hundred times thinner than a hair.
#
# The gallery below has 12 real scans of 2D crystals: materials that could end up in
# future computer chips, memory, and superconductors.

# %%
gallery = load_gallery()
for key, scan in gallery.items():
    print(f"{key:22s} {scan.material:8s} {scan.scan_um:g} µm scan")

# %% [markdown]
# ## Fly over a real surface
#
# Pick a sample from the dropdown, then drag the **Stretch** slider. Try switching
# **Colors** too — every option here is colour-blind-safe.

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
scan = gallery["atomic_staircase"]
true_relief_nm = scan.z.max() - scan.z.min()
width_nm = scan.scan_um * 1000
print(f"Real relief: about {true_relief_nm:.1f} nm tall, across a {width_nm:.0f} nm-wide scan.")
print(f"That's roughly 1 part in {width_nm / true_relief_nm:.0f} — flatter than a phone screen protector.")

# %% [markdown]
# ### Task 1 (Explore)
# Set the sample to **Atomic staircase** and try a few different **Stretch** values.
#
# 1. What stretch value makes the terraces (the stair steps) clearly visible without
#    turning them into sharp, unrealistic spikes?
# 2. What happens at a stretch of 1? Why does that match the "flatter than a phone
#    screen protector" number above?
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
# ### Task 2 (Core) — estimate a step height
# Move the line slider until the profile on the right shows a clear "staircase" step —
# a flat bit, a jump, then another flat bit. Read the jump in **nm** off the y-axis and
# enter your estimate below.
#
# SrTiO3 (the material in this scan) stacks in layers 0.39 nm tall — that's the accepted
# textbook step height. Real AFM data is noisy, so don't expect to match it exactly.

# %%
my_step_estimate_nm = 0.3  # <-- change me: your estimate from the profile, in nm

# %% [markdown]
# **✅ Check yourself (run the cell below — no need to change it)**

# %%
# @title Helper code (just run this) — estimates the real step-height range from the data
import numpy as np

def _smooth(line, w=15):
    return np.convolve(line, np.ones(w) / w, mode="same")

def _step_sizes(scan, min_sep=20, min_height=0.08):
    sizes = []
    for row in range(0, scan.z.shape[0], 2):
        line = _smooth(scan.z[row])
        i, n, marks = min_sep, len(line), []
        while i < n - min_sep:
            window = line[i - min_sep:i + min_sep + 1]
            if line[i] == window.max() and (line[i] - window.min()) > min_height:
                marks.append((i, "p")); i += min_sep
            elif line[i] == window.min() and (window.max() - line[i]) > min_height:
                marks.append((i, "t")); i += min_sep
            else:
                i += 1
        for (i0, k0), (i1, k1) in zip(marks, marks[1:]):
            if k0 != k1:
                sizes.append(abs(line[i1] - line[i0]))
    return np.array(sizes)

step_sizes = _step_sizes(gallery["atomic_staircase"])
typical_lo, typical_hi = np.percentile(step_sizes, [25, 75])
wide_lo, wide_hi = np.percentile(step_sizes, [10, 90])
print(f"Across {len(step_sizes)} step edges measured from the real scan:")
print(f"  typical (25th-75th percentile): {typical_lo:.2f}-{typical_hi:.2f} nm")
print(f"  wider, still-plausible range:    {wide_lo:.2f}-{wide_hi:.2f} nm")
print(f"  textbook SrTiO3 unit cell:        0.39 nm")

if typical_lo <= my_step_estimate_nm <= typical_hi:
    print("\n🎯 Right in the typical range for this scan — nice reading!")
elif wide_lo <= my_step_estimate_nm <= wide_hi:
    print("\n👍 Reasonable — real AFM data is noisy, and this is a plausible single-step reading.")
else:
    print("\n🔁 Try again: find a clean flat-jump-flat pattern on the profile and re-read the y-axis in nm.")

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
# @title Helper code (just run this) — checks your formula
expected = hair_nm / scan_nm
if abs(scans_per_hair - expected) < 0.05:
    print(f"✅ Correct: {expected:.1f} scans span one hair's width.")
else:
    print(f"🔁 Not quite — hair_nm / scan_nm gives {expected:.1f}. Check your formula above.")

# %% [markdown]
# ## Reading the heights: histogram, mean, and median
#
# Every pixel in a scan has a height. Plot all of them as a histogram and you get the
# **distribution** of heights across the whole crystal.
#
# ### 🔬 Scientist's note: why is the median so often exactly 0.00 nm?
# Every scan here was processed with "per-line linear flatten, median set to 0" (check
# `scan.story` or the gallery table). That's a deliberate instrument-correction step, not
# a coincidence — researchers force each scan line's middle value to zero so that a
# microscope tilt or drift doesn't get mistaken for real crystal height. Keep that in
# mind before you assume "median = 0" means "nothing is happening" — it's a processing
# choice, and it also means you should compare **mean vs. median**, not just read either
# number alone.

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

# %% [markdown]
# ### Task 4b (Explore)
# Is the gap between mean and median bigger for the gallium selenide bumps or the WS2
# islands? What does that tell you about which surface has more extreme outliers?
#
# **Your answer:**
# _(write here)_

# %% [markdown]
# ## Spot the glitch
#
# Not every unusual-looking line in a scan is a real crystal feature. Instruments have
# bad moments too: a spike of static, a skipped line, the needle briefly losing contact.
#
# Fly over the WSe2 triangles below and look for something that doesn't look like a
# crystal feature at all.

# %%
explore_cross_section(gallery["wse2_triangles"])

# %%
surface_3d(gallery["wse2_triangles"], exaggeration=5).show()

# %% [markdown]
# ### Task 5 (Explore) — real feature or scan artifact?
# 1. Describe what you noticed that looks out of place.
# 2. Real WSe2 triangles are small, three-sided, and only a few nm tall (see the story
#    text for this sample). Why doesn't the odd feature you found fit that description?
# 3. Name one thing about *how* an AFM works (needle dragging across a surface, line by
#    line) that could cause a single line to glitch like this.
#
# **Your answer:**
# _(write here)_

# %%
# @title Helper code (just run this) — reveals exactly where the glitch is
wse2 = gallery["wse2_triangles"]
row_std = wse2.z.std(axis=1)
glitch_row = int(np.argmax(row_std))
print(f"The noisiest row is row {glitch_row} "
      f"(std ≈ {row_std[glitch_row]:.1f} nm, vs ≈ {np.median(row_std):.1f} nm for a typical row).")
print(f"That's about {glitch_row * wse2.pixel_nm:.0f} nm down from the top of the scan — "
      "a single scan-line artifact, not a crystal feature.")

# %% [markdown]
# ## Exit ticket
# Answer these without running any code.
#
# 1. A scan is 2 µm wide. How many nanometres is that?
# 2. Two AFM scans of the same material have the same median height but very different
#    means. What does that difference tell you about the surface?
# 3. A friend says, "the 3D plot proves this crystal has huge mountains on it." What
#    question would you ask them before agreeing?
