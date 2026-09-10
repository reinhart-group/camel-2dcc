import numpy as np
import pandas as pd
import pytest

from camel_data.contracts import ContractError, check_shapes


def test_series_ok_and_bad():
    ns = {"series_values": np.array([1.0, 2.0, 3.0]), "series_label": "area", "series_unit": "nm²"}
    check_shapes(ns, ["series"])
    with pytest.raises(ContractError, match="series_unit"):
        check_shapes({k: v for k, v in ns.items() if k != "series_unit"}, ["series"])
    with pytest.raises(ContractError, match="finite"):
        check_shapes({**ns, "series_values": np.array([1.0, np.nan, 3.0])}, ["series"])


def test_groups_needs_value_and_group_columns():
    ok = {"groups_table": pd.DataFrame({"value": [1.0, 2.0], "group": ["a", "b"]}),
          "groups_label": "area", "groups_unit": "nm²"}
    check_shapes(ok, ["groups"])
    with pytest.raises(ContractError, match="group"):
        check_shapes({**ok, "groups_table": pd.DataFrame({"value": [1.0]})}, ["groups"])
