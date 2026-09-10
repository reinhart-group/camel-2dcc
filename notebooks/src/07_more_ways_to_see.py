# %% [markdown]
# # More Ways to See a Crystal: X-rays, Light, Electrons, and Electricity
#
# An atomic force microscope (AFM) feels a surface with a tiny needle. But that's only one way
# scientists "see" a crystal. This notebook has **four independent stations**, each built around a
# different real instrument and a different real 2D Crystal Consortium (2DCC) sample:
# - **Station A** — X-ray diffraction (a triangle hidden inside a crystal)
# - **Station B** — Raman spectroscopy (reading two peaks to estimate a layer count)
# - **Station C** — Scanning electron microscopy (scale, area, and counting)
# - **Station D** — Electrical transport (a piecewise function you can measure)
#
# **What you'll do**
# - Use trigonometry to turn an X-ray diffraction angle into an atomic spacing — and check your
#   answer two independent ways.
# - Read real spectroscopy peaks and use a reference table to estimate how many atomic layers a
#   film is.
# - Convert pixels to real distance with a proportion, measure a crystal, and count crystals in a
#   microscope image.
# - Read a real resistance-vs-temperature graph as a piecewise function and find where a
#   superconductor's resistance hits zero.
#
# **Time:** each station takes about **12–15 minutes** and stands on its own — you don't need to
# do them in order, or do all four. **For a 45-minute class, pick 2–3 stations.**
#
# **Materials science words**
# - **X-ray diffraction (XRD):** shines X-rays at a crystal and records how strongly they bounce
#   back at each angle. Because the X-ray wavelength is close to the spacing between atomic planes,
#   the reflected waves interfere, and only reinforce each other — bounce back strongly — at
#   specific angles that depend on that spacing.
# - **Wavelength (λ):** the distance between repeating peaks of a wave. The X-ray source used here
#   has λ = 0.15406 nm (a specific X-ray "color" called Cu Kα).
# - **Raman spectroscopy:** shines laser light on a material and looks at the tiny fraction of
#   light that bounces back with a shifted energy — shifted by the material's own atomic bonds
#   vibrating. The pattern of shifts acts like a fingerprint for the material.
# - **Wavenumber (cm⁻¹):** the unit Raman shifts are measured in — literally how many wave cycles
#   fit in one centimeter. Bigger number = higher energy shift.
# - **Scanning electron microscope (SEM):** rasters (scans) a focused beam of electrons across a
#   sample and builds an image from how many electrons bounce back or are knocked loose at each
#   spot — a camera that "sees" with electrons instead of light, at far higher magnification.
# - **Scale bar:** a marked line on a microscope image showing what real distance a given number of
#   pixels represents — the key to turning a picture into measurements.
# - **Electrical resistance:** how strongly a material opposes the flow of electric current,
#   measured in ohms (Ω). **Ohm's law** relates voltage, current, and resistance: V = I × R.
# - **Superconductor:** a material whose electrical resistance drops to *exactly* zero below a
#   **critical temperature** (Tc) — not just "very low," but zero.
# - **Piecewise function:** a function built from different rules over different intervals of its
#   input — like a graph that's flat, then steep, then flat again.
# - **Proportion:** an equation stating two ratios are equal — the tool that turns "this many pixels
#   = this many micrometers" into "that many pixels = how many micrometers?"

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
import importlib, camel_data.classroom  # reload so an updated data file never runs old helper code
importlib.reload(camel_data.classroom)
try:
    from google.colab import output
    output.enable_custom_widget_manager()
except ImportError:
    pass  # running outside Colab
from camel_data.classroom import *
print("✅ Data ready:", sorted(os.listdir("camel-2dcc"))[:6], "...")

# %%
# @title Helper code (just run this) — imports used by every station
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

COLOR_A = "#0072B2"  # blue — colour-blind-safe (Okabe-Ito palette), used throughout
COLOR_B = "#E69F00"  # orange

# %% [markdown]
# ---
# ## Station A — X-ray diffraction: measuring atomic spacing with a triangle
# X-ray diffraction (XRD) shines X-rays at a crystal and records how strongly they bounce back at
# each angle. Sample **20958** is a thin film grown on a sapphire (Al₂O₃) wafer. Here's its scan.

# %%
# @title Helper code (just run this)
xrd = load_extra("xrd_20958.csv")

