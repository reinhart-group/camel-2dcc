# %% [markdown]
# # Colder and Colder: Graphs With a Surprise
#
# Electricity is a flow of tiny charged particles moving through a wire. Most materials
# fight that flow a little — scientists call that fight **resistance**. The more resistance
# a wire has, the harder electricity must push to get through.
#
# What happens if you make a wire really, really cold? For most materials, resistance just
# drifts down a little — it never disappears. But for a few special crystals, something
# surprising happens: at a certain cold temperature, their resistance suddenly drops until
# it's too small to measure. In this notebook you'll graph real measurements from four
# crystal films made at Penn State and use temperature scales and slope to describe what
# you see.
#
# **What you'll do**
# - Convert between three temperature scales: Celsius, Kelvin, and Fahrenheit.
# - Graph real resistance measurements and describe the graph in pieces.
# - Find the slope of one part of the graph, in ohms per kelvin.
# - Compare four real crystal films — including one that never hits zero.
# - *If you have time:* use voltage = current × resistance to compare two temperatures.
#
# **Time:** about 30–40 minutes for Tasks 1–4 and the exit ticket. Task 5 is optional.

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
# This is a real **crystal** film grown at Penn State, made of iron and selenium (FeSe). Its
# atoms sit in neat, repeating blocks — that's what makes it a crystal. This particular
# piece is sample 20382. Later you'll graph resistance measurements from four *other* FeSe
# films — different pieces of the same material, made the same way — to see how cold they
# must get before their resistance disappears.

# %%
gallery = load_gallery()
surface_3d(gallery["superconductor_blocks"]).show()

# %% [markdown]
# ## Task 1 — Three temperature scales
# Scientists mostly use **kelvin** (K) for very cold temperatures. It starts at "absolute
# zero," the coldest anything can ever get. Here are two conversions (the kelvin one is
# rounded for class — the exact number is 273.15, but 273 is close enough here):
# $$K = C + 273 \qquad\qquad F = 1.8 \times C + 32$$
# Convert room temperature, 20 °C, to kelvin.

# %%
room_K = ...  # ✏️ type your answer here: 20 + 273

# %%
# @title Helper code (just run this)
if room_K == 293:
    print("✅ Nice! 20 °C = 293 K.")
elif room_K == ...:
    print("🔁 Replace the `...` with 20 + 273.")
else:
    print("🔁 Check your formula: K = C + 273. It should give 293.")

# %% [markdown]
# Now convert liquid nitrogen, a coolant labs use all the time, from −196 °C to Fahrenheit.

# %%
nitrogen_F = ...  # ✏️ type your answer here: 1.8 * -196 + 32

# %%
# @title Helper code (just run this)
expected_nF = 1.8 * -196 + 32
if nitrogen_F == expected_nF:
    print(f"✅ Nice! −196 °C = {expected_nF:.1f} °F — bitterly cold.")
elif nitrogen_F == ...:
    print("🔁 Replace the `...` with 1.8 * -196 + 32.")
else:
    print(f"🔁 Check your formula: F = 1.8 × C + 32. It should give {expected_nF:.1f}.")

# %% [markdown]
# One more, in reverse: a lab cools something down to 5 K. Convert that to Celsius, then to
# Fahrenheit. (Hint: solve $K = C + 273$ for $C$ first.)

# %%
cold_C = ...  # ✏️ type your answer here: 5 - 273
cold_F = ...  # ✏️ type your answer here: 1.8 * cold_C + 32

# %%
# @title Helper code (just run this)
expected_cC = 5 - 273
expected_cF = 1.8 * expected_cC + 32
if cold_C == expected_cC and cold_F == expected_cF:
    print(f"✅ Nice! 5 K = {expected_cC:g} °C = {expected_cF:.1f} °F. That's far colder than natural "
          "outdoor temperatures on Earth — labs use special refrigeration to get there.")
else:
    print(f"🔁 Check both formulas. C should be {expected_cC:g}, and F should be about {expected_cF:.1f}.")

# %% [markdown]
# ## Meet the four films
# Penn State grew four FeSe films and measured how each one's resistance changes as it
# cools. To keep things simple, we'll call them Film A, B, C, and D instead of their lab
# sample numbers:
#
# | Name we'll use | Lab sample number |
# |---|---|
# | Film A | 20198 |
# | Film B | 20199 |
# | Film C | 20200 |
# | Film D | 20201 |
#
# These are four *different* pieces of FeSe — not the one pictured above, but made of the
# same material, the same way.

