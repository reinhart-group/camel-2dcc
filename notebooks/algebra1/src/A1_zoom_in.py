# %% [markdown]
# # Zoom In! How Small Is a Nanometre?
#
# At Penn State, scientists grow crystals so thin that no regular microscope can see their
# bumps. They use a special microscope with a tiny tip that feels its way across the
# surface, like a finger reading braille. It records the height at every point, and you get
# to fly over the result.
#
# Today's math: converting units, ratios, and scale factor — the numbers that turn "too
# small to see" into a picture you can explore.
#
# **What you'll do**
# - Fly over a real crystal surface in 3D.
# - Convert metres → millimetres → micrometres → nanometres.
# - Use a ratio to see how many scans fit across a human hair.
# - Blow a scan up to the size of a soccer field.
#
# **Time:** about 30–40 minutes.

# %% [markdown]
# ## 🔧 Setup (run this first)
# Click the ▶ button on the cell below. It downloads the real data (about 20 MB) and takes
# 10–30 seconds.
#
# *Teachers:* if your school hosts its own copy of the data, paste its link into `DATA_URL`.
# No internet link? Upload `camel-2dcc-v1.zip` with the 📁 Files panel on the left, then run
# this cell.

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
# ## Task 1 — Meet a real crystal
# Here's a real crystal surface. The picture stretches the height so tiny bumps are easy to
# see (without stretching, most crystals look almost flat). Turn it around and zoom in.

# %%
gallery = load_gallery()
surface_3d(gallery["mos2_film"], exaggeration=30).show()

# %% [markdown]
# **Optional — try more crystals:** the cell below adds a dropdown of 12 scans and a
# **Stretch** slider. It's optional — if it doesn't load, the picture above already has
# everything you need for the question below.

# %%
explore_3d(gallery)

# %% [markdown]
# **Try it:** if the dropdown loaded, set the sample to **Smooth MoS2 carpet (MoS2)** and
# move the Stretch slider from low to high (otherwise just look at the picture above). Write
# one sentence: what changes on the plot when Stretch goes up?
#
# **Your answer:**
# _(write here)_

# %% [markdown]
# **Check your thinking:** ▶ run the cell below to see one good answer.

# %%
# @title Helper code (just run this) — reveals a model answer
print("Model answer: as Stretch goes up, the same bumps look taller and easier to see. "
      "Flat, low areas barely change height — only the up-and-down is being stretched, "
      "not the width.")

# %% [markdown]
# ## Task 2 — The conversion ladder
# Every measurement below uses the metric system, so each step is the same move: ×1,000 to
# go down a size, ÷1,000 to go back up.
#
# | Unit | Symbol | How many metres | How many of the *next* unit |
# |---|---|---|---|
# | metre | m | 1 | 1 m = 1,000 mm |
# | millimetre | mm | 0.001 | 1 mm = 1,000 µm |
# | micrometre | µm | 0.000001 | 1 µm = 1,000 nm |
# | nanometre | nm | 0.000000001 | — |
#
# The crystal scan you just saw is **5 µm** wide. Fill in the missing conversion below.

# %%
scan_width_um = gallery["mos2_film"].scan_um   # 5 micrometres wide
scan_width_nm = ...  # ✏️ type your answer here: convert scan_width_um to nanometres

# %%
# @title Helper code (just run this) — checks your conversion
expected_nm = scan_width_um * 1000
if scan_width_nm == expected_nm:
    print(f"✅ Nice! {scan_width_um:g} µm = {scan_width_nm:g} nm.")
elif scan_width_nm == ...:
    print("🔁 Replace the `...` with a number: micrometres × 1,000 = nanometres.")
else:
    print(f"🔁 Not quite. Remember: µm → nm means ×1,000. Try again — it should be {expected_nm:.0f} nm.")

# %% [markdown]
# ## Task 3 — How many scans fit across a hair?
# A human hair is about **80 µm** wide. The scan you're studying is 5 µm wide. That's a
# ratio: hair width ÷ scan width tells you how many scans, laid edge to edge, span one hair.

# %%
hair_um = 80        # a human hair, in micrometres
scan_um = 5          # the crystal scan, in micrometres
scans_per_hair = ...  # ✏️ type your answer here: write the ratio as a formula (hair_um / scan_um)

