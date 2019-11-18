"""

"""

import pandas as pd
from datetime import date
import numpy as np
from collections import OrderedDict
from dateutil.relativedelta import *
from datetime import datetime, timedelta

from absl import flags
from absl import app

FLAGS = flags.FLAGS

flags.DEFINE_float('mortgage_principal', 500000, 'Loan amount (principal)')
flags.DEFINE_float('interest_rate', 0.04, 'Interest rate for mortage amortization')
flags.DEFINE_integer('mortgage_years', 30, 'Mortgage length')
flags.DEFINE_string('interest_type', 'fixed', 'Interest rate type - fixed or variable')
flags.DEFINE_string('variable_interest_fluct', 'conservative', 'Interest rate fluctuation / behaviour setting')
flags.DEFINE_float('additional_principal', 0, 'Additional principal payment above minimum repayment')
flags.DEFINE_integer('annual_payments', 12, 'Number of payments (and compounding events) per year')

def amortize(argv, principal,
             interest_rate,
             years,
             var_interest_rate = False,
             interest_rate_fluct = 'aggressive',
             addl_principal=0,
             annual_payments=12,
             start_date=date.today()):

    """
    """
    

    pmt = -round(np.pmt(interest_rate/annual_payments, years*annual_payments, principal), 2)
    # initialize the variables to keep track of the periods and running balances
    p = 1
    beg_balance = principal
    end_balance = principal
    
    while end_balance > 0:
        if var_interest_rate and start_date.month == 6 and interest_rate < 0.06:
#             print('Modifying interest rate...')
            # Assumes that interest rate changes occur mid-year
            if interest_rate_fluct == 'chaotic':
                interest_rate = interest_rate * np.random.uniform(0.5, 1.5)
            if interest_rate_fluct == 'aggressive':
                interest_rate = interest_rate * np.random.uniform(0.8,1.2)
            if interest_rate_fluct == 'moderate':
                interest_rate = interest_rate * np.random.uniform(0.875,0.125)
            if interest_rate_fluct == 'conservative':
                interest_rate = interest_rate * np.random.uniform(0.95,1.05)
#             print(interest_rate)
        
        # Recalculate the interest based on the current balance
        interest = round(((interest_rate/annual_payments) * beg_balance), 2)

        # Determine payment based on whether or not this period will pay off the loan
        pmt = min(pmt, beg_balance + interest)
        principal = pmt - interest

        # Ensure additional payment gets adjusted if the loan is being paid off
        addl_principal = min(addl_principal, beg_balance - principal)
        end_balance = beg_balance - (principal + addl_principal)

        yield OrderedDict([('Month',start_date),
                           ('Period', p),
                           ('Begin Balance', beg_balance),
                           ('Payment', pmt),
                           ('Principal', principal),
                           ('Interest', interest),
                           ('Additional_Payment', addl_principal),
                           ('End Balance', end_balance)])

        # Increment the counter, balance and date
        p += 1
        start_date += relativedelta(months=1)
        beg_balance = end_balance


def amortize_format(df):
    """
    Format amortize generator.
    
    """
    
    df.set_index('Month', inplace=True)
    df.index = pd.to_datetime(df.index)
    return df

def mc_sim(argv, iters=10):
    """
    """
    sim_results = {i: amortize_format(pd.DataFrame(amortize(argv, 700000, 0.04, 30, 
                                     var_interest_rate=True,
                                     interest_rate_fluct='conservative',
                                     addl_principal=200,
                                     start_date=date(2019, 12,1))))['Interest'] for i in range(iters)}
    # sim_results_formatted = {}
    
    return sim_results


def main(argv):
    
    sim_results = mc_sim(argv)
    print(sim_results[0].head(50))
    
    
    

if __name__ == '__main__':
    app.run(main)