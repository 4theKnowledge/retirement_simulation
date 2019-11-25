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
    #           Also, shift interest calc to be on the last months value not the same months value as this is more realistic.
    
    
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
            # print('in bal = 0 loop, cum_val: ', cumulative_super_val)
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


def expenses_model(model_phase, cumulative_savings_val, monthly_disposable_income, begin_balance):
    """
    Emulates general expenses in both phases 1 and 2. It is assumed that expenses reduce by 50% within retirement.
    Functionality for random events to occur are added. These occur at a cost of 10x the expected expense within that month with
    a very low probability of occurence over the model timeline. The disposable income is tested to see if it can absorb the event, otherwise the savings model is used to buffer these random events, if the savings
    is not sufficient then a loan is automatically generated to cover the difference (current dev just adds to existing loan principal...) (if allowed; theres a selection for loan generation or family/friend buffer for certain amounts)
    
    Note: the disposable income accessible is from the previous month... similarly for the cum sum savings
    """
    
    random_event = True
    
    if model_phase == 1:       
        if random_event and np.random.uniform(0,1) < 0.01:
            expenses = 2000*np.random.uniform(0.75, 1.25)
            expenses_re = expenses*np.random.randint(3, 30)
            expenses += expenses_re
            if monthly_disposable_income > expenses:
                print(f'Phase 1: Absorbing expenses of {expenses} into disposable income')
                return expenses, cumulative_savings_val, begin_balance
            if monthly_disposable_income < expenses < cumulative_savings_val:
                print(f'Phase 1: Paying expenses of {expenses} with savings')
                cumulative_savings_val -= expenses_re
                expenses_re = 0
                expenses += expenses_re
                return expenses, cumulative_savings_val, begin_balance
            if cumulative_savings_val < expenses:
                print(f'Phase 1: Absorbing expenses of {expenses} by adding to existing loan principal')
                begin_balance += expenses_re
                expenses_re = 0
                expenses += expenses_re
                return expenses, cumulative_savings_val, begin_balance
        else:
            # if RE is false or doesn't meet above criteria...
            expenses = 2000*np.random.uniform(0.75, 1.25)
            return expenses, cumulative_savings_val, begin_balance
    
    if model_phase == 2:
        if random_event and np.random.uniform(0,1) < 0.01:
            expenses = 1000*np.random.uniform(0.75, 1.25)
            expenses_re = expenses*np.random.randint(3, 15)
            expenses += expenses_re
            if monthly_disposable_income > expenses:
                print(f'Phase 2: Absorbing expenses of {expenses} into disposable income')
                return expenses, cumulative_savings_val, begin_balance
            if monthly_disposable_income < expenses <= cumulative_savings_val:
                print(f'Phase 2: Paying expenses of {expenses} with savings')
                cumulative_savings_val -= expenses_re
                expenses_re = 0
                expenses += expenses_re
                return expenses, cumulative_savings_val, begin_balance
            if cumulative_savings_val < expenses:
                # TODO: Phase 2 would generate a new loan or tap their superannuation if a loan doesn't exist
                print(f'Phase 2: Absorbing expenses of {expenses} by adding to existing loan principal')
                
                begin_balance += expenses_re
                expenses_re = 0
                expenses += expenses_re
                return expenses, cumulative_savings_val, begin_balance
                
        else:
            # if RE is false or doesn't meet above criteria...
            expenses = 1000*np.random.uniform(0.75, 1.25)
            return expenses, cumulative_savings_val, begin_balance

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
    

