"""
A basic model for personal income over time. It is assumed that the growth rate is 4% p.a.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from dateutil.relativedelta import *

# start_date = datetime.strptime("01-01-2020", "%d-%m-%Y")

# start_date += relativedelta(months=1)


# current_age = 26
# current_income = 50000
# income_growth_rate = 0.04   # 4% per annum; static.
# retirement_age = 65

# date_range = pd.date_range('01-01-2020', periods=12*(retirement_age-current_age), freq='MS')    # AS - year start frequency; MS - month start frequency.
# dummy_data = np.ones(len(date_range))
# df = pd.DataFrame({'Months': date_range, 'Data': dummy_data})

# df['Data'] = df.groupby(df['Months'].dt.year).apply(lambda x: df['Data']*current_income*(1+income_growth_rate))
# print(df)
# print(len(df))

# for group in df.groupby(df['Months'].dt.year).apply(lambda x: df['Data']*current_income*(1+income_growth_rate)):
#     print(group)

def basic_model(start_year, end_year, basic_income_level):
    date_range = pd.date_range('01-01-2020', periods=12*(end_year - start_year), freq='MS')
    income_data = np.ones(len(date_range))*basic_income_level
    df = pd.DataFrame({'Months': date_range, 'Income': income_data})
    return df

if __name__ == '__main__':
    print('Running in main')
    df = basic_model(2020, 2050, 50000)
    print(df.head())
    print(len(df))