"""
Testing module for Kruskals
"""

from setup_tests import Kruskals
import numpy as np
import pandas as pd
import pytest

def test_driver_score():
    """ Test driver_score is calculated correctly """
    ndarr = np.array([
      [1, 2, 3, 4, 5, 6],
      [6, 5, 4, 3, 8, 1],
      [1, 1, 9, 1, 1, 1],
      [9, 2, 2, 2, 2, 2],
      [3, 3, 3, 9, 3, 3],
      [1, 2, 2, 9, 1, 4]
    ])

    arr = np.array([1, 2, 3, 4, 5, 6])

    exp_driver_score = np.array([ 0.14721,  0.44398,  0.23979,  0.62493,  0.71898,  0.31662])
    driver_score = np.round(Kruskals.Kruskals(ndarr, arr).driver_score(), decimals=5)

    assert np.array_equal(driver_score, exp_driver_score)

def test_from_pandas_df():
    """ Test from pandas_df correctly slices the data """
    ndarr = np.array([
      [1, 2, 3, 4, 5, 6, 1],
      [6, 5, 4, 3, 8, 1, 2],
      [1, 1, 9, 1, 1, 1, 3],
      [9, 2, 2, 2, 2, 2, 4],
      [3, 3, 3, 9, 3, 3, 5],
      [1, 2, 2, 9, 1, 4, 6]
    ])

    exp_driver_score = np.array([ 0.14721,  0.44398,  0.23979,  0.62493,  0.71898,  0.31662])

    df = pd.DataFrame(ndarr)
    driver_score = np.round(Kruskals.Kruskals.from_pandas_df(df, list(range(6)), 6).driver_score(), decimals=5)

    assert np.array_equal(driver_score, exp_driver_score)

def test_percentage():
    """ Test percentage is calculated correctly """
    ndarr = np.array([
      [1, 2, 3, 4, 5, 6],
      [6, 5, 4, 3, 8, 1],
      [1, 1, 9, 1, 1, 1],
      [9, 2, 2, 2, 2, 2],
      [3, 3, 3, 9, 3, 3],
      [1, 2, 2, 9, 1, 4]
    ])

    arr = np.array([1, 2, 3, 4, 5, 6])

    exp_driver_score = np.array([  5.90856,  17.81959,   9.62429,  25.08222,  28.85722,  12.70813])
    driver_score = np.round(Kruskals.Kruskals(ndarr, arr).percentage(), decimals=5)

    assert np.array_equal(driver_score, exp_driver_score)

def test_series_output():
    """ Test percentage is calculated correctly """
    ndarr = np.array([
      [1, 2, 3, 4, 5, 6],
      [6, 5, 4, 3, 8, 1],
      [1, 1, 9, 1, 1, 1],
      [9, 2, 2, 2, 2, 2],
      [3, 3, 3, 9, 3, 3],
      [1, 2, 2, 9, 1, 4]
    ])

    arr = np.array([1, 2, 3, 4, 5, 6])

    exp_driver_score = np.array([ 0.14721,  0.44398,  0.23979,  0.62493,  0.71898,  0.31662])
    series = Kruskals.Kruskals(ndarr, arr).driver_score_to_series()

    assert np.array_equal(np.round(series.values, decimals=5), exp_driver_score)
    assert series.name == 'score'
    assert series.index.name == 'driver'

def test_ivars_sub_into_series():
    """
    Test that the column names are correctly mapped
    to the index values of the series
    """
    ndarr = np.array([
      [1, 2, 3, 4, 5, 6, 1],
      [6, 5, 4, 3, 8, 1, 2],
      [1, 1, 9, 1, 1, 1, 3],
      [9, 2, 2, 2, 2, 2, 4],
      [3, 3, 3, 9, 3, 3, 5],
      [1, 2, 2, 9, 1, 4, 6]
    ])


    df = pd.DataFrame(ndarr)
    df.columns = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
    ind_cols = ['a', 'b', 'c', 'd', 'e', 'f']

    series = Kruskals.Kruskals.from_pandas_df(df, ind_cols, 'g').driver_score_to_series()

    assert (series.index.values == ind_cols).all()

def test_that_direction_is_applied_on_directional_drivers_analysis():
    """ Test whether some driver scores are negative """
    ndarr = np.array([
      [10, 2, 3, 4, 5, 6],
      [6, 5, 4, 3, 8, 1],
      [1, 1, 9, 1, 1, 1],
      [9, 2, 2, 2, 2, 2],
      [3, 3, 3, 9, 3, 3],
      [1, 2, 2, 9, 1, 4],
      [1, 2, 2, 9, 1, 4],
      [1, 2, 2, 9, 1, 4]
    ])

    arr = np.array([1, 2, 3, 4, 5, 6, 7, 8])

    series = Kruskals.Kruskals(ndarr, arr).driver_score_to_series(True)

    assert (series.values < 0).any()

