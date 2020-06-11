import numpy as np
import pandas as pd
from scipy.special import factorial
from itertools import combinations, permutations, chain
from warnings import warn

class Kruskals(object):
    """
    Class to run William Kruskal's algorithm
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
        self._arr = arr[~np.isnan(arr)]
        self._ndarr = ndarr[~np.isnan(arr)]
        self._driver_score = None
        self._i_vars = i_vars

        if self._arr.shape[0] < arr.shape[0]:
            warn("NaN values have been removed from the dependent variable")

        if i_vars is not None and len(i_vars) != ndarr.shape[1]:
            raise ValueError("driver labels: {}, not sufficient for ndarray of shape {}".format(i_vars, ndarr.shape))

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

    def driver_score_to_series(self, directional=False, percentage=False):
        """
        Returns the driver score for each variable in the independent set
        as a pandas series
        """
        series = pd.Series(self.driver_score(directional, percentage), index=self._i_vars)
        series.name = 'score'
        series.index.name = 'driver'
        return series

    def driver_score(self, directional=False, percentage=False):
        """
        Calculate the driver score for all independent variables
        """
        if self._driver_score is None:
            ind_c, m_ij, m_ijm = self.generate_diff(self._ndarr, self._arr)
            m_ij_row_mean = np.nanmean(m_ij, axis=1) * (ind_c - 1)
            fact = factorial(ind_c - 1) / (2 * factorial(ind_c - 3))
            m_ijm_row_mean = np.nanmean(m_ijm, axis=1) * fact
            self._driver_score = (m_ij_row_mean + m_ijm_row_mean) / ((ind_c - 1) + fact)
            self._driver_score = np.nan_to_num(self._driver_score)
        driver_score = self._driver_score
        if directional:
            driver_score = driver_score * np.apply_along_axis(self.correlation_coef, 0, self._ndarr, self._arr)
        if percentage:
            return driver_score / np.fabs(driver_score).sum() * 100
        else:
            return driver_score

    def percentage(self, directional=False):
        """ Distance as a relative percentage """
        warn("percentage() has been deprecated, please use driver_score(percentage=True)")
        return self.driver_score(directional) / np.fabs(self.driver_score(directional)).sum() * 100

    def generate_diff(self, ndarr, arr):
        """
        Internal method to calculate the partial correlation squared between
        the independent and the dependent variables
        """
        l = ndarr.shape[1]
        cov_ij = tuple(
            np.cov(np.array([ndarr[:,j], arr, ndarr[:,i]]))
            for j, i in permutations(range(l), 2)
        )
        pinv_ij = np.linalg.pinv(cov_ij, hermitian=True)
        pcor_ij = ((pinv_ij[:, 0, 1] * pinv_ij[:, 0, 1]) / (pinv_ij[:, 0, 0] * pinv_ij[:, 1, 1]))

        m_ijm = np.empty((l,l,l)) * np.nan

        cov_mij = [
            np.cov(np.array([ndarr[:,i], arr, ndarr[:,j], ndarr[:, m]]))
            for i, j in permutations(range(l), 2)
            for m in range(j+1, l) if m != i
        ]
        pinv_mij = np.linalg.pinv(cov_mij, hermitian=True)
        pcor_mij = ((pinv_mij[:, 0, 1] * pinv_mij[:, 0, 1]) / (pinv_mij[:, 0, 0] * pinv_mij[:, 1, 1]))

        return (l, pcor_ij.reshape(-1, l-1), pcor_mij.reshape(l, -1))

    @staticmethod
    def correlation_coef(ind, dep):
        return 1 if np.corrcoef(ind, dep)[0][1] >= 0 else -1
