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
# - Use ratio and multiplication models to see why atom-thin 2D materials interest chip designers.
# - Turn a 2D material's band gap into the color of light it can emit, and convert superconductor
#   temperatures between Kelvin, Celsius, and Fahrenheit.
#
# **Time:** about 45-50 minutes.
#
# **Materials science words**
# - **Transistor:** a tiny electronic switch. Chips are made of billions of them wired together.
# - **Exponential growth:** growth where the amount is multiplied by the same factor in every equal
#   time step (as opposed to *adding* the same amount each step, which is linear growth).
# - **Doubling time:** how long it takes an exponentially growing quantity to multiply by 2.
# - **Monolayer:** a layer of a material exactly one atom (or one unit cell) thick — as thin as a
#   material can be and still exist as a solid.
# - **2D material:** a material that naturally forms in single-atom-thick or few-atom-thick sheets
#   held together by weak forces, like MoS2 (molybdenum disulfide) or WSe2 (tungsten diselenide).
# - **Band gap:** the minimum energy needed to free an electron inside a material so it can carry
#   current or absorb/emit light. Measured in **electron-volts (eV)**.
# - **Photon:** a single particle of light. Its energy (eV) sets its **wavelength** (color, in nm) —
#   higher energy means shorter wavelength.
# - **Optical fiber:** a hair-thin glass strand that carries data as pulses of infrared light,
#   used to connect computers inside (and between) data centers.
# - **Superconductor:** a material that, below a **critical temperature**, carries electric current
#   with *exactly zero* electrical resistance — no energy wasted as heat.
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
# years — how many years it takes the count to double. Move the slider until your curve tracks the
# real chips. Watch both plots: the left one is a normal (linear) y-axis, the right one is a **log**
# y-axis, where equal steps mean "×10," not "+10."

# %%
# @title Helper code (just run this)
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import ipywidgets as widgets

BLUE, ORANGE = "#0072B2", "#E69F00"  # colour-blind-safe (Okabe-Ito palette)

def plot_doubling_guess(chips, d):
    t0, N0 = 1971, 2300
    t_grid = np.linspace(1971, 2026, 200)
    N_model = N0 * 2 ** ((t_grid - t0) / d)

    fig = make_subplots(rows=1, cols=2, subplot_titles=("Linear y-axis", "Log y-axis"))
    for col in (1, 2):
        fig.add_trace(go.Scatter(x=chips.year, y=chips.transistors, mode="markers",
                                  name="real chips", marker=dict(size=9, color=ORANGE),
                                  showlegend=(col == 1)), row=1, col=col)
        fig.add_trace(go.Scatter(x=t_grid, y=N_model, mode="lines", name=f"your model, d={d:g} yr",
                                  line=dict(color=BLUE, width=3), showlegend=(col == 1)), row=1, col=col)
    fig.update_yaxes(type="log", row=1, col=2)
    fig.update_xaxes(title_text="year")
    fig.update_yaxes(title_text="transistors", row=1, col=1)
    fig.update_yaxes(title_text="transistors (log scale)", row=1, col=2)
    fig.update_layout(height=430, title=f"N(t) = 2300 x 2^((t-1971)/d),  d = {d:g} years",
                       margin=dict(t=80))
    fig.show()

def explore_doubling(chips):
    widgets.interact(lambda d: plot_doubling_guess(chips, d),
                      d=widgets.FloatSlider(value=3.0, min=0.5, max=6.0, step=0.1,
                                            description="d (years)", continuous_update=False))

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
# > **Scientist's note:** A doubling time near 2 years matches what's usually called "Moore's
# > law." But Moore's law is an **observed historical trend** from real engineering progress, not a
# > law of physics like gravity — nothing guarantees it continues. It also only measures transistor
# > *count*. More transistors is not the same thing as more AI capability: how those transistors are
# > wired together, how fast data moves between them, and how much energy they use all matter too.

# %% [markdown]
# ## Part 2 — Why go atom-thin?
#
# A transistor's **channel** is the material current flows through when it's switched on. A
# thinner channel lets engineers build smaller, more tightly packed switches. Silicon channels are
# three-dimensional blocks — even the thinnest research silicon channels are only reported down to
# roughly 5 nm before the transistor becomes hard to switch off cleanly. A single monolayer of MoS2
# is naturally just 0.65 nm thick and still works as a channel, because a 2D material has no
# "extra" atoms above or below the working layer.

# %% [markdown]
# ### Task 3 (Core) — Ratio problem
# How many MoS2 monolayers (0.65 nm each) would it take to match a ~5 nm silicon research channel?

# %%
si_channel_nm = 5.0      # <-- change me: try other silicon research figures, e.g. 3 or 10
mos2_layer_nm = 0.65

layers_to_match = si_channel_nm / mos2_layer_nm
print(f"{si_channel_nm} nm silicon is about {layers_to_match:.1f} MoS2 monolayers thick.")
print(f"One MoS2 layer is about {si_channel_nm / mos2_layer_nm:.1f}x thinner than that silicon channel.")

# %% [markdown]
# > **Scientist's note:** "~5 nm" is a rough, order-of-magnitude research figure for illustration —
# > real silicon transistors use complex 3D fin or wrap-around shapes, not one flat layer, so there
# > is no single official "silicon channel thickness" to quote precisely.

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
# `materials_reference.csv` lists each monolayer's band gap in eV.

