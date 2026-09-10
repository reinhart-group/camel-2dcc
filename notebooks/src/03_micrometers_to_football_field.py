# %% [markdown]
# # From Micrometres to a Football Field: Scaling, Stacking, and 3D Printing a Crystal
#
# A real AFM scan of a crystal is only a few **micrometres** wide — millionths of a
# metre. That is about 20 times thinner than a human hair. In this notebook you blow
# a real scan up to the size of a football field, count atomic layers from a measured
# step height, build a honeycomb lattice, shrink a cube down to nanometre size, and
# 3D print your own crystal.
#
# **What you'll do**
# - Compute a scale factor big enough to turn a microscopic scan into a football field,
#   and use it to predict how thick one atomic layer would look at that size.
# - Measure a real step height in a crystal surface and turn it into a layer count.
# - Build a hexagonal lattice, compute its unit-cell area, and estimate how many unit
#   cells fit on a fingernail.
# - Shrink a cube from 1 cm to 1 nm and watch its surface-area-to-volume ratio explode.
# - Export a real AFM scan as a 3D-printable STL file and download it.
#
# **Time:** about 45–50 minutes.
#
# ### Materials science words
# | Word | Meaning |
# |---|---|
# | **Scale factor** | How many times bigger (or smaller) a model is than the real thing. |
# | **Monolayer / layer** | One atom-thick (or few-atom-thick) sheet of a crystal. |
# | **Terrace / step** | A flat "stair tread" on a crystal surface, one or more layers tall. |
# | **Unit cell** | The smallest repeating tile that, copied over and over, builds the whole crystal surface. |
# | **Lattice constant (a)** | The side length of that repeating tile, usually in nanometres. |
# | **Hexagonal / honeycomb lattice** | A repeating pattern of six-sided cells, like chicken wire. |
# | **Surface-area-to-volume ratio** | How much outside surface an object has compared to how much "stuff" is inside it. |
# | **STL file** | A 3D file format that describes an object's shape as a mesh of triangles, ready to 3D print. |
# | **Vertical exaggeration** | How much taller a 3D model's height is stretched compared to its width, so tiny bumps become visible. |

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
# ## Meet your crystal
# `mos2_film` is a 5 µm × 5 µm AFM scan of molybdenum disulfide (MoS₂), a semiconductor
# only one atom-layer thick when peeled down to its thinnest form. This whole scan —
# every hill and valley you see below — is about the width of a fine human hair.

# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

scans = load_gallery()
materials = load_table("materials_reference")
surface_3d(scans["mos2_film"], exaggeration=15).show()

# %% [markdown]
# ## Part 1 — Scale factor: crystal to football field
# ### Task 1 (Core) — HSN.Q.A.1–3, HSG.SRT
# A **scale factor** is (size of the model) ÷ (size of the real thing) — or here, the other
# way around: how many times we blow the tiny scan up. Scale the 5 µm-wide `mos2_film`
# scan up to a 100 m football field (goal line to goal line; a full field with end zones
# is closer to 110 m, but we'll use 100 m so the scale factor stays a clean number).

# %%
scan_width_um = 5       # <-- change me: width of the scan, in micrometres
field_length_m = 100    # <-- change me: length of the football field, in metres

scan_width_m = scan_width_um * 1e-6
scale_factor = field_length_m / scan_width_m
print(f"Scan width: {scan_width_m:.2e} m")
print(f"Scale factor: {scale_factor:.3g}×")

# %% [markdown]
# **Check yourself:** with the numbers above, the scale factor should be a few times
# 10 million (10⁷).

# %%
if 1e7 <= scale_factor <= 4e7:
    print("✅ That's the right ballpark — a scan a few micrometres wide, blown up to a football field.")
else:
    print("↺ Check your units: scan_width_um should be a small number of micrometres, field_length_m about 100.")

# %% [markdown]
# ### Task 2 (Core) — scale a feature
# The bright islands in the `ws2_islands` scan are roughly 300 nm across. How wide would
# one look on the football field, at your scale factor?

