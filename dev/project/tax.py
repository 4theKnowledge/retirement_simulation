"""
Tax: The Tax class is used to calculate payable tax on taxable income in accordance with tax rates set by the Australian Tax Office (ATO).

"""

class Tax():
    """
    Model for taxing income.
    Calculates tax on gross annual income.
    Note: Tax rates are current as of 2019-2020 and sourced from the ATO.
    """
    
    def __init__(self):
        self.tax_table_income = {1: [0, 18200],
                    2: [18201, 37000],
                    3: [37001, 90000],
                    4: [90001, 180000],
                    5: [180001, 1000000000]}   # ridiculous upper limit

        self.tax_table_paymt = {1: [0, 0],
                        2: [0.19, 0],
                        3: [0.325, 3572],
                        4: [0.37, 20797],
                        5: [0.45, 54097]}
    
    def getTaxAmount(self, income):
        
        income = income * 12 # input is per month...
        
        for key, value in self.tax_table_income.items():
            if value[0] <= income <= value[1]:
                tax_to_pay = self.tax_table_paymt[key][1] + self.tax_table_paymt[key][0] * \
                (income - self.tax_table_income[key][0])
                
        monthlyIncomeTax = tax_to_pay / 12
        
        return monthlyIncomeTax
    
    
if __name__ == '__main__':
    pass