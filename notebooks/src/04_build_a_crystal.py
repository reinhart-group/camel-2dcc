# %% [markdown]
# # Build a Crystal: Reading a Real Recipe as a Graph
#
# Growing a 2D crystal is a lot like cooking, except the "ingredients" are atoms and the "oven" is
# a furnace or a vacuum chamber. Every real crystal grown at Penn State's 2D Crystal Consortium
# (2DCC) follows a written **recipe**: an exact sequence of steps, each with a duration,
# temperature, and pressure. Two very different kitchens show up in this notebook:
# - **MOCVD** (metal-organic chemical vapor deposition): gaseous metal-organic and chalcogen
#   precursors react on a heated substrate, and can build up one- or few-layer films. *This*
#   recipe's setpoint happens to be 1000 °C — that's a choice for this material, not a rule for
#   every MOCVD recipe.
# - **Hybrid MBE** (molecular beam epitaxy): controlled beams of atoms or molecules, aimed at a
#   wafer inside a high- or ultra-high-vacuum chamber — so empty that the beams travel in a
#   straight line without bumping into air molecules first — sometimes combined with a precursor
#   gas (that's the "hybrid" part).
#
# In this notebook you'll turn one real MOCVD recipe into a **piecewise graph**, build a
# hypothetical linear model of its temperature ramp, and use that model to make a conditional
# prediction. Then you'll see why a blank cell in a data table is dangerous to guess at, and use
# real pressure numbers to see just how different "empty" is between a MOCVD chamber and an MBE
# chamber.
#
# **What you'll do**
# - Turn a table of recipe steps into cumulative time, then into a piecewise temperature-vs-time
#   graph, and find the slope of a *hypothetical* linear model of the ramp (°C/min).
# - Convert 1000 °C between Celsius, Kelvin, and Fahrenheit, and compare pressures that span
#   *eleven* orders of magnitude using scientific notation.
# - Use a dropdown to explore a few contrasting real MoS2 recipes, then look honestly at whether
#   growth time predicts film roughness across ~300 real samples.
#
# **Time:** Tasks 1–5 (**Core**) take about 30 minutes and fit a 45-minute period with the exit
# ticket. Tasks 6–8 (**Explore**/**Extend**) are optional — use them for early finishers, or as
# homework, if time allows.
#
# **Materials science words**
# - **MOCVD / Hybrid MBE:** two different "recipes" for growing a 2D crystal — see above.
# - **Wafer / substrate:** the flat crystal disk (often sapphire, Al₂O₃) that the new film grows
#   on top of.
# - **Setpoint:** the temperature or pressure the furnace is *told* to hold. It is not necessarily
#   the exact value the sample itself experiences — the recipe records the setpoint, not a direct
#   measurement of the crystal.
# - **Anneal:** a heat-treatment step with no intended net deposition — holding a material at a
#   steady high temperature so its structure can settle, without the recipe aiming to add atoms.
# - **Ramp:** a step where a controlled variable (like temperature) changes steadily from one
#   value to another.
# - **Piecewise function:** a function built from different rules over different intervals — like
#   a recipe that ramps, then holds, then cools.
# - **Average rate of change:** how much a quantity changes divided by how much time passed — the
#   slope between two points. For a ramp, this is measured in °C per minute.
# - **Cumulative time:** the running total of time elapsed since the recipe started.
# - **Torr:** a unit of pressure. Normal air pressure at sea level is about 760 Torr.
# - **Correlation coefficient (r):** a number from −1 to 1 that measures how tightly two variables
#   follow a straight-line trend. Near 0 means no clear straight-line trend.

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
# ## Part 1 — Meet the crystal your recipe makes
#
# Sample **23451** is a real MoS₂ (molybdenum disulfide) film grown by MOCVD at 2DCC. Here is the
# actual surface an AFM measured after this recipe finished:

# %%
gallery = load_gallery()
surface_3d(gallery["mos2_film"], exaggeration=30).show()

