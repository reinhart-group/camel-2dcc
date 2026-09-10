# %% [markdown]
# # Counting Crystals: Grains, Samples, and Populations
#
# WSe2 is a semiconductor that comes in sheets only about **three atoms thick** (a
# selenium-tungsten-selenium sandwich, Se-W-Se) — one of the thinnest working
# semiconductors anyone can grow. Scientists at Penn State's 2D Crystal Consortium (2DCC) grow
# it as tiny triangles on a sapphire wafer, then scan the wafer with an atomic force microscope
# (AFM) to see what actually grew. In this notebook you'll use real AFM data — hundreds of real
# triangles — to ask the questions every crystal grower asks: how big are these things, how do we
# know, and can we trust one measurement to speak for the whole wafer?
#
# **What you'll do**
# - Judge a computer's grain-finding rule against the actual picture — and catch it making a
#   mistake.
# - Measure a triangle's side length two independent ways and check them against the geometry of
#   a 60° crystal.
# - Read real height profiles across a WSe2 triangle, a bigger WSe2 flake, and a stack of SnSe
#   crystals — and meet a case where AFM height doesn't mean quite what you'd expect.
# - Build a **population** of 501 real triangles measured in three scans on one wafer, draw random
#   **samples** from it, and watch sample means converge on the population mean as sample size grows.
#
# **Time:** about 45 minutes, plus an optional extension.
#
# **Materials science words**
# - **Grain:** one individual crystal — here, one WSe2 triangle sitting on the wafer, formed where
#   atoms landed and grew.
# - **Wafer / substrate:** the sapphire disc the crystals grow on.
# - **MOCVD:** the growth method used here — reactive gases deposit atoms on a heated wafer.
# - **Population:** literally *every* member of the group you care about. In this notebook, our
#   population is every whole, cleanly separated triangle *we measured* in three small 2 µm × 2 µm
#   scans on wafer 17458 — not every triangle on the whole wafer, which we never fully scanned.
# - **Sample:** a smaller group you actually measure, used to estimate something about the whole
#   population.
# - **Random sample:** a sample chosen so every member of the population has an equal chance of
#   being picked — the opposite of "whichever ones are easiest to find."
# - **Sampling variability:** how much a statistic (like a sample's mean) changes from one random
#   sample to the next, just by chance.
# - **Bias:** a sample skewed in one direction by *how* it was chosen (not by chance) — for
#   example, always measuring near one edge of the wafer.

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
try:
    import skimage  # noqa: F401 — the grain outlines and line profiles below need this
except ImportError:
    raise ImportError("This notebook needs scikit-image. Run `%pip install -q scikit-image` in a "
                       "new cell above, choose Runtime ▸ Restart session, then run this cell again.")

# %% [markdown]
# ## Load the grain data
# `scans` holds the AFM height maps (and the computer's grain outlines); `table` is one row per
# detected grain, with its size, shape, and a `kind` (`single`, `merged`, `dust`, or `streak`).

# %%
from camel_data.grains import *
import numpy as np
import matplotlib.pyplot as plt

scans, table = load_grain_scans()
print("scans available:", list(scans))
print("grains.csv rows:", len(table))

# %% [markdown]
# ## Part 1 — Spot the mistake
#
# A simple computer rule looked at every pixel of the `wse2_17458_center` scan (2 µm × 2 µm, the
# middle of the wafer) and outlined every grain it found, colored by what kind of blob it thinks
# each one is:
# - 🟩 **single** — one blob that passed simple shape checks (not too tall, not too stretched-out,
#   not too concave). A good candidate for "one clean triangle" — but the rule never actually
#   checks that the shape *is* a triangle, so treat this label as "our best guess," not a proof.
# - 🟧 **merged** — a blob shaped like two things stuck together (low solidity) — probably two or
#   more triangles that grew into each other.
# - 🩷 **dust** — a blob much taller than a typical triangle (probably a stray particle, not a crystal).
# - 🟦 **streak** — a thin, stretched-out sliver (probably a scan glitch, not a crystal).
#
# ### Task 1 (Core) — Judge the rule
# Look at the full picture. The rule is just "measure height, measure shape" — it never *knows*
# what a real triangle looks like.

# %%
# @title Helper code (just run this)
from matplotlib.lines import Line2D