# %%
feature_width_nm = 300    # <-- change me: width of a feature on the real scan, in nanometres

feature_width_scaled_m = feature_width_nm * 1e-9 * scale_factor
print(f"A {feature_width_nm} nm feature would be {feature_width_scaled_m:.2f} m wide on the football field.")

# %% [markdown]
# ### Task 3 (Core) — how tall is *one layer*, scaled up?
# `materials_reference` lists how thick one layer of each material is. Look up MoS₂'s
# layer thickness and scale it by the same factor.

# %%
mos2_layer_nm = materials.loc[materials.material == "MoS2", "layer_thickness_nm"].iloc[0]
layer_scaled_m = mos2_layer_nm * 1e-9 * scale_factor
print(f"One MoS2 layer is {mos2_layer_nm} nm thick in real life.")
print(f"Scaled up by {scale_factor:.3g}×, that layer would be {layer_scaled_m * 100:.1f} cm tall "
      f"— about as thick as a smartphone!")

# %% [markdown]
# > **Scientist's note:** Horizontal scale (width) and vertical scale (height) don't have
# > to use the same factor in a 3D model or plot — but when you *do* use the same factor
# > for both, as we just did, comparisons like "as thick as a phone" are fair. Watch for
# > this again in Part 5, where the 3D print deliberately uses different factors.

# %% [markdown]
# ## Part 2 — Counting atomic layers from a measured step
# ### Task 4 (Core) — HSA.CED.A.1–4
# `triangle_pyramids` is a scan of bismuth selenide (Bi₂Se₃), a topological insulator
# that grows as stacked triangular "steps," each one quintuple layer (five atomic
# sheets bonded together) tall. Explore the surface, then look at a line profile.

# %%
surface_3d(scans["triangle_pyramids"], exaggeration=8).show()
explore_cross_section(scans["triangle_pyramids"])

# %% [markdown]
# The helper cell below zooms in on one clean step along row 206 of that scan and reads
# off the average height on each side of the edge.

# %%
# @title Helper code (just run this)
def show_step_measurement(scan, row, col_edge, half_width=10):
    d, h = cross_section(scan, row)
    left = h[col_edge - half_width:col_edge]
    right = h[col_edge:col_edge + half_width]
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(d, h, color="0.4", lw=1)
    ax.axvspan(d[col_edge - half_width], d[col_edge], color="tab:blue", alpha=0.3, label="terrace A")
    ax.axvspan(d[col_edge], d[col_edge + half_width - 1], color="tab:orange", alpha=0.3, label="terrace B")
    ax.set(title=f"{scan.title} — line {row}", xlabel="distance (nm)", ylabel="height (nm)")
    ax.legend()
    ax.grid(alpha=0.3)
    plt.show()
    return float(np.median(left)), float(np.median(right))

terrace_a_nm, terrace_b_nm = show_step_measurement(scans["triangle_pyramids"], row=206, col_edge=361)
print(f"Terrace A (blue): {terrace_a_nm:.2f} nm")
print(f"Terrace B (orange): {terrace_b_nm:.2f} nm")

# %% [markdown]
# Now measure the step: subtract the two terrace heights (use the values printed above).

# %%
terrace_a_nm = 0.99     # <-- change me: copy the "Terrace A" value printed above
terrace_b_nm = -0.08    # <-- change me: copy the "Terrace B" value printed above

step_height_nm = abs(terrace_a_nm - terrace_b_nm)
print(f"Measured step height: {step_height_nm:.2f} nm")

# %% [markdown]
# ### Task 5 (Core) — layers = height ÷ layer thickness
# Look up Bi₂Se₃'s layer thickness from `materials_reference` (do **not** reuse the MoS₂
# value from Part 1 — different materials have different layer thicknesses).

