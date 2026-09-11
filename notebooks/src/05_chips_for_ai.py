# %% [markdown]
# [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/reinhart-group/camel-2dcc/blob/main/notebooks/05_chips_for_ai.ipynb)

# %% [markdown]
# # Chips for AI: Exponents, Light, and Super-Cold Wires
#
# Every AI chatbot, image generator, and self-driving car runs on chips built from billions of
# tiny switches called **transistors**. In this notebook you'll use exponential functions to
# model how transistor counts grew, use an inverse-proportion formula physicists use for light to
# find the color a 2D material glows, and use linear temperature conversions to understand why
# "zero resistance" materials matter for the huge amount of electricity AI data centers use.
#
# **What you'll do**
# - Fit an exponential model to 50+ years of real transistor-count data and find its doubling time.
# - Use ratio and multiplication models to see why ultra-thin 2D materials interest chip designers.
# - Turn a 2D material's optical energy into the color of light it can emit, and convert
#   superconductor temperatures between Kelvin, Celsius, and Fahrenheit.
#
# **Time:** about 45-50 minutes (plus an optional ~5-minute "see real data" add-on in Part 4).
#
# **Materials science words**
# - **Transistor:** a tiny electronic switch. Chips are made of billions of them wired together.
# - **Exponential growth:** growth where the amount is multiplied by the same factor in every equal
#   time step (as opposed to *adding* the same amount each step, which is linear growth).
# - **Doubling time:** how long it takes an exponentially growing quantity to multiply by 2.
# - **Monolayer:** one repeating layer of a material's structure — the thinnest a material can be
#   and still exist as that solid. A monolayer can hold more than one plane of atoms: a MoS2
#   monolayer is a three-plane S–Mo–S sandwich, about 0.65 nm thick.
# - **2D material:** a material that naturally forms in single-layer or few-layer sheets held
#   together by weak forces, like MoS2 (molybdenum disulfide) or WSe2 (tungsten diselenide).
# - **Electronic band gap:** the minimum energy needed to free an electron inside a material so it
#   can carry current. Measured in **electron-volts (eV)**.
# - **Optical energy:** the energy of the main photon a material absorbs or emits. It's close to,
#   but not exactly the same as, the electronic band gap, and it shifts with substrate, strain, and
#   temperature.
# - **Photon:** a single particle of light. Its energy (eV) sets its **wavelength** (color, in nm) —
#   higher energy means shorter wavelength.
# - **Optical fiber:** a hair-thin glass strand that carries data as pulses of infrared light,
#   used to connect computers inside (and between) data centers.
# - **Superconductor:** a material that, below a **critical temperature**, carries electric current
#   with *exactly zero* electrical resistance — no energy wasted as heat in the wire itself.
#   Reaching that critical temperature still takes real cryogenic cooling, which uses energy.
# - **Electrical resistance:** how much a material "fights" the flow of current; fighting current
#   wastes energy as heat, the same way rubbing your hands together warms them up.

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

# %% [markdown]
# ## Part 1 — How fast do transistor counts grow?
#
# `chips_timeline.csv` lists real, publicly announced transistor counts for famous chips, from
# Intel's first microprocessor (1971) to a modern AI chip (2024).

# %%
chips = load_table("chips_timeline")
chips[["year", "chip", "maker", "transistors", "used_for"]]

# %% [markdown]
# ### Task 1 (Core) — Guess the doubling time
# A simple model for this kind of growth is
#
# $$N(t) = N_0 \cdot 2^{\,(t - 1971)/d}$$
#
# where $N_0 = 2{,}300$ (the 4004's transistor count in 1971) and $d$ is the **doubling time** in
# years — how many years it takes the count to double. The static plot below compares two candidate
# values of $d$ against the real chips; decide which tracks the data better. Watch both plots: the
# left one is a normal (linear) y-axis, the right one is a **log** y-axis, where equal steps mean
# "×10," not "+10." If your notebook's interactive widgets are working, the slider further down lets
# you try any value of $d$.