def kind_legend(ax):
    handles = [Line2D([0], [0], color=c, lw=3, label=k) for k, c in KIND_COLOURS.items()]
    ax.legend(handles=handles, loc="upper right", fontsize=8, framealpha=0.9)

# %%
scan = scans["wse2_17458_center"]
print(scan["growth_note"], f"— {scan['scan_um']:g} µm x {scan['scan_um']:g} µm scan")

fig, ax = plt.subplots(figsize=(7, 7))
show_grains(scan, table, ax=ax)
kind_legend(ax)
plt.show()

# %% [markdown]
# **Your answer:** Pick *one* colored outline you're suspicious of — one that might not be what
# its color claims. Which one, and why?
#
# _(write your answer here — then run the next cell to zoom in and check)_

# %%
# @title Helper code (just run this) — zoom near the top edge
fig, ax = plt.subplots(figsize=(6, 6))
show_grains(scan, table, ax=ax)
kind_legend(ax)
ax.set_xlim(560, 700)
ax.set_ylim(70, 0)  # zoomed near the top edge of the scan
plt.show()

mistake = table[(table.scan == "wse2_17458_center") & (table.grain.isin([3, 7]))]
print(mistake[["grain", "kind", "area_nm2", "height_nm", "row", "touches_edge", "touches_glitch"]])

# %% [markdown]
# > **What actually happened:** row 1 of this scan is a bad line — the tip glitched and recorded
# > nonsense heights hundreds of nanometers tall for a moment. That one bad row sits right through
# > the middle of a real bright particle, cutting it into two disconnected pieces: a thin sliver
# > right at the top edge (labeled **streak**, grain 3) and a rounder blob just below it (labeled
# > **dust**, grain 7 — it looks extra-tall partly because part of its top was chopped off with the
# > bad row). The rule isn't "wrong" about the pixels — it correctly found two disconnected blobs —
# > but a student looking at the picture can tell they're really one broken measurement, not two
# > separate objects.
# >
# > This is exactly why every grain here has a `touches_glitch` flag, and both grain 3 and grain 7
# > are flagged `True`. `whole_single()` — the function every population/sample task below uses —
# > throws out *any* grain that touches a bad row or the scan's edge, before it ever gets counted.

# %%
print("all detected blobs in this scan:            ", len(table[table.scan == "wse2_17458_center"]))
print("whole, single-candidate, undamaged blobs only:", len(whole_single(table, "wse2_17458_center")))

# %% [markdown]
# ## Part 2 — Why triangles, and how big is one?
#
# WSe2's atoms bond in a repeating hexagonal pattern, which only allows crystal edges along
# directions 60° apart — and the growth conditions here favor two of those three edge directions
# over the third, which is why these grains come out as triangles instead of hexagons, blobs, or
# squares. For an **equilateral** triangle
# with side length $s$, geometry gives its area directly:
#
# $$A = \frac{\sqrt{3}}{4} s^2$$
#
# ### Task 2 (Core) — Measure a side two independent ways
# The table already lists a `side_nm` for every grain — but that number was calculated *backward*
# from the measured area using this exact formula, so comparing it to the formula would just prove
# the formula equals itself. Instead, **measure a side yourself** from the picture's nm grid, then
# check it against the area the computer measured by counting pixels. These are two differently
# measured numbers, not two *independent* ones — both come from the same thresholded image and the
# same x-y calibration, so a shared calibration error would show up in both.

# %%
# @title Helper code (just run this) — pick a numbered grain, then zoom in to measure it
GRAIN = 217  # <-- change me: pick any numbered id from the left-hand map below

candidates = set(whole_single(table, "wse2_17458_center")["grain"])
if GRAIN not in candidates:
    raise ValueError(f"grain {GRAIN} isn't one of the whole single-candidate triangles in this scan "
                      f"— pick one of these ids instead: {sorted(candidates)[:20]} ...")
row = table[(table.scan == "wse2_17458_center") & (table.grain == GRAIN)].iloc[0]
px = scan["pixel_nm"]
cx, cy = row.col * px, row.row * px
print(f"grain {GRAIN}: area = {row.area_nm2:.0f} nm² (measured by counting its pixels), "
      f"measured height = {row.height_nm:.2f} nm")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