# %%
# @title Helper code (just run this)
FILM_NAMES = {20198: "Film A", 20199: "Film B", 20200: "Film C", 20201: "Film D"}

# %% [markdown]
# ## Task 2 — Graph a real film's resistance
# Below is real data from Film A. Scientists cooled it down and measured its resistance
# (in ohms) the entire time.

# %%
# @title Helper code (just run this)
import pandas as pd
import matplotlib.pyplot as plt

BLUE, ORANGE = "#0072B2", "#E69F00"  # colours anyone can tell apart

fese = load_extra("transport_fese.csv")
sample_id = 20198  # Film A
film = fese[fese.sample_id == sample_id].sort_values("temperature_K")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
ax1.plot(film.temperature_K, film.resistance_ohm, color=BLUE, lw=1.5)
ax1.set(xlabel="temperature (K)", ylabel="resistance (ohm)",
        title=f"{FILM_NAMES[sample_id]}: the full cool-down, 0-300 K")
ax1.grid(alpha=0.3)

zoom = film[film.temperature_K <= 40]
ax2.plot(zoom.temperature_K, zoom.resistance_ohm, color=ORANGE, lw=1.5, marker="o", ms=3)
ax2.set(xlabel="temperature (K)", ylabel="resistance (ohm)",
        title=f"{FILM_NAMES[sample_id]}: zoomed in, 0-40 K")
ax2.grid(alpha=0.3)
plt.tight_layout()
plt.show()

# %% [markdown]
# **Your answer:** This graph has three parts. In one short sentence each, describe what
# happens to resistance (a) from 300 K down to about 150 K, (b) from about 150 K down to
# 40 K, and (c) below about 5 K.
#
# _(write your answer here)_

# %% [markdown]
# **Check your thinking:** ▶ run the cell below to see one good answer.

# %%
# @title Helper code (just run this) — reveals a model answer
print("Model answer: (a) From 300 K down to about 150 K, resistance rises a little as the "
      "film cools — real data is a little bumpy, not a perfectly straight line. (b) From "
      "about 150 K down to 40 K, resistance drifts back down in a fairly straight line. "
      "(c) Below about 5 K, resistance drops fast until it's too small to measure — that "
      "sudden drop is the sign of a superconductor.")

# %% [markdown]
# Now read a number off the zoomed-in graph: about what temperature does resistance suddenly
# drop close to zero?

# %%
zero_temp_K = ...  # ✏️ type your answer here: your best reading of the graph, in kelvin

# %%
# @title Helper code (just run this)
true_zero_temp = load_extra("transport_summary.csv").set_index("sample_id").loc[20198, "T_zero_1pct_K"]
if zero_temp_K is not ... and abs(zero_temp_K - true_zero_temp) <= 3:
    print(f"✅ Nice! It drops close to zero at about {true_zero_temp:.1f} K.")
elif zero_temp_K == ...:
    print("🔁 Replace the `...` with a number you read off the zoomed-in graph.")
else:
    print(f"🔁 Look again at the zoomed-in graph — the real drop happens around {true_zero_temp:.1f} K.")

# %% [markdown]
# ## Task 3 — Slope of the middle part, in ohms per kelvin
# Zoom back out to the whole graph. Between about 50 K and 150 K, the line is fairly
# straight. Two real points from that part:
# - at 50 K, resistance ≈ 1156 ohms
# - at 150 K, resistance ≈ 1256 ohms
#
# Find the slope: $\dfrac{\text{change in resistance}}{\text{change in temperature}}$

# %%
slope_ohm_per_K = ...  # ✏️ type your answer here: (1256 - 1156) / (150 - 50)

# %%
# @title Helper code (just run this)
expected_slope = (1256 - 1156) / (150 - 50)
if slope_ohm_per_K == expected_slope:
    print(f"✅ Nice! About {expected_slope:g} ohm per kelvin. Resistance goes UP a little as it warms here —"
          " the opposite of what happens near zero!")