# %% [markdown]
# The recipe you're about to graph shaped this surface — but it isn't the only thing that did.
# The substrate underneath, how the sample was handled and stored, its environment, and even how
# the AFM measurement itself was processed all leave a mark too. This notebook follows one
# possible connection (the recipe); it doesn't claim every bump has a recipe cause. Let's read it.
#
# ## Part 2 — The recipe as data
# `growth_recipes` has one row per real step from the 2DCC recipe database: how long the step
# lasted (`duration_min`), when it started (`start_min`, measured from the recipe's t = 0), the
# furnace setpoint (`temperature_C`), and the chamber pressure (`pressure_torr`).

# %%
import pandas as pd

recipes = load_table("growth_recipes")
SAMPLE_ID = 23451  # <-- change me later, in Part 7

recipe = (recipes[(recipes.sample_id == SAMPLE_ID) & (recipes.recipe_number == 1)]
          .sort_values("step_number").reset_index(drop=True))
recipe[["step_number", "step", "duration_min", "start_min", "temperature_C", "pressure_torr"]]

# %% [markdown]
# ### Task 1 (Core)
# `start_min` is already computed for you — but you can rebuild it yourself. The **running total**
# (cumulative sum) of `duration_min`, up through a given step, is the time that step *ends*. That
# end time, minus that step's own duration, should equal its `start_min`.

# %%
import numpy as np

my_end_min = recipe["duration_min"].cumsum()          # <-- change me: try building this a different way
my_start_min = my_end_min - recipe["duration_min"]
print("my computed start times:", my_start_min.round(2).tolist())
print("actual start_min column:", recipe["start_min"].tolist())

# %%
# @title Check yourself
if np.allclose(my_start_min, recipe["start_min"]):
    print("✅ Your running total matches start_min exactly!")
else:
    print("❌ Not matching yet — check that you're subtracting each step's OWN duration.")

# %% [markdown]
# ## Part 3 — Graphing the recipe
# A recipe like this is a **piecewise function** of time: temperature follows a different rule on
# each step — flat during a hold or anneal, sloped during a ramp.

# %%
# @title Helper code (just run this)
import matplotlib.pyplot as plt

COLOR_A = "#0072B2"  # blue — colour-blind-safe (Okabe-Ito palette)
COLOR_B = "#E69F00"  # orange

ROOM_TEMP_C = 25.0  # <-- an ASSUMPTION: not measured, not in the data. Furnaces start near room temp.

def timeline_xy(rec, room_temp_C=ROOM_TEMP_C, treat_missing_as_zero=False):
    """Turn one recipe (sorted by step_number) into (time_min, temperature_C) points for
    plotting. A step named "Ramp..." is drawn as a straight line from the last known
    temperature up to its listed temperature. Steps with a blank temperature_C are left as a
    GAP in the line (missing is not zero) unless treat_missing_as_zero=True."""
    xs, ys, prev_T = [], [], room_temp_C
    for _, row in rec.iterrows():
        t0, t1, T = row["start_min"], row["start_min"] + row["duration_min"], row["temperature_C"]
        if pd.isna(T):
            if treat_missing_as_zero:
                xs += [t0, t1]; ys += [0.0, 0.0]
                prev_T = 0.0
            else:
                xs.append(np.nan); ys.append(np.nan)  # matplotlib breaks the line at a NaN
                prev_T = np.nan
            continue
        is_ramp = "ramp" in str(row["step"]).lower()
        start_T = prev_T if (is_ramp and not pd.isna(prev_T)) else T
        xs += [t0, t1]; ys += [start_T, T]
        prev_T = T
    return np.array(xs), np.array(ys)

def plot_timeline(xs, ys, title, color=COLOR_A, ax=None):
    own_fig = ax is None
    if own_fig:
        fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(xs, ys, color=color, lw=2, marker="o", ms=3)
    ax.set(xlabel="cumulative time (min)", ylabel="temperature (°C)", title=title)
    ax.grid(alpha=0.3)
    if own_fig:
        plt.tight_layout()
        plt.show()

