"""
This package provides a python implementation of Kruskals Algorithm
"""
import argparse
import savReaderWriter as spss
import pandas as pd
from .kruskals import Kruskals

def main():
    """Entry point when module is run from command line"""

    parser = argparse.ArgumentParser(description='Run Kruskal\'s Algorithm')
    parser.add_argument('file')
    parser.add_argument('dependent_variable', nargs=1)
    parser.add_argument('independent_variables', nargs='+')
    nspace = parser.parse_args()

    if nspace.file[-4:] == '.csv':
        data = pd.read_csv(nspace.file)
    elif nspace.file[-4:] == '.sav':
        raw_data = spss.SavReader(nspace.file, returnHeader = True, rawMode=True)
        raw_data_list = list(raw_data)
        data = pd.DataFrame(raw_data_list)
        data = data.rename(columns=data.loc[0]).iloc[1:]
    else:
        print('Could not detect file type. Please select one from "csv" or "sav"')

    print(Kruskals.from_pandas_df(data, nspace.independent_variables,
                                nspace.dependent_variable[0]).driver_score_to_series())

if __name__ == "__main__":
    main()
