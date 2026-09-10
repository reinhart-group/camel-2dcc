# %% [markdown]
# # How Smooth Is Smooth? Statistics of Atom-Scale Surfaces
#
# A silicon chip fails if the films inside it are bumpier than a few atoms. The only way
# engineers know how smooth a film really is: scan it with an atomic force microscope (AFM),
# then do statistics on the heights it measures. In this notebook you'll build the exact number
# scientists use for "how bumpy" — **RMS roughness** — by hand, then use it on real AFM scans
# from Penn State's 2D Crystal Consortium (2DCC).
#
# **What you'll do**
# - Build RMS roughness from scratch on five made-up numbers, and show it's the same thing as
#   standard deviation.
# - Compare histograms of a smooth surface and a bumpy one, and see mean and median disagree.
# - Clean a real, messy data table of ~500-1000 AFM scans yourself, and see how your cleaning
#   choices change the answer — then argue, with evidence, whether one growth method really
#   makes smoother films.
#
# **Time:** about 45-50 minutes.
#
# **Materials science words**
# - **AFM (atomic force microscope):** an instrument that drags a tiny needle over a surface and
#   records the height at every point, like a robotic fingertip reading braille at the nanometer
#   scale.
# - **Roughness:** how much a surface's height varies from point to point. Smoother = flatter.
# - **RMS roughness:** the specific number scientists use for roughness — the root-mean-square
#   distance of every point from the average height. It has the same formula as standard
#   deviation.
# - **Substrate:** the base material a film is grown on top of, like the wafer a chip is built on.
# - **Growth method:** how a film was made. `MOCVD` and `MBE` (or `Hybrid MBE`) are two common
#   recipes for growing atom-thin films, and they use very different equipment and chemistry.
# - **Outlier:** a value far from the rest of the data — here, often a speck of dust sitting on
#   the surface, not a property of the film itself.
# - **Median vs. mean:** the mean is pulled toward extreme values; the median (the middle value)
#   usually isn't. **IQR** (interquartile range) is the spread of the middle 50% of the data.

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
# ## Part 1 — Building RMS roughness by hand
#
# ### Task 1 (Core)
# Here are five made-up surface heights, in nanometers. Find how "bumpy" they are:
# 1. Find the mean.
# 2. Find each point's **deviation** from the mean (point − mean).
# 3. **Square** each deviation (so positive and negative deviations don't cancel out).
# 4. Take the **mean** of those squares.
# 5. Take the **square root**. That's RMS roughness.

# %%
import numpy as np

heights = np.array([8, 10, 12, 9, 11])  # <-- change me: try your own 5 numbers (nm)
mean_height = heights.mean()
deviations = heights - mean_height
print("mean height:", mean_height, "nm")
print("deviations from the mean:", deviations)

# %%
squared_deviations = deviations ** 2
mean_square = squared_deviations.mean()
rms_by_hand = mean_square ** 0.5
print("squared deviations:", squared_deviations)
print("mean of the squares:", round(mean_square, 3))
print("square root (RMS roughness):", round(rms_by_hand, 3), "nm")

# %% [markdown]
# That formula — deviations, square, mean, square root — is exactly how **standard deviation**
# is defined. RMS roughness *is* the standard deviation of the heights. Check it:

# %%
print("My by-hand RMS:   ", round(rms_by_hand, 4), "nm")
print("NumPy's std():    ", round(float(np.std(heights)), 4), "nm")
print("classroom rms():  ", round(rms(heights), 4), "nm")

# %% [markdown]
# ### Task 1b (Core) — Now try it on a real surface
# `rms()` does exactly those same five steps on a whole AFM scan (thousands of height points
# instead of 5).

# %%
gallery = load_gallery()
scan = gallery["smoothest_surface"]  # <-- change me: try "gallium_selenide_bumps" or "ws2_islands"
print(scan.title, "-", scan.material, f"({scan.scan_um:g} µm x {scan.scan_um:g} µm scan)")
print("RMS roughness:", round(rms(scan.z), 3), "nm")

# %% [markdown]
# ## Part 2 — Comparing a smooth surface and a bumpy one
#
# ### Task 2 (Core)
# `smoothest_surface` is a nearly-flat SnTe film. `gallium_selenide_bumps` is covered in bumps.
# Before you look: guess how much rougher the bumpy one is.

# %%
my_guess_nm = 5  # <-- change me: guess the RMS roughness of the BUMPY scan, in nm

# %%
# @title Helper code (just run this)
import matplotlib.pyplot as plt

