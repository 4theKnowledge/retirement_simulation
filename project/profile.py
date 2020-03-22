"""
Profile:The Profile class is for generating user profiles. 
        A user profile can have the previously defined classes attributed to it e.g. income, expenses, savings, tax, superannuations, and asset value. 
        A user profile is simulated over a lifetime, the lifetime is split into two phases 1. working, and 2. retirement. 
        In the first phase, working, the user typically would take out loans, have income, commit to superannuation, etc. 
        In the second phase, retirement, the income streams change, superannuation starts to be drawn down, etc. 
        Parameters of the user profile include 1. name, 2. age, 3. expected retirement age (will be an output rather than an input in the future), 
        and 4. expected age of death (assumed from health statistics based on gender; could be extended based on other salient factors).

"""

from income import Income
from expenses import Expenses
from savings import Savings
from tax import Tax
from superannuation import Superannuation
from asset_value import AssetValue
from education import Education
from loan import Loan
from earnings import Earnings


class Profile(Income, Expenses, Savings, Tax, Superannuation, AssetValue, Education, Earnings):
    """
    Profile for user. Contains their general information and meta data for financial modeling.
    """
    
    # Initializer / Instance Attributes
    def __init__(self, name, age, retireAge, deadAge, incomePA, expensesPM, proportionSaved):
        self.name = name
        self.age = age
        self.retireAge = retireAge
        self.deadAge = deadAge
        
        # Education
        # Currently does not take user input and is hard coded in the Education Class initialisation...
        
       
        # Loans
        self.hasLoan = False
        self.loanDict = {}
        self.noLoans = 0
        self.loanPaymentSum = 0

        # Earnings
        

        # Income
        self.hasIncome = False
        self.incomePA = incomePA
        self.income = self.incomePA / 12
        self.hasIncome = True
        
        # Expenses
        self.expenses = expensesPM    # Expenses per month
        
        # Savings
        self.proportionSaved = proportionSaved

        
        # Inherit Loan init.. by inheriting this class, we can access it's attributes and methods...
        Income.__init__(self, self.income)  # pass attribute to class
        
        # Init Expenses
        Expenses.__init__(self, self.expenses)
        
        
        # Init Savings
        Savings.__init__(self, self.proportionSaved)
        
        # Init Tax
        Tax.__init__(self)
        
        # Init super
        Superannuation.__init__(self, 0.095)
        
        # Init asset value
        AssetValue.__init__(self, 0.06)
        
        # Init Education 
        Education.__init__(self)
        
        # Init Earnings
        Earnings.__init__(self, self.eduLevel, self.age, self.retireAge)
        
        
    # Profile
    def ageStep(self, year):
        """
        Used to age the users profile and step through time.
        """
        self.age += year
    
    def summary(self):
        print(f'{self.name} is {self.age} years old and has an income of ${self.income:0.2f} per month.\n')
    
    # Loan
    def getLoan(self, principal, interestRate, annualPayments, duration, startDate, loanPaymentExtra):
        """
        Allocates a loan to the profile.
        """
        
        self.hasLoan = True
        self.noLoans += 1
#         print(f'Number of loans: {self.noLoans}')
        loanID = str(self.noLoans)
        self.loanDict[loanID] = Loan(loanID, principal, interestRate, annualPayments, duration, startDate, loanPaymentExtra)
        
    def removeLoan(self, loanID):
        """
        Removes a loan from the profile. TODO: update to remove once paid off.
        """
        try:
            del self.loanDict[loanID]
        except:
            print('Loan doesnt exist')
            
    def loanDesc(self):
        """
        Summary of active loans.
        """
        self.currentLoans = len(self.loanDict)
        try:
            return f'Current active loans for {self.name}: {self.currentLoans}'
        except:
            return f'{self.name} has no loan'
        
    def loanInfo(self):
        """
        Detailed description of loan dict. For debugging purposes.
        """
        for loanID, loanDetails in self.loanDict.items():
            print(f'{loanDetails.initDesc()}')