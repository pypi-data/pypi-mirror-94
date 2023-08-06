import pytest
from pandas import Series, DataFrame

from trashpanda import (
    add_blank_rows,
    cut_dataframe_after_max,
    _ensure_dataframe,
    add_missing_indexes_to_series,
)


_a_list_of_3 = [1, 2, 3]


def test_add_blank_rows_exceptions():
    with pytest.raises(TypeError):
        add_blank_rows(_a_list_of_3, 0.0)


def test_cut_dataframe_after_max_exception():
    with pytest.raises(ValueError):
        cut_dataframe_after_max(DataFrame([[1, 2]], columns=["a", "b"]))


def test_add_missing_index_to_series_exception():
    with pytest.raises(TypeError):
        add_missing_indexes_to_series(Series([1]), [0.1])


def test_ensuring_dataframe():
    sample_series = Series(_a_list_of_3)
    now_a_dataframe = _ensure_dataframe(sample_series)
    assert isinstance(now_a_dataframe, DataFrame)