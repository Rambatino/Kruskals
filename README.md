<img src="https://img.shields.io/pypi/v/Kruskals.svg"> <img src="https://img.shields.io/pypi/pyversions/pytest.svg"> <img src="https://circleci.com/gh/Rambatino/Kruskals.png?style=shield&circle-token=031aab51ad1dea4a698d02f02288887f06c1a9ef"><a href="https://www.quantifiedcode.com/app/project/664c0a32a4b745a8b3728c4a3033e055"><img src="https://www.quantifiedcode.com/api/v1/project/664c0a32a4b745a8b3728c4a3033e055/badge.svg" alt="Code issues"/></a> <a href="https://codecov.io/gh/Rambatino/Kruskals"><img src="https://codecov.io/gh/Rambatino/Kruskals/branch/master/graph/badge.svg" alt="Codecov" /></a>


[Kruskal's Relative Importance / Driver Analysis](http://amstat.tandfonline.com/doi/abs/10.1080/00031305.1987.10475432) (Not to be confused with Joseph's Distance Measure algorithm)
=========================================

This package provides a python implementation of [Kruskal's Algorithm](http://amstat.tandfonline.com/doi/abs/10.1080/00031305.1987.10475432)

Caveats
------------

To calculate the inverse it uses the [Moore–Penrose pseudoinverse](https://en.wikipedia.org/wiki/Moore%E2%80%93Penrose_pseudoinverse) which permits highly correlated independent variables to be passed as well as variables that have zero variance. It is up to the user of this library to ensure they are comfortable with this. N.B. if the normal matrix inversion would work, that is used, the psuedoinverse is only applied if the former fails.

Installation
------------

Kruskals is distributed via [pypi](https://pypi.python.org/pypi/Kruskals) and can be installed like:

``` bash
pip install Kruskals
```

Alternatively, you can clone the repository and install via
``` bash
pip install -e path/to/your/checkout
```

Creating the Kruskal's Distance Measure
---------------

``` python

from Kruskals import Kruskals

# drivers score can be calculated straight from numpy:

>>> import Kruskals
>>> import numpy as np

>>> ndarr = np.array([
...     [1, 2, 3, 4, 5, 6],
...     [6, 5, 4, 3, 8, 1],
...     [1, 1, 9, 1, 1, 1],
...     [9, 2, 2, 2, 2, 2],
...     [3, 3, 3, 9, 3, 3],
...     [1, 2, 2, 9, 1, 4]
...   ])
>>> arr = np.array([1, 2, 3, 4, 5, 6])

>>> Kruskals.Kruskals(ndarr, arr).driver_score()
array([ 0.14721238,  0.44397682,  0.23979013,  0.62492599,  0.71898045,
        0.31662422])

# or from a pandas dataframe:

>>> import pandas as pd
>>> df = pd.DataFrame(ndarr)
>>> df.columns = ['a', 'b', 'c', 'd', 'e', 'f']
>>> df
   a  b  c  d  e  f
0  1  2  3  4  5  6
1  6  5  4  3  8  1
2  1  1  9  1  1  1
3  9  2  2  2  2  2
4  3  3  3  9  3  3
5  1  2  2  9  1  4
>>> ind_cols = ['a', 'b', 'c', 'd', 'e']
>>> Kruskals.Kruskals.from_pandas_df(df, ind_cols, 'f').driver_score_to_series()
driver
a    0.382246
b    0.267348
c    0.485063
d    0.262053
e    0.165562
Name: score, dtype: float64

# it also supports directional drivers (determined by the correlation coefficient between
# each independent variable, and the dependent)

>>> Kruskals.Kruskals.from_pandas_df(df, ind_cols, 'f').driver_score_to_series(directional=True)
driver
a   -0.382246
b   -0.267348
c   -0.485063
d    0.262053
e   -0.165562
Name: score, dtype: float64
```

Running from the Command Line
-----------------------------

You can play around with the repo by cloning and running this from the command line:

```
python -m Kruskals tests/data/kruskals_data.csv y x1 x2 x3 x4 x5 x6 x7 x8 x9 x10 x11 x12 x13 x14 x15 x16 x17 x18 x19 x20
```
This prints out the distance metrics for each column (in the same order). It can run about 50 columns within 10 seconds.

Testing
-------

Kruskals uses [`pytest`](https://pypi.python.org/pypi/pytest) for its unit testing. The tests can be run from the root of a checkout with:
``` bash
py.test
```