show_grains(scan, table, ax=ax1, kinds=("single",), number=True)
ax1.set_xlim(cx - 150, cx + 150)
ax1.set_ylim(cy + 150, cy - 150)
ax1.set_title("numbered candidates — pick any id shown here")

show_grains(scan, table, ax=ax2)
ax2.set_xlim(cx - 80, cx + 80)
ax2.set_ylim(cy + 80, cy - 80)
ax2.set_xticks(np.arange(round(cx - 80, -1), cx + 81, 20))
ax2.set_yticks(np.arange(round(cy - 80, -1), cy + 81, 20))
ax2.grid(True, color="white", alpha=0.5)
ax2.set_title(f"grain {GRAIN} — measure a side (nm grid)")
plt.tight_layout()
plt.show()

# %%
my_side_nm = 55  # <-- change me: estimate one side's length (corner to corner) from the grid above, in nm

predicted_area_nm2 = (np.sqrt(3) / 4) * my_side_nm ** 2
print(f"predicted area from A = (√3/4)s²:     {predicted_area_nm2:.0f} nm²")
print(f"area the computer measured (pixels):  {row.area_nm2:.0f} nm²")

# %%
# @title Helper code (just run this) — check yourself
ratio = predicted_area_nm2 / row.area_nm2
if 0.75 <= ratio <= 1.25:
    print(f"Reasonable! Your grid estimate predicts an area within 25% of the measured area "
          f"(ratio = {ratio:.2f}).")
else:
    print(f"That's more than 25% off (ratio = {ratio:.2f}) — look at the grid again and re-measure "
          f"the triangle's side.")

# %% [markdown]
# ## Part 3 — Line scans: reading a height profile
#
# A **line scan** (or line profile) is just the height along one straight line drawn across a map
# — the same idea as a cross-section. Reading one tells you widths and heights directly, in real
# units.
#
# ### Task 3 (Core) — Across one grain
# `profile_through_grain` draws a line through a grain's center and reports the heights along it.

# %%
# @title Helper code (just run this)
def plot_grain_profile(scan, table, grain, angle_deg=0.0, reach=1.6):
    (d, h), (start, end) = profile_through_grain(scan, table, grain, angle_deg, reach)
    r = table[(table.scan == scan["key"]) & (table.grain == grain)].iloc[0]
    pad = 1.8 * r.side_nm
    cx, cy = r.col * scan["pixel_nm"], r.row * scan["pixel_nm"]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5))
    show_grains(scan, table, ax=ax1)
    ax1.plot([start[0], end[0]], [start[1], end[1]], "r-", lw=2)
    ax1.set_xlim(cx - pad, cx + pad)
    ax1.set_ylim(cy + pad, cy - pad)
    ax2.plot(d, h, color="#D55E00")
    ax2.axhline(0, color="gray", lw=1, ls=":")
    ax2.set(xlabel="distance along the red line (nm)", ylabel="height (nm)", title="height along the red line")
    ax2.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()
    print(f"measured peak height on this line: {h.max():.2f} nm")
    return d, h

# %%
d, h = plot_grain_profile(scans["wse2_17458_center"], table, GRAIN, angle_deg=90.0)

# %% [markdown]
# **Your answer:** From the profile above, about how *wide* (in nm) is the raised part, and about
# how *tall* is its peak (in nm)?
#
# _(write your answer here)_
#
# > **Scientist's note:** This triangle's peak height usually reads about **1.5–1.8 nm** — but a
# > textbook WSe2 monolayer step is only about **0.65–0.7 nm**. AFM height can read high on
# > sapphire for reasons that have nothing to do with the crystal itself: a thin layer of adsorbed
# > water on the surface, how the scan was leveled, and where the calibration sets the "substrate"
# > level can all shift the reported height. (A microscope tip's shape mostly affects *lateral*
# > size, not vertical height.) We're not going to claim this tells us a layer count — just that
# > "measured height" and "true crystal thickness" aren't automatically the same number.

# %% [markdown]
# ### Task 3b (Explore, optional — skip this if you're short on time)
# Same idea, on scans that don't have a grain table — just raw height maps. `wse2_24111_center` has
# **bigger** WSe2 triangles with brighter rims and bright inner patches. `snse_39166_top` is a
# completely different material, SnSe, grown as stacked pyramids.

