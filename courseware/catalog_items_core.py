"""Reference items, written by hand as the pattern for the rest."""
from __future__ import annotations

import catalog_data as cd

ITEMS = [
    {
        "id": "M-01",
        "round": "mess",
        "title": "Does the growth method change how rough the film is?",
        "blurb": "Box plots of measured roughness by growth method, material, or substrate, with "
                 "medians and the gap between the two biggest groups.",
        "grades": "6-12",
        "source": "1,005 samples with AFM roughness, 2DCC LiST records",
        "item": "group_compare",
        "data": lambda: cd.compact(cd.samples(clean=True),
                                   ["mat", "meth", "sub", "rough", "scan"]),
        "opts": {
            "question": "Penn State grew these crystals two different ways and measured how rough "
                        "each film came out. Do the groups look different?",
            "groupings": [{"key": "meth", "label": "growth method"},
                          {"key": "mat", "label": "material"},
                          {"key": "sub", "label": "substrate"}],
            "value_key": "rough", "value_label": "roughness (nm)", "unit": "nm",
            "allow_log": True, "max_groups": 5, "min_n": 8,
            "note": "Roughness depends on how big an area the microscope scanned, so groups "
                    "measured at different scan sizes are not a fair comparison.",
        },
    },
]