def plot_xrd(df, xlim=None, title="XRD scan — sample 20958"):
    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.plot(df["two_theta_deg"], df["intensity_counts"], color=COLOR_A, lw=1)
    ax.set_yscale("log")
    if xlim:
        ax.set_xlim(xlim)
    ax.set(xlabel="2θ (degrees)", ylabel="intensity (counts, log scale)", title=title)
    ax.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()

plot_xrd(xrd)

# %% [markdown]
# Most of the scan is quiet, with two razor-sharp spikes. Those spikes come from the sapphire
# wafer's own atomic planes reflecting the X-rays. Bragg's law connects a peak's angle to the
# spacing *d* between those planes:
#
# $$n\lambda = 2d\sin\theta$$
#
# where λ = 0.15406 nm (this X-ray source's wavelength, called Cu Kα), θ = (2θ)/2, and *n* is a
# whole number (1, 2, 3, ...) called the **order** of the reflection.
#
# ### Task A1 (Core) — Read the first peak
# Zoom in and read the sharp peak's angle **2θ**, in degrees.

# %%
plot_xrd(xrd, xlim=(35, 48), title="Zoom near the first sharp peak")

# %%
my_two_theta_1_deg = 41.7  # <-- change me: read the sharp peak's angle from the plot above (degrees)

lam_nm = 0.15406
theta_1 = np.radians(my_two_theta_1_deg / 2)
d_1_nm = 1 * lam_nm / (2 * np.sin(theta_1))  # n = 1
print(f"2θ = {my_two_theta_1_deg:g}°  ->  θ = {np.degrees(theta_1):.3f}°  ->  d ≈ {d_1_nm:.4f} nm (n = 1)")

# %%
# @title Check yourself
window_1 = xrd[(xrd.two_theta_deg > 35) & (xrd.two_theta_deg < 48)]
true_two_theta_1 = window_1.loc[window_1.intensity_counts.idxmax(), "two_theta_deg"]
if abs(my_two_theta_1_deg - true_two_theta_1) <= 1.0:
    print(f"✅ Close! An automatic peak search on the raw scan finds this peak at 2θ = {true_two_theta_1:.2f}°.")
else:
    print(f"❌ Look again — an automatic peak search finds this peak at 2θ = {true_two_theta_1:.2f}°, "
          f"not {my_two_theta_1_deg:g}°.")

# %% [markdown]
# ### Task A2 (Core) — A second, independent measurement
# The *same* atomic planes reflect a second time, at a much higher angle, with n = 2. Find that
# peak too.

# %%
plot_xrd(xrd, xlim=(85, 95), title="Zoom near the second-order (n = 2) peak")

# %%
my_two_theta_2_deg = 90.8  # <-- change me: read the second sharp peak's angle above (degrees)

theta_2 = np.radians(my_two_theta_2_deg / 2)
d_2_nm = 2 * lam_nm / (2 * np.sin(theta_2))  # n = 2
print(f"2θ = {my_two_theta_2_deg:g}°  ->  θ = {np.degrees(theta_2):.3f}°  ->  d ≈ {d_2_nm:.4f} nm (n = 2)")

# %%
# @title Check yourself
window_2 = xrd[(xrd.two_theta_deg > 85) & (xrd.two_theta_deg < 95)]
true_two_theta_2 = window_2.loc[window_2.intensity_counts.idxmax(), "two_theta_deg"]
if abs(my_two_theta_2_deg - true_two_theta_2) <= 1.0:
    print(f"✅ Close! An automatic peak search finds this peak at 2θ = {true_two_theta_2:.2f}°.")
else:
    print(f"❌ Look again — an automatic peak search finds this peak at 2θ = {true_two_theta_2:.2f}°, "
          f"not {my_two_theta_2_deg:g}°.")

# %% [markdown]
# ### Do the two routes agree?
# n = 1 and n = 2 are two *completely independent* readings of the same scan. If Bragg's law is
# right, they should give nearly the same spacing *d*.

# %%
sapphire_c6_nm = 0.2165  # literature value for sapphire's c/6 spacing
print(f"n = 1 peak gives d ≈ {d_1_nm:.4f} nm")
print(f"n = 2 peak gives d ≈ {d_2_nm:.4f} nm")
print(f"known sapphire spacing (c/6): {sapphire_c6_nm:.4f} nm")