def saving_model(model_phase, initial_savings_bal, monthly_disposable_income, cumulative_savings_bal, cumulative_savings_val):
    """
    Research into best % saving recommendations
    """
    
    
    # Amount saved per month
    if model_phase == 1:
        saving_proportion = 0.25    # 25 %
        monthly_saved_amt = saving_proportion * monthly_disposable_income
    else:
        # TODO: REVISE THIS LOGIC TO SEE IF IT MAKES SENSE TO ALLOW FOR PHASE 2
        monthly_saved_amt = 0

    # Interest earned on savings
    if cumulative_savings_bal == 0:
        cumulative_savings_val += monthly_saved_amt + initial_savings_bal
        # print('in bal = 0 loop, cum_val: ', cumulative_savings_val)
    else:
        cumulative_savings_val = (cumulative_savings_val + monthly_saved_amt) * (1 + (0.03 / 12)) # 3% return p.a. assumes term deposit
    
    # Cumulative savings
    if cumulative_savings_bal == 0:
        cumulative_savings_bal += monthly_saved_amt + initial_savings_bal
    else:
        cumulative_savings_bal += monthly_saved_amt
    
    return  monthly_saved_amt, cumulative_savings_bal, cumulative_savings_val
    
    
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
    cumulative_super_bal = 0  # w/o compound interest
    cumulative_super_val = 0  # w/ compound interest 
    
    # SAVINGS INIT DETAILS
    initial_savings_bal = 5000
    cumulative_savings_bal = 0  # w/o compound interest
    cumulative_savings_val = 0  # w/ compound interest
    monthly_disposable_income = 0   # init
    
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
        monthly_expenses, cumulative_savings_val, begin_balance = expenses_model(model_phase, cumulative_savings_val, monthly_disposable_income, begin_balance)
        
        # LOAN (MORTGAGE)
        period, begin_balance, pmt, interest = loan_model(principal, interest_rate, annual_payments, years, period, pmt, begin_balance, end_balance)
    
        # DISPOSABLE INCOME
        # print(monthly_income, monthly_expenses, pmt)
        monthly_disposable_income = monthly_income - monthly_expenses - pmt
        
        # SAVINGS
        monthly_saved_amt, cumulative_savings_bal, cumulative_savings_val = saving_model(model_phase, initial_savings_bal, monthly_disposable_income, cumulative_savings_bal, cumulative_savings_val)

        yield OrderedDict([('Date', temp_dt_p1), 
                           ('Model_Phase', model_phase),
                           ('Earned_Income', monthly_income),
                           ('Earned_Income_Tax', monthly_income_tax),
                           ('Employer_Super_Contrib', monthly_super_contrib),
                           ('Super_Balance_Contrib', cumulative_super_bal),
                           ('Super_Fees', super_fees),
                           ('Super_Balance_Value', cumulative_super_val),
                           ('Super_Drawdown', 0),
                           ('Expenses', monthly_expenses),
                           ('Loan_Period', period),
                           ('Loan_Begin_Balance', begin_balance),
                           ('Loan_Payment', pmt),
                           ('Loan_Interest', interest),
                           ('Disposable_Income', monthly_disposable_income),
                           ('Amount_Saved', monthly_saved_amt),
                           ('Savings_Bal', cumulative_savings_bal),
                           ('Savings_Val', cumulative_savings_val)])
    
        temp_dt_p1 += relativedelta(months=1)

    # PHASE 2
    temp_dt_p2 = end_date_p1    # init

    # SAVINGS INIT
    initial_savings_bal = 0 # no more savings at start of retirement phase

    while temp_dt_p2 <= end_date_p2:
        model_phase = 2
        
        # EXPENSES
        monthly_expenses, cumulative_savings_val, _ = expenses_model(model_phase, cumulative_savings_val, monthly_disposable_income, begin_balance)
        
        # SAVINGS
        monthly_saved_amt, cumulative_savings_bal, cumulative_savings_val = saving_model(model_phase, initial_savings_bal, monthly_disposable_income, cumulative_savings_bal, cumulative_savings_val)
        
        # SUPER DRAWDOWN
        monthly_super_contrib, cumulative_super_bal, super_fees, cumulative_super_val, drawdown_amt = super_model(model_phase, start_annual_income, monthly_super_contrib, initial_super_bal, cumulative_super_bal, cumulative_super_val)
        
        # DISPOSABLE INCOME
        monthly_disposable_income = drawdown_amt - monthly_expenses
               
        yield OrderedDict([('Date', temp_dt_p2), 
                           ('Model_Phase', model_phase),
                           ('Earned_Income', 0),
                           ('Earned_Income_Tax', 0),
                           ('Employer_Super_Contrib', 0),
                           ('Super_Balance_Contrib', 0),
                           ('Super_Fees', super_fees),
                           ('Super_Balance_Value', cumulative_super_val),
                           ('Super_Drawdown', drawdown_amt),
                           ('Expenses', monthly_expenses),
                           ('Loan_Period', 0),
                           ('Loan_Begin_Balance', 0),
                           ('Loan_Payment', 0),
                           ('Loan_Interest', 0),
                           ('Disposable_Income', monthly_disposable_income),
                           ('Amount_Saved', 0),
                           ('Savings_Bal', cumulative_savings_bal),
                           ('Savings_Val', cumulative_savings_val)])
        temp_dt_p2 += relativedelta(months=1)


def main(): 
    
    df = pd.DataFrame(phase_model(start_date, income))
    # Aggregation calculations are done after monthly models are generated...
    # df = agg_function(df)
    df.to_csv('simulation_results.csv', index=False)

    # FOR DEBUGGING
    print(df.head(12))
    print(df.tail(12))
    
    plt.subplot(511)
    plt.plot(df['Date'], df['Super_Balance_Value'])
    plt.ylabel('$')
    plt.title('Super Balance')
    
    plt.subplot(512)
    plt.plot(df['Date'], df['Savings_Val'])
    plt.ylabel('$')
    plt.title('Savings')
    
    plt.subplot(513)
    plt.plot(df['Date'], df['Loan_Begin_Balance'])
    plt.ylabel('$')
    plt.title('Loan Principal')
    
    plt.subplot(514)
    plt.plot(df['Date'], df['Super_Drawdown'])
    plt.ylabel('$')
    plt.title('Super Drawdown')
    
    plt.subplot(515)
    plt.plot(df['Date'], df['Disposable_Income'])
    plt.xlabel('Date')
    plt.ylabel('$')
    plt.title('Disposable Income')
    plt.show()


if __name__ == '__main__':
    print('Running in main')
    main()