# %%
# @title Helper code (just run this)
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import ipywidgets as widgets

BLUE, ORANGE = "#0072B2", "#E69F00"  # colour-blind-safe (Okabe-Ito palette)

def _doubling_figure(chips, ds, colors, title):
    t0, N0 = 1971, 2300
    t_grid = np.linspace(1971, 2026, 200)
    fig = make_subplots(rows=1, cols=2, subplot_titles=("Linear y-axis", "Log y-axis"))
    for col in (1, 2):
        fig.add_trace(go.Scatter(x=chips.year, y=chips.transistors, mode="markers",
                                  name="real chips", marker=dict(size=9, color=ORANGE),
                                  showlegend=(col == 1)), row=1, col=col)
        for d, color in zip(ds, colors):
            N_model = N0 * 2 ** ((t_grid - t0) / d)
            fig.add_trace(go.Scatter(x=t_grid, y=N_model, mode="lines", name=f"d = {d:g} yr",
                                      line=dict(color=color, width=3), showlegend=(col == 1)),
                          row=1, col=col)
    fig.update_yaxes(type="log", row=1, col=2)
    fig.update_xaxes(title_text="year")
    fig.update_yaxes(title_text="transistors", row=1, col=1)
    fig.update_yaxes(title_text="transistors (log scale)", row=1, col=2)
    fig.update_layout(height=430, title=title, margin=dict(t=80))
    fig.show()

def plot_doubling_static(chips, ds=(2.0, 3.0)):
    """A static (non-widget) comparison of a couple of candidate doubling times."""
    colors = [BLUE, "#009E73"]  # colour-blind-safe (Okabe-Ito) blue and green
    title = "N(t) = 2300 x 2^((t-1971)/d) for d = " + " and ".join(f"{d:g}" for d in ds) + " years"
    _doubling_figure(chips, ds, colors, title)

def plot_doubling_guess(chips, d):
    _doubling_figure(chips, [d], [BLUE], f"N(t) = 2300 x 2^((t-1971)/d),  d = {d:g} years")

def explore_doubling(chips):
    widgets.interact(lambda d: plot_doubling_guess(chips, d),
                      d=widgets.FloatSlider(value=3.0, min=0.5, max=6.0, step=0.1,
                                            description="d (years)", continuous_update=False))

# %%
plot_doubling_static(chips)  # static fallback — works even if interactive widgets don't load

# %% [markdown]
# **Optional:** if widgets are working in your notebook, try any value of $d$ with the slider below.

# %%
explore_doubling(chips)

# %%
my_doubling_guess = 2.0  # <-- change me: your best-fit guess for d, in years

# %% [markdown]
# ### Task 2 (Explore) — Fit it properly
# Eyeballing a slider is a guess. To actually **fit** $d$, take log base 2 of both sides:
# $\log_2 N = \log_2 N_0 + (t - 1971)/d$ — a straight line in $(t, \log_2 N)$ with slope $1/d$.
# `numpy.polyfit` finds that best-fit line.

# %%
log2_N = np.log2(chips["transistors"].to_numpy(dtype=float))
slope, intercept = np.polyfit(chips["year"].to_numpy(dtype=float) - 1971, log2_N, 1)
d_fit = 1 / slope
print(f"Fitted doubling time: d = {d_fit:.2f} years")
print(f"Your slider guess:    d = {my_doubling_guess:.2f} years")

if abs(my_doubling_guess - d_fit) <= 1.0:
    print("Nice — your guess is close to the fitted value.")
else:
    print(f"The real fit is about {d_fit:.1f} years; try the slider again with that in mind.")

# %% [markdown]
# **Selection check:** `chips_timeline.csv` is a hand-picked set of famous chips, not a random or
# complete series. How much does the fit change if you drop the non-Intel chips?

# %%
intel_only = chips[chips["maker"] == "Intel"]
slope_intel, _ = np.polyfit(intel_only["year"].to_numpy(dtype=float) - 1971,
                            np.log2(intel_only["transistors"].to_numpy(dtype=float)), 1)
