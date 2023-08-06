from pandas import DataFrame

from trashpanda import (
    cut_after,
    meld_along_columns,
    cut_before,
    cut_dataframe_after_max,
)
import examplecurves
import pytest


def test_cut_after():
    """
    >>> from trashpanda import cut_after
    >>> import examplecurves
    >>> from doctestprinter import print_pandas
    >>> sample_curves = examplecurves.Static.create("verticallinear0")
    >>> print_pandas(sample_curves[0], formats="{:.2g}")
            y
    x
    0.00  0.0
    0.23  2.3
    0.45  4.6
    0.68  6.9
    0.91  9.2
    >>> print_pandas(cut_after(sample_curves[0], 1.0), formats="{:.2g}")
            y
    x
    0.00  0.0
    0.23  2.3
    0.45  4.6
    0.68  6.9
    0.91  9.2
    1.00  nan
    """
    sample_curves = examplecurves.Static.create("verticallinear0")
    for index, curve in enumerate(sample_curves):
        curve.name = "y_{}".format(index)

    single_source_curve = sample_curves[0]
    single_result_curve = cut_after(single_source_curve, 0.0)
    assert len(single_result_curve) == 1

    single_result_curve = cut_after(single_source_curve, -1.0)
    assert len(single_result_curve) == 0

    single_result_curve = cut_after(single_source_curve, 1.0)
    assert len(single_result_curve) == 6

    with pytest.raises(TypeError):
        cut_after([1, 2, 3], 0.0)


def test_cut_before():
    """
    >>> from trashpanda import cut_before
    >>> import examplecurves
    >>> from doctestprinter import print_pandas
    >>> sample_curves = examplecurves.Static.create("verticallinear0")
    >>> print_pandas(sample_curves[0], formats="{:.2g}")
            y
    x
    0.00  0.0
    0.23  2.3
    0.45  4.6
    0.68  6.9
    0.91  9.2
    >>> print_pandas(cut_before(sample_curves[0], -1.0), formats="{:.2g}")
             y
    x
    -1.00  nan
     0.00  0.0
     0.23  2.3
     0.45  4.6
     0.68  6.9
     0.91  9.2
    """
    sample_curves = examplecurves.Static.create("verticallinear0")
    for index, curve in enumerate(sample_curves):
        curve.name = "y_{}".format(index)

    single_source_curve = sample_curves[0]
    single_result_curve = cut_before(single_source_curve, 0.0)
    assert len(single_result_curve) == 5

    single_result_curve = cut_before(single_source_curve, -1.0)
    assert len(single_result_curve) == 6

    single_result_curve = cut_before(single_source_curve, 1.0)
    assert len(single_result_curve) == 0

    with pytest.raises(TypeError):
        cut_before([1, 2, 3], 0.0)


def test_cut_after_max_with_auto_condition_column():
    sample_frame = DataFrame([0, 1, 2, 1])
    resulting_frame = cut_dataframe_after_max(sample_frame)
    assert len(resulting_frame) == 3