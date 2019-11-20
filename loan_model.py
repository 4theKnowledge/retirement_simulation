"""
"""

import pandas as pd
from datetime import date
import numpy as np
from collections import OrderedDict
from dateutil.relativedelta import *
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

from absl import flags
from absl import app

FLAGS = flags.FLAGS

flags.DEFINE_float('loan_amt', 500000, 'Loan amount (principal)')
flags.DEFINE_float('loan_ir', 0.04, 'Interest rate for mortage amortization')
flags.DEFINE_integer('loan_length_yrs', 30, 'Mortgage length')
flags.DEFINE_string('interest_type', 'fixed', 'Interest rate type - fixed or variable')
flags.DEFINE_string('var_ir_fluct', 'conservative', 'Interest rate fluctuation / behaviour setting')
flags.DEFINE_float('add_payment', 0, 'Additional principal payment above minimum repayment')
flags.DEFINE_integer('pa_payments', 12, 'Number of payments (and compounding events) per annum')
flags.DEFINE_float('lump_sum', 0, 'Value of lump sum to apply to loan')
flags.DEFINE_string('lump_sum_dt', None, 'Date that lump sum is applied to loan')

loan_amt = 300000
loan_ir = 0.04
loan_length_yrs = 30
var_ir = True
var_ir_fluct = 'conservative'
add_principal = 500
loan_start = date(2020,1,1)
lump_sum = 25000
lump_sum_dt = date(2022,6,1)



def amortize(principal,
             interest_rate,
             years,
             var_interest_rate = False,
             interest_rate_fluct = 'aggressive',
             addl_principal=0,
             annual_payments=12,
             start_date=date.today(),
             lump_sum_paymnt = 0,
             lump_sum_date = date(2050,1,1)):

    init_addl_principal = addl_principal
    
    pmt = -round(np.pmt(interest_rate/annual_payments, years*annual_payments, principal), 2)
    # initialize the variables to keep track of the periods and running balances
    p = 1
    beg_balance = principal
    end_balance = principal
    
    while end_balance > 0:
        # Fluctuate variable interest...
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
        

        # Ensure additional payment gets adjusted if the loan is being paid off.
        # If the difference between the beginning balance and principal is < additional payment, reduce additional
        # payment to match remaining balance.
        
        # Add lump-sum event (Assumes that payment occurs at month begin)
        if start_date == lump_sum_date:
            
            adhoc_paymnt = min((addl_principal+lump_sum_paymnt), beg_balance - principal)
            # print(f'Adhoc - Lump sum payment: ${adhoc_paymnt:0.0f}')
            end_balance = beg_balance - (principal + adhoc_paymnt)
        else:
            addl_principal = min(addl_principal, beg_balance - principal)
            end_balance = beg_balance - (principal + addl_principal)
            adhoc_paymnt = 0

        yield OrderedDict([('Month',start_date),
                           ('Period', p),
                           ('Begin Balance', beg_balance),
                           ('Payment', pmt),
                           ('Principal', principal),
                           ('Interest', interest),
                           ('Additional_Payment', addl_principal),
                           ('Adhoc Payment', adhoc_paymnt),
                           ('End Balance', end_balance)])
        
        if addl_principal > (beg_balance - principal):
            addl_principal = init_addl_principal
        
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


def loan_comparison(df_ls, df_nls):
    """
    """
    
    # Loan payoff time
    time_ls = df_ls['Month'].iloc[-1]
    time_nls = df_nls['Month'].iloc[-1]
    print(f'Time saved on loan: {time_nls.year - time_ls.year} years (Make this more accurate later on...)')
    
    # Interest saved
    total_interest_ls = df_ls['Interest'].sum()
    total_interest_nls = df_nls['Interest'].sum()
    print(f'Interest Saved: ${(total_interest_nls - total_interest_ls):0.0f}')
    

def loan_plot(df_ls, df_nls):
    """
    """
    
    plt.scatter(x=df_ls['Month'], y=df_ls['Interest'], color='g')
    plt.scatter(x=df_nls['Month'], y=df_nls['Interest'], color='r')
    plt.legend(['Lump Sum', 'No Lump Sum'])
    plt.ylabel('Interest ($)')
    plt.xlabel('Time (Months)')
    plt.show()


loan_amt = 300000
loan_ir = 0.04
loan_length_yrs = 30
var_ir = True
var_ir_fluct = 'conservative'
add_principal = 500
loan_start = date(2020,1,1)
lump_sum = 25000
lump_sum_dt = date(2022,6,1)

# Lump Sum (ls)
loan_ls = pd.DataFrame(amortize(loan_amt, loan_ir, loan_length_yrs,
                              var_interest_rate=var_ir,
                              interest_rate_fluct=var_ir_fluct,
                              addl_principal=add_principal,
                              start_date=loan_start,
                              lump_sum_paymnt = lump_sum,
                              lump_sum_date=lump_sum_dt
                              ))
# No Lump Sum (nls)
loan_nls = pd.DataFrame(amortize(loan_amt, loan_ir, loan_length_yrs,
                              var_interest_rate=var_ir,
                              interest_rate_fluct=var_ir_fluct,
                              addl_principal=add_principal,
                              start_date=loan_start,
                              lump_sum_paymnt=0,
                              lump_sum_date=None
                              ))

if __name__ == '__main__':
    loan_comparison(loan_ls, loan_nls)
    loan_plot(loan_ls, loan_nls)