COLOR_A = "#0072B2"  # blue — colour-blind-safe (Okabe-Ito palette)
COLOR_B = "#E69F00"  # orange

def plot_two_histograms(scan_a, scan_b, label_a=None, label_b=None):
    """Compare the height distributions of two AFM scans."""
    label_a = label_a or f"{scan_a.title} ({scan_a.material})"
    label_b = label_b or f"{scan_b.title} ({scan_b.material})"
    heights_a, heights_b = scan_a.z.ravel(), scan_b.z.ravel()

    lo = min(heights_a.min(), heights_b.min())
    hi = max(heights_a.max(), heights_b.max())
    bin_edges = np.linspace(lo, hi, 41)  # same 40 bins for both scans, so the bars are comparable

    fig, ax = plt.subplots(figsize=(8, 5))
    for heights, color, label in ((heights_a, COLOR_A, label_a), (heights_b, COLOR_B, label_b)):
        ax.hist(heights, bins=bin_edges, weights=np.ones(len(heights)) / len(heights),
                 alpha=0.6, color=color, label=label)
    for heights, color in ((heights_a, COLOR_A), (heights_b, COLOR_B)):
        ax.axvline(heights.mean(), color=color, ls="--", lw=2)
        ax.axvline(np.median(heights), color=color, ls=":", lw=2)
    ax.set(xlabel="height (nm)", ylabel="fraction of pixels per bin",
           title="Dashed line = mean   Dotted line = median")
    ax.legend()
    plt.tight_layout()
    plt.show()

    for name, heights in ((label_a, heights_a), (label_b, heights_b)):
        print(f"{name}:")
        print(f"    mean = {heights.mean():.3f} nm   median = {np.median(heights):.3f} nm   "
              f"RMS roughness = {rms(heights):.3f} nm")

# %%
smooth = gallery["smoothest_surface"]
bumpy = gallery["gallium_selenide_bumps"]
plot_two_histograms(smooth, bumpy)

# %%
actual_bumpy_rms = rms(bumpy.z)
ratio = my_guess_nm / actual_bumpy_rms
if 0.3 <= ratio <= 3:
    print(f"Nice estimate! The real RMS roughness is about {actual_bumpy_rms:.1f} nm.")
else:
    print(f"Off by a fair amount — the real RMS roughness is about {actual_bumpy_rms:.1f} nm "
          f"(the smooth scan is about {rms(smooth.z):.2f} nm).")

# %% [markdown]
# ### Task 2b (Explore)
# **Your answer:** For the bumpy scan, is the mean bigger or smaller than the median? What does
# that tell you about a few very tall bumps in the data — do they pull the mean up, or down?
#
# _(write your answer here)_

# %% [markdown]
# ## Part 3 — A real table, and the decisions hiding inside it
#
# `afm_summary.csv` has **one selected AFM scan per sample** — for every public 2DCC sample with a
# usable scan, the data pipeline picked one representative scan by a fixed rule (skip anything an
# operator marked "modified," then take the largest scan on file). Most samples have several AFM
# scans; this table is a curated one-per-sample summary, not a census of every scan ever taken.
# It's authentically messy, on purpose. Two things you'll notice:
# - The `material` column is sometimes just the **substrate** (`Al2O3`, `Sapphire`) or even a gas
#   or element (`H2`, `Se`) — meaning that particular scan wasn't of a grown film at all.
# - `growth_method` is blank for some rows. **Missing is not zero** — a blank doesn't mean "no
#   growth method," it means the record doesn't say.
#
# ### Task 3 (Core)
# You get to decide how to handle both. Try the defaults below first, then come back and flip them.

# %%
table = load_table("afm_summary")

EXCLUDE_SUBSTRATE_LABELS = True   # <-- change me: True or False
MISSING_GROWTH_METHOD = "drop"    # <-- change me: "drop" or "unknown"

# %%
# @title Helper code (just run this)
# This is a *classroom heuristic*, not a physical fact: it's a short list of `material` labels that
# usually mean the selected scan imaged bare substrate or a leftover gas/element rather than a grown
# film — going only by whatever label a scientist typed into that one column. It doesn't prove what
# the AFM tip actually scanned, and a couple of these labels (GaAs, Se) can also be a real film's
# material on some samples.
SUBSTRATE_HEURISTIC_LABELS = {"Al2O3", "Sapphire", "GaAs", "H2", "Se"}

