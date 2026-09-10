# %% [markdown]
# # Graph a Recipe: Slope Is a Rate
#
# Scientists don't just mix chemicals — they follow a recipe, like a recipe for cookies.
# Instead of a bowl, they use a super-hot oven. Instead of flour and sugar, they use gases
# full of atoms. Heat, wait, cool — and a brand new **crystal** comes out. A crystal is a
# material whose atoms line up in a neat, repeating pattern, like tiles on a floor.
#
# Today you'll graph a real recipe that Penn State scientists used to grow a tiny crystal
# called MoS₂ (say "moly-sulfide"). You'll read the graph, find its slope, and use that
# slope to predict the future — all with an ordinary linear equation.
#
# **What you'll do**
# - Turn a table of recipe steps into a running total of minutes.
# - Read temperature and time straight off a graph.
# - Find the slope of the heat-up part, in °C per minute.
# - Write an equation and solve it for a target temperature.
# - See how changing one number changes the whole answer.
# - Convert the recipe's hottest temperature to Fahrenheit.
#
# **Time:** about 30–40 minutes.

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
# ## Meet the crystal
# Here's the actual crystal this recipe makes, its surface measured by a special
# **microscope** that feels its way across the surface, like a finger reading braille.

# %%
gallery = load_gallery()
surface_3d(gallery["mos2_film"], exaggeration=30).show()

# %% [markdown]
# That bumpy hill is one crystal layer, far too small to touch. The bumps are stretched
# taller here so you can see them — the real crystal is almost perfectly flat.
#
# ## Task 1 — Read the recipe
# `recipe` below is the real, step-by-step recipe for this exact crystal: `duration_min` is
# how long each step lasted, and `start_min` is the minute it started, counting from when the
# recipe began.

# %%
import pandas as pd

recipes = load_table("growth_recipes")
recipe = (recipes[(recipes.sample_id == 23451) & (recipes.recipe_number == 1)]
          .sort_values("step_number").reset_index(drop=True))
recipe[["step_number", "step", "duration_min", "start_min", "temperature_C"]]

# %% [markdown]
# `start_min` is a **running total** — each step's own minutes, added to every step before
# it. Add up the first four steps' minutes by hand (Ramp up T, Anneal 1, Anneal 2, Growth),
# then type your total below.

# %%
running_total_min = ...  # ✏️ type your answer here: 17 + 5 + 5 + 3
print(f"My running total: {running_total_min} minutes")

# %%
# @title Helper code (just run this) — checks your total
expected_total = recipe.loc[:3, "duration_min"].sum()
if running_total_min == expected_total:
    print(f"✅ Nice! {expected_total:g} minutes — and that matches start_min for step 5 in the table above!")
elif running_total_min == ...:
    print("🔁 Replace the `...` with 17 + 5 + 5 + 3.")
else:
    print(f"🔁 Not quite — add up the first four durations. It should be {expected_total:g}.")

# %% [markdown]
# ## Task 2 — Read the time–temperature graph
# The table above doesn't say what temperature the oven started at — that was never
# written down. So we'll **guess** it started at room temperature, about 25 °C. That's an
# assumption, not a measurement, and the graph below says so.

# %%
# @title Helper code (just run this)
import matplotlib.pyplot as plt

BLUE, ORANGE = "#0072B2", "#E69F00"  # colours anyone can tell apart

# What the data tells us: heats up for 17 minutes to 1000 °C, then holds at 1000 °C
# until minute 40. We ASSUME it started at 25 °C (room temperature) — that part isn't
# in the data, so it's a guess, not a measurement.
known_time = [0, 17, 40]
known_temp = [25, 1000, 1000]

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(known_time, known_temp, color=BLUE, lw=3, marker="o", ms=8)
ax.axvspan(40, 56, color=ORANGE, alpha=0.15)
ax.text(48, 550, "cool-down\n(temperature\nnot recorded)", ha="center", color="#946200", fontsize=10)
ax.set(xlabel="cumulative time (minutes)", ylabel="temperature (°C)",
       title="Sample 23451's recipe: temperature vs. time (25 °C start is a guess)",
       xlim=(0, 56), ylim=(0, 1100))
ax.grid(alpha=0.3)
plt.tight_layout()
plt.show()

# %% [markdown]
# Read the two questions below straight off the graph, then type your answers.

# %%
highest_temp_C = ...  # ✏️ type your answer here: the highest temperature shown on the graph
minutes_at_highest = ...  # ✏️ type your answer here: how many minutes the line stays flat at that height (40 - 17)

# %%
# @title Helper code (just run this)
expected_high = recipe["temperature_C"].max()
expected_hold = 40 - 17
ok_high = highest_temp_C == expected_high
ok_hold = minutes_at_highest == expected_hold
if ok_high and ok_hold:
    print(f"✅ Nice! It peaks at {expected_high:g} °C and stays there for {expected_hold:g} minutes.")
else:
    if not ok_high:
        print(f"🔁 Look at the tallest flat part of the line — it should read {expected_high:g} °C.")
    if not ok_hold:
        print(f"🔁 The flat part runs from minute 17 to minute 40 — that's {expected_hold:g} minutes.")

# %% [markdown]
# The shaded part on the right is real too — the oven really did cool down. We just don't
# have the numbers, so we leave it blank instead of guessing. A blank is not the same as zero.
#
# ## Task 3 — Find the slope of the heat-up
# Slope is a **rate of change**: how much one thing changes for every unit of another. Here,
# it's how many degrees the oven heats up *per minute*:
# $$\text{slope} = \dfrac{\text{change in temperature}}{\text{change in time}} = \dfrac{1000 - 25}{17}$$