print(f"Doubling time using only the {len(intel_only)} Intel chips: {1 / slope_intel:.2f} years "
      f"(vs {d_fit:.2f} years using all {len(chips)} hand-picked chips)")

# %% [markdown]
# > **Scientist's note:** A doubling time near 2 years matches what's usually called "Moore's
# > law." But Moore's law is an **observed historical trend** from real engineering progress, not a
# > law of physics like gravity — nothing guarantees it continues. It also only measures transistor
# > *count*. More transistors is not the same thing as more AI capability: how those transistors are
# > wired together, how fast data moves between them, and how much energy they use all matter too.
# >
# > `chips_timeline.csv` is also a **hand-picked** set of famous chips, not a random or complete
# > series — it moves from single-die Intel CPUs to Apple phone/laptop chips to NVIDIA AI
# > accelerators, and the last row (B200) packages **two dies**. That makes $d_\text{fit}$ a
# > selection-sensitive estimate, not an independent verification of Moore's law — the Intel-only
# > fit above gives a different number from the same underlying idea.

# %% [markdown]
# ## Part 2 — Why go atom-thin?
#
# A transistor's **channel** is the material current flows through when it's switched on. A
# thinner channel lets engineers build smaller, more tightly packed switches — but "thin" can mean
# several different things that are easy to mix up:
# - **Channel thickness** — how thick the current-carrying layer itself is (what this section compares).
# - **Gate length** — how long the switch is along the direction current flows; a separate dimension.
# - The marketing **"node" name** (like "3 nm") — a naming convention today, not a direct
#   measurement of any single physical feature.
# - **Manufacturability** — whether a thin channel can be built, wired up, and mass-produced
#   reliably at scale, which is a different challenge from how thin a single lab device can be made.
#
# For this section we'll use **5 nm** as a deliberately chosen, illustrative silicon channel
# thickness — not a record. Research silicon channels well under 1 nm have been reported, but "how
# thin can a lab make silicon" and "how thin is manufacturable at scale" are different questions. A
# single monolayer of MoS2 is naturally just 0.65 nm thick and still works as a channel, because a
# 2D material has no "extra" atoms above or below the working layer.

# %% [markdown]
# ### Task 3 (Core) — Ratio problem (hypothetical)
# How many MoS2 monolayers (0.65 nm each) would it take to match an illustrative ~5 nm silicon
# channel? (This is a hypothetical ratio, not a claim about any specific manufactured chip.)

# %%
si_channel_nm = 5.0      # <-- change me: try other silicon research figures, e.g. 3 or 10
mos2_layer_nm = 0.65

layers_to_match = si_channel_nm / mos2_layer_nm
print(f"{si_channel_nm} nm silicon is about {layers_to_match:.1f} MoS2 monolayers thick.")
print(f"One MoS2 layer is about {si_channel_nm / mos2_layer_nm:.1f}x thinner than that silicon channel.")

# %% [markdown]
# > **Scientist's note:** "~5 nm" is a deliberately chosen illustrative figure, **not** the
# > thinnest silicon channel ever reported — some research devices have used silicon channels under
# > 1 nm thick. Real silicon transistors also use complex 3D fin or wrap-around shapes, not one flat
# > layer, so there is no single official "silicon channel thickness" to quote precisely, and this
# > ratio task stays a hypothetical comparison, not a claim about any real device's exact dimensions.

# %% [markdown]
# ### Task 4 (Core) — Stacking as multiplication
# One real 2DCC data package is titled *"Wafer-scale MOCVD TMD films used for 3D Monolithic
# Integration"* — growing MoS2 as a flat, wafer-wide film so multiple device layers could someday
# be **stacked** directly on top of each other, all within the same chip footprint. Here's that
# MoS2 film:

# %%
gallery = load_gallery()
surface_3d(gallery["mos2_film"]).show()