# %% [markdown]
# ### Task 5 (Core)
# Compute the wavelength for every 2D material that has a listed monolayer band gap.

# %%
materials = load_table("materials_reference")
# band_gap_monolayer_eV == 0 (graphene, a semimetal) is a real value, not a missing one — but a
# zero gap has no finite wavelength, so it doesn't belong in a "color of light" table.
glowing = materials[materials["band_gap_monolayer_eV"] > 0].copy()
glowing["wavelength_nm"] = 1240 / glowing["band_gap_monolayer_eV"]
glowing[["material", "name", "band_gap_monolayer_eV", "wavelength_nm"]]

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
        ax.text(wl, 1.05, f"{row['material']}\n{row['band_gap_monolayer_eV']:g} eV, {wl:.0f} nm",
                ha="center", va="bottom", fontsize=9)
    ax.set(xlabel="wavelength (nm)", xlim=(380, 900), ylim=(0, 1))
    ax.set_yticks([])
    ax.set_title("Color of light matching each monolayer's band gap")
    plt.tight_layout()
    plt.show()
    for _, row in df.iterrows():
        print(f"{row['material']}: {row['band_gap_monolayer_eV']:g} eV -> {row['wavelength_nm']:.0f} nm "
              f"({color_name(row['wavelength_nm'])})")

# %%
plot_spectrum(glowing)

# %% [markdown]
# > **Scientist's note:** This is the color a photon *at exactly the band-gap energy* would be.
# > Whether a real device actually emits light efficiently at that color depends on defects,
# > temperature, and device design — a material that can *absorb* photons above its band gap does
# > not automatically *emit* light well at that same energy (emission and detection are different
# > processes).

# %% [markdown]
# ### Task 6 (Explore) — Data-center light
# AI chips inside (and between) data centers often talk to each other over optical fibers carrying
# infrared light near 1310 nm and 1550 nm. What photon energies are those, and how do they compare
# to the monolayer band gaps above?

# %%
for wl in (1310, 1550):  # <-- change me: try other fiber wavelengths, e.g. 850
    print(f"{wl} nm fiber light carries photons of about {1240 / wl:.2f} eV")

smallest = glowing.loc[glowing["band_gap_monolayer_eV"].idxmin()]
print(f"\nSmallest monolayer band gap above: {smallest['band_gap_monolayer_eV']:.2f} eV "
      f"({smallest['material']}) — every fiber-light photon here has noticeably less energy than "
      f"any of these gaps.")

# %% [markdown]
# ## Part 4 — Superconductors and the cold-electricity problem
#
# `superconductors.csv` lists **critical temperatures** ($T_c$): below $T_c$, a material carries
# current with *zero* electrical resistance.

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
sconductors[["material", "year_discovered", "critical_temp_K", "critical_temp_C", "critical_temp_F"]]

# %%
# @title Helper code (just run this)
def plot_tc_history(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["year_discovered"], y=df["critical_temp_K"], mode="markers+text",
                              text=df["material"], textposition="top center",
                              marker=dict(size=11, color=ORANGE)))
    fig.add_hline(y=77, line=dict(color=BLUE, dash="dash"),
                  annotation_text="77 K — liquid nitrogen boils here", annotation_position="bottom right")
    fig.update_layout(xaxis_title="year discovered", yaxis_title="critical temperature (K)",
                      title="Higher points need less extreme cooling", height=460)
    fig.show()

# %%
plot_tc_history(sconductors)

# %% [markdown]
# Here is a real FeSe (iron selenide) superconductor film from the 2DCC, grown on SrTiO3:

# %%
surface_3d(gallery["superconductor_blocks"]).show()

# %% [markdown]
# > **Scientist's note:** The single-layer FeSe/SrTiO3 row's $T_c$ is a *range* — different labs
# > have reported different onset temperatures for this one-atom-thin film, so treat it as
# > approximate. Also: superconductors are **not** already wiring together AI data centers today.
# > Zero-resistance materials are an active research direction for a *possible future* — this data
# > does not show them in current commercial use.

# %% [markdown]
# ### Task 9 (Explore/Extend) — Why zero resistance would matter
# A normal wire carrying current $I$ through resistance $R$ wastes power as heat: $P = I^2 R$.

# %%
current_A = 100    # <-- change me: amps through a normal (non-superconducting) wire
resistance_ohm = 0.01

heat_watts = current_A ** 2 * resistance_ohm
print(f"A normal wire: {current_A} A through {resistance_ohm} ohm wastes {heat_watts:.1f} W as heat.")
print("The same current through a superconductor (R = 0) wastes 0 W as heat.")

# %% [markdown]
# The IEA estimates data centers used about 415 TWh of electricity in 2024 (about 1.5% of world
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
# - **Explore:** Tasks 2, 6, 8, 9 — fit the model, compare energies, read the Tc-vs-year plot.
# - **Extend:** Task 11 — open-ended comparison across all four TMDs.

# %% [markdown]
# ## Exit ticket
# Answer without writing any code.
#
# 1. If a chip's transistor count doubles about every 2 years, roughly what multiplying factor is
#    that after 10 years (how many doublings, and $2$ raised to that power)?
# 2. Between a 650 nm red photon and an 800 nm near-infrared photon, which one carries **more**
#    energy? How do you know from $\lambda = 1240/E$ without a calculator?
# 3. In your own words, why is "more transistors" not automatically "smarter AI," and why can't we
#    say superconductors are already cooling today's AI data centers?
