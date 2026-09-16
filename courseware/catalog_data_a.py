"""Extra payload builders for the warmup/mess items, layered on top of catalog_data."""
from __future__ import annotations

import base64
import io
from collections import Counter

import catalog_data as cd


def material_labels() -> list[dict]:
    """Every raw material spelling as typed, with its row count and what auto-cleanup would call it."""
    rows = cd.samples(clean=False)
    c = Counter(r["mat"] for r in rows if r["mat"] is not None)
    return [{"raw": raw, "n": n, "canon": cd.canonical(raw), "is_sub": raw in cd.SUBSTRATES}
            for raw, n in c.most_common()]


def _nice_bar_um(width_um: float) -> float:
    """A round scale-bar length near 30% of the scan width, never hardcoded to one scan."""
    candidates = [0.05, 0.1, 0.2, 0.25, 0.5, 1, 2, 5, 10, 20, 50]
    target = width_um * 0.3
    best = candidates[0]
    for c in candidates:
        if c <= target:
            best = c
    return best


def small_heightmap(key: str, px: int = 320, dpi: int = 110, colors: int = 64) -> dict:
    """A labelled AFM height map as a PNG, rendered from the full-resolution source array.

    Unlike cd.heightmap (which strides the source down to ~96 px before drawing it), this
    renders every real pixel of the scan -- no source downsampling -- with a colourbar
    (height in nm) and a scale bar whose length is derived from the scan's real width.
    A matplotlib render of untouched, noisy real-valued data does not compress as PNG at
    full color depth, so the rendered picture (only the picture, never the underlying
    height values) is palette-quantized to `colors` colors afterward to stay near the
    CONTRACT's per-item payload budget. Kept as PNG throughout: this is false-color
    scientific data, and JPEG's block artifacts would misrepresent it.
    """
    import numpy as np
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from PIL import Image

    z = np.load(cd.SLICE / f"afm_gallery/{key}.npz")
    h = z["height_nm"]
    width_um = float(z["x_um"].max())
    lo, hi = np.percentile(h, [1, 99])  # this gallery has a glitch reaching -455 nm; percentile
    # limits keep the color scale on the real crystals instead of being blown out by it.
    bar_um = _nice_bar_um(width_um)

    fig, ax = plt.subplots(figsize=(px / dpi, px / dpi), dpi=dpi)
    im = ax.imshow(h, cmap="afmhot", vmin=lo, vmax=hi, origin="lower",
                    extent=[0, width_um, 0, width_um])
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    cb = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.03)
    cb.set_label("height (nm)", fontsize=9)
    cb.ax.tick_params(labelsize=8)
    x0, y0 = width_um * 0.06, width_um * 0.06
    ax.plot([x0, x0 + bar_um], [y0, y0], color="white", lw=3, solid_capstyle="butt")
    ax.text(x0 + bar_um / 2, y0 + width_um * 0.035, f"{bar_um:g} µm", color="white",
            ha="center", va="bottom", fontsize=9, fontweight="bold")

    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", pad_inches=0.04)
    plt.close(fig)

    picture = Image.open(io.BytesIO(buf.getvalue())).convert("RGB")
    quantized = picture.quantize(colors=colors, method=Image.MEDIANCUT)
    out = io.BytesIO()
    quantized.save(out, format="PNG", optimize=True)
    return {"img": base64.b64encode(out.getvalue()).decode(), "width_um": width_um}


def recipe_trace(sample_id: int) -> dict:
    """A growth recipe's step-by-step *target* temperature versus elapsed time.

    This is a table of setpoints, not a continuous measurement: every flat segment and any
    instant jump between segments comes from how the steps were logged, not a real-time
    reading, so a real furnace's ramp/cooldown time is simply not in this data. A step can be
    missing its target two different ways depending on the sample: as a blank (None), where
    this function stops the trace, or as a literal 0.0, which some recipes (this dataset's
    cooldown steps, for example) use in place of a blank. This function does NOT special-case
    0.0 -- it is plotted like any other value -- so callers must check `zero_steps` and say so
    before describing a 0.0 point as a real temperature reading.
    """
    steps = cd.recipe(sample_id)
    points = []
    for s in steps:
        if s["temp"] is None:
            break
        points.append([s["start"], s["temp"]])
        if s["dur"] is not None:
            points.append([s["start"] + s["dur"], s["temp"]])
    return {
        "points": points,
        "blank_steps": sum(1 for s in steps if s["temp"] is None),
        "zero_steps": sum(1 for s in steps if s["temp"] == 0.0),
    }


def transport_points() -> list[list[float]]:
    return [[r["T"], r["R"]] for r in cd.transport()]