# %% [markdown]
# > **Scientist's note:** XRD measures an *average* spacing over billions of atomic planes stacked
# > through the wafer — that's exactly why it can be this precise. But precision isn't the same as
# > completeness: matching sapphire's known spacing tells you the substrate is sapphire, oriented
# > this way. It doesn't, by itself, tell you anything about a single atom, a single defect, or
# > what's sitting on top of the substrate.
#
# ### Task A3 (Extend)
# Look at the full scan again (the very first plot). Besides the two sharp sapphire peaks, there
# are three much **broader**, weaker bumps near 2θ ≈ 23°, 46°, and 72° — these come from the thin
# **film** grown on top of the sapphire, not the substrate.
#
# **Your answer:** Why might the film's peaks look broad and low, while the sapphire substrate's
# peaks are tall and razor-sharp? (Hint: think about how many repeating atomic planes an X-ray beam
# passes through in a wafer that's millimeters thick, versus a film that might be only a few
# nanometers thick.)
#
# _(write your answer here)_

# %% [markdown]
# ---
# ## Station B — Raman spectroscopy: reading two peaks and a lookup table
# Raman spectroscopy shines laser light on a material and looks at the tiny fraction of light that
# bounces back with a shifted energy. MoS₂ (molybdenum disulfide) has two especially useful peaks:
# **E₂g** (atoms sliding side-to-side) and **A₁g** (atoms moving up and down). The gap between them
# changes with how many layers thick the film is.

# %%
# @title Helper code (just run this)
spectra = load_extra("raman_spectra.csv")
peaks = load_extra("raman_peaks.csv")

s32093 = spectra[spectra.sample_id == 32093]
fig, ax = plt.subplots(figsize=(9, 4.5))
ax.plot(s32093["raman_shift_cm1"], s32093["intensity"], color=COLOR_A, lw=1)
ax.set(xlabel="Raman shift (cm⁻¹)", ylabel="intensity (arbitrary units)",
       title="Raman spectrum — sample 32093 (MoS₂)")
ax.grid(alpha=0.3)
plt.tight_layout()
plt.show()

# %% [markdown]
# ### Task B1 (Core) — Read the two peaks
# Read each peak's position (its x-value, in cm⁻¹) from the plot above. The lower one is E₂g, the
# higher one is A₁g.

# %%
my_E2g_cm1 = 383  # <-- change me: read the LOWER peak's position from the plot (cm⁻¹)
my_A1g_cm1 = 403  # <-- change me: read the HIGHER peak's position from the plot (cm⁻¹)

my_separation_cm1 = my_A1g_cm1 - my_E2g_cm1
print(f"E2g ≈ {my_E2g_cm1:g} cm⁻¹, A1g ≈ {my_A1g_cm1:g} cm⁻¹  ->  separation ≈ {my_separation_cm1:g} cm⁻¹")

# %%
# @title Check yourself
fit_row = peaks[peaks.sample_id == 32093].iloc[0]
print(f"the lab's own peak-fitting software found: E2g = {fit_row.E2g_cm1:.1f} cm⁻¹, "
      f"A1g = {fit_row.A1g_cm1:.1f} cm⁻¹, separation = {fit_row.separation_cm1:.1f} cm⁻¹")
if abs(my_separation_cm1 - fit_row.separation_cm1) <= 3:
    print("✅ Close enough — reading peaks by eye is never exact to a fraction of a cm⁻¹.")
else:
    print("❌ Look again at the two peak positions on the plot above.")

# %% [markdown]
# ### Task B2 (Core) — Estimate the layer count
# Researchers have measured this same separation on samples where the layer count is known
# independently (for example, by AFM step height), and built a rough reference. These are typical
# values, not exact rules — real separations also shift a little with strain, doping, the
# substrate, and even the laser used.
#
# | Layers | Typical E2g–A1g separation |
# |---|---|
# | 1 (monolayer) | ≈ 18–19 cm⁻¹ |
# | 2 | ≈ 21–22 cm⁻¹ |
# | 3 | ≈ 23 cm⁻¹ |
# | bulk (many layers) | ≈ 25 cm⁻¹ |
#
# **Your answer:** Using the lab's separation for sample 32093 (printed above) and the reference
# table, what's your best estimate for how many layers this film is? Is it a clean match to one row
# of the table, or does it fall between two rows?
#
# _(write your answer here)_

# %% [markdown]
# ### Task B3 (Core) — One film vs. 29 films
# Sample 32093 is just one MoS₂ film. 2DCC has measured this same separation on 29 different MoS₂
# samples.

