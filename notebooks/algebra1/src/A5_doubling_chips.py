# %% [markdown]
# # Doubling Chips: The Power of 2
#
# A computer chip is built from billions of tiny switches called **transistors**. Think of a
# light switch that flips on and off — a transistor does that too, but billions of times every
# second.
#
# Fifty years ago, chips had a few thousand transistors. Today's chips have billions. In this
# notebook you'll use math — tables, graphs, and ratios — to explore that growth.
#
# **What you'll do**
# - Build a doubling table by hand.
# - Compare doubling growth to steady, "add the same amount" growth.
# - Check which doubling speed fits real chip data best.
# - Use a ratio to see why super-thin materials matter to chipmakers.
#
# **Time:** about 30–40 minutes.

# %% [markdown]
# ## 🔧 Setup (run this first)
# Click ▶ on the cell below. It downloads the data (about 20 MB). This takes 10–30 seconds.
#
# *Teachers:* if your school hosts its own copy of the data, put its link in `DATA_URL`.
# No internet? Upload `camel-2dcc-v1.zip` with the 📁 Files panel on the left, then run this cell.

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
# ## Part 1 — A table of real chips
# `chips_timeline.csv` lists real transistor counts for famous chips, from 1971 to 2024.

# %%
chips = load_table("chips_timeline")
chips[["year", "chip", "maker", "transistors", "used_for"]]

# %% [markdown]
# ### Task 1 — Fill in a doubling table
# In 1971, the first chip (the Intel 4004) had **2,300** transistors. Since then, chip counts
# have often followed a doubling pattern: the count doubles about every 2 years.
#
# Fill in the blanks below. Each number is **2 times** the number 2 years before it.

# %%
year_1971 = 2300   # given: the first chip (1971)
year_1973 = 0      # ✏️ type your answer here
year_1975 = 0      # ✏️ type your answer here
year_1977 = 0      # ✏️ type your answer here
year_1979 = 0      # ✏️ type your answer here

# %%
answers = [year_1973, year_1975, year_1977, year_1979]
correct = [4600, 9200, 18400, 36800]
if answers == correct:
    print("✅ Nice! 2,300 -> 4,600 -> 9,200 -> 18,400 -> 36,800.")
else:
    right_so_far = sum(a == c for a, c in zip(answers, correct))
    print(f"Hint: {right_so_far}/4 correct so far. Each number is 2 x the one two years before it.")

# %% [markdown]
# ### Task 2 — Doubling vs. adding
# Doubling isn't the only way a number can grow. It could grow by **adding** 2,300 every 2 years
# instead of doubling.
#
# The table below shows both patterns side by side. Read it, then answer: in what year does
# doubling first pass adding?

# %%
# @title Helper code (just run this)
import pandas as pd

years = [1971, 1973, 1975, 1977, 1979, 1981, 1983]
adding = [2300 + 2300 * n for n in range(7)]
doubling = [2300 * 2 ** n for n in range(7)]
pd.DataFrame({"year": years, "adding (+2,300 every 2 yrs)": adding, "doubling (x2 every 2 yrs)": doubling})

# %%
year_doubling_wins = 0   # ✏️ type your answer here: the first year doubling is bigger than adding

# %%
if year_doubling_wins == 1975:
    print("✅ Nice! By 1975, doubling (9,200) has already passed adding (6,900).")
else:
    print("Hint: find the first row where the doubling column is bigger than the adding column.")

# %% [markdown]
# ### Task 3 — Which curve fits the real chips?
# Now check the doubling pattern against real chip data. The dots below are real chips. The
# lines are doubling models — one doubles every 2 years, one every 3 years.
#
# The early dots sit close to the bottom — that's normal. Early chips had far fewer transistors
# than today's, so they look tiny next to billions.
#
# Which line follows the dots more closely, from the early years to the most recent one?

# %%
# @title Helper code (just run this)
import numpy as np
import matplotlib.pyplot as plt

BLUE, GREEN, ORANGE = "#0072B2", "#009E73", "#E69F00"  # colour-blind-safe (Okabe-Ito palette)

def plot_doubling(chips, doubling_times, colors):
    t0, N0 = 1971, 2300
    t_grid = np.linspace(1971, 2026, 200)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter(chips["year"], chips["transistors"], color=ORANGE, s=70, zorder=3, label="real chips")
    for d, color in zip(doubling_times, colors):
        model = N0 * 2 ** ((t_grid - t0) / d)
        ax.plot(t_grid, model, color=color, lw=3, label=f"doubles every {d:g} years")
    ax.set(xlabel="year", ylabel="number of transistors",
           title="Real chips (dots) vs. two doubling guesses (lines)")
    ax.legend()
    ax.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()