# %% [markdown]
# If one layer packs some number of devices into a given footprint, and you stack $k$ *identical*
# layers on that same footprint, the simplest model is just multiplication: $\text{total} = k \times
# \text{(devices in one layer)}$.

# %%
one_layer_devices = 500_000  # <-- change me: a made-up devices-per-layer number, for illustration only
stack_layers = 4             # <-- change me: try 2, 4, or 8 layers

total_devices = stack_layers * one_layer_devices
print(f"{stack_layers} stacked layers x {one_layer_devices:,} devices/layer = {total_devices:,} devices "
      f"in the same footprint as one layer.")

# %% [markdown]
# > **Scientist's note:** `one_layer_devices` above is a made-up round number, **not** a measured
# > device density — this is only a multiplication model to show how stacking scales devices per
# > footprint. Real monolithic 3D chips also have to solve heat removal, wiring between layers, and
# > manufacturing yield, none of which this simple model includes.

# %% [markdown]
# ## Part 3 — The color of light a monolayer makes
#
# A photon's energy $E$ (eV) and wavelength $\lambda$ (nm) are related by
# $\lambda = 1240 / E$ — an **inverse proportion**: higher energy, shorter (bluer) wavelength.
# `materials_reference.csv` lists each monolayer's **optical energy** in eV — the energy of the
# main light a single layer absorbs and emits. That's close to, but not exactly the same as, the
# **electronic band gap** (the energy needed to free a current-carrying electron): light striking a
# material also has to overcome the attraction between the freed electron and the "hole" it leaves
# behind. The colour a monolayer shows can also shift with its substrate, strain, and temperature.

# %% [markdown]
# ### Task 5 (Core)
# Compute the wavelength for every 2D material that has a listed monolayer optical energy.

# %%
materials = load_table("materials_reference")
# optical_energy_monolayer_eV is blank for materials with no single meaningful classroom value
# (including graphene, a semimetal with no gap) — filtering for values greater than 0 keeps only
# the materials that have a listed optical energy.
glowing = materials[materials["optical_energy_monolayer_eV"] > 0].copy()
glowing["wavelength_nm"] = 1240 / glowing["optical_energy_monolayer_eV"]
glowing[["material", "name", "optical_energy_monolayer_eV", "wavelength_nm"]]

# %%
# @title Helper code (just run this)
import matplotlib.pyplot as plt

def wavelength_to_rgb(wl, gamma=0.8):
    """Approximate visible-light RGB for a wavelength (nm); gray if outside human vision."""
    if wl < 380 or wl > 750:
        return (0.55, 0.55, 0.55)
    if wl < 440:
        r, g, b = -(wl - 440) / 60, 0.0, 1.0
    elif wl < 490:
        r, g, b = 0.0, (wl - 440) / 50, 1.0
    elif wl < 510:
        r, g, b = 0.0, 1.0, -(wl - 510) / 20
    elif wl < 580:
        r, g, b = (wl - 510) / 70, 1.0, 0.0
    elif wl < 645:
        r, g, b = 1.0, -(wl - 645) / 65, 0.0
    else:
        r, g, b = 1.0, 0.0, 0.0
    factor = 0.3 + 0.7 * (750 - wl) / (750 - 645) if wl >= 645 else 1.0
    return tuple((max(c, 0) * factor) ** gamma for c in (r, g, b))

def color_name(wl):
    for hi, name in ((450, "violet"), (495, "blue"), (570, "green"), (590, "yellow"),
                     (625, "orange"), (750, "red")):
        if wl < hi:
            return name
    return "near-infrared (outside human vision)"

