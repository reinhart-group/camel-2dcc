"""Extra payload builders for the model and dials round items.

Imports catalog_data and reshapes its outputs; never edits catalog_data.py.
"""
from __future__ import annotations

import catalog_data as cd


def heightmap_profile(key: str, size: int = 96) -> dict:
    """Same real height grid as cd.heightmap, without the rendered PNG.

    profile_reader draws its own heatmap from the numeric grid (so a learner
    can drag a line and read exact values), so the base64 image would only
    add payload weight without being used.
    """
    hm = cd.heightmap(key, size=size)
    return {"heights": hm["heights"], "width_um": hm["width_um"], "info": hm["info"]}