# %%
# @title Helper code (just run this)
fig, ax = plt.subplots(figsize=(9, 3.5))
rng = np.random.default_rng(0)
jitter = rng.uniform(-0.15, 0.15, size=len(peaks))
ax.scatter(peaks["separation_cm1"], jitter, color=COLOR_A, alpha=0.7, s=45, edgecolor="white")
for x, label in [(18.5, "1L"), (21.5, "2L"), (23, "3L"), (25, "bulk")]:
    ax.axvline(x, color="#999999", ls=":", lw=1)
    ax.text(x, 0.22, label, ha="center", fontsize=8, color="#555555")
ax.set(xlabel="E2g–A1g separation (cm⁻¹)", yticks=[],
       title=f"E2g–A1g separation, {len(peaks)} MoS₂ films (dashed lines = reference table values)")
plt.tight_layout()
plt.show()

print(f"median separation: {peaks['separation_cm1'].median():.1f} cm⁻¹")
print(f"range: {peaks['separation_cm1'].min():.1f}–{peaks['separation_cm1'].max():.1f} cm⁻¹")

# %% [markdown]
# **Your answer:** Based on the dot plot and the reference table, is it fair to say "most of these
# films are one or two layers thick, with a few thicker ones"? Point to where the dots sit to
# support your answer.
#
# _(write your answer here)_
#
# > **Scientist's note:** Not every spectrum is this clean. Sample 32578 (separation 16.9 cm⁻¹, the
# > smallest in this dataset) has a much noisier signal — compare it side-by-side with 32093:

# %%
# @title Helper code (just run this)
fig, axs = plt.subplots(1, 2, figsize=(11, 3.8))
for ax, sid, label in [(axs[0], 32093, "clean (sample 32093)"), (axs[1], 32578, "noisy (sample 32578)")]:
    d = spectra[spectra.sample_id == sid]
    ax.plot(d["raman_shift_cm1"], d["intensity"], color=COLOR_A, lw=1)
    ax.set(xlabel="Raman shift (cm⁻¹)", ylabel="intensity (arb. units)", title=label)
    ax.grid(alpha=0.3)
plt.tight_layout()
plt.show()

# %% [markdown]
# A separation estimate from a noisy spectrum like this one is a lot less certain than one from a
# clean spectrum — the same math (find two peaks, subtract) is being applied to a much fuzzier
# reading. Strain, doping, the substrate, and the laser used can *also* shift real peak positions by
# a cm⁻¹ or two — so a single separation number is a reasonable estimate, not a precise, guaranteed
# layer count.

# %% [markdown]
# ---
# ## Station C — Scanning electron microscopy: scale, area, and counting
# A scanning electron microscope (SEM) scans a focused beam of electrons across a sample and builds
# an image from how many electrons bounce back at each spot. Sample **32096** is a sapphire wafer
# with small MoS₂ triangles grown on it. In *this* image, the triangles show up **dark** and the
# bare sapphire shows up **light** — a contrast effect of this imaging mode, not a height
# measurement (unlike the AFM height maps you may have seen elsewhere in this course).

# %%
# @title Helper code (just run this)
sem = load_extra("sem_32096.png")
meta = load_extra("sem_32096.json")
print(meta)

fig, ax = plt.subplots(figsize=(9, 6))
ax.imshow(sem, cmap="gray", vmin=0, vmax=255)
ax.set(xlabel="x (pixels)", ylabel="y (pixels)",
       title=f"SEM image — sample {meta['sample_id']} ({meta['material']})")
bar_px, bar_um = meta["scale_bar_px"], meta["scale_bar_um"]
x0, y0 = 40, sem.shape[0] - 40
ax.plot([x0, x0 + bar_px], [y0, y0], color=COLOR_B, lw=3)
ax.text(x0 + bar_px / 2, y0 - 12, f"{bar_um:g} µm", color=COLOR_B, ha="center", fontsize=10)
plt.tight_layout()
plt.show()

# %% [markdown]
# The yellow scale bar above is redrawn from the microscope's own calibration (from the original
# burned-in scale bar, before the info strip beneath the image was cropped off for this notebook).
#
# ### Task C1 (Core) — Pixels to nanometers
# The scale bar is `scale_bar_px` pixels wide and represents `scale_bar_um` micrometers. Use that as
# a **proportion** to find how many nanometers one pixel represents.