# %%
xs, ys = timeline_xy(recipe)
plot_timeline(xs, ys, title=f"Sample {SAMPLE_ID} — temperature vs. cumulative time")

# %% [markdown]
# ### Task 2 (Core)
# Look at the recipe table from Part 2 and the graph above.
#
# **Your answer:** Which step is the ramp? What are its start and end time (minutes), and its end
# temperature (°C)? (We don't have a *measured* starting temperature for the ramp — the recipe's
# first row is already at 1000 °C. For Task 3, we'll build a hypothetical model that *assumes* it
# starts at room temperature, about 25 °C, since that's how a furnace often begins its day. State
# that assumption in your answer, and note that it's an assumption, not a measurement.)
#
# _(write your answer here)_

# %% [markdown]
# ### Task 3 (Core) — A hypothetical linear model of the ramp
# We don't have a measured starting temperature, so **if the ramp were linear and started at
# 25 °C**, it would follow `temperature = ROOM_TEMP_C + slope × time`. Find the slope this
# hypothetical model implies (°C per minute), then use the model to estimate when the furnace
# would cross 500 °C. Both numbers are *conditional on the 25 °C assumption* — not measurements.

# %%
ramp = recipe[recipe["step"].str.contains("ramp", case=False)].iloc[0]  # <-- change me if you like
slope = (ramp["temperature_C"] - ROOM_TEMP_C) / ramp["duration_min"]
print(f"ramp: {ramp['step']!r}, {ramp['duration_min']:g} min, "
      f"IF it started at {ROOM_TEMP_C:g} °C -> {ramp['temperature_C']:g} °C")
print(f"hypothetical slope (average rate of change) ≈ {slope:.2f} °C per minute")

# %%
def T(t):
    """T(t) = 25 + slope * t  — a HYPOTHETICAL linear model of the ramp, assuming it started at
    ROOM_TEMP_C. Not a measured function — change ROOM_TEMP_C and this model changes too."""
    return ROOM_TEMP_C + slope * t

t_500 = (500 - ROOM_TEMP_C) / slope   # <-- change me: solve T(t) = 500 for t, a different way if you want
print(f"under this model, the furnace would cross 500 °C at about t ≈ {t_500:.2f} minutes "
      f"(a conditional estimate, not a measurement)")
print(f"check: T({t_500:.2f}) = {T(t_500):.1f} °C")

# %% [markdown]
# **Quick comparison — change one number.** The slope and the 500 °C crossing both came from
# assuming the ramp started at 25 °C. What if the furnace hadn't fully cooled down and actually
# started at 200 °C instead?

# %%
ALT_ROOM_TEMP_C = 200.0  # <-- change me: try another assumed starting temperature
alt_slope = (ramp["temperature_C"] - ALT_ROOM_TEMP_C) / ramp["duration_min"]
alt_t_500 = (500 - ALT_ROOM_TEMP_C) / alt_slope
print(f"assumed start {ROOM_TEMP_C:g} °C -> hypothetical slope {slope:.2f} °C/min, "
      f"500 °C crossing ≈ {t_500:.2f} min")
print(f"assumed start {ALT_ROOM_TEMP_C:g} °C -> hypothetical slope {alt_slope:.2f} °C/min, "
      f"500 °C crossing ≈ {alt_t_500:.2f} min")
print("changing ONE assumed number changed both answers — neither version is a measurement.")

# %% [markdown]
# > **Scientist's note:** `temperature_C` is the furnace **setpoint** — what the furnace is told
# > to hold — not a direct measurement of the wafer's surface. Real hot-zone temperature can lag
# > or differ slightly from the setpoint. And the ramp's *starting* temperature isn't in the data
# > at all — the slope and the 500 °C crossing are outputs of a hypothetical model conditional on
# > an assumed starting temperature, not lab measurements of the crystal itself. The comparison
# > above shows how much that one assumption matters.