# %%
heatup_slope = ...  # ✏️ type your answer here: (1000 - 25) / 17
print(f"My slope: {heatup_slope} °C per minute")

# %%
# @title Helper code (just run this)
true_slope = (recipe["temperature_C"].max() - 25) / 17
if heatup_slope is not ... and abs(heatup_slope - true_slope) < 0.2:
    print(f"✅ Nice! About {true_slope:.1f} °C per minute — a fast heat-up!")
elif heatup_slope == ...:
    print("🔁 Replace the `...` with (1000 - 25) / 17.")
else:
    print(f"🔁 Check your formula. (1000 - 25) / 17 should give about {true_slope:.1f}.")

# %% [markdown]
# ## Task 4 — Write an equation, then solve it
# A linear equation for this heat-up is $T = 25 + m \times t$, where $m$ is the slope you
# just found and $t$ is minutes. Solve for $t$ when $T = 500$:
# $$500 = 25 + m \times t \quad\Rightarrow\quad t = \dfrac{500 - 25}{m}$$

# %%
minutes_to_500 = ...  # ✏️ type your answer here: (500 - 25) / heatup_slope

# %%
# @title Helper code (just run this)
expected_t500 = (500 - 25) / true_slope
if minutes_to_500 is not ... and abs(minutes_to_500 - expected_t500) < 1:
    print(f"✅ Nice! About {expected_t500:.1f} minutes — under this model, of course.")
elif minutes_to_500 == ...:
    print("🔁 Replace the `...` with (500 - 25) / heatup_slope.")
else:
    print(f"🔁 Check your algebra. It should give about {expected_t500:.1f} minutes.")

# %% [markdown]
# ## Task 5 — Change one number
# Our 25 °C start was just a guess. What if the oven hadn't fully cooled from the day
# before, and actually started at 200 °C? Try the slider (it doesn't need code) and watch
# both the slope and the time to 500 °C change.

# %%
# @title Helper code (just run this) — try the slider
import ipywidgets as widgets

def show_alt_start(start_C):
    m = (1000 - start_C) / 17
    t500 = (500 - start_C) / m
    print(f"Start at {start_C} °C  ->  slope = {m:.1f} °C/min  ->  reaches 500 °C at t = {t500:.1f} min")

widgets.interact(show_alt_start, start_C=widgets.IntSlider(value=25, min=0, max=300, step=5,
                                                            description="Start °C"))

# %% [markdown]
# **No slider showing?** Here's the fixed comparison: start at 200 °C instead of 25 °C.
# Type the two new numbers below.

# %%
alt_slope = ...  # ✏️ type your answer here: (1000 - 200) / 17
alt_minutes_to_500 = ...  # ✏️ type your answer here: (500 - 200) / alt_slope

# %%
# @title Helper code (just run this)
true_alt_slope = (1000 - 200) / 17
true_alt_t500 = (500 - 200) / true_alt_slope
ok_slope = alt_slope is not ... and abs(alt_slope - true_alt_slope) < 0.5
ok_t500 = alt_minutes_to_500 is not ... and abs(alt_minutes_to_500 - true_alt_t500) < 0.5
if ok_slope and ok_t500:
    print(f"✅ Nice! Slope {true_alt_slope:.1f} °C/min, reaching 500 °C at t ≈ {true_alt_t500:.1f} min "
          f"— faster than the {expected_t500:.1f} min from a 25 °C start, since there's less climbing to do.")
else:
    print(f"🔁 Slope should be about {true_alt_slope:.1f}, and the time to 500 °C about {true_alt_t500:.1f} min.")

# %% [markdown]
# Changing **one** number — the starting temperature — changed both the slope and the
# answer. Neither version is a measurement; both are "if this, then that" models.
#
# ## Task 6 — Same heat, a different scale
# Scientists (and recipes) use Celsius. Cooks in the US often use Fahrenheit instead:
# $$F = 1.8 \times C + 32$$
# Convert this recipe's hottest temperature, 1000 °C, to Fahrenheit.

# %%
growth_temp_F = ...  # ✏️ type your answer here: 1.8 * 1000 + 32

# %%
# @title Helper code (just run this)
expected_F = 1.8 * recipe["temperature_C"].max() + 32
if growth_temp_F == expected_F:
    print(f"✅ Nice! 1000 °C = {expected_F:.0f} °F. A home oven usually tops out around 550 °F — "
          "this crystal oven runs more than three times hotter!")
elif growth_temp_F == ...:
    print("🔁 Replace the `...` with 1.8 * 1000 + 32.")
else:
    print(f"🔁 Check your formula. 1.8 × 1000 + 32 should give {expected_F:.0f}.")

# %% [markdown]
# ## Exit ticket
# Answer without running any code.
#
# 1. A step starts at minute 22 and lasts 6 minutes. What minute does it end, and what
#    minute does the *next* step start?
# 2. A recipe's temperature cell is blank instead of showing a number. Why is it wrong to
#    read that blank as "0 °C"?
# 3. If the heat-up slope were 60 °C per minute instead of about 57 °C per minute, would the
#    oven reach 500 °C sooner or later? How do you know, without finding the exact number?

# %% [markdown]
# **Nice work!** You turned a real lab recipe into a graph, found its slope, and used a
# linear equation to predict the future — the same math (and the same care about
# assumptions) real scientists use every day.