# %%
bi2se3_thickness_nm = materials.loc[materials.material == "Bi2Se3", "layer_thickness_nm"].iloc[0]
layers_raw = step_height_nm / bi2se3_thickness_nm
layers_rounded = round(layers_raw)
print(f"{step_height_nm:.2f} nm ÷ {bi2se3_thickness_nm} nm/layer = {layers_raw:.2f} layers "
      f"→ round to {layers_rounded} layer(s)")

# %% [markdown]
# > **Scientist's note — uncertainty:** A measured step is never perfectly clean. Thermal
# > drift, the microscope tip's own shape, and surface adsorbates all blur a step edge by
# > a few tenths of a nanometre. `layers_raw` almost never lands exactly on a whole number
# > — that's expected, not a mistake. Round to the nearest whole layer and say *why* you
# > rounded that way, rather than reporting extra decimal places you can't actually justify.

# %% [markdown]
# ### Task 6 (Explore) — is one step typical, or lucky?
# One measurement could be an outlier. The helper below scans **hundreds** of clean step
# edges across the whole `triangle_pyramids` image and reports the spread for steps that
# look like a single layer.

# %%
# @title Helper code (just run this)
def survey_step_heights(scan, window=10, noise_max=0.15, layer_min=0.5, layer_max=1.5):
    z = scan.z
    n = z.shape[0]
    steps = []
    for row in range(n):
        h = z[row]
        for c in range(window, n - window, 2):
            left, right = h[c - window:c], h[c:c + window]
            step = abs(right.mean() - left.mean())
            noise = max(left.std(), right.std())
            if noise < noise_max and layer_min < step < layer_max:
                steps.append(step)
    return np.array(steps)

single_layer_steps = survey_step_heights(scans["triangle_pyramids"])
print(f"Found {len(single_layer_steps)} single-layer-like step edges across the scan.")
print(f"Median: {np.median(single_layer_steps):.2f} nm   "
      f"Middle 50% range: {np.percentile(single_layer_steps, 25):.2f}–{np.percentile(single_layer_steps, 75):.2f} nm")
print(f"Compare to the reference value for Bi2Se3: {bi2se3_thickness_nm} nm/layer")

# %% [markdown]
# **Your answer:** Was your single measurement in Task 4 close to the whole-scan median,
# or off to one side? What might explain the difference?

# %% [markdown]
# ### Task 7 (Explore) — a linear function for stack thickness
# Stack thickness is a linear function of the number of layers: `thickness = layer_thickness × n`.

# %%
n_layers = np.arange(0, 11)
thickness_nm = bi2se3_thickness_nm * n_layers

table = pd.DataFrame({"layers (n)": n_layers, "thickness (nm)": thickness_nm})
print(table)

plt.plot(n_layers, thickness_nm, marker="o", color="tab:orange")
plt.xlabel("number of layers (n)")
plt.ylabel("stack thickness (nm)")
plt.title(f"Bi2Se3: thickness = {bi2se3_thickness_nm} nm × n")
plt.grid(alpha=0.3)
plt.show()

# %% [markdown]
# ## Part 3 — Hexagon geometry: the honeycomb lattice
# ### Task 8 (Core) — HSG.MG.A.1–3
# Many 2D crystals, including MoS₂, arrange their atoms in a hexagonal (honeycomb)
# pattern when viewed from above. Run the helper cell to draw one.

