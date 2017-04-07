"""
Testing module for Kruskals
"""

from setup_tests import Kruskals
import numpy as np
import pandas as pd

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
    """ Test percentage is calculated correctly """
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

def test_direction_on_directional_drivers_analysis():
    """ Test percentage is calculated correctly """
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