# %% [markdown]
# ## Part 4 — Missing is not zero
# Look again at the table in Part 2: `Cooldown 1` and `Cooldown 2` have a **blank**
# `temperature_C`. The recipe log simply didn't record a temperature during cooldown — that is
# not the same as the furnace being at 0 °C.

# %%
# @title Helper code (just run this)
fig, (ax_wrong, ax_right) = plt.subplots(1, 2, figsize=(12, 5), sharey=False)

xs_wrong, ys_wrong = timeline_xy(recipe, treat_missing_as_zero=True)
plot_timeline(xs_wrong, ys_wrong, "Wrong: blanks filled with 0", color=COLOR_B, ax=ax_wrong)

xs_right, ys_right = timeline_xy(recipe, treat_missing_as_zero=False)
plot_timeline(xs_right, ys_right, "Honest: blanks left as a gap", color=COLOR_A, ax=ax_right)

plt.tight_layout()
plt.show()

# %% [markdown]
# ### Task 4 (Core)
# **Your answer:** What claim does the left ("wrong") graph make about the furnace during
# cooldown that we have no evidence for? Why is leaving a gap in the right-hand graph more
# honest, even though it looks less complete?
#
# _(write your answer here)_

# %% [markdown]
# ## Part 5 — Same temperature, three scales
# This MOCVD recipe's growth setpoint is 1000 °C (other MOCVD recipes use other setpoints).
# Convert that one temperature to Kelvin and Fahrenheit.

# %%
T_C = 1000

T_K = T_C + 273.15       # <-- change me: fill in the °C -> K conversion
T_F = T_C * 9 / 5 + 32    # <-- change me: fill in the °C -> °F conversion
print(f"{T_C} °C  =  {T_K:g} K  =  {T_F:g} °F")

# %% [markdown]
# ## Part 6 — How empty is "empty"?
# MOCVD and Hybrid MBE run at wildly different pressures. Here's a real Hybrid MBE step for
# comparison — a SnSe deposition from 2DCC's Se-concentration study:

# %%
mbe_example = recipes[(recipes.sample_id == 39165) & (recipes["step"].str.contains("Deposition"))]
mbe_example[["sample_id", "step", "temperature_C", "pressure_torr"]]

# %%
# @title Helper code (just run this)
mbe_deposition = recipes[(recipes.growth_method == "Hybrid MBE") &
                         (recipes["step"].str.contains("Deposition", na=False))]
mbe_pressures = mbe_deposition["pressure_torr"].dropna()  # some deposition steps have no recorded pressure — skip, don't zero
mbe_pressure_torr = mbe_pressures.median()
print(f"typical Hybrid MBE deposition pressure (median of {len(mbe_pressures)} steps "
      f"with a recorded pressure, out of {len(mbe_deposition)} deposition steps total): "
      f"{mbe_pressure_torr:.2e} Torr")

# %% [markdown]
# ### Task 6 (Explore)
# Compare three pressures using scientific notation and **ratios** ("how many times emptier"),
# not subtraction — subtracting numbers this different in size doesn't mean much.

# %%
mocvd_pressure_torr = ramp["pressure_torr"]  # sample 23451's own MOCVD chamber pressure
air_pressure_torr = 760                       # <-- an assumption: normal sea-level air, not in the data

print(f"MOCVD chamber:  {mocvd_pressure_torr:.2e} Torr")
print(f"MBE chamber:    {mbe_pressure_torr:.2e} Torr")
print(f"air:            {air_pressure_torr:.2e} Torr")
print()
print(f"air is about {air_pressure_torr / mocvd_pressure_torr:.1f}x fuller than the MOCVD chamber")
print(f"the MOCVD chamber is about {mocvd_pressure_torr / mbe_pressure_torr:.2e}x fuller than the MBE chamber")
print(f"air is about {air_pressure_torr / mbe_pressure_torr:.2e}x fuller than the MBE chamber")

