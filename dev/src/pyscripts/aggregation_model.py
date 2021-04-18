"""
The purpose of this module is aggregate all data streams into a singular data format for future simulation and analysis.
"""

import numpy as np
import pandas as pd


# Custom modules
from income_model import basic_model


def info_breakdown(df):
    """
    """
    
    print('df shape:', df.shape)
    print(df.tail(24))


def basic_agg_frame(start_dt, start_year, end_year):
    """
    Generates basic aggregation DataFrame for use with other data sources.
    This includes generating a basic date series for joining as well as pre-generating
    calculated columns of interest.
    """
    
    date_range = pd.date_range(start_dt, periods=12*(end_year - start_year), freq='MS')
    disposable_income_init = np.zeros(len(date_range))

    df = pd.DataFrame({'Months': date_range, 'Disposable_Income': disposable_income_init})
    return df


def join_function(df_lhs, df_rhs):
    """
    """
    df = df_lhs.merge(df_rhs, how='outer', left_on='Months', right_on='Months')
    return df


def main():
    
    # Generate agg DataFrame
    # Inputs will be start working age and end of life...
    df = basic_agg_frame('01-01-2020', 2020, 2051)
    
    info_breakdown(df)
    # Generate income data
    start_year = 2020
    end_year = 2050
    income = 50000 # p.a. constant
    df_income = basic_model(start_year, end_year, income)
    
    info_breakdown(df_income)
    
    # Join DataFrames on common column, 'Months'
    df_agg = join_function(df, df_income)    
    
    info_breakdown(df_agg)


if __name__ == '__main__':
    print('Running in main')
    main()