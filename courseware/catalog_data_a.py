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


def small_heightmap(key: str, max_px: int = 224, quality: int = 78) -> dict:
    """A phone-sized JPEG version of cd.heightmap's PNG, so one image stays well under budget."""
    from PIL import Image

    d = cd.heightmap(key)
    im = Image.open(io.BytesIO(base64.b64decode(d["png"]))).convert("RGB")
    im.thumbnail((max_px, max_px))
    buf = io.BytesIO()
    im.save(buf, format="JPEG", quality=quality)
    return {"img": base64.b64encode(buf.getvalue()).decode(), "width_um": d["width_um"]}


def recipe_trace(sample_id: int) -> dict:
    """A growth recipe's temperature over time, stopping at the first step with no recorded temperature."""
    steps = cd.recipe(sample_id)
    points = []
    for s in steps:
        if s["temp"] is None:
            break
        points.append([s["start"], s["temp"]])
        if s["dur"] is not None:
            points.append([s["start"] + s["dur"], s["temp"]])
    return {"points": points, "blank_steps": sum(1 for s in steps if s["temp"] is None)}


def transport_points() -> list[list[float]]:
    return [[r["T"], r["R"]] for r in cd.transport()]
