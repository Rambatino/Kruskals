<img src="https://img.shields.io/pypi/v/Kruskals.svg"> <img src="https://img.shields.io/pypi/pyversions/pytest.svg"> <img src="https://circleci.com/gh/Rambatino/Kruskals.png?style=shield&circle-token=031aab51ad1dea4a698d02f02288887f06c1a9ef"><a href="https://www.quantifiedcode.com/app/project/664c0a32a4b745a8b3728c4a3033e055"><img src="https://www.quantifiedcode.com/api/v1/project/664c0a32a4b745a8b3728c4a3033e055/badge.svg" alt="Code issues"/></a> <a href="https://codecov.io/gh/Rambatino/Kruskals"><img src="https://codecov.io/gh/Rambatino/Kruskals/branch/master/graph/badge.svg" alt="Codecov" /></a>


Kruskal's Driver Analysis (Not to be confused with his Distance Measure algorithm)
=========================================

This package provides a python implementation of [Kruskal's Algorithm](https://en.wikipedia.org/wiki/Kruskal%27s_algorithm)


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

pandas_data_frame = ...
independent_variable_columns = ['a', 'b', 'c']
dep_variable = 'd'
Kruskals.from_pandas_df(df, independent_variable_columns, dep_variable).distance()
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