def clean_afm_summary(raw_table, exclude_substrate_labels=True, missing_growth_method="drop"):
    """Apply the two cleaning decisions above and report how many rows survive."""
    n_start = len(raw_table)
    df = raw_table[raw_table["material"].notna()].copy()

    if exclude_substrate_labels:
        df = df[~df["material"].isin(SUBSTRATE_HEURISTIC_LABELS)]

    if missing_growth_method == "drop":
        df = df[df["growth_method"].notna()]
    elif missing_growth_method == "unknown":
        df["growth_method"] = df["growth_method"].fillna("Unknown")
    else:
        raise ValueError('missing_growth_method must be "drop" or "unknown"')

    print(f"Rows in the raw table:     {n_start}")
    print(f"Rows after your cleaning:  {len(df)}   ({n_start - len(df)} removed)")
    print(f"Median RMS roughness:      {df['rms_roughness_nm'].median():.3f} nm")
    print(f"Mean RMS roughness:        {df['rms_roughness_nm'].mean():.3f} nm")
    return df

# %%
clean = clean_afm_summary(table, EXCLUDE_SUBSTRATE_LABELS, MISSING_GROWTH_METHOD)

# %% [markdown]
# ### Task 3b (Explore)
# Go back two cells up, flip **one** variable at a time (`EXCLUDE_SUBSTRATE_LABELS` or
# `MISSING_GROWTH_METHOD`), and rerun both cells.
#
# **Your answer:** Did the row count change a little or a lot? Did the median roughness change a
# little or a lot? Why do you think the median moved less than the row count did (or didn't)?
#
# _(write your answer here — then set the variables back to the defaults above before continuing)_

# %% [markdown]
# ## Part 4 — Box plots: comparing many scans at once
#
# A **box plot** shows the median (middle line), the IQR (the box — middle 50% of the data), and
# flags **outliers**: points more than 1.5 x IQR beyond the box. Because roughness values here
# span orders of magnitude (some films are 100x rougher than others), a **log scale** is often
# easier to read — equal steps mean "x10 rougher," not "10 nm rougher."
#
# ### Task 4a (Core) — Predict first
# Which of the top 6 materials (by number of scans) do you think has the **roughest** typical
# (median) surface?

# %%
my_guess_material = "MoS2"  # <-- change me: your prediction

# %%
# @title Helper code (just run this)
PALETTE = ["#0072B2", "#E69F00", "#009E73", "#D55E00", "#CC79A7", "#56B4E9", "#F0E442"]

def plot_box_by(df, group_col, value_col="rms_roughness_nm", top_n=6, log_scale=False, min_n=10):
    """Box plot of value_col grouped by group_col, for the top_n most common groups.

    Groups with fewer than min_n scans are still drawn (nothing is hidden) but greyed out and
    marked with a `*` — a box plot built from a handful of points has unstable quartiles and
    whiskers, so it isn't a fair comparison against a group built from hundreds of scans.
    """
    counts = df[group_col].value_counts()
    groups = counts.nlargest(top_n).index.tolist()
    groups = sorted(groups, key=lambda g: df.loc[df[group_col] == g, value_col].median())
    data = [df.loc[df[group_col] == g, value_col].dropna().values for g in groups]
    tiny = [g for g in groups if counts[g] < min_n]

    fig, ax = plt.subplots(figsize=(8, 5))
    bp = ax.boxplot(data, patch_artist=True)
    ax.set_xticks(range(1, len(groups) + 1))
    ax.set_xticklabels([f"{g}{' *' if g in tiny else ''}\n(n={counts[g]})" for g in groups])
    for patch, g, color in zip(bp["boxes"], groups, (PALETTE * 2)):
        if g in tiny:
            patch.set_facecolor("#BBBBBB")
            patch.set_alpha(0.5)
            patch.set_hatch("//")
        else:
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
    if log_scale:
        ax.set_yscale("log")
    ax.set(ylabel=f"RMS roughness, nm ({'log scale' if log_scale else 'linear scale'})",
           title=f"RMS roughness by {group_col}" + ("   (* = fewer than "
                 f"{min_n} scans — too few for a stable box)" if tiny else ""))
    ax.grid(alpha=0.3, axis="y")
    plt.tight_layout()
    plt.show()

    for g in groups:
        vals = df.loc[df[group_col] == g, value_col].dropna()
        q1, q3 = vals.quantile(0.25), vals.quantile(0.75)
        iqr = q3 - q1
        lo, hi = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        n_out = int(((vals < lo) | (vals > hi)).sum())
        flag = "  <- fewer than {} scans; exclude from the core comparison".format(min_n) if g in tiny else ""
        print(f"{g}: n={len(vals)}, median={vals.median():.3f} nm, IQR={iqr:.3f} nm, "
              f"outliers (1.5xIQR rule)={n_out} ({n_out / len(vals):.1%}){flag}")

