"""
Superannuation: The Superunnuation class is used for capturing superannuation acquisition over time. 
Factors that are integrated into this class include: 1. super contributions (monthly freq), 2. initial balance, 3. rate of return, 4. employer contribution rate, 
5. fees (administration and investment), 6. insurance premiums, and 7. indireect costs that aren't captured within these buckets.
"""


class Superannuation():
    """
    Note: Assumes superannuation is run via an institution and is not self managed.
    
    """
    
    def __init__(self, contribRate):
        self.superContrib = 0
        self.superInitialBal = 1000   # initial super balance
        self.superReturnRate = 0.06 / 12
        
        self.contribRate = contribRate   # Employer contribution rate
        
        # Cumulative Sum of Super Balance and Value
        self.superBalCumSum = 0
        self.superValCumSum = 0
        
    def superFees(self, phase):
        if phase == 1:
            # phase 1 - before retirement
            self.contribFee = 1/12
        if phase == 2:
            # phase 2 - retirement
            self.contribFee = 0
        self.adminFee = 100
        self.investmentFee = 1/12
        self.insurancePrem = 1/12
        self.indirectCosts = 0.2/12
        self.superFeesTotal = 0
        
        self.superFeesTotal = self.adminFee + self.investmentFee * self.superContrib + \
                            self.contribFee * self.superContrib + self.insurancePrem * self.superContrib + \
                            self.indirectCosts * self.superContrib
#         print(f'Super Fees: ${self.superFeesTotal:0.2f}')
        
    def superValue(self, phase):
        
        if self.superBalCumSum == 0:
#             print('adding initial value to superVal')
            self.superValCumSum += self.superContrib + self.superInitialBal
        elif phase == 1:
#             print(f'{self.superValCumSum}-{self.superContrib}-{self.superFeesTotal}-{1 + self.superReturnRate}')
            self.superValCumSum = (self.superValCumSum + self.superContrib - self.superFeesTotal) * (1 + self.superReturnRate)
        elif phase == 2:
            self.superValCumSum = (self.superValCumSum - self.drawdownAmt - self.superFeesTotal) * (1 + self.superReturnRate)
        
#         print(f'Super Value: ${self.superValCumSum:0.2f}')
        
        
    def superBalance(self):
        
        if self.superBalCumSum == 0:
#             print('adding initial value to superBal')
            self.superBalCumSum += self.superContrib + self.superInitialBal
        else:
            self.superBalCumSum += self.superContrib - self.superFeesTotal
        
#         print(f'Super Balance: ${self.superBalCumSum:0.2f}')
        
    def superContribution(self, phase, income):
        # Monthly income...
        self.superContrib = self.contribRate * income
#         print(f'Super Contribution: ${self.superContrib:0.2f}')
        
        self.superFees(phase)
        self.superValue(phase)
        self.superBalance()
        
        
    def superDrawDown(self):
        # Drawdown once retirement starts and contributions cease
        retirementIncome = 25000
        self.drawdownAmt = retirementIncome / 12
        
        self.superContribution(2, 0)   # no income within phase 2
        
if __name__ == '__main__':
    pass