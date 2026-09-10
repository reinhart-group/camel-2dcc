"""Find islands ("grains") on an AFM height map with a simple, visible rule.

The rule, in words a student can check against the picture:
1. Level each scan line using only the low (substrate) pixels, so the islands
   don't tilt the fit.
2. Call a pixel "island" if it is higher than halfway between the substrate
   level and the typical island top.
3. Each connected blob of island pixels is one grain. Blobs smaller than a
   few pixels are noise; blobs touching the scan border are cut off, so they
   are flagged rather than measured as whole grains.

This is a height-threshold rule, not a scientist's hand count; the notebook
always draws the outlines so the rule can be judged by eye.
"""

from __future__ import annotations

import numpy as np


KIND_COLOURS = {"single": "#2ca02c", "merged": "#ff7f0e", "dust": "#d62798", "streak": "#1f77b4"}


def load_grain_scans(data_dir: str = "camel-2dcc"):
    """(scans, table): scans = {key: {"z", "labels", **meta}}, table = grains DataFrame."""
    import json
    from pathlib import Path

    import pandas as pd

    root = Path(data_dir) / "grains"
    table = pd.read_csv(root / "grains.csv")
    scans = {}
    for meta in json.loads((root / "scans.json").read_text()):
        with np.load(root / f"{meta['key']}.npz") as blob:
            scans[meta["key"]] = {"z": blob["height_nm"].astype(float), "labels": blob["labels"], **meta}
    return scans, table


def whole_single(table, scan: str | None = None):
    """Grains that are one clean island fully inside the scan (the ones we measure)."""
    t = table[(table["kind"] == "single") & ~table["touches_edge"] & ~table["touches_glitch"]]
    return t if scan is None else t[t["scan"] == scan]


def show_grains(scan: dict, table, ax=None, kinds=("single", "merged", "dust", "streak"), number=False):
    """Grey height map with each grain outlined in its kind's colour."""
    import matplotlib.pyplot as plt
    from matplotlib.colors import to_rgba
    from skimage.segmentation import find_boundaries

    z, labels = scan["z"], scan["labels"]
    ax = ax or plt.subplots(figsize=(7, 7))[1]
    size_nm = scan["scan_um"] * 1000
    lo, hi = np.percentile(z, [1, 99])
    ax.imshow(z, cmap="gray", vmin=lo, vmax=hi, extent=[0, size_nm, size_nm, 0])
    edges = find_boundaries(labels)
    overlay = np.zeros((*z.shape, 4))
    rows = table[table["scan"] == scan["key"]]
    for gid, kind in zip(rows["grain"], rows["kind"]):
        if kind in kinds:
            overlay[edges & (labels == gid)] = to_rgba(KIND_COLOURS[kind])
    ax.imshow(overlay, extent=[0, size_nm, size_nm, 0])
    if number:
        for _, r in rows[rows["kind"].isin(kinds)].iterrows():
            ax.text(r["col"] * scan["pixel_nm"], r["row"] * scan["pixel_nm"], str(r["grain"]),
                    color="yellow", fontsize=7, ha="center", va="center")
    ax.set(xlabel="x (nm)", ylabel="y (nm)", title=f"{scan['key']} ({scan['position']})")
    return ax


def line_profile(scan: dict, start_nm, end_nm, width_px: int = 3):
    """Heights along a straight line between two points given in nm (x, y).

    Returns (distance_nm, height_nm). ``width_px`` averages a few neighbouring
    lines to calm the noise.
    """
    from skimage.measure import profile_line

    px = scan["pixel_nm"]
    (x0, y0), (x1, y1) = start_nm, end_nm
    h = profile_line(scan["z"], (y0 / px, x0 / px), (y1 / px, x1 / px), linewidth=width_px,
                     mode="reflect", reduce_func=np.mean)
    d = np.linspace(0, np.hypot(x1 - x0, y1 - y0), len(h))
    return d, h


def profile_through_grain(scan: dict, table, grain: int, angle_deg: float = 0.0, reach: float = 1.6):
    """A line through a grain's centre at ``angle_deg``, extending ``reach`` × the grain's
    triangle side on each side so the flat substrate shows at both ends."""
    r = table[(table["scan"] == scan["key"]) & (table["grain"] == grain)].iloc[0]
    cx, cy = r["col"] * scan["pixel_nm"], r["row"] * scan["pixel_nm"]
    half = reach * r["side_nm"] / 2
    dx, dy = half * np.cos(np.radians(angle_deg)), half * np.sin(np.radians(angle_deg))
    start, end = (cx - dx, cy - dy), (cx + dx, cy + dy)
    return line_profile(scan, start, end), (start, end)