# %%
# @title Helper code (just run this)
def draw_honeycomb(a_nm=0.316, n_rows=3, n_cols=3):
    dx, dy = 1.5 * a_nm, np.sqrt(3) * a_nm
    fig, ax = plt.subplots(figsize=(6, 6))
    metal_pts, chalc_pts = [], []
    for row in range(n_rows):
        for col in range(n_cols):
            cx = col * dx
            cy = row * dy + (dy / 2 if col % 2 else 0)
            verts = [(cx + a_nm * np.sin(k * np.pi / 3), cy + a_nm * np.cos(k * np.pi / 3)) for k in range(6)]
            ax.add_patch(plt.Polygon(verts, closed=True, facecolor="none", edgecolor="0.6", linewidth=1))
            for k, (vx, vy) in enumerate(verts):
                (metal_pts if k % 2 == 0 else chalc_pts).append((vx, vy))
    metal_pts, chalc_pts = np.array(metal_pts), np.array(chalc_pts)
    ax.scatter(*metal_pts.T, s=80, color="#2b6cb0", label="metal atom (e.g. Mo)", zorder=3)
    ax.scatter(*chalc_pts.T, s=50, color="#dd6b20", label="chalcogen atom (e.g. S)", zorder=3)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.legend(loc="upper right", fontsize=9)
    ax.set_title(f"Top-down honeycomb lattice, a = {a_nm} nm")
    plt.tight_layout()
    plt.show()

draw_honeycomb()

# %% [markdown]
# > **Scientist's note:** A real TMD like MoS₂ is *not* a sheet of identical dots. Each
# > 2D unit cell holds **two kinds of atoms** — one metal atom (Mo, W, ...) and two
# > chalcogen atoms (S, Se, ...) — sitting at different heights, not just different spots
# > on one flat honeycomb. The picture above is a simplified top-down model, useful for
# > the geometry ahead, not a literal atom-for-atom photograph.

# %% [markdown]
# The area of one 2D unit cell of a hexagonal lattice with lattice constant `a` is
# `area = (√3 / 2) × a²`. Look up MoS₂'s lattice constant from `materials_reference`.

# %%
mos2_a_nm = materials.loc[materials.material == "MoS2", "lattice_constant_nm"].iloc[0]
cell_area_nm2 = (np.sqrt(3) / 2) * mos2_a_nm ** 2
print(f"MoS2 lattice constant a = {mos2_a_nm} nm")
print(f"Unit cell area = {cell_area_nm2:.4f} nm²")

# %% [markdown]
# ### Task 9 (Explore) — unit cells on a fingernail
# A fingernail is roughly 1 cm² — that's 1×10¹⁴ nm². How many MoS₂ unit cells fit on it?

# %%
fingernail_area_nm2 = 1e14   # 1 cm^2 in nm^2 -- <-- change me to try a different area (e.g. a grain of rice)

cells_on_fingernail = fingernail_area_nm2 / cell_area_nm2
print(f"About {cells_on_fingernail:.2e} unit cells fit on a 1 cm² fingernail.")

# %% [markdown]
# ### Task 10 (Extend) — atoms, not just cells
# Each MoS₂ unit cell holds 1 Mo atom and 2 S atoms (3 atoms total). How many atoms is that?

# %%
atoms_per_cell = 3   # <-- change me if you pick a different material's formula
atoms_on_fingernail = cells_on_fingernail * atoms_per_cell
print(f"About {atoms_on_fingernail:.2e} atoms on that fingernail.")

# %% [markdown]
# ## Part 4 — Surface-area-to-volume: why nanomaterials are "all surface"
# ### Task 11 (Core) — HSG.MG.A.1–3
# Shrink a cube from 1 cm down to 1 nm. For a cube of side `s`, surface area is `6s²` and
# volume is `s³`, so the surface-area-to-volume ratio simplifies to `6/s`.

# %%
sides_m = np.array([1e-2, 1e-3, 1e-4, 1e-5, 1e-6, 1e-7, 1e-8, 1e-9])   # 1 cm down to 1 nm
side_labels = ["1 cm", "1 mm", "100 µm", "10 µm", "1 µm", "100 nm", "10 nm", "1 nm"]

sa_to_v = 6 / sides_m   # units: 1/m
cube_table = pd.DataFrame({"side": side_labels, "side (m)": sides_m, "SA:V (1/m)": sa_to_v})
print(cube_table)