elif slope_ohm_per_K == ...:
    print("🔁 Replace the `...` with (1256 - 1156) / (150 - 50).")
else:
    print(f"🔁 Check your formula. It should give {expected_slope:g} ohm per kelvin.")

# %% [markdown]
# ## Task 4 — Four films, compared
# 2DCC grew all four films (A, B, C, D) the same way, then measured how cold each one had
# to get before its resistance dropped below 1% of its value at 40 K — in kid words, before
# it became too small to measure (about zero). **A blank means that film never got that cold
# in this data** — not that it reached zero at 0 K.

# %%
# @title Helper code (just run this) — a plain-language table
summary = load_extra("transport_summary.csv")
summary_table = pd.DataFrame({
    "Film": summary["sample_id"].map(FILM_NAMES),
    "Temperature where resistance is near zero (K)": summary["T_zero_1pct_K"].apply(
        lambda t: f"{t:.1f}" if pd.notna(t) else "— never got that cold in this data"),
})
summary_table

# %% [markdown]
# How many of the four films reach close to zero resistance somewhere in this data?

# %%
films_reaching_zero = ...  # ✏️ type your answer here: count the rows in the table above that AREN'T blank

# %%
# @title Helper code (just run this)
expected_count = summary["T_zero_1pct_K"].notna().sum()
missing_films = ", ".join(FILM_NAMES[s] for s in summary.loc[summary["T_zero_1pct_K"].isna(), "sample_id"])
if films_reaching_zero == expected_count:
    print(f"✅ Nice! {expected_count} of the 4 films reach close to zero in this data — "
          f"{missing_films} simply wasn't measured cold enough in this data to find out.")
elif films_reaching_zero == ...:
    print("🔁 Replace the `...` with a count (0-4).")
else:
    print(f"🔁 Count the non-blank rows in the table above. It should be {expected_count}.")

# %% [markdown]
# ## A name for what you just found
# A material that can carry electricity with resistance too small to measure, once it's
# cold enough, is called a **superconductor**. Look back at the zoomed-in graph in Task 2 —
# that sudden drop is the sign scientists look for. The four films above don't all reach
# that point at the same temperature, and one of them didn't reach it anywhere in this data
# — we can't say why from this table alone, only that it needed more cooling than we
# measured. Reaching that cold takes real, working refrigeration; a superconductor doesn't
# cool anything itself.
#
# ## Task 5 (optional) — Voltage before and after
# A simple formula connects voltage, current, and resistance: $V = I \times R$. **Voltage**
# is the electrical push needed to send a flow of charge through a wire — more resistance
# needs a bigger push for the same flow.
#
# Send a tiny, steady flow — 1 microamp (0.000001 A) — through Film A at 20 K, where its
# resistance ≈ 1015.6 ohm:
# $$V = 0.000001 \times 1015.6$$

# %%
current_A = 0.000001
voltage_20K = ...  # ✏️ type your answer here: current_A * 1015.6

# %%
# @title Helper code (just run this)
true_R_20K = film.loc[(film.temperature_K - 20).abs().idxmin(), "resistance_ohm"]
expected_v20 = current_A * true_R_20K
if voltage_20K is not ... and abs(voltage_20K - expected_v20) < 0.0001:
    print(f"✅ Nice! V = 0.000001 × {true_R_20K:.1f} ≈ {expected_v20 * 1000:.2f} mV. "
          "At 3 K the resistance is about 0 ohms, so V would be about 0 too — that's what "
          "'resistance too small to measure' means for electricity.")
elif voltage_20K == ...:
    print("🔁 Replace the `...` with current_A * 1015.6.")
else:
    print(f"🔁 Check your multiplication. V = I × R should give about {expected_v20 * 1000:.2f} mV.")

# %% [markdown]
# ## Exit ticket
# Answer without running any code.
#
# 1. Water freezes at 0 °C. What is that in kelvin?
# 2. A film's cell in the "near zero" column is blank in the table. What does that blank
#    actually tell you?
# 3. Between 50 K and 150 K, the slope of the resistance graph is positive. Does resistance
#    go up or down as the film warms up in that range?

# %% [markdown]
# **Nice work!** You read a graph in pieces, found a slope in ohms per kelvin, and compared
# four real films — the same tools scientists use to describe any curve that isn't a
# straight line all the way through.
