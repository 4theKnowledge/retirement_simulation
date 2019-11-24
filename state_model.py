"""
generator function that evaluates every month

income state = 1 if year <= end_income
superannuation state = 1 if income_state = 1

Two main phases:
1) working life
2) retirement

"""

import pandas as pd
import numpy as np
import datetime
from dateutil.relativedelta import relativedelta
from collections import OrderedDict
import matplotlib.pyplot as plt

# Phase 1 development

income = 50000

start_date = datetime.date(2020,1,1)    # Y-d-m
current_age = 26
retire_age = 65
retirement_end_age = 80
end_date_p1 = start_date + relativedelta(years=(retire_age-current_age))
end_date_p2 = start_date + relativedelta(years=(retirement_end_age-current_age))

print(f'Work life start date: {start_date} Work life end date/Retirement start date: {end_date_p1} Retirement end date: {end_date_p2}')


def tax_model(annual_income):
    tax_table_income = {1: [0, 18200],
                2: [18201, 37000],
                3: [37001, 90000],
                4: [90001, 180000],
                5: [180001, 1000000000]}   # ridiculous upper limit

    tax_table_paymt = {1: [0, 0],
                    2: [0.19, 0],
                    3: [0.325, 3572],
                    4: [0.37, 20797],
                    5: [0.45, 54097]}

    for key, value in tax_table_income.items():
        # print(key, value)
        if value[0] <= annual_income <= value[1]:
            # print(key)
            # print(f'Tax rate to pay on the dollar over ${value[0]} is ${tax_table_paymt[key][0]} with lump sum ${tax_table_paymt[key][1]}')
            tax_to_pay = tax_table_paymt[key][1] + tax_table_paymt[key][0] * (annual_income-tax_table_income[key][0])
            # print(f'Required to pay income tax of: ${tax_to_pay:0.0f}')
           
    monthly_income_tax = tax_to_pay / 12
    
    return monthly_income_tax


def super_model(model_phase, annual_income, monthly_super_contrib, initial_super_bal, cumulative_super_bal, cumulative_super_val):
    """
    Assumes super annuation is run via an institution and is not self managed
    """
    
    # TODO CONVERT ALL INFORMATION TO TODAYS DOLLARS AS PER THE ASSUMPTIONS ON: https://www.moneysmart.gov.au/tools-and-resources/calculators-and-apps/superannuation-calculator
    
    # Monthly Contribution from Employer.
    if model_phase == 1:
        # Earned Income is active and employer is contributing
        contrib_rate = 0.095    # % p.a.
        monthly_super_contrib = (annual_income * contrib_rate) / 12
    
    # Deductions - Insurance, Administration and investment fees, etc.
    admin_fee = (100 / 12) # $100 p.a. administration fee
    investment_fee = (0.01 / 12) * cumulative_super_bal # 1% investment fee p.a.
    if model_phase == 1:
        contrib_fee = (0.01 / 12) * cumulative_super_bal # 1% contribution fee p.a.
    else:
        contrib_fee = 0
    insurance_premium = 0
    indirect_costs = (0.002 / 12) * cumulative_super_bal # Indirect unforeseen costs 0.2% p.a.
    super_fees = admin_fee + investment_fee + contrib_fee + insurance_premium + indirect_costs
    
    if model_phase == 1:
        # Returns - cumulative value of superannuation
        if cumulative_super_bal == 0:
            cumulative_super_val += monthly_super_contrib + initial_super_bal
            print('in bal = 0 loop, cum_val: ', cumulative_super_val)
        else:
            cumulative_super_val = (cumulative_super_val + monthly_super_contrib - super_fees) * (1 + (0.06 / 12)) # 8% return p.a.
            # cumulative_super_val + monthly_super_contrib
            
        # Cumulative Contributions to super
        if cumulative_super_bal == 0:
            # Adds initial balance to monthly super balance
            cumulative_super_bal += monthly_super_contrib + initial_super_bal
        else:
            # if initial balance is added, just add new contributions
            cumulative_super_bal += monthly_super_contrib - super_fees
        
            
        return monthly_super_contrib, cumulative_super_bal, super_fees, cumulative_super_val


    # Drawdown for Phase 2
    if model_phase == 2:
        retirement_income = 100000
        drawdown_amt = retirement_income / 12
        monthly_super_contrib = 0
        cumulative_super_val = (cumulative_super_val - drawdown_amt - super_fees) * (1 + (0.06 / 12))
        if cumulative_super_val < 0:
            # Superannuation has been depleted
            drawdown_amt = 0
            cumulative_super_val = 0
            super_fees = 0
            
        return monthly_super_contrib, cumulative_super_bal, super_fees, cumulative_super_val, drawdown_amt