# %%
# @title Helper code (just run this)
def plot_line_scan(scan, start_nm, end_nm, title):
    d, h = line_profile(scan, start_nm, end_nm, width_px=3)
    lo, hi = np.percentile(scan["z"], [2, 98])
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5))
    size_nm = scan["scan_um"] * 1000
    ax1.imshow(scan["z"], cmap="viridis", vmin=lo, vmax=hi, extent=[0, size_nm, size_nm, 0])
    ax1.plot([start_nm[0], end_nm[0]], [start_nm[1], end_nm[1]], "r-", lw=2)
    ax1.set(xlabel="x (nm)", ylabel="y (nm)", title=title)
    ax2.plot(d, h, color="#D55E00")
    ax2.set(xlabel="distance along the red line (nm)", ylabel="height (nm)", title="height along the red line")
    ax2.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()
    return d, h

# %%
d1, h1 = plot_line_scan(scans["wse2_24111_center"], (615, 882), (695, 882), "wse2_24111_center")

# %% [markdown]
# **Your answer:** Find the three parts of that profile: the flat substrate, the step up onto the
# triangle, and the bright rim. Roughly how many nm does the height jump at the step?
#
# _(write your answer here)_

# %%
d2, h2 = plot_line_scan(scans["snse_39166_top"], (3200, 1550), (4900, 1550), "snse_39166_top")

# %% [markdown]
# **Your answer:** This profile looks like a staircase. About how many distinct "steps" (flat
# treads) can you count between the two ends of the red line?
#
# _(write your answer here)_

# %% [markdown]
# ## Part 4 — Population vs. sample
#
# This is the big idea of the notebook. Sample 17458 was scanned at **three spots on the same
# wafer** — center, toward the flat, toward the edge — each a small 2 µm × 2 µm field. Every whole,
# undamaged single-candidate triangle found across *all three* fields together is **our
# population**: every triangle we measured, in these three scans. It is *not* every triangle on the
# whole wafer — we never scanned the rest of it, so we can't say what's out there.

# %%
POP_KEYS = ["wse2_17458_center", "wse2_17458_flat", "wse2_17458_edge"]
pop_grains = whole_single(table)
pop_grains = pop_grains[pop_grains["scan"].isin(POP_KEYS)]
population = pop_grains["area_nm2"].to_numpy()
mu = population.mean()
print(f"population size N = {len(population)} triangles (every triangle we measured in these three "
      f"2 µm × 2 µm fields — not the whole wafer)")
print(f"population mean area μ = {mu:.0f} nm²   (population SD σ = {population.std():.0f} nm²)")

# %%
# @title Helper code (just run this)
fig, ax = plt.subplots(figsize=(8, 5))
ax.hist(population, bins=30, color="#0072B2", alpha=0.75, edgecolor="white")
ax.axvline(mu, color="black", lw=2, ls="--", label=f"population mean μ = {mu:.0f} nm²")
ax.set(xlabel="grain area (nm²)", ylabel="number of grains",
       title=f"Our population: all {len(population)} triangles we measured, in 3 scanned fields "
             f"on wafer 17458")
ax.legend()
plt.tight_layout()
plt.show()

# %% [markdown]
# ### Task 4 (Core) — Draw one random sample
# A real scientist can't measure all 501 triangles every time — they scan a smaller area and
# **sample** it. `random_sample` picks values at random, like drawing names from a hat, giving every
# triangle in our 501 an equal chance — that's a simplified stand-in for scanning a smaller area: a
# real area scan grabs whichever triangles happen to sit inside that patch, not an equal-chance draw
# from every triangle we know about. Changing the `seed` picks a *different* random sample (same
# seed = same sample, every time).

# %%
SEED = 3  # <-- change me: try a few different whole numbers

my_sample = random_sample(population, 10, seed=SEED)
x_bar = my_sample.mean()
print(f"my random sample (n=10): x̄ = {x_bar:.0f} nm²")
print(f"population:               μ = {mu:.0f} nm²")
print(f"difference: {x_bar - mu:+.0f} nm²")

# %% [markdown]
# **Your answer:** Try at least 3 different seeds. Does x̄ land on exactly μ? Does it land closer to
# μ sometimes than others?
#
# _(write your answer here)_

# %% [markdown]
# ### Task 5 (Core) — The sampling distribution
# One sample of 10 can land anywhere. What if we drew **1,000** random samples, at three different
# sample sizes, and plotted a histogram of all their means?

