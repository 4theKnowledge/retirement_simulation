"""
Simple taxable income model.

Assumptions:
- Income is constant each month

I/O:
- Model takes in gross income and returns gross, net and tax per month

Ref: https://www.ato.gov.au/Rates/Individual-income-tax-rates/
"""


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

taxable_income = 190000

for key, value in tax_table_income.items():
    # print(key, value)
    if value[0] <= taxable_income <= value[1]:
        print(key)
        print(f'Tax rate to pay on the dollar over ${value[0]} is ${tax_table_paymt[key][0]} with lump sum ${tax_table_paymt[key][1]}')
        tax_to_pay = tax_table_paymt[key][1] + tax_table_paymt[key][0] * (taxable_income-tax_table_income[key][0])
        print(f'Required to pay income tax of: ${tax_to_pay:0.0f}')