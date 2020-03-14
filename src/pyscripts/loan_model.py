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
flags.DEFINE_boolean('var_ir', False, 'Interest rate type - fixed (False) or variable (True)')
flags.DEFINE_string('var_ir_fluct', 'conservative', 'Interest rate fluctuation / behaviour setting')
flags.DEFINE_float('add_payment', 0, 'Additional principal payment above minimum repayment')
flags.DEFINE_integer('pa_payments', 12, 'Number of payments (and compounding events) per annum')
flags.DEFINE_string('loan_start_dt', '01-01-2020', 'Start date of loan')


def amortize(argv, lump_sum=0, lump_sum_dt=None):

    init_addl_principal = FLAGS.add_payment
    
    pmt = -round(np.pmt(FLAGS.loan_ir/FLAGS.pa_payments, FLAGS.loan_length_yrs*FLAGS.pa_payments, FLAGS.loan_amt), 2)
    # initialize the variables to keep track of the periods and running balances
    p = 1
    # Init temporary variables with default flag values; this is because we do not want to override the flag values 
    beg_balance = FLAGS.loan_amt
    end_balance = FLAGS.loan_amt
    start_date = datetime.strptime(FLAGS.loan_start_dt, "%d-%m-%Y")
    if lump_sum_dt:
        lump_sum_dt = datetime.strptime(lump_sum_dt, "%d-%m-%Y")
    var_ir = FLAGS.var_ir
    loan_ir = FLAGS.loan_ir
    add_payment = FLAGS.add_payment
    loan_amt = FLAGS.loan_amt
    
    while end_balance > 0:
        # Fluctuate variable interest...
        if var_ir and start_date.month == 6 and loan_ir < 0.06:
#             print('Modifying interest rate...')
            # Assumes that interest rate changes occur mid-year
            if FLAGS.var_ir_fluct == 'chaotic':
                loan_ir = loan_ir * np.random.uniform(0.5, 1.5)
            if FLAGS.var_ir_fluct == 'aggressive':
                loan_ir = loan_ir * np.random.uniform(0.8,1.2)
            if FLAGS.var_ir_fluct == 'moderate':
                loan_ir = loan_ir * np.random.uniform(0.875,0.125)
            if FLAGS.var_ir_fluct == 'conservative':
                loan_ir = loan_ir * np.random.uniform(0.95,1.05)
#             print(loan_ir)
        
        # Recalculate the interest based on the current balance
        interest = round(((loan_ir/FLAGS.pa_payments) * beg_balance), 2)

        # Determine payment based on whether or not this period will pay off the loan
        pmt = min(pmt, beg_balance + interest)
        loan_amt = pmt - interest
        
        # Ensure additional payment gets adjusted if the loan is being paid off.
        # If the difference between the beginning balance and principal is < additional payment, reduce additional
        # payment to match remaining balance.
        
        # Add lump-sum event (Assumes that payment occurs at month begin)
        if start_date == lump_sum_dt:
            
            adhoc_paymnt = min((add_payment + lump_sum), beg_balance - loan_amt)
            # print(f'Adhoc - Lump sum payment: ${adhoc_paymnt:0.0f}')
            end_balance = beg_balance - (loan_amt + adhoc_paymnt)
        else:
            FLAGS.add_payment = min(add_payment, beg_balance - loan_amt)
            end_balance = beg_balance - (loan_amt + add_payment)
            adhoc_paymnt = 0

        yield OrderedDict([('Month', start_date),
                           ('Period', p),
                           ('Begin Balance', beg_balance),
                           ('Payment', pmt),
                           ('Principal', FLAGS.loan_amt),
                           ('Interest', interest),
                           ('Interest_Rate', loan_ir),
                           ('Additional_Payment', add_payment),
                           ('Adhoc Payment', adhoc_paymnt),
                           ('End Balance', end_balance)])
        
        if add_payment > (beg_balance - loan_amt):
            add_payment = init_addl_principal
        
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


def loan_comparison(argv, df_ls, df_nls):
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
    
    total_cost_ls = total_interest_ls + FLAGS.loan_amt
    total_cost_nls = total_interest_nls + FLAGS.loan_amt 
    print(f'Total Loan Cost: NLS ${total_cost_nls:0.0f} LS ${total_cost_ls:0.0f}')
    

def loan_plot(df_ls, df_nls):
    """
    """
    
    fig, axs = plt.subplots(2, 1)
    axs[0].scatter(x=df_ls['Month'], y=df_ls['Interest'], color='g')
    axs[0].scatter(x=df_nls['Month'], y=df_nls['Interest'], color='r')
    axs[0].legend(['Lump Sum', 'No Lump Sum'])
    axs[0].set_ylabel('Interest ($)')
    axs[0].set_xlabel('Time (Months)')
    
    axs[1].scatter(x=df_ls['Month'], y=df_ls['Interest_Rate'] * 100, color='g')
    axs[1].scatter(x=df_nls['Month'], y=df_nls['Interest_Rate'] * 100, color='r')
    axs[1].legend(['Lump Sum', 'No Lump Sum'])
    axs[1].set_ylim([-10,10])
    axs[1].set_ylabel('Interest Rate (%)')
    axs[1].set_xlabel('Time (Months)')
    
    fig.tight_layout()
    plt.show()



def main(argv):
    # Lump Sum (ls)
    loan_ls = pd.DataFrame(amortize(argv))
    # print(loan_ls.head(25))
    # No Lump Sum (nls)
    loan_nls = pd.DataFrame(amortize(argv, lump_sum = 200000, lump_sum_dt = '01-06-2022'))
    print(loan_nls.head(25))
    loan_comparison(argv, loan_ls, loan_nls)
    loan_plot(loan_ls, loan_nls)
    

if __name__ == '__main__':
    app.run(main)