# %%
my_nm_per_px = meta["scale_bar_um"] * 1000 / meta["scale_bar_px"]  # <-- change me: try building this a different way

print(f"{bar_px} px = {bar_um:g} µm  ->  {my_nm_per_px:.3f} nm per pixel")
print(f"the microscope's own calibration: {meta['nm_per_px']:.3f} nm per pixel")

field_um_x = sem.shape[1] * my_nm_per_px / 1000
field_um_y = sem.shape[0] * my_nm_per_px / 1000
print(f"full image field of view: {field_um_x:.1f} µm × {field_um_y:.1f} µm")

# %% [markdown]
# ### Task C2 (Core) — Measure one triangle two independent ways
# Here's one triangle, close up, with a 100 nm grid.

# %%
# @title Helper code (just run this)
from skimage import measure as skmeasure
from skimage.segmentation import find_boundaries
from matplotlib.colors import to_rgba

NM_PER_PX = meta["nm_per_px"]

def find_islands(gray, dark_below=100, min_px=8):
    """Label dark blobs (the crystal islands) against the lighter substrate — the same kind of
    threshold idea as camel_data.grains uses on AFM height, applied here to brightness instead."""
    mask = gray < dark_below
    labels_all = skmeasure.label(mask, connectivity=1)
    sizes = np.bincount(labels_all.ravel())
    mask = mask & (sizes[labels_all] >= min_px)  # drop specks smaller than min_px
    labels = skmeasure.label(mask, connectivity=1)
    rows = []
    for r in skmeasure.regionprops(labels):
        minr, minc, maxr, maxc = r.bbox
        area_nm2 = r.area * NM_PER_PX ** 2
        rows.append(dict(blob=r.label, area_px=r.area, area_nm2=area_nm2,
                          row=r.centroid[0], col=r.centroid[1],
                          touches_edge=bool(minr == 0 or minc == 0
                                            or maxr == gray.shape[0] or maxc == gray.shape[1])))
    return labels, pd.DataFrame(rows)

# the marked square region used for Task C3, in full-image pixel coordinates
ROW0, ROW1, COL0, COL1 = 300, 400, 450, 550
region = sem[ROW0:ROW1, COL0:COL1]
region_labels, region_table = find_islands(region)

# a tight zoom on one single, whole triangle from that region (blob 8) for Task C2
Z0, Z1, C0, C1 = 348, 387, 477, 516
zoom = sem[Z0:Z1, C0:C1]
fig, ax = plt.subplots(figsize=(6, 6))
extent_zoom = [0, zoom.shape[1] * NM_PER_PX, zoom.shape[0] * NM_PER_PX, 0]
ax.imshow(zoom, cmap="gray", vmin=0, vmax=255, extent=extent_zoom)
ax.set_xticks(np.arange(0, extent_zoom[1], 100))
ax.set_yticks(np.arange(0, extent_zoom[2], 100))
ax.grid(True, color=COLOR_B, alpha=0.6)
ax.set(xlabel="x (nm)", ylabel="y (nm)", title="One triangle, close up — 100 nm grid (this is 'blob 8')")
plt.tight_layout()
plt.show()

blob_8 = region_table.loc[region_table.blob == 8].iloc[0]
print(f"the computer's pixel count for this triangle: {blob_8.area_nm2:.0f} nm²")

# %% [markdown]
# The microscope's resolution blurs a small triangle's edges — don't expect a crisp geometric
# shape. Estimate its side length (corner to corner) using the grid above, in nanometers.

# %%
my_side_nm = 200  # <-- change me: estimate the triangle's side length from the grid above, in nm

predicted_area_nm2 = (np.sqrt(3) / 4) * my_side_nm ** 2
print(f"predicted area from A = (√3/4)s²:            {predicted_area_nm2:.0f} nm²")
print(f"area the computer measured (counting pixels): {blob_8.area_nm2:.0f} nm²")

# %%
# @title Check yourself
ratio = predicted_area_nm2 / blob_8.area_nm2
if 0.5 <= ratio <= 2.0:
    print(f"✅ Reasonable! Your grid estimate predicts an area within 2x of the measured area "
          f"(ratio = {ratio:.2f}).")
else:
    print(f"❌ That's more than 2x off (ratio = {ratio:.2f}) — look at the grid again and re-measure.")

