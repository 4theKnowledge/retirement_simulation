"""
Loan: The Loan class captures loans and their attributes. 
    Attributes include: 1. principal, 2. interest rate, 3. annual payments, 4. duration, and 5. startdate. 
    Loans are an important factor in user simulation as they can be stackable (have more than one at a time).<br><br>

Note: This model should be referenced against typical mortgage qualifiers such as requiring a certain deposit % before being allowed a mortgage. 
Wheras personal loans like cars can have anything given a certain asset value is there. If this isn't met then the loan is pushed into the future until this is reached.
"""

import datetime
from dateutil.relativedelta import relativedelta
import numpy as np

class Loan():
    """
    Model for user profile loans.
    """
    
    def __init__(self, loanID, principal, interestRate, annualPayments, duration, startDate, loanPaymentExtra):
        self.principal = principal
        self.interestRate = interestRate
        self.annualPayments = annualPayments
        self.duration = duration
        self.startDate = datetime.datetime.strptime(startDate, '%d-%m-%Y').date()
        self.loanID = loanID
        self.period = 1
        self.endDate = (self.startDate + relativedelta(years=self.duration))
        self.beginBalance = self.principal
        self.endBalance = self.principal
        self.loanPaidOff = False
        self.loanPaidOffDate = 'Not paid off - Active'
        self.loanActive = False
        self.loanPaymentExtra = loanPaymentExtra
        self.loanPaymentMinimum = -round(np.pmt(self.interestRate/self.annualPayments, self.duration*self.annualPayments, self.principal), 2)
        
        # First loan payment amount
        # Note: loanPaymentExtra is a nominal payment that is added to the minimum loan service amount.
        self.loanPayment = self.loanPaymentExtra + self.loanPaymentMinimum
            
        # For data capture
        self.dateHistory = []
        self.loanHistory = []
    
    def initDesc(self):
        return f'''Loan {self.loanID} has principal of ${self.principal} over duration {self.duration} years with expected finish date of {self.endDate} - remaining balance: ${self.endBalance} - Minimum payment amount: ${self.loanPaymentMinimum}'''
    
    # Main Functions
    def makePayment(self):
        """
        Make a payment against the principal.
        """
        self.loanActive = True
        self.interest = round(((self.interestRate/self.annualPayments) * self.beginBalance), 2)
        self.loanPayment = min(self.loanPayment, self.beginBalance + self.interest)
        self.endBalance = self.beginBalance - (self.loanPayment - self.interest)
        self.period += 1
        self.beginBalance = self.endBalance
        
    def paymentSummary(self):
        try:
            print(f'Period: {self.period} BeginBalance: {self.beginBalance:0.2f} Principal: {self.principal:0.2f} Interest: {self.interest:0.2f} Payment: {self.loanPayment:0.2f}')
        except:
            print('Not enough information. Loan has likely not become active.')

    def loanFinished(self, date):
        """
        Used when a loan is finished.
        """
        #TODO: Add date for when loan finishes... as this may not be constant...
        self.loanPaidOff = True
        self.loanActive = False
        self.loanPaidOffDate = date
    
    # Misc Functions
    def increasePrincipal(self, increaseAmt):
        """
        Increase the amount of loan principal via month begin balance.
        """
        self.beginBalance += increaseAmt
        
    def increasePrincipalRandomly(self):
        """
        Increase principal by a random amount to simulate expense tranfers.
        This can only occur if the loan is still active. 
        TODO: integrate expenses and ability for profile to override 'active' status to ressurect their paid off loans...
        """
        if (0.99 < np.random.uniform(0,1)) and self.loanActive:
            if self.loanPaidOff == False:
                increaseAmt = np.random.randint(0,10)*1000
                self.beginBalance += increaseAmt
#                 print(f'Increased {self.loanID} balance by ${increaseAmt}')
        
    # Data Capture Functions
    def getLoanHistory(self, date, loanInfo):
        """
        Used to capture temporal data for plotting and analysis.
        """
        self.dateHistory.append(date)
        self.loanHistory.append(loanInfo)
        
        
if __name__ == '__main__':
    pass