# %%
LOG_SCALE = False  # <-- change me: try True — roughness spans orders of magnitude

plot_box_by(clean, "material", top_n=6, log_scale=LOG_SCALE)

# %%
medians = clean.groupby("material")["rms_roughness_nm"].median()
top6 = clean["material"].value_counts().nlargest(6).index
roughest = medians[top6].idxmax()
if my_guess_material == roughest:
    print(f"Correct! {roughest} has the highest median RMS roughness among the top 6.")
else:
    print(f"Not quite — {roughest} has the highest median RMS roughness among the top 6 "
          f"(you guessed {my_guess_material}).")

# %% [markdown]
# ### Task 4b (Core)
# Now compare by growth method instead of material. One group (`MBE`) usually has only a handful of
# scans — it'll show up greyed out with a `*`, because comparing a 3-point box to a 700-point box
# isn't fair. Focus your comparison on the two solid-colored boxes.

# %%
plot_box_by(clean, "growth_method", top_n=6, log_scale=LOG_SCALE)

# %% [markdown]
# **Your answer:** Between the two groups with enough scans to trust, which growth method's box is
# lowest (smoothest typical film)? Using the *fraction* of outliers (not just the raw count — the
# groups are very different sizes), does that group have a higher or lower outlier rate than the
# other?
#
# _(write your answer here)_

# %% [markdown]
# ## Part 5 — Claim, evidence, reasoning
#
# ### Task 5 (Explore)
# **Claim:** "One growth method makes smoother films than the other."
#
# Before you write your own claim, look at this: for each material, which growth method was
# actually used to make it?

# %%
import pandas as pd
pd.crosstab(clean["material"], clean["growth_method"])

# %% [markdown]
# > **Scientist's note:** Look closely at that table. In this slice, almost every material was
# > grown by only *one* method — MOCVD films are mostly MoS2/WSe2/WS2/MoSe2, Hybrid MBE films are
# > mostly different materials entirely (In2Se3, GaSe, InSe, MnTe...). Growth method and material
# > are **confounded**: they change together, so a box-plot difference could be caused by the
# > growth method, the material, the substrate, the scan size, or which samples researchers chose
# > to publish. A box plot can show a *difference*. It can't by itself show *cause*.
#
# **Now write your own claim-evidence-reasoning response:**
# - **Claim:** Which growth method looks smoother in *this* data, if either?
# - **Evidence:** Give the actual numbers (median, IQR, or n) that support it.
# - **Reasoning + limitation:** Name at least one reason this data alone can't prove one method
#   *causes* smoother films.
#
# _(write your answer here)_

# %% [markdown]
# ## Complexity dials
# - **Core:** Tasks 1, 1b, 2, 3, 4a, 4b — change the marked variables, run the helper cells, read
#   the plots.
# - **Explore:** Tasks 2b, 3b, 5 — compare, flip a cleaning decision, reason about confounding.
# - **Extend:** Task 6 below — open-ended, uses a second variable.
#
# ### Task 6 (Extend)
# Bigger scans cover more area — does that change the *measured* roughness? Plot RMS roughness
# against scan size and look for a trend.

# %%
# @title Helper code (just run this)
def plot_scatter(df, x_col, y_col):
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.scatter(df[x_col], df[y_col], alpha=0.5, color="#0072B2", edgecolor="white", linewidth=0.3)
    ax.set(xlabel=x_col, ylabel=y_col, title=f"{y_col} vs. {x_col}")
    ax.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()
    r = df[x_col].corr(df[y_col])
    print(f"correlation coefficient r = {r:.3f}  (closer to +1 or -1 = stronger straight-line trend)")

# %%
plot_scatter(clean, "scan_size_um", "rms_roughness_nm")  # <-- change me: try "pixels" instead

# %% [markdown]
# **Your answer:** Is there a clear trend? Would you trust a small r as strong evidence either
# way, given how spread out the roughness values are?
#
# _(write your answer here)_

# %% [markdown]
# ## Exit ticket
# Answer without writing any code.
#
# 1. In your own words, what does RMS roughness measure, and why would a chip maker care whether
#    it's 5 nm or 0.5 nm?
# 2. Suppose a group of scans has mean roughness 2.0 nm but median roughness 0.7 nm. What does
#    that gap tell you about the shape of the data?
# 3. Name one reason this AFM dataset alone can't prove that one growth method *causes* smoother
#    films.