# %% [markdown]
# ### Task C3 (Core) — Count triangles and compute density
# Here's the marked square region (2 µm scale, roughly), with every dark blob the threshold rule
# found outlined and numbered.

# %%
# @title Helper code (just run this)
fig, ax = plt.subplots(figsize=(7, 7))
extent_region = [0, region.shape[1] * NM_PER_PX, region.shape[0] * NM_PER_PX, 0]
ax.imshow(region, cmap="gray", vmin=0, vmax=255, extent=extent_region)
edges = find_boundaries(region_labels)
overlay = np.zeros((*region.shape, 4))
overlay[edges] = to_rgba(COLOR_B)
ax.imshow(overlay, extent=extent_region)
for _, r in region_table.iterrows():
    ax.text(r.col * NM_PER_PX, r.row * NM_PER_PX, str(int(r.blob)), color="cyan", fontsize=8,
            ha="center", va="center")
ax.set_xticks(np.arange(0, extent_region[1], 250))
ax.set_yticks(np.arange(0, extent_region[2], 250))
ax.grid(True, color="white", alpha=0.3)
ax.set(xlabel="x (nm)", ylabel="y (nm)", title="Marked region — every blob the threshold rule found")
plt.tight_layout()
plt.show()

# %% [markdown]
# Count the dark triangles you see in this region (include ones partly cut off by the box's edge).
# Then compare to the threshold rule's own count.

# %%
my_count = 15  # <-- change me: your own count from the picture above

computer_count = len(region_table)
region_area_um2 = (region.shape[0] * NM_PER_PX / 1000) * (region.shape[1] * NM_PER_PX / 1000)
density_per_um2 = computer_count / region_area_um2
print(f"your count:              {my_count}")
print(f"the threshold rule's count: {computer_count}")
print(f"region area: {region_area_um2:.2f} µm²  ->  density ≈ {density_per_um2:.2f} triangles per µm²")

# %% [markdown]
# > **Scientist's note:** Brightness here is *not* height — islands appear dark in this image, the
# > opposite of an AFM height map, where taller usually means brighter. Also look closely at blobs
# > 2 and 5 on the map: they're really two or more triangles that grew close enough to touch and
# > merge into one connected blob, so a simple counting rule like this one can *undercount* the true
# > number of triangles. (This same sample, 32096, also has multi-position AFM scans in the full
# > public LiST catalog — not included in this data slice — that a researcher could use to check a
# > count like this one against real height data.)

# %% [markdown]
# ---
# ## Station D — Electrical transport: a piecewise function you can measure
# A transport measurement cools a sample down step by step and records its electrical resistance at
# each temperature. Sample **20198** is a thin film of FeSe (iron selenide) grown at 2DCC. Bulk FeSe
# becomes a **superconductor** — resistance drops to *exactly* zero — below about 8 K (about
# −265 °C). Let's see what this particular film actually does.

# %%
# @title Helper code (just run this)
transport = load_extra("transport_fese.csv")
summary = load_extra("transport_summary.csv")

def plot_rt(sample_id, xlim=None, ax=None, label=None):
    d = transport[transport.sample_id == sample_id].sort_values("temperature_K")
    own_fig = ax is None
    if own_fig:
        fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(d["temperature_K"], d["resistance_ohm"], lw=1.5, label=label)
    if xlim:
        ax.set_xlim(xlim)
    ax.set(xlabel="temperature (K)", ylabel="resistance (Ω)")
    ax.grid(alpha=0.3)
    if own_fig:
        ax.set_title(f"sample {sample_id}: R vs. T")
        plt.tight_layout()
        plt.show()
    return d

d20198 = plot_rt(20198)

# %%
plot_rt(20198, xlim=(0, 40));

# %% [markdown]
# ### Task D1 (Core) — Describe the shape
# **Your answer:** Describe this graph as a piecewise function: what does resistance do above about
# 10 K, and what does it do between about 10 K and 5 K?
#
# _(write your answer here)_
#
# ### Task D2 (Core) — Slope of the normal (metal) part
# Above the transition, resistance falls **slowly and steadily** as the film cools — ordinary
# "normal metal" behavior. Pick two points from that flatter, higher-temperature part of the curve
# and find the **average rate of change** (the slope), in Ω per K.

# %%
def nearest(sample_id, target_T):
    """The measured row closest to a chosen temperature."""
    d = transport[transport.sample_id == sample_id]
    row = d.loc[(d.temperature_K - target_T).abs().idxmin()]
    return row.temperature_K, row.resistance_ohm