def plot_spectrum(df):
    grid = np.linspace(380, 900, 400)
    image = np.array([[wavelength_to_rgb(w) for w in grid]])
    fig, ax = plt.subplots(figsize=(9, 3.2))
    ax.imshow(image, extent=[grid.min(), grid.max(), 0, 1], aspect="auto")
    for _, row in df.iterrows():
        wl = row["wavelength_nm"]
        ax.axvline(wl, color="black", lw=1.5)
        ax.text(wl, 1.05, f"{row['material']}\n{row['optical_energy_monolayer_eV']:g} eV, {wl:.0f} nm",
                ha="center", va="bottom", fontsize=9)
    ax.set(xlabel="wavelength (nm)", xlim=(380, 900), ylim=(0, 1))
    ax.set_yticks([])
    ax.set_title("Color of light matching each monolayer's optical energy")
    plt.tight_layout()
    plt.show()
    for _, row in df.iterrows():
        print(f"{row['material']}: {row['optical_energy_monolayer_eV']:g} eV -> {row['wavelength_nm']:.0f} nm "
              f"({color_name(row['wavelength_nm'])})")

# %%
plot_spectrum(glowing)

# %% [markdown]
# > **Scientist's note:** This is the color a photon *at exactly the listed optical energy* would
# > be. Whether a real device actually emits light efficiently at that color depends on defects,
# > temperature, and device design — a material that can *absorb* photons above its optical energy
# > does not automatically *emit* light well at that same energy (emission and detection are
# > different processes). And remember, optical energy is not the same quantity as the electronic
# > band gap used to talk about current flow (see the Part 3 intro).

# %% [markdown]
# ### Task 6 (Explore) — Data-center light
# AI chips inside (and between) data centers often talk to each other over optical fibers carrying
# infrared light near 1310 nm and 1550 nm. What photon energies are those, and how do they compare
# to the monolayer optical energies above?

# %%
for wl in (1310, 1550):  # <-- change me: try other fiber wavelengths, e.g. 850
    print(f"{wl} nm fiber light carries photons of about {1240 / wl:.2f} eV")

smallest = glowing.loc[glowing["optical_energy_monolayer_eV"].idxmin()]
print(f"\nSmallest monolayer optical energy above: {smallest['optical_energy_monolayer_eV']:.2f} eV "
      f"({smallest['material']}) — every fiber-light photon here has noticeably less energy than "
      f"any of these optical energies.")

# %% [markdown]
# ## Part 4 — Superconductors: zero resistance, but real cooling costs
#
# `superconductors.csv` lists **critical temperatures** ($T_c$): below $T_c$, a material carries
# current with *zero* electrical resistance. Watch the direction of cause and effect: a
# superconductor doesn't cool anything — it has to *be* cooled, with real refrigeration equipment
# that itself uses energy, before it becomes a superconductor.

# %% [markdown]
# ### Task 7 (Core) — Temperature conversions
# Liquid nitrogen, a cheap coolant labs use, boils at 77 K. Convert that to Celsius and Fahrenheit:
# $$C = K - 273.15 \qquad F = \tfrac{9}{5}C + 32$$

# %%
temp_K = 77  # <-- change me: try 4.2 K (liquid helium) or a superconductor's own Tc
temp_C = temp_K - 273.15
temp_F = 9 / 5 * temp_C + 32
print(f"{temp_K} K = {temp_C:.2f} C = {temp_F:.2f} F")

# %% [markdown]
# ### Task 8 (Explore) — Critical temperature vs. year discovered

# %%
sconductors = load_table("superconductors")
sconductors["critical_temp_C"] = sconductors["critical_temp_K"] - 273.15
sconductors["critical_temp_F"] = 9 / 5 * sconductors["critical_temp_C"] + 32
print("Note: single-layer FeSe on SrTiO3 has no single critical_temp_K — it's stored as a "
      "tc_low_K-tc_high_K range instead (see the plot below).")
sconductors[["material", "year_discovered", "critical_temp_K", "tc_low_K", "tc_high_K", "criterion",
             "critical_temp_C", "critical_temp_F"]]

# %%
# @title Helper code (just run this)
PINK = "#CC79A7"  # colour-blind-safe (Okabe-Ito palette)