def expenses_model(model_phase):
    
    if model_phase == 1:
        expenses = 1000*np.random.uniform(0.75, 1.25)
        return expenses
    if model_phase == 2:
        expenses = 500*np.random.uniform(0.75, 1.25)
        return expenses


def loan_model(principal, interest_rate, annual_payments, years, period, pmt, begin_balance, end_balance):
    
    # TODO: integrate additional payment functionality into this model per https://pbpython.com/amortization-model-revised.html model
          
    if 0 < end_balance: 
        interest = round((interest_rate/annual_payments * begin_balance), 2)
        
        pmt = min(pmt, begin_balance + interest)
        principal = pmt - interest
        
        end_balance = begin_balance - principal
        
        period += 1
        begin_balance = end_balance
        
    return period, begin_balance, pmt, interest
    

def phase_model(start_date, start_annual_income):
    
    # TODO: integrated model types into phase model
    # model_type = conservative, chaotic, etc.
    
    # TODO: Pass date into models to do date specific logic...
    
    
    # LOAN INIT DETAILS
    principal = 350000
    interest_rate = 0.04
    annual_payments = 12
    years = 25
    period = 1
    pmt = -round(np.pmt(interest_rate/annual_payments, years*annual_payments, principal), 2)
    begin_balance = principal
    end_balance = principal
    
    # SUPER INIT DETAILS
    initial_super_bal = 35000
    monthly_super_contrib = 0
    cumulative_super_bal = 0
    cumulative_super_val = 0
    
    # PHASE 1
    temp_dt_p1 = start_date # init
    
    while temp_dt_p1 <= end_date_p1:
        model_phase = 1
        
        # EARNED INCOME & TAX
        monthly_income = start_annual_income / 12
        monthly_income_tax = tax_model(start_annual_income)
        
        # SUPERANNUATION
        monthly_super_contrib, cumulative_super_bal, super_fees, cumulative_super_val = super_model(model_phase, start_annual_income, monthly_super_contrib, initial_super_bal, cumulative_super_bal, cumulative_super_val)
        
        # LIVING EXPENSES
        monthly_expenses = expenses_model(model_phase)
        
        # LOAN (MORTGAGE)
        period, begin_balance, pmt, interest = loan_model(principal, interest_rate, annual_payments, years, period, pmt, begin_balance, end_balance)
    
        yield OrderedDict([('Date', temp_dt_p1), 
                           ('Model_Phase', model_phase),
                           ('Earned_Income', monthly_income),
                           ('Earned_Income_Tax', monthly_income_tax),
                           ('Employer_Super_Contrib', monthly_super_contrib),
                           ('Super_Balance_Contrib', cumulative_super_bal),
                           ('Super_Fees', super_fees),
                           ('Super_Balance_Value', cumulative_super_val),
                           ('Expenses', monthly_expenses),
                           ('Loan_Period', period),
                           ('Loan_Begin_Balance', begin_balance),
                           ('Loan_Payment', pmt),
                           ('Loan_Interest', interest)])
    
        temp_dt_p1 += relativedelta(months=1)

    # PHASE 2
    temp_dt_p2 = end_date_p1    # init
    while temp_dt_p2 <= end_date_p2:
        model_phase = 2
        
        monthly_expenses = expenses_model(model_phase)
        
        monthly_super_contrib, cumulative_super_bal, super_fees, cumulative_super_val, drawdown_amt = super_model(model_phase, start_annual_income, monthly_super_contrib, initial_super_bal, cumulative_super_bal, cumulative_super_val)
        
        yield OrderedDict([('Date', temp_dt_p2), 
                           ('Model_Phase', model_phase),
                           ('Expenses', monthly_expenses),
                           ('Super_Fees', super_fees),
                           ('Super_Balance_Value', cumulative_super_val),
                           ('Super_Drawdown', drawdown_amt)
                           ])
        
        temp_dt_p2 += relativedelta(months=1)


def agg_function(df):
    
    # print(df.columns)
    # Replace NaNs with 0s
    df.fillna(0, inplace=True)
    df['Disposable_Income'] = df['Earned_Income'] + df['Super_Drawdown'] - df['Expenses'] - df['Loan_Payment']

    return df

def main(): 
    
    df = pd.DataFrame(phase_model(start_date, income))
    # Aggregation calculations are done after monthly models are generated...
    df = agg_function(df)

    # FOR DEBUGGING
    print(df.head(12))
    print(df.tail(12))
    
    plt.subplot(211)
    plt.plot(df['Date'], df['Super_Balance_Value'])

    plt.ylabel('$')
    plt.title('Super Balance')
    plt.subplot(212)
    plt.plot(df['Date'], df['Disposable_Income'])
    plt.xlabel('Date')
    plt.ylabel('$')
    plt.title('Disposable Income')
    plt.show()


if __name__ == '__main__':
    print('Running in main')
    main()
