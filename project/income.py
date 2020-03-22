"""
Income: The Income class is used for generating cash flow for users. 
        Income is determined by three means (as defined by various financial institutions): 1. earned, 2. passive, and 3. portfolio.
"""


class Income():
    """
    Model for income (earned, passive, portfolio).
    """
    
    def __init__(self, income):
        """
        
        """
        
        # Everything is on a monthly basis in the model...
        self.income = income
        self.remainingIncome = self.income    # init
        self.dateHistory = []
        self.incomeHistory = []

        
    def incomeAfterCosts(self, loanPaymentSum):
        """
        Aggregated Monthly.
        """
        costs = loanPaymentSum
        self.remainingIncome = self.income - costs
        
    def getIncomeHistory(self, date, incomeInfo):
        """
        Used to capture temporal data for plotting and analysis.
        """
        self.dateHistory.append(date)
        self.incomeHistory.append(incomeInfo)
        
if __name__ == '__main__':
    pass