def plot_tc_history(df):
    solid = df[df["critical_temp_K"].notna()]
    ranged = df[df["critical_temp_K"].isna()]  # reported signature given as a range, not a point

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=solid["year_discovered"], y=solid["critical_temp_K"], mode="markers+text",
                              text=solid["material"], textposition="top center",
                              marker=dict(size=11, color=ORANGE, symbol="circle"),
                              name="zero-resistance Tc"))
    if len(ranged):
        mid = (ranged["tc_low_K"] + ranged["tc_high_K"]) / 2
        fig.add_trace(go.Scatter(
            x=ranged["year_discovered"], y=mid, mode="markers+text",
            text=ranged["material"], textposition="bottom center",
            marker=dict(size=13, color=PINK, symbol="diamond"),
            error_y=dict(type="data", symmetric=False,
                        array=ranged["tc_high_K"] - mid, arrayminus=mid - ranged["tc_low_K"]),
            name="reported signature (range, not a zero-resistance point)"))
    fig.add_hline(y=77, line=dict(color=BLUE, dash="dash"),
                  annotation_text="77 K — liquid nitrogen boils here", annotation_position="bottom right")
    fig.update_layout(xaxis_title="year discovered", yaxis_title="critical temperature (K)",
                      title="Higher points need less extreme cooling to reach Tc", height=460)
    fig.show()

# %%
plot_tc_history(sconductors)

# %% [markdown]
# ### See it happen: real FeSe films from the 2DCC (Explore, ~5 minutes)
# The points above are one number per material. Here are actual resistance-vs-temperature sweeps
# from four different FeSe thin films grown and measured at the 2DCC — real, noisy lab data.

# %%
fese_transport = load_extra("transport_fese.csv")  # sample_id, temperature_K, resistance_ohm
fese_summary = load_extra("transport_summary.csv")  # per-film summary, incl. T_zero_1pct_K
fese_summary

# %% [markdown]
# `T_zero_1pct_K` is the temperature where a film's resistance first drops to about 1% of its 40 K
# value — close enough to call "zero" for a real noisy measurement. A blank means the film never
# got that low in the range measured.

# %%
# @title Helper code (just run this)
GREEN = "#009E73"  # colour-blind-safe (Okabe-Ito palette)

def plot_fese_transport(df):
    fig = make_subplots(rows=1, cols=2, subplot_titles=("0-40 K (the transition)", "0-300 K (full range)"))
    colors = {20198: BLUE, 20199: ORANGE, 20200: GREEN, 20201: PINK}
    for sample_id, group in df.groupby("sample_id"):
        g = group.sort_values("temperature_K")
        color = colors.get(sample_id, "gray")
        fig.add_trace(go.Scatter(x=g.temperature_K, y=g.resistance_ohm, mode="lines+markers",
                                  name=str(sample_id), marker=dict(size=5, color=color),
                                  line=dict(color=color)), row=1, col=1)
        fig.add_trace(go.Scatter(x=g.temperature_K, y=g.resistance_ohm, mode="lines+markers",
                                  name=str(sample_id), marker=dict(size=4, color=color),
                                  line=dict(color=color), showlegend=False), row=1, col=2)
    fig.add_hline(y=0, line=dict(color="black", dash="dash"), row=1, col=1)
    fig.add_hline(y=0, line=dict(color="black", dash="dash"), row=1, col=2)
    fig.update_xaxes(title_text="temperature (K)", range=[0, 40], row=1, col=1)
    fig.update_xaxes(title_text="temperature (K)", range=[0, 300], row=1, col=2)
    fig.update_yaxes(title_text="resistance (ohm)")
    fig.update_layout(height=430, title="Real FeSe thin-film resistance vs. temperature (four 2DCC samples)",
                      legend_title="sample_id", margin=dict(t=80))
    fig.show()

plot_fese_transport(fese_transport)

# %% [markdown]
# From the plot (or the `T_zero_1pct_K` column above): about what temperature does each film first
# reach ~zero resistance? Which film never gets there in this data? How do these compare to bulk
# FeSe's 8 K critical temperature (from `superconductors.csv`)?