# %%
# @title Helper code (just run this)
expected_ratio = hair_um / scan_um
if scans_per_hair == expected_ratio:
    print(f"✅ Nice! About {expected_ratio:g} scans, laid side by side, span one hair's width.")
elif scans_per_hair == ...:
    print("🔁 Replace the `...` with a formula: hair_um / scan_um.")
else:
    print(f"🔁 Check your formula. It should divide hair_um by scan_um and give {expected_ratio:g}.")

# %% [markdown]
# ## Task 4 — Blow it up to a soccer field
# A **scale factor** tells you how many times bigger a model is than the real thing:
# $$\text{scale factor} = \dfrac{\text{model size}}{\text{real size}}$$
# Let's turn the 5 µm-wide scan into a model the length of a soccer field (100 m long).
#
# First, both numbers need the *same* unit. The scan is in micrometres, the field is in
# metres — so convert the scan to metres. There are 1,000,000 µm in 1 m, so:
# $$5\ \mu m \times \dfrac{1\ m}{1{,}000{,}000\ \mu m} = 0.000005\ m$$
#
# **Worked example** (read it — you'll use `scale_factor` in the next step):

# %%
field_length_m = 100          # a soccer field, in metres
scan_width_m = 0.000005        # the 5 µm scan, converted to metres (given above)
scale_factor = field_length_m / scan_width_m   # model size ÷ real size
print(f"Scale factor: {scale_factor:,.0f}× — the field is {scale_factor:,.0f} times wider "
      "than the scan.")

# %% [markdown]
# ### Now stretch a crystal layer by that same factor
# One layer of this crystal (MoS₂, used inside some computer chips) is only **0.00000000065
# metres** thick — that's 0.65 nanometres. If we blow the whole scan up to a soccer field,
# how tall would one layer look at that same scale?
#
# $$\text{scaled height} = \text{real height} \times \text{scale factor}$$

# %%
layer_thickness_m = 0.00000000065   # one crystal layer, in metres (0.65 nm)
layer_scaled_m = ...  # ✏️ type your answer here: layer_thickness_m * scale_factor

# %%
# @title Helper code (just run this)
expected_layer_m = layer_thickness_m * scale_factor
if layer_scaled_m == ...:
    print("🔁 Replace the `...`: layer_thickness_m * scale_factor.")
elif abs(layer_scaled_m - expected_layer_m) < 1e-4:
    print(f"✅ Nice! About {expected_layer_m * 100:.1f} cm tall — roughly as thick as a phone!")
else:
    print(f"🔁 Check your formula. It should give about {expected_layer_m * 100:.1f} cm.")

# %% [markdown]
# ## Task 5 (optional) — 3D print your crystal
# Turn the scan into a file you could send to a 3D printer. This step is optional and does
# **not** run by itself — change `MAKE_MY_PRINT` to `True` below, then run the cell, when
# you're ready to make your file. (**Safety note:** this only creates a digital file — if you
# send it to a real printer, follow your school's printer rules.)

# %%
MAKE_MY_PRINT = False  # ✏️ change to True to make the file
if MAKE_MY_PRINT:
    stl_path = to_stl(gallery["mos2_film"], "my_crystal.stl", width_mm=100, relief_mm=15)
    print(f"Saved {stl_path}")
    try:
        from google.colab import files
        files.download(str(stl_path))
    except ImportError:
        print(f"Not running in Colab — find {stl_path} in this notebook's working folder.")
else:
    print("Set MAKE_MY_PRINT = True above and run this cell again to make your file.")

# %% [markdown]
# ## Exit ticket
# Answer these without running any code.
#
# 1. A scan is 3 µm wide. How many nanometres is that?
# 2. A hair is 80 µm wide and a scan is 4 µm wide. How many scans span the hair?
# 3. If you doubled the scale factor in Task 4, would the soccer-field layer look thicker
#    or thinner — and by how many times?

# %% [markdown]
# **Nice work!** You used ratios and scale factor to turn a crystal too small to see into a
# picture the size of a soccer field — the same math engineers use to design anything from
# a computer chip to a bridge.