# %%
plot_doubling(chips, [2, 3], [BLUE, GREEN])

# %%
best_doubling_time = 0   # ✏️ type your answer here: 2 or 3

# %%
if best_doubling_time == 2:
    print("✅ Nice! A 2-year doubling time tracks the real chips best.")
else:
    print("Hint: look again — one line stays closer to the dots across the whole graph.")

# %% [markdown]
# ### Optional extra — try your own doubling time
# Move the slider to test any doubling time between 1 and 6 years. If no slider appears, that's
# fine — skip it.

# %%
# @title Helper code (just run this)
import ipywidgets as widgets

def _one_line(years_to_double):
    plot_doubling(chips, [years_to_double], [BLUE])

widgets.interact(_one_line, years_to_double=widgets.FloatSlider(
    value=3.0, min=1.0, max=6.0, step=0.5, description="years to double", continuous_update=False))

# %% [markdown]
# ### Optional extra — a log-scale view
# Scientists often use a **log scale** for fast-growing data. On a log scale, each gridline is
# **10 times** the one before it (10, then 100, then 1,000...) instead of adding the same amount.
# That squeezes huge growth onto one readable graph.

# %%
# @title Helper code (just run this)
fig, ax = plt.subplots(figsize=(8, 5))
ax.scatter(chips["year"], chips["transistors"], color=ORANGE, s=70, zorder=3, label="real chips")
t_grid = np.linspace(1971, 2026, 200)
for d, color in zip([2, 3], [BLUE, GREEN]):
    model = 2300 * 2 ** ((t_grid - 1971) / d)
    ax.plot(t_grid, model, color=color, lw=3, label=f"doubles every {d:g} years")
ax.set_yscale("log")
ax.set(xlabel="year", ylabel="number of transistors (log scale)",
       title="Same data, log scale: doubling looks like a straight line")
ax.legend()
ax.grid(alpha=0.3, which="both")
plt.tight_layout()
plt.show()

# %% [markdown]
# ### Task 4 — How many doublings to 80 billion?
# The newest chip in our table has about **80 billion** transistors. Starting from 2,300 in
# 1971, how many times does the number have to double to reach about 80 billion?
#
# You don't need logarithms — use the table below. Find the row closest to 80,000,000,000, and
# read off the number of doublings.

# %%
# @title Helper code (just run this)
doublings = list(range(28))
values = [2300 * 2 ** n for n in doublings]
pd.DataFrame({"doublings": doublings, "value": values})

# %%
my_doublings_guess = 0   # ✏️ type your answer here

# %%
if 23 <= my_doublings_guess <= 27:
    print("✅ Nice! Around 25 doublings gets you from 2,300 to about 80 billion.")
else:
    print("Hint: scroll the table for the row where value is closest to 80,000,000,000.")

# %% [markdown]
# ### Task 5 — Why thin materials matter
# Chipmakers like materials that come in super-thin layers. One material, called MoS2, naturally
# forms layers just **0.65 nanometres (nm)** thick — a nanometre is a tiny length, far too small
# to see.
#
# A sheet of paper is about **100,000 nm** thick. How many MoS2 layers would it take to stack up
# to the thickness of one sheet of paper?

# %%
crystal_layer_nm = 0.65   # given
paper_nm = 100_000        # given
my_layers_guess = 0       # ✏️ type your answer here: divide paper_nm by crystal_layer_nm

# %%
actual = paper_nm / crystal_layer_nm
if abs(my_layers_guess - actual) / actual < 0.1:
    print(f"✅ Nice! About {actual:,.0f} layers stack up to one sheet of paper.")
else:
    print("Hint: divide paper_nm by crystal_layer_nm. Try again.")

# %% [markdown]
# > **Scientist's note:** The doubling pattern people found for chips is often called *Moore's
# > law*. It isn't a law of nature like gravity — it's a **trend** people noticed in real
# > engineering, and it has been slowing down. Newer chips don't always double every 2 years
# > anymore. Also, `chips_timeline.csv` is a hand-picked list of famous chips, not every chip ever
# > made, so a different list could give a different doubling time.
# >
# > Some of today's biggest chips work inside **data centers** — buildings full of computer chips
# > that power apps and websites.

# %% [markdown]
# ## Exit ticket
# Answer without the computer.
#
# 1. A number starts at 100 and doubles every 3 years. What is it after 9 years?
# 2. Which grows faster over time: adding the same amount every time, or doubling every time?
#    Why?
# 3. In your own words, why is the chip doubling pattern a *trend*, not a rule like gravity?