# %%
# @title Helper code (just run this)
def sampling_distribution(values, n, n_samples=1000, seed=0):
    rng = np.random.default_rng(seed)
    return np.array([rng.choice(values, size=n, replace=False).mean() for _ in range(n_samples)])

def plot_sampling_distributions(values, sizes, n_samples=1000):
    mu = values.mean()
    fig, axs = plt.subplots(1, len(sizes), figsize=(4 * len(sizes), 4), sharex=True, sharey=True)
    for ax, n in zip(axs, sizes):
        means = sampling_distribution(values, n, n_samples)
        ax.hist(means, bins=30, color="#009E73", alpha=0.8, edgecolor="white")
        ax.axvline(mu, color="black", lw=2, ls="--")
        ax.set(xlabel="sample mean area (nm²)", title=f"n = {n}\nSD of these means = {means.std():.0f} nm²")
    axs[0].set_ylabel(f"count (out of {n_samples} samples)")
    plt.tight_layout()
    plt.show()

# %%
plot_sampling_distributions(population, sizes=[5, 20, 50])

# %% [markdown]
# **Your answer:** As the sample size n grows from 5 to 20 to 50, what happens to the *spread* of
# the sample-mean histogram? In your own words: why would a bigger random sample give you a more
# trustworthy estimate of μ?
#
# _(write your answer here)_

# %% [markdown]
# ## Part 5 — Where you sample matters
# The three spots on this wafer aren't identical. Compare them directly.

# %%
# @title Helper code (just run this)
SPOT_COLORS = {"center": "#0072B2", "toward the flat": "#E69F00", "toward the edge": "#CC79A7"}

fig, ax = plt.subplots(figsize=(7, 5))
spots = [scans[k]["position"] for k in POP_KEYS]
data = [pop_grains.loc[pop_grains["scan"] == k, "area_nm2"].values for k in POP_KEYS]
bp = ax.boxplot(data, patch_artist=True)
ax.set_xticks(range(1, len(spots) + 1))
ax.set_xticklabels([f"{s}\n(n={len(d)})" for s, d in zip(spots, data)])
for patch, s in zip(bp["boxes"], spots):
    patch.set_facecolor(SPOT_COLORS[s])
    patch.set_alpha(0.7)
ax.axhline(mu, color="black", lw=1.5, ls="--", label=f"population μ = {mu:.0f} nm²")
ax.set(ylabel="grain area (nm²)", title="Grain area by spot on the wafer (sample 17458)")
ax.legend()
plt.tight_layout()
plt.show()

for k in POP_KEYS:
    vals = pop_grains.loc[pop_grains["scan"] == k, "area_nm2"]
    print(f"{scans[k]['position']:>16}: n={len(vals)}, mean={vals.mean():.0f} nm²")

# %% [markdown]
# ### Task 6 (Core) — The lazy scientist
# Imagine a scientist who is always in a hurry, and *always* scans "toward the edge" because it's
# the first spot on the sample holder.
#
# > **Careful:** we only scanned *one* field at each position. The "toward the edge" field's
# > triangles really are bigger than the "center" field's, in this data — but one field per
# > position can't prove that's true of the whole edge of this wafer. It might be a real
# > wafer-position effect, or it might just be how this one patch happened to look. To find out for
# > sure you'd need to scan several separate fields near the edge and see whether they agree.

# %%
edge_mean = pop_grains.loc[pop_grains["scan"] == "wse2_17458_edge", "area_nm2"].mean()
percent_off = 100 * (edge_mean - mu) / mu
print(f"'toward the edge' field only: mean = {edge_mean:.0f} nm²")
print(f"our pooled 3-field mean μ:    {mu:.0f} nm²")
print(f"that's {percent_off:+.0f}% off — and every grain in that number came from the same one "
      f"field, so measuring more grains *from that same field* can't change which field it is")

# %% [markdown]
# **Your answer:** A random sample of n=10 (Task 4) was sometimes off from μ by a lot, sometimes by
# a little — that's **random error**, and more grains would shrink it (Task 5). The lazy scientist
# always scans the *same* one edge field, so their number is off by roughly the same amount, in the
# same direction, *systematically* — that's what **bias** means: an error that comes from *how* (or
# *where*) you sampled, not one that random chance produces and more data from that same biased
# place would shrink. Would scanning *more* grains at that same edge field fix the lazy scientist's
# problem? Would scanning several *different* edge-area fields tell you something one field can't?
#
# _(write your answer here)_

