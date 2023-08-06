#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
.. doctest::

    # Test for wrong __all__ module attribute.
    >>> from trashpanda import *
"""
__author__ = """David Scheliga"""
__email__ = "david.scheliga@gmx.de"
__version__ = "1.0.0"
__all__ = [
    "add_blank_rows",
    "add_columns_to_dataframe",
    "add_missing_indexes_to_series",
    "cut_after",
    "cut_before",
    "cut_dataframe_after_max",
    "cut_series_after_max",
    "get_intersection",
    "get_unique_index_positions",
    "find_index_of_value_in_series",
    "meld_along_columns",
    "override_left_with_right_dataframe",
    "override_left_with_right_series",
    "remove_duplicated_indexes",
]

import logging
import warnings
from typing import (
    Optional,
    List,
    Any,
    Union,
    overload,
    Iterable,
)

# create LOGGER with this namespace's name
import numpy
import pandas
from pandas import DataFrame, Series

_logger = logging.getLogger("trashpanda")
_logger.setLevel(logging.ERROR)
# create console handler and set level to debug
writes_logs_onto_console = logging.StreamHandler()
# add formatter to ch
writes_logs_onto_console.setFormatter(
    logging.Formatter(
        "%(asctime)s - %(name)s - %(module)s - %(funcName)s "
        "- %(lineno)s - %(levelname)s - %(message)s"
    )
)


DEFAULT_NA = pandas.NA


@overload
def get_intersection(
    source: DataFrame, targeted_indexes: Union[List, pandas.Index]
) -> DataFrame:
    pass


@overload
def get_intersection(
    source: Series, targeted_indexes: Union[List, pandas.Index]
) -> Series:
    pass


def get_intersection(
    source: Union[DataFrame, Series], targeted_indexes: Union[List, pandas.Index]
) -> Union[DataFrame, Series]:
    """
    Intersects Series or DataFrame by requested indexes. A subsection from the
    *source* is made for the *targeted_indexes*, which must not necessaraly
    be whithin the *source*.

    Args:
        source(Union[DataFrame, Series]):
            Values from which an intersection will be retrieved.

        targeted_indexes(Index):
            The indexes which the returned Series should contain.

    Returns:
        Union[DataFrame, Series]

    Examples:

        *Usage with pandas.Series*

        >>> from pandas import Series
        >>> sample_series = Series(list(range(3)), index=list(iter("abc")), name="foo")
        >>> get_intersection(sample_series, ["b", "c", "d"])
        b    1
        c    2
        Name: foo, dtype: int64
        >>> get_intersection(sample_series, ["x", "y", "z"])
        Series([], Name: foo, dtype: int64)

        *Usage with pandas.DataFrame*

        >>> from pandas import DataFrame
        >>> sample_series = DataFrame(
        ...     list(range(3)), index=list(iter("abc")), columns=["foo"]
        ... )
        >>> get_intersection(sample_series, ["b", "c", "d"])
           foo
        b    1
        c    2
        >>> get_intersection(sample_series, ["x", "y", "z"])
        Empty DataFrame
        Columns: [foo]
        Index: []

    """
    existing_indexes = source.index
    possible_indexes = existing_indexes.intersection(targeted_indexes)
    requested_series = source.loc[possible_indexes]
    return requested_series


@overload
def cut_after(source_to_cut: Series, cutting_index: float) -> Series:
    pass


@overload
def cut_after(source_to_cut: DataFrame, cutting_index: float) -> DataFrame:
    pass


def cut_after(
    source_to_cut: Union[Series, DataFrame], cutting_index: float
) -> Union[Series, DataFrame]:
    """
    Cuts a dataframe dropping the part after the cutting index. The cutting
    index will be added to the frame, which values are being interpolated, if inside.

    Args:
        source_to_cut(Union[Series, DataFrame]):
            Source frame to be cut at the cutting index.

        cutting_index(float):
            Cutting index at which the source frame should be cut.

    Returns:
        Union[Series, DataFrame]

    Examples:

        *Usage with pandas.Series*

        >>> import numpy
        >>> from pandas import Series, Index
        >>> from doctestprinter import doctest_print
        >>> from trashpanda import cut_after
        >>> sample_series = Series(
        ...     numpy.arange(3.0),
        ...     index=Index([0.1, 0.2, 0.3], name="x"),
        ...     name="y"
        ... )
        >>> sample_series
        x
        0.1    0.0
        0.2    1.0
        0.3    2.0
        Name: y, dtype: float64
        >>> cut_after(sample_series, 0.1)
        x
        0.1    0.0
        Name: y, dtype: float64
        >>> cut_after(sample_series, 0.14)
        x
        0.10    0.0
        0.14    0.4
        Name: y, dtype: float64
        >>> cut_after(sample_series, 0.2)
        x
        0.1    0.0
        0.2    1.0
        Name: y, dtype: float64
        >>> cut_after(sample_series, 0.31)
        x
        0.10    0.0
        0.20    1.0
        0.30    2.0
        0.31    NaN
        Name: y, dtype: float64
        >>> cut_after(sample_series, 0.0)
        Series([], Name: y, dtype: float64)

        *Usage with a pandas.DataFrame*

        >>> import numpy
        >>> from pandas import DataFrame, Index
        >>> from doctestprinter import doctest_print
        >>> from trashpanda import cut_after
        >>> sample_frame = DataFrame(
        ...     numpy.arange(6.0).reshape(3, 2),
        ...     columns=["b", "a"],
        ...     index=Index([0.1, 0.2, 0.3], name="x")
        ... )
        >>> doctest_print(sample_frame)
               b    a
        x
        0.1  0.0  1.0
        0.2  2.0  3.0
        0.3  4.0  5.0
        >>> doctest_print(cut_after(sample_frame, 0.1))
               b    a
        x
        0.1  0.0  1.0
        >>> doctest_print(cut_after(sample_frame, 0.14))
                b    a
        x
        0.10  0.0  1.0
        0.14  0.8  1.8
        >>> doctest_print(cut_after(sample_frame, 0.2))
               b    a
        x
        0.1  0.0  1.0
        0.2  2.0  3.0
        >>> doctest_print(cut_after(sample_frame, 0.31))
                b    a
        x
        0.10  0.0  1.0
        0.20  2.0  3.0
        0.30  4.0  5.0
        0.31  NaN  NaN
        >>> cut_after(sample_frame, 0.0)
        Empty DataFrame
        Columns: [b, a]
        Index: []

    """
    if isinstance(source_to_cut, Series):
        return _cut_series_after(
            series_to_cut=source_to_cut, cutting_index=cutting_index
        )
    elif isinstance(source_to_cut, DataFrame):
        return _cut_dataframe_after(
            frame_to_cut=source_to_cut, cutting_index=cutting_index
        )
    raise TypeError(
        "Wrong type for `source`. "
        "Either pandas.Series or pandas.DataFrame are supported. "
        "Got {} instead.".format(type(source_to_cut))
    )


def cut_before(
    source_to_cut: Union[Series, DataFrame], cutting_index: float
) -> Union[Series, DataFrame]:
    """
    Cuts a dataframe dropping the part after the cutting index. The cutting
    index will be added to the frame, which values are being interpolated, if inside.

    Args:
        source_to_cut(Union[Series, DataFrame]):
            Source frame to be cut at the cutting index.

        cutting_index(float):
            Cutting index at which the source frame should be cut.

    Returns:
        Union[Series, DataFrame]

    Examples:

        *Usage with pandas.Series*

        >>> import numpy
        >>> from pandas import Series, Index
        >>> from doctestprinter import doctest_print
        >>> from trashpanda import cut_after
        >>> sample_series = Series(
        ...     numpy.arange(3.0),
        ...     index=Index([0.1, 0.2, 0.3], name="x"),
        ...     name="y"
        ... )
        >>> sample_series
        x
        0.1    0.0
        0.2    1.0
        0.3    2.0
        Name: y, dtype: float64
        >>> cut_before(sample_series, 0.3)
        x
        0.3    2.0
        Name: y, dtype: float64
        >>> cut_before(sample_series, 0.14)
        x
        0.14    0.4
        0.20    1.0
        0.30    2.0
        Name: y, dtype: float64
        >>> cut_before(sample_series, 0.2)
        x
        0.2    1.0
        0.3    2.0
        Name: y, dtype: float64
        >>> cut_before(sample_series, 0.09)
        x
        0.09    NaN
        0.10    0.0
        0.20    1.0
        0.30    2.0
        Name: y, dtype: float64
        >>> cut_before(sample_series, 0.31)
        Series([], Name: y, dtype: float64)

        *Usage with a pandas.DataFrame*

        >>> import numpy
        >>> from pandas import DataFrame, Index
        >>> from doctestprinter import doctest_print
        >>> from trashpanda import cut_before
        >>> sample_frame = DataFrame(
        ...     numpy.arange(6.0).reshape(3, 2),
        ...     columns=["b", "a"],
        ...     index=Index([0.1, 0.2, 0.3], name="x")
        ... )
        >>> doctest_print(sample_frame)
               b    a
        x
        0.1  0.0  1.0
        0.2  2.0  3.0
        0.3  4.0  5.0
        >>> doctest_print(cut_before(sample_frame, 0.3))
               b    a
        x
        0.3  4.0  5.0
        >>> doctest_print(cut_before(sample_frame, 0.14))
                b    a
        x
        0.14  0.8  1.8
        0.20  2.0  3.0
        0.30  4.0  5.0
        >>> doctest_print(cut_before(sample_frame, 0.2))
               b    a
        x
        0.2  2.0  3.0
        0.3  4.0  5.0
        >>> doctest_print(cut_before(sample_frame, 0.09))
                b    a
        x
        0.09  NaN  NaN
        0.10  0.0  1.0
        0.20  2.0  3.0
        0.30  4.0  5.0
        >>> cut_before(sample_frame, 0.31)
        Empty DataFrame
        Columns: [b, a]
        Index: []

    """
    if isinstance(source_to_cut, Series):
        return _cut_series_before(
            series_to_cut=source_to_cut, cutting_index=cutting_index
        )
    elif isinstance(source_to_cut, DataFrame):
        return _cut_dataframe_before(
            frame_to_cut=source_to_cut, cutting_index=cutting_index
        )
    raise TypeError(
        "Wrong type for `source`. "
        "Either pandas.Series or pandas.DataFrame are supported. "
        "Got {} instead.".format(type(source_to_cut))
    )


@overload
def add_blank_rows(
    source: Series,
    indexes_to_add: Union[Iterable, pandas.Index],
    fill_value: Optional[Any] = None,
    override: bool = False,
) -> Series:
    pass


@overload
def add_blank_rows(
    source: DataFrame,
    indexes_to_add: Union[Iterable, pandas.Index],
    fill_value: Optional[Any] = None,
    override: bool = False,
) -> DataFrame:
    pass


def add_blank_rows(
    source: Union[Series, DataFrame],
    indexes_to_add: Union[Iterable, pandas.Index],
    fill_value: Optional[Any] = None,
    override: bool = False,
) -> Union[Series, DataFrame]:
    """
    Adds blank rows into a Series or DataFrame with `numpy.nan` by default. Double
    indexes are either overriden if argumend *override* is True or ignored.

    Args:
        source(Union[Series, DataFrame]):
            Series or DataFrame in which additional 'blank' rows should be filled.

        indexes_to_add(Union[Iterable, pandas.Index]):
            The targeted indexes, which are going to be added or overriden.

        fill_value(Optional[Any]):
            Default `numpy.nan`; value which is going to be used as the
            added rows values.

        override(bool):
            States if the *indexes to add* are overriding the source or ignored.

    Returns:
        Union[Series, DataFrame]

    Examples:

        *Usage with a pandas.Series*

        >>> from pandas import Series, Index
        >>> import numpy as np
        >>> from doctestprinter import doctest_print
        >>> from trashpanda import add_blank_rows
        >>> sample_series = Series(
        ...     np.arange(3.0), name="a", index=Index([0.1, 0.2, 0.3], name="x")
        ... )
        >>> prepared_frame = add_blank_rows(
        ...     source=sample_series, indexes_to_add=[0.15, 0.3, 0.35]
        ... )
        >>> doctest_print(prepared_frame)
        x
        0.10    0.0
        0.15    NaN
        0.20    1.0
        0.30    2.0
        0.35    NaN
        Name: a, dtype: float64
        >>> doctest_print(
        ...     prepared_frame.interpolate(method="index", limit_area="inside")
        ... )
        x
        0.10    0.0
        0.15    0.5
        0.20    1.0
        0.30    2.0
        0.35    NaN
        Name: a, dtype: float64
        >>> doctest_print(
        ...     add_blank_rows(
        ...         source=sample_series,
        ...         indexes_to_add=[0.15, 0.3, 0.35],
        ...         override=True
        ...     )
        ... )
        x
        0.10    0.0
        0.15    NaN
        0.20    1.0
        0.30    NaN
        0.35    NaN
        Name: a, dtype: float64
        >>> doctest_print(
        ...     add_blank_rows(
        ...         source=sample_series, indexes_to_add=[],
        ...     )
        ... )
        x
        0.1    0.0
        0.2    1.0
        0.3    2.0
        Name: a, dtype: float64

        *Usage with a pandas.DataFrame*

        >>> from pandas import DataFrame, Index
        >>> import numpy as np
        >>> from doctestprinter import doctest_print
        >>> from trashpanda import add_blank_rows
        >>> sample_series = DataFrame(
        ...     np.arange(6.0).reshape(3, 2),
        ...     columns=["b", "a"],
        ...     index=Index([0.1, 0.2, 0.3], name="x")
        ... )
        >>> prepared_frame = add_blank_rows(
        ...     source=sample_series, indexes_to_add=[0.15, 0.3, 0.35]
        ... )
        >>> doctest_print(prepared_frame)
                b    a
        x
        0.10  0.0  1.0
        0.15  NaN  NaN
        0.20  2.0  3.0
        0.30  4.0  5.0
        0.35  NaN  NaN
        >>> doctest_print(
        ...     prepared_frame.interpolate(method="index", limit_area="inside")
        ... )
                b    a
        x
        0.10  0.0  1.0
        0.15  1.0  2.0
        0.20  2.0  3.0
        0.30  4.0  5.0
        0.35  NaN  NaN
        >>> doctest_print(
        ...     add_blank_rows(
        ...         source=sample_series,
        ...         indexes_to_add=[0.15, 0.3, 0.35],
        ...         override=True
        ...     )
        ... )
                b    a
        x
        0.10  0.0  1.0
        0.15  NaN  NaN
        0.20  2.0  3.0
        0.30  NaN  NaN
        0.35  NaN  NaN
        >>> doctest_print(
        ...     add_blank_rows(
        ...         source=sample_series, indexes_to_add=[],
        ...     )
        ... )
               b    a
        x
        0.1  0.0  1.0
        0.2  2.0  3.0
        0.3  4.0  5.0

    """
    if isinstance(source, Series):
        return _add_blank_rows_to_series(
            source_series=source,
            indexes_to_add=indexes_to_add,
            fill_value=fill_value,
            override=override,
        )
    elif isinstance(source, DataFrame):
        return _add_blank_rows_to_dataframe(
            source_frame=source,
            indexes_to_add=indexes_to_add,
            fill_value=fill_value,
            override=override,
        )
    raise TypeError(
        "Wrong type for `source`. "
        "Either pandas.Series or pandas.DataFrame are supported. "
        "Got {} instead.".format(type(source))
    )


def _add_blank_rows_to_dataframe(
    source_frame: DataFrame,
    indexes_to_add: Union[Iterable, pandas.Index],
    fill_value: Optional[Any] = None,
    override: bool = False,
) -> DataFrame:
    """
    Adds blank rows into the DataFrame with `numpy.nan` by default. Double
    indexes are either overriden if argumend *override* is True or ignored.


    Args:
        source_frame(DataFrame):
            Frame in which additional 'blank' rows should be filled.

        indexes_to_add(Union[Iterable, pandas.Index]):
            The targeted indexes, which are going to be added or overriden.

        fill_value(Optional[Any]):
            Default `numpy.nan`; value which is going to be used as the
            added rows values.

        override(bool):
            States if the *indexes to add* are overriding the source or ignored.

    Returns:
        DataFrame

    Examples:
        >>> from pandas import DataFrame, Index
        >>> import numpy as np
        >>> from doctestprinter import doctest_print
        >>> # access to protected member for doctest
        >>> # noinspection PyProtectedMember
        >>> from trashpanda import _add_blank_rows_to_dataframe
        >>> sample_series = DataFrame(
        ...     np.arange(6.0).reshape(3, 2),
        ...     columns=["b", "a"],
        ...     index=Index([0.1, 0.2, 0.3], name="x")
        ... )
        >>> doctest_print(sample_series)
               b    a
        x
        0.1  0.0  1.0
        0.2  2.0  3.0
        0.3  4.0  5.0
        >>> prepared_frame = _add_blank_rows_to_dataframe(
        ...     source_frame=sample_series, indexes_to_add=[0.15, 0.3, 0.35]
        ... )
        >>> doctest_print(prepared_frame)
                b    a
        x
        0.10  0.0  1.0
        0.15  NaN  NaN
        0.20  2.0  3.0
        0.30  4.0  5.0
        0.35  NaN  NaN
        >>> doctest_print(
        ...     prepared_frame.interpolate(method="index", limit_area="inside")
        ... )
                b    a
        x
        0.10  0.0  1.0
        0.15  1.0  2.0
        0.20  2.0  3.0
        0.30  4.0  5.0
        0.35  NaN  NaN
        >>> doctest_print(
        ...     _add_blank_rows_to_dataframe(
        ...         source_frame=sample_series,
        ...         indexes_to_add=[0.15, 0.3, 0.35],
        ...         override=True
        ...     )
        ... )
                b    a
        x
        0.10  0.0  1.0
        0.15  NaN  NaN
        0.20  2.0  3.0
        0.30  NaN  NaN
        0.35  NaN  NaN
        >>> doctest_print(
        ...     _add_blank_rows_to_dataframe(
        ...         source_frame=sample_series, indexes_to_add=[],
        ...     )
        ... )
               b    a
        x
        0.1  0.0  1.0
        0.2  2.0  3.0
        0.3  4.0  5.0

    """
    if fill_value is None:
        fill_value = numpy.nan

    nothing_do_add_just_copy_source = len(indexes_to_add) == 0
    if nothing_do_add_just_copy_source:
        return source_frame.copy(deep=True)[source_frame.columns]

    column_count = len(source_frame.columns)
    index_count = len(indexes_to_add)

    double_indexes = source_frame.index.intersection(indexes_to_add)

    just_need_to_add = len(double_indexes) == 0
    if just_need_to_add:
        blank_lines = [[fill_value] * column_count] * index_count
        rows_to_add = DataFrame(
            blank_lines,
            index=indexes_to_add,
            columns=source_frame.columns.copy(),
        )
        requested_frame = pandas.concat((source_frame, rows_to_add), axis=0, sort=True)
        requested_frame.sort_index(inplace=True)
        requested_frame.index.name = source_frame.index.name
        return requested_frame[source_frame.columns]

    ignore_equal_adding_row_indexes_to_source = not override
    if ignore_equal_adding_row_indexes_to_source:
        actual_indexes_to_add = pandas.Index(indexes_to_add).drop(double_indexes)
        blank_lines = [[fill_value] * column_count] * len(actual_indexes_to_add)
        rows_to_add = DataFrame(
            blank_lines,
            index=actual_indexes_to_add,
            columns=source_frame.columns.copy(),
        )
        requested_frame = pandas.concat((source_frame, rows_to_add), axis=0, sort=True)
        requested_frame.sort_index(inplace=True)
        requested_frame.index.name = source_frame.index.name
        return requested_frame[source_frame.columns]

    blank_lines = [[fill_value] * column_count] * len(indexes_to_add)
    rows_to_add = DataFrame(
        blank_lines,
        index=indexes_to_add,
        columns=source_frame.columns.copy(),
    )
    different_indexes = source_frame.index.difference(double_indexes)
    requested_frame = pandas.concat(
        (source_frame.loc[different_indexes], rows_to_add), axis=0, sort=True
    )
    requested_frame.sort_index(inplace=True)
    requested_frame.index.name = source_frame.index.name
    return requested_frame[source_frame.columns]


def add_columns_to_dataframe(
    frame_to_enlarge: DataFrame,
    column_names: List[str],
    fill_value: Optional[Any] = None,
) -> DataFrame:
    """
    Adds columns to a dataframe. By default the columns are filled with
    pandas.NA values if no *fill_value* is explizitly given.

    Args:
        frame_to_enlarge(DataFrame):
            pandas.DataFrame which gets additional columns.

        column_names(List[str]):
            Names of additional columns to create.

        fill_value(Optional[Any]):
            Value which will fill the newly created columns. Default pandas.NA

    Returns:
        DataFrame

    Examples:
        >>> from pandas import DataFrame
        >>> import numpy
        >>> sample_series = DataFrame(numpy.arange(4).reshape((2,2)), columns=["b", "a"])
        >>> sample_series
           b  a
        0  0  1
        1  2  3
        >>> add_columns_to_dataframe(sample_series, ["d", "c"], "+")
           b  a  d  c
        0  0  1  +  +
        1  2  3  +  +
        >>> add_columns_to_dataframe(sample_series, ["d", "c"])
           b  a     d     c
        0  0  1  <NA>  <NA>
        1  2  3  <NA>  <NA>
    """
    if fill_value is None:
        fill_value = DEFAULT_NA

    for column_name_to_add in column_names:
        frame_to_enlarge[column_name_to_add] = fill_value
    return frame_to_enlarge


def _cut_dataframe_after(frame_to_cut: DataFrame, cutting_index: float) -> DataFrame:
    """
    Cuts a dataframe dropping the part after the cutting index. The cutting
    index will be added to the frame, which values are being interpolated, if inside.

    Args:
        frame_to_cut(DataFrame):
            Source frame to be cut at the cutting index.

        cutting_index(float):
            Cutting index at which the source frame should be cut.

    Returns:
        DataFrame

    Examples:
        >>> import numpy
        >>> from pandas import DataFrame, Index
        >>> from doctestprinter import doctest_print
        >>> sample_frame = DataFrame(
        ...     numpy.arange(6.0).reshape(3, 2),
        ...     columns=["b", "a"],
        ...     index=Index([0.1, 0.2, 0.3], name="x")
        ... )
        >>> doctest_print(sample_frame)
               b    a
        x
        0.1  0.0  1.0
        0.2  2.0  3.0
        0.3  4.0  5.0
        >>> doctest_print(_cut_dataframe_after(sample_frame, 0.1))
               b    a
        x
        0.1  0.0  1.0
        >>> doctest_print(_cut_dataframe_after(sample_frame, 0.14))
                b    a
        x
        0.10  0.0  1.0
        0.14  0.8  1.8
        >>> doctest_print(_cut_dataframe_after(sample_frame, 0.2))
               b    a
        x
        0.1  0.0  1.0
        0.2  2.0  3.0
        >>> doctest_print(_cut_dataframe_after(sample_frame, 0.31))
                b    a
        x
        0.10  0.0  1.0
        0.20  2.0  3.0
        0.30  4.0  5.0
        0.31  NaN  NaN
        >>> _cut_dataframe_after(sample_frame, 0.0)
        Empty DataFrame
        Columns: [b, a]
        Index: []

    """
    if cutting_index < frame_to_cut.index.min():
        return DataFrame(columns=frame_to_cut.columns.copy())
    if cutting_index == frame_to_cut.index[0]:
        cut_frame = frame_to_cut.iloc[:1]
        return cut_frame.copy(deep=True)
    if cutting_index in frame_to_cut.index:
        cut_frame = frame_to_cut.loc[frame_to_cut.index <= cutting_index]
        return cut_frame.copy(deep=True)
    prepared_frame = _add_blank_rows_to_dataframe(
        source_frame=frame_to_cut, indexes_to_add=[cutting_index]
    )
    interpolated_frame = prepared_frame.interpolate(
        method="index", axis=0, limit_area="inside"
    )
    cut_frame = interpolated_frame.loc[interpolated_frame.index <= cutting_index]
    return cut_frame.copy(deep=True)


def cut_dataframe_after_max(
    frame_to_cut: DataFrame, condition_column: Optional[Union[str, int]] = None
) -> DataFrame:
    """
    Cuts a DataFrame after the maximum value of its *condition column*. If the
    DataFrame contains only 1 column, then this column is the *condition column*.

    .. warning::
        This method is being replaced by `:func:trashpanda.cut_after_max` in
        the next release.

    Args:
        frame_to_cut(DataFrame):
            Source frame to be cut at the cutting index.

        condition_column(Union[str, int]):
            Column or its integer position, which contains the conditional
            maximum value.

    Returns:
        DataFrame

    Examples:
        >>> from pandas import DataFrame, Index
        >>> import numpy as np
        >>> from doctestprinter import doctest_print
        >>> v1, v2 = np.arange(0.0, np.pi, np.pi/4.0), np.arange(4)
        >>> test_data = np.stack((np.sin(v1), v2), axis=1)
        >>> test_frame = DataFrame(
        ...     data=test_data,
        ...     columns=["b", "a"],
        ...     index=Index(numpy.arange(0.0, 0.4, 0.1), name="x")
        ... )
        >>> doctest_print(test_frame)
                    b    a
        x
        0.0  0.000000  0.0
        0.1  0.707107  1.0
        0.2  1.000000  2.0
        0.3  0.707107  3.0
        >>> doctest_print(cut_dataframe_after_max(test_frame, "b"))
                    b    a
        x
        0.0  0.000000  0.0
        0.1  0.707107  1.0
        0.2  1.000000  2.0
        >>> doctest_print(cut_dataframe_after_max(test_frame, 0))
                    b    a
        x
        0.0  0.000000  0.0
        0.1  0.707107  1.0
        0.2  1.000000  2.0
    """
    # warnings.warn(
    #     "`cut_dataframe_after_max` is being replaced "
    #     "by `cut_after_max` in the next release."
    # )

    target_column_is_not_clear = (
        condition_column is None and len(frame_to_cut.columns) > 1
    )
    if target_column_is_not_clear:
        raise ValueError(
            "Only a 1-column DataFrame can be cut without defining a condition_column."
        )

    condition_column = condition_column
    if condition_column is None:
        condition_column = frame_to_cut.columns[0]
    column_at_position_is_requested = (
        isinstance(condition_column, int)
        and condition_column not in frame_to_cut.columns
    )
    if column_at_position_is_requested:
        condition_column = frame_to_cut.columns[condition_column]

    cutting_index = frame_to_cut[condition_column].idxmax()
    return _cut_dataframe_after(frame_to_cut=frame_to_cut, cutting_index=cutting_index)


def _cut_dataframe_before(frame_to_cut: DataFrame, cutting_index: float) -> DataFrame:
    """
    Cuts a dataframe dropping the part before the cutting index. The cutting
    index will be added to the frame, which values are being interpolated, if inside.

    Args:
        frame_to_cut(DataFrame):
            Source frame to be cut at the cutting index.

        cutting_index(float):
            Cutting index at which the source frame should be cut.

    Returns:
        DataFrame

    Examples:
        >>> import numpy
        >>> from pandas import DataFrame, Index
        >>> from doctestprinter import doctest_print
        >>> sample_frame = DataFrame(
        ...     numpy.arange(6.0).reshape(3, 2),
        ...     columns=["b", "a"],
        ...     index=Index([0.1, 0.2, 0.3], name="x")
        ... )
        >>> doctest_print(sample_frame)
               b    a
        x
        0.1  0.0  1.0
        0.2  2.0  3.0
        0.3  4.0  5.0
        >>> doctest_print(_cut_dataframe_before(sample_frame, 0.3))
               b    a
        x
        0.3  4.0  5.0
        >>> doctest_print(_cut_dataframe_before(sample_frame, 0.14))
                b    a
        x
        0.14  0.8  1.8
        0.20  2.0  3.0
        0.30  4.0  5.0
        >>> doctest_print(_cut_dataframe_before(sample_frame, 0.2))
               b    a
        x
        0.2  2.0  3.0
        0.3  4.0  5.0
        >>> doctest_print(_cut_dataframe_before(sample_frame, 0.09))
                b    a
        x
        0.09  NaN  NaN
        0.10  0.0  1.0
        0.20  2.0  3.0
        0.30  4.0  5.0
        >>> _cut_dataframe_before(sample_frame, 0.31)
        Empty DataFrame
        Columns: [b, a]
        Index: []

    """
    old_column_order = frame_to_cut.columns.copy(deep=True)
    if cutting_index > frame_to_cut.index.max():
        return DataFrame(columns=old_column_order)
    if cutting_index == frame_to_cut.index[-1]:
        cut_frame = frame_to_cut.iloc[-1:]
        return cut_frame.copy(deep=True)[old_column_order]
    if cutting_index in frame_to_cut.index:
        cut_frame = frame_to_cut.loc[cutting_index <= frame_to_cut.index]
        return cut_frame.copy(deep=True)[old_column_order]
    prepared_frame = _add_blank_rows_to_dataframe(
        source_frame=frame_to_cut, indexes_to_add=[cutting_index]
    )
    interpolated_frame = prepared_frame.interpolate(
        method="index", axis=0, limit_area="inside"
    )
    cut_frame = interpolated_frame.loc[cutting_index <= interpolated_frame.index]
    return cut_frame.copy(deep=True)[old_column_order]


def override_left_with_right_dataframe(
    left_target: DataFrame, overriding_right: DataFrame
) -> DataFrame:
    """
    Overrides overlapping items of left with right.

    Args:
        left_target(DataFrame):
            Dataframe which should be overridden.

        overriding_right(DataFrame):
            The new values as frame, which overrides the *left target*.

    Returns:
        DataFrame

    Examples:
        >>> from pandas import DataFrame
        >>> import numpy as np
        >>> left = DataFrame(np.full(3, 1), index=list(iter("abc")), columns=["v"])
        >>> left
           v
        a  1
        b  1
        c  1
        >>> right = DataFrame(np.full(2, 2), index=list(iter("ad")), columns=["v"])
        >>> right
           v
        a  2
        d  2
        >>> override_left_with_right_dataframe(left, right)
           v
        a  2
        b  1
        c  1
        d  2
        >>> double_data = [list(range(1, 3)) for i in range(3)]
        >>> left = DataFrame(double_data, index=list(iter("abc")), columns=["m", "x"])
        >>> left
           m  x
        a  1  2
        b  1  2
        c  1  2
        >>> double_data = [list(range(3, 5)) for i in range(2)]
        >>> right = DataFrame(double_data, index=list(iter("ad")), columns=["x", "m"])
        >>> right
           x  m
        a  3  4
        d  3  4
        >>> override_left_with_right_dataframe(left, right)
           m  x
        a  4  3
        b  1  2
        c  1  2
        d  4  3
        >>> right = DataFrame(double_data, index=list(iter("ad")), columns=["z", "m"])
        >>> right
           z  m
        a  3  4
        d  3  4
        >>> override_left_with_right_dataframe(left, right)
           m    x     z
        a  4  2.0     3
        b  1  2.0  <NA>
        c  1  2.0  <NA>
        d  4  NaN     3

    """
    old_frame = left_target.copy()
    columns_to_add = overriding_right.columns.difference(left_target.columns)
    if not columns_to_add.empty:
        for column_name in columns_to_add:
            old_frame[column_name] = pandas.NA
    targeted_columns = overriding_right.columns
    same_indexes = overriding_right.index.intersection(old_frame.index)
    new_indexes = overriding_right.index.difference(old_frame.index)
    old_frame.loc[same_indexes, targeted_columns] = overriding_right.loc[same_indexes]
    new_rows = overriding_right.loc[new_indexes]
    overridden_frame = pandas.concat([old_frame, new_rows], sort=True)
    return overridden_frame


@overload
def get_unique_index_positions(
    source_with_duplicates: Series, keep: Union[str, bool] = "first"
) -> pandas.Index:
    pass


@overload
def get_unique_index_positions(
    source_with_duplicates: DataFrame, keep: Union[str, bool] = "first"
) -> pandas.Index:
    pass


def get_unique_index_positions(
    source_with_duplicates: Union[Series, DataFrame], keep: Union[str, bool] = "first"
) -> pandas.Index:
    """
    Determines positions of unique indexes from a Series or DataFrame.

    Notes:
        This method assumes duplicates are within the *frame with duplicates*.
        Check with *index.is_unique* beforehand.

    Args:
        source_with_duplicates(Union[Series, DataFrame]):
            Series or DataFrame with duplicated indexes.

        keep(Union[str, bool]):
            Determines which duplicates to keep.
            - *first*: Default; keeps all first occurrences of duplicated indexes.
            - *last*: Keeps all last occurrences of duplicated indexes.
            - False: Drops all duplicated indexes.

    Returns:
        pandas.Index

    Examples:
        >>> from pandas import DataFrame
        >>> import numpy as np
        >>> from doctestprinter import doctest_print
        >>> sample_frame = pandas.DataFrame(
        ...     np.arange(5),
        ...     columns=["iloc"],
        ...     index=pandas.Index(['a', 'a', 'b', 'b', 'c'], name="index")
        ... )
        >>> doctest_print(sample_frame)
               iloc
        index
        a         0
        a         1
        b         2
        b         3
        c         4

        Keeping the first occurrence.

        >>> get_unique_index_positions(sample_frame, "first")
        Int64Index([0, 2, 4], dtype='int64')

        Keeping the last occurrence.

        >>> get_unique_index_positions(sample_frame, "last")
        Int64Index([1, 3, 4], dtype='int64')

        Dropping all duplicates.

        >>> get_unique_index_positions(sample_frame, False)
        Int64Index([4], dtype='int64')

    .. doctest::
       :hide:

        >>> from pandas import Series
        >>> import numpy as np
        >>> sample_series = pandas.Series(
        ...     np.arange(5),
        ...     name="location",
        ...     index=pandas.Index(['a', 'a', 'b', 'b', 'c'], name="index")
        ... )
        >>> doctest_print(sample_series)
        index
        a    0
        a    1
        b    2
        b    3
        c    4
        Name: location, dtype: int64
        >>> get_unique_index_positions(sample_series, "first")
        Int64Index([0, 2, 4], dtype='int64')
        >>> get_unique_index_positions(sample_series, "last")
        Int64Index([1, 3, 4], dtype='int64')
        >>> get_unique_index_positions(sample_series, False)
        Int64Index([4], dtype='int64')

    .. doctest::
       :hide:

        >>> empty_series = Series([], index=[], dtype=float)
        >>> get_unique_index_positions(empty_series, "first")
        Int64Index([], dtype='int64')
        >>> get_unique_index_positions(empty_series, "last")
        Int64Index([], dtype='int64')
        >>> get_unique_index_positions(empty_series, False)
        Int64Index([], dtype='int64')

    """
    all_indexes = source_with_duplicates.index.to_series()
    all_indexes.index = numpy.arange(len(all_indexes))
    unique_indexes = all_indexes.drop_duplicates(keep=keep)
    return unique_indexes.index


@overload
def remove_duplicated_indexes(
    source_with_duplicates: Series, keep: Union[str, bool] = "first"
) -> Series:
    pass


@overload
def remove_duplicated_indexes(
    source_with_duplicates: DataFrame, keep: Union[str, bool] = "first"
) -> DataFrame:
    pass


def remove_duplicated_indexes(
    source_with_duplicates: Union[DataFrame, Series], keep: Union[str, bool] = "first"
) -> DataFrame:
    """
    Removes rows of duplicated indexes from a DataFrame.
    Keeps by default all first occurrences.

    Notes:
        This method assumes duplicates are within the *frame with duplicates*.
        Check with *index.is_unique* beforehand.

    Args:
        source_with_duplicates(Union[DataFrame, Series]):
            Removes existing duplicates

        keep(Union[str, bool]):
            Determines which duplicates to keep.
            - *first*: Default; keeps all first occurrences of duplicated indexes.
            - *last*: Keeps all last occurrences of duplicated indexes.
            - False: Drops all duplicated indexes.

    Returns:
        Union[DataFrame, Series]

    Examples:

        >>> from pandas import DataFrame
        >>> import numpy as np
        >>> from doctestprinter import doctest_print
        >>> sample_frame = pandas.DataFrame(
        ...     np.arange(5),
        ...     columns=["location"],
        ...     index=pandas.Index(['a', 'a', 'b', 'b', 'c'], name="index")
        ... )
        >>> doctest_print(sample_frame)
               location
        index
        a             0
        a             1
        b             2
        b             3
        c             4

        Keeping the first occurrence.

        >>> first_kept = remove_duplicated_indexes(
        ...     source_with_duplicates=sample_frame, keep="first"
        ... )
        >>> doctest_print(first_kept)
               location
        index
        a             0
        b             2
        c             4

        Keeping the last occurrence.

        >>> last_kept = remove_duplicated_indexes(
        ...     source_with_duplicates=sample_frame, keep="last"
        ... )
        >>> doctest_print(last_kept)
               location
        index
        a             1
        b             3
        c             4

        Dropping all duplicates.

        >>> dropped_duplicates = remove_duplicated_indexes(
        ...     source_with_duplicates=sample_frame, keep=False
        ... )
        >>> doctest_print(dropped_duplicates)
               location
        index
        c             4

    .. doctest::
       :hide:

        >>> from pandas import Series
        >>> import numpy as np
        >>> from doctestprinter import doctest_print
        >>> sample_frame = pandas.Series(
        ...     np.arange(5),
        ...     name="iloc",
        ...     index=pandas.Index(['a', 'a', 'b', 'b', 'c'], name="index")
        ... )
        >>> doctest_print(sample_frame)
        index
        a    0
        a    1
        b    2
        b    3
        c    4
        Name: iloc, dtype: int64
        >>> first_kept = remove_duplicated_indexes(
        ...     source_with_duplicates=sample_frame, keep="first"
        ... )
        >>> doctest_print(first_kept)
        index
        a    0
        b    2
        c    4
        Name: iloc, dtype: int64
        >>> last_kept = remove_duplicated_indexes(
        ...     source_with_duplicates=sample_frame, keep="last"
        ... )
        >>> doctest_print(last_kept)
        index
        a    1
        b    3
        c    4
        Name: iloc, dtype: int64
        >>> dropped_duplicates = remove_duplicated_indexes(
        ...     source_with_duplicates=sample_frame, keep=False
        ... )
        >>> doctest_print(dropped_duplicates)
        index
        c    4
        Name: iloc, dtype: int64

    """
    unique_positions = get_unique_index_positions(
        source_with_duplicates=source_with_duplicates, keep=keep
    )
    frame_without_duplicates = source_with_duplicates.iloc[unique_positions]
    return frame_without_duplicates.copy()


def _remove_duplicates_or_raise_error(
    source_frame: Union[DataFrame, Series], keep: Union[str, bool] = "raise"
) -> DataFrame:
    """
    Removes duplicated indexes but warns the user about it.

    Notes:
        This method is written this way to enforce a descission of the user.

    Args:
        source_frame(DataFrame):
            Source with potential duplicated indexes.

        keep(Union[str, bool]):
            Determines if duplicates are to be kept.
            - *raise*: Default; raises ValueError because following code doesn't
              work with duplicates.
            - *first*: Default; keeps all first occurrences of duplicated indexes.
            - *last*: Keeps all last occurrences of duplicated indexes.
            - False: Drops all duplicated indexes.

    Returns:
        DataFrame

    .. doctest::
       :hide:

        >>> from pandas import Series
        >>> sample_series = Series([0, 1, 2], index=["a", "a", "b"])
        >>> _remove_duplicates_or_raise_error(sample_series)
        Traceback (most recent call last):
        ..
        ValueError: The given DataFrame has duplicated indexes, which will lead to a malfunction.
            Either preprocess the DataFrame beforehand or set *keep* to
            'first': keeping the first occurrence,
            'last': (keeping the last occurrence)
            'False' (dropping all duplicates).
        >>> _remove_duplicates_or_raise_error(sample_series, keep='first')
        a    0
        b    2
        dtype: int64
        >>> _remove_duplicates_or_raise_error(sample_series, keep='last')
        a    1
        b    2
        dtype: int64
        >>> _remove_duplicates_or_raise_error(sample_series, keep=False)
        b    2
        dtype: int64
    """
    has_duplicates = not source_frame.index.is_unique
    has_duplicates_but_should_not_remove_them = keep == "raise" and has_duplicates
    if has_duplicates_but_should_not_remove_them:
        raise ValueError(
            "The given DataFrame has duplicated indexes, which will lead to a "
            "malfunction.\n    Either preprocess the DataFrame beforehand or set "
            "*keep* to\n"
            "    'first': keeping the first occurrence,\n"
            "    'last': (keeping the last occurrence)\n"
            "    'False' (dropping all duplicates)."
        )
    elif has_duplicates:
        source_without_dup = remove_duplicated_indexes(source_frame, keep=keep)
    else:
        source_without_dup = source_frame
    return source_without_dup


def _ensure_dataframe(source: Union[DataFrame, Series]) -> DataFrame:
    """
    Ensures a DataFrame, converting a Series to such.

    Args:
        source(Union[DataFrame, Series]):
            A DataFrame being untouched and a Series being converted to a DataFrame.

    Returns:
        DataFrame
    """
    if isinstance(source, Series):
        return source.to_frame()
    return source


def meld_along_columns(
    left: Union[Series, DataFrame],
    right: Union[Series, DataFrame],
    copy_at_meld: bool = True,
    keep: Union[str, bool] = "raise",
) -> DataFrame:
    """
    Melds two DataFrames of Series into a single DataFrame with a common index.

    Notes:
        This method is called meld because it doesn't fit into existing categories
        of pandas join, merge or concat.

    Warnings:
        This method will override values of equal named columns in *left* with *right*.

    Args:
        left(DataFrame):
            Left curve to be merged with the right one.

        right(DataFrame):
            Right curve, which will merge to the left one.

        copy_at_meld(bool):
            Makes a copy during the concat process, creating a new DataFrame
            instead of overriding the source.

        keep(Union[str, bool]):
            Determines which duplicates to keep.
            - *first*: Default; keeps all first occurrences of duplicated indexes.
            - *last*: Keeps all last occurrences of duplicated indexes.
            - False: Drops all duplicated indexes.

    Returns:
        DataFrame

    Examples:

        Melding of two DataFrame.

        >>> from pathlib import Path
        >>> from pandas import DataFrame, Series
        >>> import numpy as np
        >>> import examplecurves
        >>> left_curve, right_curve = examplecurves.Static.create(
        ...     family_name="nonlinear0", cut_curves_at=3, curve_selection=[1, 2]
        ... )
        >>> left_curve.columns = ["left"]
        >>> right_curve.columns = ["right"]
        >>> from doctestprinter import doctest_print
        >>> doctest_print(meld_along_columns(left_curve, right_curve))
                 left     right
        x
        0.000  0.0000  0.000000
        0.100  1.5625       NaN
        0.111     NaN  1.607654
        0.200  3.0000       NaN
        0.222     NaN  3.085479

        Melding of 2 Series.

        >>> left_series = left_curve["left"]
        >>> right_series = right_curve["right"]
        >>> doctest_print(meld_along_columns(left_curve, right_curve))
                 left     right
        x
        0.000  0.0000  0.000000
        0.100  1.5625       NaN
        0.111     NaN  1.607654
        0.200  3.0000       NaN
        0.222     NaN  3.085479

        Example of melding two DataFrames with duplicated indexes and one duplicated
        column. Left values of the intersecting columns are being overriden with the
        right values.

        >>> left_sample = pandas.DataFrame(
        ...     np.arange(10).reshape(5, 2),
        ...     columns=["b", "a"],
        ...     index=pandas.Index(np.linspace(0.1, 0.5, num=5), name="x")
        ... )
        >>> doctest_print(left_sample)
             b  a
        x
        0.1  0  1
        0.2  2  3
        0.3  4  5
        0.4  6  7
        0.5  8  9
        >>> right_sample = pandas.DataFrame(
        ...     np.linspace(0.5, 9.5, num=10).reshape(5, 2),
        ...     columns=["a", "c"],
        ...     index=pandas.Index([0.1, 0.1, 0.15, 0.15, 0.2], name="x")
        ... )
        >>> doctest_print(right_sample)
                a    c
        x
        0.10  0.5  1.5
        0.10  2.5  3.5
        0.15  4.5  5.5
        0.15  6.5  7.5
        0.20  8.5  9.5
        >>> merged_frame = meld_along_columns(left_sample, right_sample, keep='first')
        >>> doctest_print(merged_frame)
                b    a    c
        x
        0.10  0.0  0.5  1.5
        0.15  NaN  4.5  5.5
        0.20  2.0  8.5  9.5
        0.30  4.0  5.0  NaN
        0.40  6.0  7.0  NaN
        0.50  8.0  9.0  NaN

    """
    left_frame = _ensure_dataframe(left)
    right_frame = _ensure_dataframe(right)
    left_without_dup = _remove_duplicates_or_raise_error(left_frame, keep=keep)
    right_without_dup = _remove_duplicates_or_raise_error(right_frame, keep=keep)

    left_index = left_without_dup.index
    right_index = right_without_dup.index
    equal_indexes = right_index.intersection(left_index).unique()
    different_indexes = right_index.difference(left_index).unique()
    combined = pandas.concat(
        [left_without_dup, right_without_dup.loc[different_indexes]],
        copy=copy_at_meld,
    )
    overriding_values = right_without_dup.loc[equal_indexes]
    combined.loc[equal_indexes, right_without_dup.columns] = overriding_values
    return combined.sort_index()


def _add_blank_rows_to_series(
    source_series: Series,
    indexes_to_add: Union[Iterable, pandas.Index],
    fill_value: Optional[Any] = None,
    override: bool = False,
) -> Series:
    """
    Adds blank rows into the Series with `numpy.nan` by default. Double
    indexes are either overriden if argumend *override* is True or ignored.


    Args:
        source_series(Series):
            Series in which additional 'blank' rows should be filled.

        indexes_to_add(Union[Iterable, pandas.Index]):
            The targeted indexes, which are going to be added or overriden.

        fill_value(Optional[Any]):
            Default `numpy.nan`; value which is going to be used as the
            added rows values.

        override(bool):
            States if the *indexes to add* are overriding the source or ignored.

    Returns:
        Series

    Examples:
        >>> from pandas import DataFrame, Index
        >>> import numpy as np
        >>> from doctestprinter import doctest_print
        >>> # access to protected member for doctest
        >>> # noinspection PyProtectedMember
        >>> from trashpanda import _add_blank_rows_to_dataframe
        >>> sample_series = Series(
        ...     np.arange(3.0), name="a", index=Index([0.1, 0.2, 0.3], name="x")
        ... )
        >>> prepared_frame = _add_blank_rows_to_series(
        ...     source_series=sample_series, indexes_to_add=[0.15, 0.3, 0.35]
        ... )
        >>> doctest_print(prepared_frame)
        x
        0.10    0.0
        0.15    NaN
        0.20    1.0
        0.30    2.0
        0.35    NaN
        Name: a, dtype: float64
        >>> doctest_print(
        ...     prepared_frame.interpolate(method="index", limit_area="inside")
        ... )
        x
        0.10    0.0
        0.15    0.5
        0.20    1.0
        0.30    2.0
        0.35    NaN
        Name: a, dtype: float64
        >>> doctest_print(
        ...     _add_blank_rows_to_series(
        ...         source_series=sample_series,
        ...         indexes_to_add=[0.15, 0.3, 0.35],
        ...         override=True
        ...     )
        ... )
        x
        0.10    0.0
        0.15    NaN
        0.20    1.0
        0.30    NaN
        0.35    NaN
        Name: a, dtype: float64
        >>> doctest_print(
        ...     _add_blank_rows_to_series(
        ...         source_series=sample_series, indexes_to_add=[],
        ...     )
        ... )
        x
        0.1    0.0
        0.2    1.0
        0.3    2.0
        Name: a, dtype: float64

    """
    if fill_value is None:
        fill_value = numpy.nan

    nothing_do_add_just_copy_source = len(indexes_to_add) == 0
    if nothing_do_add_just_copy_source:
        return source_series.copy()

    index_count = len(indexes_to_add)

    double_indexes = source_series.index.intersection(indexes_to_add)

    just_need_to_add = len(double_indexes) == 0
    if just_need_to_add:
        blank_lines = [fill_value] * index_count
        rows_to_add = Series(
            blank_lines,
            index=indexes_to_add,
            name=source_series.name,
        )
        requested_series = pandas.concat(
            (source_series, rows_to_add), axis=0, sort=True
        )
        requested_series.sort_index(inplace=True)
        requested_series.index.name = source_series.index.name
        return requested_series

    ignore_equal_adding_row_indexes_to_source = not override
    if ignore_equal_adding_row_indexes_to_source:
        actual_indexes_to_add = pandas.Index(indexes_to_add).drop(double_indexes)
        blank_lines = [fill_value] * len(actual_indexes_to_add)
        rows_to_add = Series(
            blank_lines,
            index=actual_indexes_to_add,
            name=source_series.name,
        )
        requested_series = pandas.concat(
            (source_series, rows_to_add), axis=0, sort=True
        )
        requested_series.sort_index(inplace=True)
        requested_series.index.name = source_series.index.name
        return requested_series

    blank_lines = [fill_value] * len(indexes_to_add)
    rows_to_add = Series(
        blank_lines,
        index=indexes_to_add,
        name=source_series.name,
    )
    different_indexes = source_series.index.difference(double_indexes)
    requested_series = pandas.concat(
        (source_series.loc[different_indexes], rows_to_add), axis=0, sort=True
    )
    requested_series.sort_index(inplace=True)
    requested_series.index.name = source_series.index.name
    return requested_series


def add_missing_indexes_to_series(
    target_series: Series, new_indexes: pandas.Index, fill_value: Optional[Any] = None
) -> Series:
    """
    Adds different (missing) indexes to series.

    Args:
        target_series(Series):
            Series in which missing indexes should be added.

        new_indexes(pandas.Index):
            Indexes, which should be in the *target series*.

        fill_value(Optional[Any]):
            An optional fill value for the freshly added items.

    Returns:
        Series

    Examples:
        >>> from pandas import Series, Index, Int16Dtype
        >>> import numpy as np
        >>> target = Series(
        ...     np.full(3, 1), index=list(iter("abc")), name="foo", dtype=Int16Dtype()
        ... )
        >>> target
        a    1
        b    1
        c    1
        Name: foo, dtype: Int16
        >>> new_indexes_to_add = Index(list(iter("ad")))
        >>> add_missing_indexes_to_series(target, new_indexes_to_add)
        a       1
        b       1
        c       1
        d    <NA>
        Name: foo, dtype: object
        >>> add_missing_indexes_to_series(target, new_indexes_to_add, "X")
        a    1
        b    1
        c    1
        d    X
        Name: foo, dtype: object

    """
    if fill_value is None:
        fill_value = DEFAULT_NA

    old_series = target_series.copy()
    try:
        missing_indexes = new_indexes.difference(old_series.index)
    except AttributeError:
        raise TypeError("new_indexes must be of pandas.Index type.")
    new_rows = Series([fill_value] * len(missing_indexes), index=missing_indexes)
    overridden_series = pandas.concat([old_series, new_rows], sort=True)
    overridden_series.name = old_series.name
    return overridden_series


def _cut_series_after(
    series_to_cut: Series, cutting_index: Union[float, pandas.Index]
) -> Series:
    """
    Cuts a pandas.Series dropping the part after the cutting index. The cutting
    index will be added to the frame, which values are being interpolated, if inside.

    Args:
        series_to_cut(Series):
            Source Series to be cut at the cutting index.

        cutting_index(Union[float, pandas.Index]):
            Cutting index at which the source frame should be cut.

    Returns:
        Series

    Examples:
        >>> import numpy
        >>> from pandas import Series, Index
        >>> sample_series = Series(
        ...     numpy.arange(3.0),
        ...     index=Index([0.1, 0.2, 0.3], name="x"),
        ...     name="y"
        ... )
        >>> sample_series
        x
        0.1    0.0
        0.2    1.0
        0.3    2.0
        Name: y, dtype: float64
        >>> _cut_series_after(sample_series, 0.1)
        x
        0.1    0.0
        Name: y, dtype: float64
        >>> _cut_series_after(sample_series, 0.14)
        x
        0.10    0.0
        0.14    0.4
        Name: y, dtype: float64
        >>> _cut_series_after(sample_series, 0.2)
        x
        0.1    0.0
        0.2    1.0
        Name: y, dtype: float64
        >>> _cut_series_after(sample_series, 0.31)
        x
        0.10    0.0
        0.20    1.0
        0.30    2.0
        0.31    NaN
        Name: y, dtype: float64
        >>> _cut_series_after(sample_series, 0.0)
        Series([], Name: y, dtype: float64)

    """
    if cutting_index < series_to_cut.index.min():
        return Series(
            name=series_to_cut.name,
            index=pandas.Index([], name=series_to_cut.index.name),
            dtype=float,
        )
    if cutting_index == series_to_cut.index[0]:
        return series_to_cut.iloc[:1].copy()
    if cutting_index in series_to_cut.index:
        return series_to_cut.loc[series_to_cut.index <= cutting_index].copy()
    prepared_frame = _add_blank_rows_to_series(
        source_series=series_to_cut, indexes_to_add=[cutting_index]
    )
    interpolated_frame = prepared_frame.interpolate(
        method="index", axis=0, limit_area="inside"
    )
    return interpolated_frame.loc[interpolated_frame.index <= cutting_index].copy()


def cut_series_after_max(series_to_cut: Series) -> Series:
    """
    Cuts a Series after its maximum value.

    .. warning::
        This method is being replaced by `:func:trashpanda.cut_after_max` in
        the next release.

    Args:
        series_to_cut(Series):
            Source frame to be cut at the cutting index.

    Returns:
        Series

    Examples:
        >>> from pandas import Series, Index
        >>> import numpy as np
        >>> from doctestprinter import doctest_print
        >>> from trashpanda import cut_series_after_max
        >>> sample_data = np.sin(np.arange(0.0, np.pi, np.pi/4.0))
        >>> sample_series = Series(
        ...     data=sample_data,
        ...     name="a",
        ...     index=Index(numpy.arange(0.0, 0.4, 0.1), name="x")
        ... )
        >>> doctest_print(sample_series)
        x
        0.0    0.000000
        0.1    0.707107
        0.2    1.000000
        0.3    0.707107
        Name: a, dtype: float64
        >>> cut_sample = cut_series_after_max(sample_series)
        >>> doctest_print(cut_sample)
        x
        0.0    0.000000
        0.1    0.707107
        0.2    1.000000
        Name: a, dtype: float64
        >>> doctest_print(cut_series_after_max(cut_sample))
        x
        0.0    0.000000
        0.1    0.707107
        0.2    1.000000
        Name: a, dtype: float64
    """
    # warnings.warn(
    #     "`cut_series_after_max` is being replaced by `cut_after_max` in the next release.",
    #     DeprecationWarning,
    # )
    cutting_index = series_to_cut.idxmax()
    return _cut_series_after(series_to_cut=series_to_cut, cutting_index=cutting_index)


def _cut_series_before(
    series_to_cut: Series, cutting_index: Union[float, pandas.Index]
) -> Series:
    """
    Cuts a pandas.Series dropping the part before the cutting index. The cutting
    index will be added to the frame, which values are being interpolated, if inside.

    Args:
        series_to_cut(Series):
            Source Series to be cut at the cutting index.

        cutting_index(Union[float, pandas.Index]):
            Cutting index at which the source frame should be cut.

    Returns:
        Series

    Examples:
        >>> import numpy
        >>> from pandas import Series, Index
        >>> sample_series = Series(
        ...     numpy.arange(3.0),
        ...     index=Index([0.1, 0.2, 0.3], name="x"),
        ...     name="y"
        ... )
        >>> sample_series
        x
        0.1    0.0
        0.2    1.0
        0.3    2.0
        Name: y, dtype: float64
        >>> _cut_series_before(sample_series, 0.3)
        x
        0.3    2.0
        Name: y, dtype: float64
        >>> _cut_series_before(sample_series, 0.14)
        x
        0.14    0.4
        0.20    1.0
        0.30    2.0
        Name: y, dtype: float64
        >>> _cut_series_before(sample_series, 0.2)
        x
        0.2    1.0
        0.3    2.0
        Name: y, dtype: float64
        >>> _cut_series_before(sample_series, 0.09)
        x
        0.09    NaN
        0.10    0.0
        0.20    1.0
        0.30    2.0
        Name: y, dtype: float64
        >>> _cut_series_before(sample_series, 0.31)
        Series([], Name: y, dtype: float64)

    """
    if cutting_index > series_to_cut.index.max():
        return Series(
            name=series_to_cut.name,
            index=pandas.Index([], name=series_to_cut.index.name),
            dtype=float,
        )
    if cutting_index == series_to_cut.index[-1]:
        return series_to_cut.iloc[-1:].copy()
    if cutting_index in series_to_cut.index:
        return series_to_cut.loc[cutting_index <= series_to_cut.index].copy()
    prepared_frame = _add_blank_rows_to_series(
        source_series=series_to_cut, indexes_to_add=[cutting_index]
    )
    interpolated_frame = prepared_frame.interpolate(
        method="index", axis=0, limit_area="inside"
    )
    return interpolated_frame.loc[cutting_index <= interpolated_frame.index].copy()


def find_index_of_value_in_series(source_series: Series, search_value: float) -> float:
    """
    Finds the index of an value within a Series. Only float values as
    *search value* are supported.

    Notes:
        This method returns the first nearest hit towards the *search value*
        within the *source series*. This method doesn't detext multiple
        entries within the *source series*.

    Args:
        source_series(Series):
            Source series in which the nearest index for the *search value*
            should be found.

        search_value(float):
            The *search value* for which the nearest value's index should
            be returned.

    Returns:
        float

    Examples:
        >>> from pandas import Series, Index
        >>> import numpy as np
        >>> sample_series = Series(
        ...     data=[1.0, 2.0, 2.0, 3.0, 4.0],
        ...     index=Index([0.1, 0.2, 0.3, 0.4, 0.5])
        ... )
        >>> sample_series
        0.1    1.0
        0.2    2.0
        0.3    2.0
        0.4    3.0
        0.5    4.0
        dtype: float64

        In general the first nearest hit toward the search value ist returned.

        >>> find_index_of_value_in_series(sample_series, -1.0)
        0.1
        >>> find_index_of_value_in_series(sample_series, 5.0)
        0.5


        Search values within the range returns the first occurance.
        In this case 0.3 will never be returned.

        >>> find_index_of_value_in_series(sample_series, 2.49)
        0.2
        >>> find_index_of_value_in_series(sample_series, 2.5)
        0.2
        >>> find_index_of_value_in_series(sample_series, 2.51)
        0.4
        >>> find_index_of_value_in_series(sample_series, 3.0)
        0.4

    """
    deltas_towards_search_value = source_series - search_value
    min_is_nearest_hit = deltas_towards_search_value.abs()
    return min_is_nearest_hit.idxmin()


def override_left_with_right_series(
    left_target: Series, overriding_right: Series
) -> Series:
    """
    Overrides overlapping items of left with right.

    Args:
        left_target(DataFrame):
            Series which should be overridden.

        overriding_right(DataFrame):
            The new values as Series, which overrides the *left target*.

    Returns:
        Series

    Examples:
        >>> from pandas import Series, Int16Dtype
        >>> import numpy as np
        >>> left = Series(np.full(3, 1), index=list(iter("abc")), dtype=Int16Dtype())
        >>> left
        a    1
        b    1
        c    1
        dtype: Int16
        >>> right = Series(np.full(2, 2), index=list(iter("ad")), dtype=Int16Dtype())
        >>> right
        a    2
        d    2
        dtype: Int16
        >>> override_left_with_right_series(left, right)
        a    2
        b    1
        c    1
        d    2
        dtype: Int16

    """
    old_series = left_target.copy()
    same_indexes = overriding_right.index.intersection(old_series.index)
    new_indexes = overriding_right.index.difference(old_series.index)
    old_series.loc[same_indexes] = overriding_right.loc[same_indexes]
    new_items = overriding_right.loc[new_indexes]
    overridden_series = pandas.concat([old_series, new_items], sort=True)
    return overridden_series