T1, R1 = nearest(20198, 250)  # <-- change me: pick a different temperature if you like
T2, R2 = nearest(20198, 100)  # <-- change me

slope_ohm_per_K = (R2 - R1) / (T2 - T1)
print(f"point 1: T = {T1:.1f} K, R = {R1:.1f} Ω")
print(f"point 2: T = {T2:.1f} K, R = {R2:.1f} Ω")
print(f"slope ≈ {slope_ohm_per_K:.3f} Ω/K")

# %% [markdown]
# ### Task D3 (Core) — Where does it hit zero?
# Look at the zoomed plot again. **Your answer:** at about what temperature does the resistance
# reach (essentially) zero?
#
# _(write your answer here — then run the next cell to compare)_

# %%
# @title Check yourself
t_zero_actual = summary.loc[summary.sample_id == 20198, "T_zero_1pct_K"].iloc[0]
print(f"this sample's measured 'reaches (about) zero' temperature: {t_zero_actual:.2f} K")

# %% [markdown]
# ### Task D4 (Core) — Compare four films
# 2DCC measured four FeSe films from the same growth series. Here's how each one behaves.

# %%
# @title Helper code (just run this)
fig, ax = plt.subplots(figsize=(8, 5))
for sid in [20198, 20199, 20200, 20201]:
    plot_rt(sid, xlim=(0, 40), ax=ax, label=f"sample {sid}")
ax.set_title("R vs. T, all four FeSe films (zoomed 0–40 K)")
ax.legend(fontsize=8)
plt.tight_layout()
plt.show()

summary[["sample_id", "T_mid_50pct_K", "T_zero_1pct_K"]]

# %% [markdown]
# **Your answer:** Sample 20199's `T_zero_1pct_K` is blank in that table, not 0. What's the
# difference between "blank" and "0," and what does it tell you about this film down to the lowest
# temperature measured here?
#
# _(write your answer here)_

# %% [markdown]
# ### Task D5 (Explore) — Ohm's law above and below the transition
# Ohm's law: **V = I × R**. Imagine passing a tiny, steady current of 1 microamp
# (1 µA = 1 × 10⁻⁶ A) through sample 20198.

# %%
I_amp = 1e-6  # <-- change me: try a different current

R_above = summary.loc[summary.sample_id == 20198, "R_300K_ohm"].iloc[0]
V_above = I_amp * R_above

T_low, R_below = nearest(20198, 2)
V_below = I_amp * R_below

print(f"at 300 K:      R = {R_above:.1f} Ω    ->  V = {V_above * 1000:.4f} mV")
print(f"at {T_low:.1f} K:  R = {R_below:.4f} Ω  ->  V = {V_below * 1e9:.2f} nV "
      f"(essentially zero — this small a reading is within the instrument's own noise)")

# %% [markdown]
# > **Scientist's note:** Keeping something at 5 K takes serious refrigeration — that's about
# > −268 °C, colder than deep space. No superconductor here is "already cooling data centers"; this
# > is *research* into how cold a superconductor needs to be, not a working power line. Bulk FeSe
# > becomes superconducting around 8 K, but *thin films* of FeSe on certain substrates have been
# > reported to superconduct at noticeably higher temperatures than the bulk crystal — exactly why
# > scientists keep studying films like these.

# %% [markdown]
# ---
# ## Exit ticket
# Answer the questions for whichever stations you completed today. No code needed.
#
# **If you did Station A (XRD):**
# 1. Two different reflection orders (n = 1 and n = 2) gave you almost the same spacing *d*. Why
#    does that agreement make you more confident in the measurement than either reading alone?
#
# **If you did Station B (Raman):**
# 2. A sample's E2g and A1g peaks are at 384 cm⁻¹ and 406 cm⁻¹. What's the separation, and using the
#    reference table, about how many layers is it likely to be?
#
# **If you did Station C (SEM):**
# 3. A scale bar is 100 pixels wide and represents 2 µm. How many nanometers is one pixel?
#
# **If you did Station D (transport):**
# 4. A resistance-vs-temperature graph is flat-ish and gently sloped from 300 K down to about 10 K,
#    then drops steeply toward zero by 5 K. Describe this in your own words as a piecewise function
#    — how many "pieces" does it have, and what happens in each one?