# %% [markdown]
# ## Complexity dials
# - **Core (the 45-minute path):** Tasks 1, 2, 3, 4, 5, 6 — judge the rule, measure a grain two
#   ways, read one line scan, build our 501-triangle set, sample it, and compare fields on the
#   wafer.
# - **Explore:** Task 3b (two more line scans) if there's time, plus the "Your answer" reflections
#   throughout — write out your reasoning, not just a number.
# - **Extend:** Task 7 below — a second recipe, and a source of measurement error we deliberately
#   excluded all along.

# %% [markdown]
# ## Extension (optional)
#
# ### Task 7 (Extend) — Comparing two different recipes, and the grains we threw away
# `wse2_17464_center` and `wse2_17458_center` are two *different* growth recipes, not a
# before/after pair: 17458 was nucleated at 850 °C with no ripening step, while 17464 was
# nucleated at 875 °C and then given a 10-minute ripening step. That's two things different at
# once (temperature *and* ripening), so nothing below can tell us which one — if either — caused
# any difference we see. Treat this as a descriptive comparison, not a controlled experiment.

# %%
# @title Helper code (just run this)
for key in ["wse2_17458_center", "wse2_17464_center"]:
    s = scans[key]
    ws = whole_single(table, key)
    density = len(ws) / s["scan_um"] ** 2
    min_area_nm2 = 12 * s["pixel_nm"] ** 2  # the smallest blob the rule can keep, in nm² at this pixel size
    print(f"{key}: {s['growth_note']}")
    print(f"  above-threshold pixel fraction in this field: {100*s['covered_fraction']:.1f}%  "
          f"(every detected blob — merged, dust, streak, and single — not just clean triangles)")
    print(f"  whole single-candidate triangles: {len(ws)}  ({density:.1f} per µm²)")
    print(f"  mean triangle area:     {ws['area_nm2'].mean():.0f} nm²")
    print(f"  pixel size {s['pixel_nm']:.2f} nm → smallest detectable blob ≈ {min_area_nm2:.0f} nm²\n")

# %% [markdown]
# **Your answer:** These two scans also don't share a pixel size — look at the "smallest detectable
# blob" line above. A scan with bigger pixels can't detect a small triangle that a finer scan would
# catch, so any density or coverage difference between the two is only *approximate*, not a clean
# apples-to-apples count. Given all the printed numbers (and that caveat), does the lower coverage
# on `wse2_17464_center` look like it comes from smaller triangles, fewer triangles, or is the
# resolution difference too large to say confidently? Explain your reasoning.
#
# _(write your answer here)_
#
# Second question: every population/sample calculation above used `whole_single()`, which throws
# out every `merged` grain (two or more triangles that grew into each other).

# %%
pop_all = table[table["scan"].isin(POP_KEYS)]
merged = pop_all[pop_all["kind"] == "merged"]
print(f"merged grains in the population scans: {len(merged)} of {len(pop_all)} total detections "
      f"({100*len(merged)/len(pop_all):.0f}%)")
print(f"mean area of merged blobs:  {merged['area_nm2'].mean():.0f} nm²")
print(f"mean area of clean singles: {population.mean():.0f} nm²")

# %% [markdown]
# **Your answer:** If we had carelessly counted merged blobs as if each one were a single triangle,
# which way would that push our population mean — up or down? Is throwing merged grains away
# perfectly fair, or could it also bias the population in some way? (Hint: which triangles are more
# likely to grow into their neighbors — small ones or big ones?)
#
# _(write your answer here)_

# %% [markdown]
# ## Exit ticket
# Answer without writing any code.
#
# 1. A scientist scans only "toward the edge" of this wafer and reports the average grain area
#    there as the whole wafer's typical grain size. Is their estimate likely too high, too low, or
#    about right? Why?
# 2. If you drew 1,000 random samples of n=50 instead of n=5, would you expect the histogram of
#    sample means to be narrower or wider? Why?
# 3. In Part 1, the computer's rule labeled two pieces of the *same* real particle "streak" and
#    "dust." Why does the notebook throw out any grain that touches a bad scan row instead of
#    trying to patch it back together?
