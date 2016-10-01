import numpy as np
from scipy.special import factorial

class Kruskals(object):
    """
    Class to organise running Josef Kruskal's algorithm
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
        ind_c, pij, pijm = self.generate_diff(self._ndarr, self._arr)
        pij_row_mean = pij[~np.isnan(pij)].reshape(ind_c, ind_c-1).mean(axis=1) * (ind_c - 1)
        fact = factorial(ind_c - 1) / (2 * factorial(ind_c - 3))
        pijm_row_sum = np.nan_to_num(pijm).sum(axis=0).sum(axis=1)
        pijm_row_count = (np.nan_to_num(pijm) > 0).sum(axis=0).sum(axis=1)
        pijm_row_mean = pijm_row_sum / pijm_row_count * fact
        return (pij_row_mean + pijm_row_mean) / ((ind_c - 1) + fact)

    def generate_diff(self, ndarr, arr):
        """
        Internal method to calculate the difference between all points
        """
        l = ndarr.shape[1]
        pij = np.empty((l,l,)) * np.nan
        pijm = np.empty((l,l,l)) * np.nan
        for i in range(l):
            for j in range(l):
                if i != j:
                    pij[i, j] = self.pcor_squared(np.array([ndarr[:,i], arr, ndarr[:,j]]))
                    for m in range(l):
                        if m != i and m != j and m > j:
                            pijm[m, i, j] = self.pcor_squared(np.array([ndarr[:,i], arr, ndarr[:,j], ndarr[:, m]]))
        return (l, pij, pijm)

    def pcor_squared(self, ndarr):
        """
        Internal method to calculate the partial correlation squared
        """
        icvx = np.linalg.inv(np.cov(ndarr))
        partial = (icvx[0, 1] * np.sqrt(1.0 / icvx[0, 0]) * np.sqrt(1.0 / icvx[1, 1]))
        return partial**2

    def percentage(self):
        """
        Distance as a relative percentage
        """
        distance = self.distance()
        return distance / distance.sum() * 100
