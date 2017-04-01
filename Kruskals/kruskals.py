import numpy as np
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
    def __init__(self, ndarr, arr):
        self._ndarr = ndarr
        self._arr = arr
        self._distance = None

    @staticmethod
    def from_pandas_df(df, i_variables, d_variable):
        """
        Helper method to pre-process a pandas data frame in order to run Kruskal's algorithm
        analysis

        Parameters
        ----------
        df : pandas.DataFrame
            the dataframe with the dependent and independent variables in which
            to slice from
        i_variables : array-like
            list of the column names for the independent variables
        d_variable : string
            the name of the dependent variable in the dataframe
        """
        ind_df = df[i_variables]
        ind_values = ind_df.values
        dep_values = df[d_variable].values
        return Kruskals(ind_values, dep_values)

    def distance(self):
        """
        Calculate the average distance between a point on the
        n-dimensional plane and the other points
        """
        if self._distance is None:
            ind_c, pij, pijm = self.generate_diff(self._ndarr, self._arr)
            pij_row_mean = np.nanmean(pij, axis=1) * (ind_c - 1)
            fact = factorial(ind_c - 1) / (2 * factorial(ind_c - 3))
            pijm_row_mean = np.nanmean(pijm, axis=(0, 2)) * fact
            self._distance = (pij_row_mean + pijm_row_mean) / ((ind_c - 1) + fact)
        return self._distance

    def percentage(self):
        """
        Distance as a relative percentage
        """
        return self.distance() / self.distance().sum() * 100

    def generate_diff(self, ndarr, arr):
        """
        Internal method to calculate the difference between all points
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
        icvx = np.linalg.inv(np.cov(ndarr))
        return (icvx[0, 1] * icvx[0, 1]) / (icvx[0, 0] * icvx[1, 1])