# %%
for _, row in fese_summary.iterrows():
    tz = row["T_zero_1pct_K"]
    if np.isnan(tz):
        print(f"sample {int(row['sample_id'])}: never reaches ~zero resistance down to "
              f"{row['lowest_T_measured_K']:g} K, the lowest temperature measured")
    else:
        print(f"sample {int(row['sample_id'])}: reaches ~zero resistance at about {tz:.2f} K")

# %% [markdown]
# > **Scientist's note:** These four films don't all agree with each other, or with bulk FeSe's 8 K.
# > Some reach zero resistance at noticeably higher temperatures than the bulk crystal; one film
# > doesn't reach zero at all within the range measured here. Comparing thin films (and their
# > substrate) to bulk crystals like this is exactly what scientists study — this notebook doesn't
# > try to explain *why* the temperature differs, only that real measurements show that it does.
#
# **One-line Ohm's law check:** using film 20198's actual measured resistance, and $V = IR$ with a
# small $I = 1\ \mu A$ test current, how does the voltage in its normal state (20 K) compare to its
# near-zero-resistance state (3 K)?

# %%
def resistance_near(df, sample_id, temp_K):
    """Nearest measured resistance for one sample near a target temperature."""
    g = df[df["sample_id"] == sample_id]
    return g.loc[(g["temperature_K"] - temp_K).abs().idxmin()]

current_A = 1e-6  # 1 microamp test current
row_20K = resistance_near(fese_transport, 20198, 20)
row_3K = resistance_near(fese_transport, 20198, 3)

v_20K = current_A * row_20K["resistance_ohm"]
v_3K = current_A * row_3K["resistance_ohm"]
print(f"Sample 20198 at {row_20K['temperature_K']:.2f} K: R = {row_20K['resistance_ohm']:.1f} ohm "
      f"-> V = {v_20K * 1000:.3f} mV")
print(f"Sample 20198 at {row_3K['temperature_K']:.2f} K:  R = {row_3K['resistance_ohm']:.4f} ohm "
      f"-> V = {v_3K * 1e6:.3f} uV")

# %% [markdown]
# > **Scientist's note:** Near "zero" resistance, real instruments still read tiny nonzero (even
# > slightly negative) numbers from measurement noise — that's the noise floor, not negative
# > resistance. The 20 K voltage is thousands of times larger than the 3 K voltage, consistent with
# > (not exactly) zero.

# %% [markdown]
# Here is a real FeSe (iron selenide) superconductor film from the 2DCC, grown on SrTiO3:

# %%
surface_3d(gallery["superconductor_blocks"]).show()

# %% [markdown]
# > **Scientist's note:** The single-layer FeSe/SrTiO3 point above is plotted as a **range** (the
# > diamond marker's error bar spans `tc_low_K` to `tc_high_K`), not one exact number — different
# > labs have reported different onset temperatures for this one-layer-thin film, and it's a
# > *reported superconducting signature*, not the same kind of measurement as the other materials'
# > zero-resistance $T_c$. Also: superconductors are **not** already wiring together AI data centers
# > today, and they don't cool anything themselves — reaching any of these critical temperatures
# > takes real cryogenic refrigeration, which uses energy. Cutting resistive losses in select future
# > wires or magnets is an active research direction, not current commercial use.

# %% [markdown]
# ### Task 9 (Explore/Extend) — Why zero resistance would matter for one wire
# A normal wire carrying current $I$ through resistance $R$ wastes power as heat: $P = I^2 R$.

# %%
current_A = 100    # <-- change me: amps through a normal (non-superconducting) wire
resistance_ohm = 0.01

heat_watts = current_A ** 2 * resistance_ohm
print(f"A normal wire: {current_A} A through {resistance_ohm} ohm wastes {heat_watts:.1f} W as heat.")
print("The same current through a superconductor (R = 0) wastes 0 W as heat in the wire itself.")