plt.plot(sides_m, sa_to_v, marker="o", color="tab:green")
plt.xscale("log")
plt.yscale("log")
plt.xlabel("cube side (m, log scale)")
plt.ylabel("surface-area-to-volume ratio (1/m, log scale)")
plt.title("Shrinking a cube: SA:V ratio = 6 / side")
plt.grid(alpha=0.3, which="both")
plt.show()

# %% [markdown]
# **Your answer:** As the cube shrinks from 1 cm to 1 nm (a factor of 10 million), by what
# factor does the SA:V ratio grow? Why does that make sense from `6/s`?

# %% [markdown]
# > **Scientist's note:** A huge surface-area-to-volume ratio is *one* reason
# > nanomaterials behave differently from bulk material — more atoms sit at or near a
# > surface, where bonding is different. But it is not the *whole* story: quantum
# > confinement, electron screening, and interfaces with other materials also shape how
# > a monolayer behaves. Don't treat SA:V ratio alone as a full explanation.

# %% [markdown]
# ## Part 5 — 3D print your crystal
# ### Task 12 (Core / Extend) — HSG.SRT, scale factors
# Export the Bi₂Se₃ scan as a 3D-printable STL file. Choose a width and a "relief"
# height (how tall the tallest bump rises above the base) — the model must stay
# printable, so keep relief noticeably smaller than width.

# %%
width_mm = 80      # <-- change me: how wide the printed model should be, in millimetres
relief_mm = 10      # <-- change me: how tall the tallest bump should rise, in millimetres

stl_path = to_stl(scans["triangle_pyramids"], "my_crystal.stl", width_mm=width_mm, relief_mm=relief_mm)
print(f"Saved {stl_path}")

# %% [markdown]
# ### Task 13 (Explore) — compare the two scale factors
# The model is wide (horizontal) exactly as scaled as you chose — but the real surface
# relief was only a few nanometres tall, and you stretched it to `relief_mm`. Compute
# both scale factors and compare.

# %%
scan = scans["triangle_pyramids"]
real_width_mm = scan.scan_um * 1e-3                       # µm -> mm
real_relief_nm = float(np.ptp(scan.z))                     # tallest bump minus deepest dip, in nm
real_relief_mm = real_relief_nm * 1e-6                     # nm -> mm

horizontal_scale = width_mm / real_width_mm
vertical_scale = relief_mm / real_relief_mm
vertical_exaggeration = vertical_scale / horizontal_scale

print(f"Real scan: {real_width_mm:.4f} mm wide, {real_relief_mm:.6f} mm of real relief")
print(f"Horizontal scale factor: {horizontal_scale:.3g}×")
print(f"Vertical scale factor:   {vertical_scale:.3g}×")
print(f"Vertical exaggeration (vertical ÷ horizontal): {vertical_exaggeration:.3g}×")

# %% [markdown]
# > **Scientist's note:** Every 3D-printed AFM model uses *some* vertical exaggeration —
# > otherwise nanometre-tall bumps would be invisible on a centimetre-wide print. That's
# > fine, as long as the model says so. Never let anyone assume a printed model's height
# > is drawn to the same scale as its width.

# %% [markdown]
# ### Download your file
# **Safety note:** this notebook only creates a digital file. If you send it to a real
# 3D printer, follow your school's printer rules (supervision, ventilation, and heat
# safety) exactly as you would for any other print job.

# %%
try:
    from google.colab import files
    files.download(str(stl_path))
except ImportError:
    print(f"Not running in Colab — find {stl_path} in this notebook's working folder.")

# %% [markdown]
# ## Exit ticket
# Answer these without writing any code.
#
# 1. If you doubled the scale factor in Part 1, would the football-field-sized MoS₂
#    layer get thicker or thinner — and by what factor?
# 2. A classmate measures a step height of 2.9 nm on the Bi₂Se₃ scan. About how many
#    layers is that, and how do you know?
# 3. Two students 3D print the same scan. One uses 5 mm of relief, the other uses
#    15 mm, with the same width. Whose print has the larger vertical exaggeration, and
#    why does that matter when comparing the two prints?