def test_ability_to_handle_all_same_type():
    """
    Test to make sure that kruskals can handle data
    when all the values for and independent set are 0
    """
    ndarr = np.array([
      [10, 0, 3, 4, 5, 6],
      [6, 0, 4, 3, 5, 1],
      [1, 0, 9, 1, 5, 1],
      [9, 0, 2, 2, 5, 2],
      [3, 0, 3, 9, 5, 3],
      [1, 0, 2, 9, 5, 4],
      [1, 0, 2, 9, 5, 4],
      [1, 0, 2, 9, 5, 4]
    ])

    arr = np.array([1, 2, 3, 4, 5, 6, 7, 8])

    series = Kruskals.Kruskals(ndarr, arr).driver_score()

    assert series[1] == 0.0
    assert series[4] == 0.0

def test_can_handle_numpy_arrays_for_col_names():
    """ Test that df.columns can be passed into __init__ """
    ndarr = np.array([
      [1, 2, 3, 4, 5, 6, 1],
      [6, 5, 4, 3, 8, 1, 2],
      [1, 1, 9, 1, 1, 1, 3],
      [9, 2, 2, 2, 2, 2, 4],
      [3, 3, 3, 9, 3, 3, 5],
      [1, 2, 2, 9, 1, 4, 6]
    ])

    exp_driver_score = np.array([0.14721, 0.44398, 0.23979, 0.62493, 0.71898, 0.31662])

    df = pd.DataFrame(ndarr)
    df.columns = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
    driver_score = Kruskals.Kruskals(ndarr, exp_driver_score, i_vars=df.columns).driver_score_to_series()
    assert np.array_equal(driver_score.index.values, ['a', 'b', 'c', 'd', 'e', 'f', 'g'])

def test_return_error_if_i_vars_not_sufficient():
    """ Test that error raised when columns insufficient length """
    ndarr = np.array([
      [1, 2, 3, 4, 5, 6, 1],
      [6, 5, 4, 3, 8, 1, 2],
      [1, 1, 9, 1, 1, 1, 3],
      [9, 2, 2, 2, 2, 2, 4],
      [3, 3, 3, 9, 3, 3, 5],
      [1, 2, 2, 9, 1, 4, 6]
    ])

    exp_driver_score = np.array([0.14721, 0.44398, 0.23979, 0.62493, 0.71898, 0.31662])
    i_vars = ['a', 'b', 'c', 'd', 'e', 'f']

    with pytest.raises(ValueError) as e:
        Kruskals.Kruskals(ndarr, exp_driver_score, i_vars=i_vars).driver_score_to_series()
    assert 'driver labels: {}, not sufficient for ndarray of shape {}'.format(i_vars, ndarr.shape) in str(e.value)

def test_percentage_when_non_directional():
    """ Test the percentage function behaves as expected """
    ndarr = np.array([
      [10, 2, 3, 4, 5, 6],
      [6, 5, 4, 3, 8, 1],
      [1, 1, 9, 1, 1, 1],
      [9, 2, 2, 2, 2, 2],
      [3, 3, 3, 9, 3, 3],
      [1, 2, 2, 9, 1, 4],
      [1, 2, 2, 9, 1, 4],
      [1, 2, 2, 9, 1, 4]
    ])
    arr = np.array([1, 2, 3, 4, 5, 6, 7, 8])
    percentage = Kruskals.Kruskals(ndarr, arr).driver_score(percentage=True)
    assert (np.round(percentage, decimals=4) == [18.7523, 13.8413, 15.4078, 21.5111, 23.4954, 6.9921]).all()

def test_percentage_when_directional():
    """ Test the percentage function behaves as expected """
    ndarr = np.array([
      [10, 2, 3, 4, 5, 6],
      [6, 5, 4, 3, 8, 1],
      [1, 1, 9, 1, 1, 1],
      [9, 2, 2, 2, 2, 2],
      [3, 3, 3, 9, 3, 3],
      [1, 2, 2, 9, 1, 4],
      [1, 2, 2, 9, 1, 4],
      [1, 2, 2, 9, 1, 4]
    ])
    arr = np.array([1, 2, 3, 4, 5, 6, 7, 8])
    percentage = Kruskals.Kruskals(ndarr, arr).driver_score(directional=True, percentage=True)
    assert (np.round(percentage, decimals=4) == [-18.7523, -13.8413, -15.4078, 21.5111, -23.4954, 6.9921]).all()