# %% [markdown]
# > **Scientist's note:** This is one made-up wire, not a data center. A real superconducting wire
# > still needs continuous cryogenic cooling (which uses energy), plus contacts, power conversion,
# > and support equipment that also have losses — so "R = 0 in this wire" does not mean "this system
# > uses zero energy," and it does not mean AI data centers already use superconductors. Whether
# > cutting resistive losses in select future wires or magnets would be worth its cooling cost is an
# > open engineering question this notebook doesn't have the data to answer.
#
# ---
#
# ### A separate exercise: how big is data-center electricity use?
# This next part is **unrelated to the superconductor wire above** — it's a scale exercise using
# real-world numbers, not evidence of any superconductor savings. The IEA estimates data centers
# used about 415 TWh of electricity in 2024 (about 1.5% of world
# electricity), projected to reach about 945 TWh by 2030 (see `SOURCES.md`).

# %%
twh_2024, twh_2030 = 415, 945
kwh_per_home = 10_500  # approximate U.S. average yearly household electricity use

pct_change = (twh_2030 - twh_2024) / twh_2024 * 100
homes_2024 = twh_2024 * 1e9 / kwh_per_home
homes_2030 = twh_2030 * 1e9 / kwh_per_home
print(f"Projected change, 2024 to 2030: about +{pct_change:.0f}%")
print(f"About {homes_2024/1e6:.0f} million U.S. homes' worth of electricity in 2024, "
      f"about {homes_2030/1e6:.0f} million by 2030 (both approximate).")

# %% [markdown]
# ## Part 5 — Which materials does the 2DCC actually grow?
#
# `samples.csv` has one row per public sample. Its `materials` column is entered by scientists, so
# a sample with more than one material lists them separated by `;` — you have to split it apart to
# count correctly.

# %%
samples = load_table("samples")
samples[["sample_id", "materials", "growth_method", "data_package"]].head()

# %%
# @title Helper code (just run this)
def count_material(df, material):
    """Count samples whose `materials` cell contains `material` as one of its ';'-separated names."""
    def has_it(cell):
        if not isinstance(cell, str):
            return False
        return material in [token.strip() for token in cell.split(";")]
    return int(df["materials"].apply(has_it).sum())

# %% [markdown]
# ### Task 10 (Core)

# %%
material_to_count = "MoS2"  # <-- change me: try "WS2", "WSe2", or "MoSe2"
print(f"{material_to_count}: {count_material(samples, material_to_count)} samples")

# %% [markdown]
# ### Task 11 (Extend)
# Count all four TMDs from the photonics section and compare them on a bar chart.

# %%
tmds = ["MoS2", "WS2", "WSe2", "MoSe2"]
counts = [count_material(samples, m) for m in tmds]

fig, ax = plt.subplots(figsize=(6, 4))
ax.bar(tmds, counts, color=BLUE)
ax.set(ylabel="number of samples", title="2DCC catalog samples by material")
for i, c in enumerate(counts):
    ax.text(i, c, str(c), ha="center", va="bottom")
plt.tight_layout()
plt.show()

# %% [markdown]
# ## Complexity dials
# - **Core:** Tasks 1, 3, 4, 5, 7, 10 — move the slider, change the marked variables, read the
#   plots.
# - **Explore:** Tasks 2, 6, 8, 9, plus the optional "See it happen" real-FeSe-films add-on after
#   Task 8 (~5 min) — fit the model, compare energies, read the Tc-vs-year plot.
# - **Extend:** Task 11 — open-ended comparison across all four TMDs.

# %% [markdown]
# ## Exit ticket
# Answer without writing any code.
#
# 1. If a chip's transistor count doubles about every 2 years, roughly what multiplying factor is
#    that after 10 years (how many doublings, and $2$ raised to that power)?
# 2. Between a 650 nm red photon and an 800 nm near-infrared photon, which one carries **more**
#    energy? How do you know from $\lambda = 1240/E$ without a calculator?
# 3. In your own words, why is "more transistors" not automatically "smarter AI," and why is it
#    wrong to say superconductors "cool" a data center — what do they actually need in order to
#    work, and what problem might they help with someday?
