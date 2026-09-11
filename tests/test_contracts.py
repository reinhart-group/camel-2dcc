import numpy as np
import pandas as pd
import pytest

from camel_data.contracts import ContractError, check_shapes, clear_shapes


def test_series_ok_and_bad():
    ns = {"series_values": np.array([1.0, 2.0, 3.0]), "series_label": "area", "series_unit": "nm²"}
    check_shapes(ns, ["series"])
    with pytest.raises(ContractError, match="series_unit"):
        check_shapes({k: v for k, v in ns.items() if k != "series_unit"}, ["series"])
    with pytest.raises(ContractError, match="finite"):
        check_shapes({**ns, "series_values": np.array([1.0, np.nan, 3.0])}, ["series"])


def test_groups_needs_value_and_group_columns():
    ok = {"groups_table": pd.DataFrame({"value": [1.0, 2.0, 3.0, 4.0],
                                        "group": ["a", "b", "a", "b"]}),
          "groups_label": "area", "groups_unit": "nm²"}
    check_shapes(ok, ["groups"])
    with pytest.raises(ContractError, match="group"):
        check_shapes({**ok, "groups_table": pd.DataFrame({"value": [1.0]})}, ["groups"])


def test_map_contract_and_clear_shapes():
    ns = {"map_values": np.ones((3, 4)), "map_width_nm": 5000.0,
          "map_label": "height", "map_unit": "nm"}
    check_shapes(ns, ["map"])
    clear_shapes(ns, ["map"])
    assert not any(name.startswith("map_") for name in ns)


def test_unknown_shape_is_a_contract_error():
    with pytest.raises(ContractError, match="unknown data shape"):
        check_shapes({}, ["not-a-shape"])
