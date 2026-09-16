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
                        "each film came out. You can also compare by material, or by "
                        "“substrate” — the wafer the crystal was grown on top of. "
                        "Do the groups look different?",
            "groupings": [{"key": "meth", "label": "growth method"},
                          {"key": "mat", "label": "material"},
                          {"key": "sub", "label": "substrate"}],
            "value_key": "rough", "value_label": "roughness (nm)", "unit": "nm",
            "max_groups": 5, "min_n": 8,
            "range_toggle": True, "default_view": "full",
            "full_label": "full range (with outliers)",
            "clip_label": "typical range (zoomed in, hides the biggest outliers)",
            "note": "This chart starts by showing every sample, including the roughest outliers, "
                    "because the spread — not just the middle — is the point of this comparison. "
                    "Switch to the zoomed-in view to see the typical samples more clearly, but "
                    "remember the note it gives you: some samples get pinned to the top edge "
                    "there, not shown at their real height. Roughness also depends on how big an "
                    "area the microscope scanned, so groups measured at different scan sizes are "
                    "not a perfectly fair comparison either.",
        },
    },
]
