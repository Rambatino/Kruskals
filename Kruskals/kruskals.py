import numpy as np
import pandas as pd
from scipy.special import factorial
from itertools import combinations, chain

class Kruskals(object):
    """
    Class to run Josef Kruskal's algorithm
    Parameters
        ----------
        ndarr : numpy.ndarray (dtype: float/int)
            non-aggregated 2-dimensional array containing
            independent variables on the veritcal axis and (usually)
            respondent level data on the horizontal axis
        arr : numpy.ndarray (dtype: float/int)
            1-dimensional array of the dependent variable associated with ndarr
    """
    def __init__(self, ndarr, arr, i_vars=None):
        self._ndarr = ndarr
        self._arr = arr
        self._driver_score = None
        self._i_vars = i_vars

        if i_vars and len(i_vars) != ndarr.shape[1]:
            self._i_vars = None

    @staticmethod
    def from_pandas_df(df, i_vars, d_var):
        """
        Helper method to pre-process a pandas data frame in order to run Kruskal's algorithm
        analysis

        Parameters
        ----------
        df : pandas.DataFrame
            the dataframe with the dependent and independent variables in which
            to slice from
        i_vars : array-like
            list of the column names for the independent variables
        d_var : string
            the name of the dependent variable in the dataframe
        """
        ind_df = df[i_vars]
        ind_values = ind_df.values
        dep_values = df[d_var].values
        return Kruskals(ind_values, dep_values, i_vars)

    def driver_score_to_series(self, directional=False):
        """
        Returns the driver score for each variable in the independent set
        as a pandas series
        """
        series = pd.Series(self.driver_score(directional), index=self._i_vars)
        series.name = 'score'
        series.index.name = 'driver'
        return series

    def driver_score(self, directional=False):
        """
        Calculate the driver score for all independent variables
        """
        if self._driver_score is None:
            ind_c, pij, pijm = self.generate_diff(self._ndarr, self._arr)
            pij_row_mean = np.nanmean(pij, axis=1) * (ind_c - 1)
            fact = factorial(ind_c - 1) / (2 * factorial(ind_c - 3))
            pijm_row_mean = np.nanmean(pijm, axis=(0, 2)) * fact
            self._driver_score = (pij_row_mean + pijm_row_mean) / ((ind_c - 1) + fact)
            if directional:
                self._driver_score = self._driver_score * np.apply_along_axis(self.correlation_coef, 0, self._ndarr, self._arr)
        return np.nan_to_num(self._driver_score)

    def percentage(self):
        """
        Distance as a relative percentage
        """
        return self.distance() / self.distance().sum() * 100

    def generate_diff(self, ndarr, arr):
        """
        Internal method to calculate the partial correlation squared between
        the independent and the dependent variables
        """
        l = ndarr.shape[1]
        pij = np.empty((l,l,)) * np.nan
        pijm = np.empty((l,l,l)) * np.nan
        for i, j in chain.from_iterable(((x, y), (y, x)) for x, y in combinations(range(l), 2)):
            pij[i, j] = self.pcor_squared(np.array([ndarr[:,i], arr, ndarr[:,j]]))
            for m in (x for x in range(j+1, l) if x != i):
                pijm[m, i, j] = self.pcor_squared(np.array([ndarr[:,i], arr, ndarr[:,j], ndarr[:, m]]))
        return (l, pij, pijm)

    @staticmethod
    def pcor_squared(ndarr):
        """
        Internal method to calculate the partial correlation squared
        """
        icvx = np.linalg.pinv(np.cov(ndarr))
        return (icvx[0, 1] * icvx[0, 1]) / (icvx[0, 0] * icvx[1, 1])

    def percentage(self):
        """
        Internal method to calculate relative affect on the dependent variable
        """
        return self.driver_score() / self.driver_score().sum() * 100

    @staticmethod
    def correlation_coef(ind, dep):
        return 1 if np.corrcoef(ind, dep)[0][1] >= 0 else -1