def random_sample(values, n: int, seed: int | None = None):
    """Pick n values at random without repeats (like drawing names from a hat)."""
    rng = np.random.default_rng(seed)
    return rng.choice(np.asarray(values), size=n, replace=False)


def level_on_substrate(z: np.ndarray, iterations: int = 3) -> np.ndarray:
    """Per-line straight-line levelling fitted only to substrate pixels."""
    x = np.arange(z.shape[1])
    out = z - np.median(z, axis=1, keepdims=True)
    for _ in range(iterations):
        cut = np.percentile(out, 50)
        leveled = np.empty_like(out)
        for i, row in enumerate(out):
            low = row <= cut
            if low.sum() < 10:
                low = np.ones_like(row, dtype=bool)
            c = np.polyfit(x[low], row[low], 1)
            leveled[i] = row - np.polyval(c, x)
        out = leveled - np.median(leveled[leveled <= np.percentile(leveled, 50)])
    return out


def glitch_rows(z: np.ndarray, factor: float = 8.0) -> np.ndarray:
    """Rows whose spread is far above the typical row (tip jumps, scan errors)."""
    s = z.std(axis=1)
    return s > factor * np.median(s)


def find_grains(z: np.ndarray, pixel_nm: float, threshold_nm: float | None = None,
                min_pixels: int = 12):
    """Label islands. Returns (labels, table, threshold_nm).

    ``table`` is a list of dicts, one per grain: area_nm2, height_nm (mean
    height above substrate), side_nm (side of an equilateral triangle with the
    same area), perimeter_nm, solidity, centroid (row, col), touches_edge,
    touches_glitch.
    """
    from skimage import measure, morphology

    bad = glitch_rows(z)
    zc = z.copy()
    zc[bad] = np.nan
    if threshold_nm is None:
        # Typical island top = the median of pixels clearly above the substrate
        # noise (6 robust standard deviations). A fixed percentile fails when
        # islands cover only a few percent of the scan: it lands in the noise.
        good = zc[~np.isnan(zc)]
        noise = 1.4826 * np.median(np.abs(good - np.median(good)))
        above = good[good > np.median(good) + 6 * noise]
        top = np.median(above) if above.size >= min_pixels else np.percentile(good, 97)
        threshold_nm = 0.5 * top               # halfway between substrate (0) and top
    mask = np.nan_to_num(zc, nan=-np.inf) > threshold_nm
    labels_all = measure.label(mask, connectivity=1)
    sizes = np.bincount(labels_all.ravel())
    mask = mask & (sizes[labels_all] >= min_pixels)  # drop specks smaller than min_pixels
    labels = measure.label(mask, connectivity=1)
    rows_bad = np.where(bad)[0]
    props = list(measure.regionprops(labels, intensity_image=np.nan_to_num(zc)))
    heights = [float(np.mean(r.image_intensity[r.image])) for r in props]
    typical_height = float(np.median(heights)) if heights else 0.0
    table = []
    for r, height in zip(props, heights):
        minr, minc, maxr, maxc = r.bbox
        area = r.area * pixel_nm ** 2
        streak = r.axis_minor_length < 2.5 or r.eccentricity > 0.98  # a thin line = scan glitch
        dust = height > 2.5 * typical_height                        # far taller than the islands
        merged = r.solidity < 0.8                                   # touching grains joined together
        kind = ("streak" if streak else "dust" if dust else "merged" if merged else "single")
        table.append({
            "kind": kind,
            "grain": r.label,
            "area_nm2": float(area),
            "side_nm": float(np.sqrt(4 * area / np.sqrt(3))),
            "perimeter_nm": float(r.perimeter * pixel_nm),
            "height_nm": float(np.mean(r.image_intensity[r.image])),
            "solidity": float(r.solidity),
            "row": float(r.centroid[0]), "col": float(r.centroid[1]),
            "touches_edge": bool(minr == 0 or minc == 0 or maxr == z.shape[0] or maxc == z.shape[1]),
            "touches_glitch": bool(np.any((rows_bad >= minr - 1) & (rows_bad <= maxr))),
        })
    return labels, table, float(threshold_nm)