# %% [markdown]
# **Your answer:** Which comparison surprised you more — MOCVD vs. air, or MOCVD vs. MBE? Why do
# atoms aimed as a beam (MBE) need a chamber this much emptier than a MOCVD reaction chamber?
#
# _(write your answer here)_

# %% [markdown]
# ## Part 7 — Try a different recipe
# Hundreds of MoS₂ MOCVD samples are in the slice, but many have a blank ramp temperature or
# duration, or more than one step named "ramp" — the same missing-data problem from Part 4. The
# dropdown below is pre-filtered to 8 real recipes that each have exactly one usable ramp step, so
# every choice gives a real, computable slope.

# %%
# @title Helper code (just run this — the dropdown is below)
import ipywidgets as widgets
from IPython.display import display

# Curated, contrasting MoS2 MOCVD samples — each verified to have exactly one ramp step with a
# recorded duration AND temperature (no nan / IndexError possible from this list).
MOS2_SAMPLE_OPTIONS = [
    ("23451 — 1000 °C, 17.0 min (this notebook's default)", 23451),
    ("32465 — 600 °C, 17.0 min (slow ramp)", 32465),
    ("114343 — 850 °C, 13.5 min (fast, short ramp)", 114343),
    ("32466 — 600 °C, 10.3 min (short, lower-temperature ramp)", 32466),
    ("20398 — 900 °C, 17.0 min", 20398),
    ("32464 — 1000 °C, 17.0 min, 200 Torr (higher pressure than the rest)", 32464),
    ("44926 — 975 °C, 16.3 min", 44926),
    ("116271 — 1000 °C, 17.2 min", 116271),
]

def show_recipe(sample_id):
    rec = (recipes[(recipes.sample_id == sample_id) & (recipes.recipe_number == 1)]
           .sort_values("step_number").reset_index(drop=True))
    xs, ys = timeline_xy(rec)
    plot_timeline(xs, ys, title=f"Sample {sample_id} — temperature vs. cumulative time")
    display(rec[["step_number", "step", "duration_min", "start_min", "temperature_C", "pressure_torr"]])

widgets.interact(show_recipe, sample_id=widgets.Dropdown(options=MOS2_SAMPLE_OPTIONS, value=SAMPLE_ID,
                                                          description="Sample"));

# %% [markdown]
# *Static fallback* (in case the dropdown above doesn't render): here's the default sample again.

# %%
show_recipe(SAMPLE_ID)

# %% [markdown]
# ### Task 7 (Explore)
# Pick a different sample from the dropdown above (8 real, contrasting recipes). Find its ramp
# step and compute its slope the same way you did in Task 3.

# %%
NEW_SAMPLE_ID = 32465  # <-- change me: pick a sample id from the dropdown above
new_recipe = recipes[(recipes.sample_id == NEW_SAMPLE_ID) & (recipes.recipe_number == 1)]
new_ramp_rows = new_recipe[new_recipe["step"].str.contains("ramp", case=False)].dropna(
    subset=["temperature_C", "duration_min"])
if len(new_ramp_rows) == 0:
    print(f"No usable ramp step (recorded duration AND temperature) for sample {NEW_SAMPLE_ID} — "
          f"missing data, not a code error. Pick a different sample from the dropdown above.")
else:
    new_ramp = new_ramp_rows.iloc[0]
    new_slope = (new_ramp["temperature_C"] - ROOM_TEMP_C) / new_ramp["duration_min"]
    print(f"sample {NEW_SAMPLE_ID}: ramp slope ≈ {new_slope:.2f} °C/min "
          f"(sample {SAMPLE_ID} was {slope:.2f} °C/min)")

