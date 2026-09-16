"""Extra payload builders for the warmup/mess items, layered on top of catalog_data."""
from __future__ import annotations

import base64
import io
from collections import Counter

import catalog_data as cd


# Plain-English glosses for the 22 no-semicolon spellings, written for a reader who knows no
# materials science. Sourced from data/slice/camel-2dcc/materials_reference.csv and
# data/slice/camel-2dcc/afm_gallery/gallery.json (both shipped with this repo) wherever those
# name the substance; a few (MnTe, PtSe2, and the SnTe-Sb/SnTe-Bi/2H-MoS2/MoS2-WS2 readings) are
# general chemistry knowledge or an inferred reading of the naming pattern, not text lifted from
# either source, and are marked as such below.
MATERIAL_GLOSS = {
    "MoS2": "molybdenum disulfide — a thin semiconductor crystal, a leading candidate for "
            "ultra-thin computer-chip transistors.",
    "WSe2": "tungsten diselenide — another semiconductor crystal, often paired with MoS2 to "
            "build transistor logic.",
    "WS2": "tungsten disulfide — a semiconductor crystal that glows brightly as a single layer.",
    "GaSe": "gallium selenide — used in nonlinear optics, changing the colour of laser light.",
    "In2Se3": "indium selenide — a ferroelectric crystal that can hold a memory state with no power.",
    "MoSe2": "molybdenum diselenide — a light-emitting semiconductor crystal, often grown "
             "alongside WSe2.",
    "SnSe": "tin selenide — a thermoelectric crystal that can turn heat into electricity.",
    "Mo-WSe2": "an alloy: tungsten diselenide grown with some molybdenum mixed in — still one "
               "substance, just not pure WSe2.",
    "FeSe": "iron selenide — a superconductor: it carries electricity with zero resistance "
            "once cooled.",
    "InSe": "indium selenide — prized for very fast-moving electrons in future transistors.",
    "(Bi1-x, Inx)2Se3": "an alloy of bismuth selenide with some indium swapped in, grown to study "
                        "how the mix changes its properties.",
    "SnTe": "tin telluride — a semiconductor crystal that can grow extremely flat.",
    "MnTe": "manganese telluride — a semiconductor crystal. (General chemistry knowledge; not "
            "described anywhere else in this repo's data.)",
    "Bi2Se3": "bismuth selenide — a topological insulator: its surface conducts electricity "
              "while its interior does not.",
    "SnTe-Sb": "likely tin telluride with antimony mixed in, an alloy. (Read from the naming "
               "pattern used elsewhere for Mo-WSe2; not directly documented.)",
    "Al2O3": "aluminum oxide — this is sapphire, the disc many crystals are grown ON. It is "
             "not the crystal itself.",
    "SnTe-Bi": "likely tin telluride with bismuth mixed in, an alloy. (Read from the naming "
               "pattern used elsewhere for Mo-WSe2; not directly documented.)",
    "GaAs": "gallium arsenide — a substrate wafer some crystals are grown ON here, not a "
            "grown crystal itself.",
    "2H-MoS2": "the same substance as MoS2 — “2H” just names which way its atomic "
               "layers stack.",
    "MoS2-WS2": "reads like two crystal names joined by a hyphen instead of a semicolon — "
                "maybe two materials grown in one run. (Only 1 row; genuinely ambiguous.)",
    "Se": "selenium — a raw chemical element, not a crystal that was grown.",
    "PtSe2": "platinum diselenide — a layered semiconductor crystal in the same family as "
             "MoS2. (General chemistry knowledge; not described anywhere else in this repo's data.)",
}


def material_labels() -> list[dict]:
    """Every raw material spelling as typed, with its row count, what auto-cleanup would call it,
    and (for the 22 no-semicolon spellings) a plain-English gloss of what the substance actually is."""
    rows = cd.samples(clean=False)
    c = Counter(r["mat"] for r in rows if r["mat"] is not None)
    return [{"raw": raw, "n": n, "canon": cd.canonical(raw), "is_sub": raw in cd.SUBSTRATES,
             "gloss": MATERIAL_GLOSS.get(raw)}
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


def small_heightmap(key: str, px: int = 580, dpi: int = 110, colors: int = 256) -> dict:
    """A labelled AFM height map as a PNG, rendered from the full-resolution source array.

    Unlike cd.heightmap (which strides the source down to ~96 px before drawing it), this
    renders every real pixel of the scan -- no source downsampling -- with a colourbar
    (height in nm) and a scale bar whose length is derived from the scan's real width.
    A matplotlib render of untouched, noisy real-valued data does not compress as PNG at
    full color depth, so the rendered picture (only the picture, never the underlying
    height values) is palette-quantized to `colors` colors afterward. Kept as PNG
    throughout: this is false-color scientific data, and JPEG's block artifacts would
    misrepresent it.

    The defaults were measured on wse2_triangles, the scan W-01 uses. At 320 px and 64
    colors the picture came out 317x237 and visibly banded, because afmhot is a
    continuous color map and 64 steps are not enough to carry it: the mean error against
    an unquantized render is 1.87 of 255. At 580 px and 256 colors the picture is 519x424
    and the mean error is 0.87 of 255, with the payload at 221 KB of base64. Dropping
    quantization altogether costs 378 KB of PNG to remove that remaining 0.87, which is
    not a trade worth making on a page a phone has to load.
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