# %% [markdown]
# **Your answer:** Is your new sample's ramp faster, slower, or about the same as sample
# 23451's? Name one reason two different recipes for the *same material* might ramp at different
# rates.
#
# _(write your answer here)_

# %% [markdown]
# ## Complexity dials
# - **Core (Tasks 1–5, ~30 min):** required — read the table, run the helper cells, fill in the
#   marked formulas.
# - **Explore (Tasks 6–7) and Extend (Task 8), below, are optional.** Use them for early
#   finishers or as homework — they are not needed to reach the exit ticket.
# - **Explore:** Tasks 6–7 — compute ratios, explore a second recipe with the dropdown.
# - **Extend:** Task 8 below — open-ended, a second dataset, honest statistics.
#
# ## Part 8 (Extend, optional) — Does growing longer change the roughness?
# `growth_summary` has one row per grown sample, summarizing that sample's *first* recorded recipe
# — how long its `Growth` step(s) lasted and the AFM-measured `rms_roughness_nm` of the resulting
# film. If longer growth built up a rougher (or smoother) film, we'd expect a trend in this
# scatter plot.

# %%
# @title Helper code (just run this)
def plot_growth_vs_roughness(df):
    x, y = df["growth_time_min"], df["rms_roughness_nm"]
    slope_fit, intercept_fit = np.polyfit(x, y, 1)
    r = x.corr(y)

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.scatter(x, y, alpha=0.5, color=COLOR_A, edgecolor="white", linewidth=0.3)
    xs_line = np.linspace(x.min(), x.max(), 50)
    ax.plot(xs_line, slope_fit * xs_line + intercept_fit, color=COLOR_B, lw=2,
            label="least-squares line")
    ax.set(xlabel="growth time (min)", ylabel="RMS roughness (nm)",
           title=f"MoS2 (MOCVD): growth time vs. roughness  (n={len(df)})")
    ax.legend()
    ax.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()

    print(f"least-squares line: roughness ≈ {slope_fit:.4f} × (growth time) + {intercept_fit:.3f} nm")
    print(f"correlation coefficient r = {r:.3f}")
    return slope_fit, intercept_fit, r

# %%
summary = load_table("growth_summary")
mos2_summary = summary[summary.material == "MoS2"].dropna(subset=["growth_time_min", "rms_roughness_nm"])

fit_slope, fit_intercept, r_value = plot_growth_vs_roughness(mos2_summary)

# %% [markdown]
# > **Scientist's note:** A small |r| means no clear *straight-line* trend in this slice — it does
# > **not** prove growth time has no effect. Other things differ between these samples too:
# > temperature, pressure, and other recipe steps aren't identical; roughness was measured on
# > scans of very different sizes (`scan_size_um` ranges from 1 to 70 µm here, and roughness on a
# > small scan isn't directly comparable to roughness on a large one); a handful of these samples
# > were regrown more than once, but `growth_summary` only describes each sample's first recipe;
# > and researchers chose which samples to scan in the first place. **Correlation is not
# > causation** — and here, there isn't even much correlation to begin with.
#
# ### Task 8 (Extend)
# **Your answer:** Based on `r` and the scatter plot, would you tell a crystal grower that
# "growing longer makes MoS2 rougher"? Give the actual r value as evidence, and name at least one
# reason (from the note above, or your own) why this data alone can't prove growth time causes
# roughness either way.
#
# _(write your answer here)_

# %% [markdown]
# ## Exit ticket
# Answer without writing any code.
#
# 1. A recipe step has `start_min = 30` and `duration_min = 8`. What time does the *next* step
#    start, and how did you find it?
# 2. A table cell for temperature is blank instead of showing a number. Why is it wrong to treat
#    that blank as "0 °C," and what should you do instead when you don't know a value?
# 3. The MOCVD chamber runs at about 50 Torr and the MBE chamber runs at about 4 × 10⁻¹⁰ Torr.
#    Is it more useful to say MBE is "50 Torr emptier" or "about 10¹¹ times emptier"? Why?
