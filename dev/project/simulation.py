"""
Simulation: The simulation class is used for simulating user lifetimes for stochastic modeling and analysis.
"""

from profile import Profile
from tqdm import tqdm
import pandas as pd
import datetime
import logging
logging.basicConfig(filename=f'logs/simulation_{datetime.datetime.now().strftime("%d-%m-%y_%H-%M")}.log', level=logging.DEBUG)
from collections import OrderedDict
from dateutil.relativedelta import relativedelta


class Simulation(Profile):
    """
    Simulation class. Used for simulation functions and data capture.
    """
        
    def init_user_profile(self):
        """
        Initialises a user profile for simulation.
        """
        
        # Initialise Profile class
        self.userProfile = Profile(self.name, self.age, self.retireAge, self.deadAge, self.incomePA, self.expenses, self.proportionSaved)

        # Initialise loans and attribute them to the user profile
        for loan in self.data_dict['loanDetails']:
            self.userProfile.getLoan(self.data_dict['loanDetails'][loan]['principal'],
                                     self.data_dict['loanDetails'][loan]['interestRate'],
                                     self.data_dict['loanDetails'][loan]['annualPayments'],
                                     self.data_dict['loanDetails'][loan]['duration'],
                                     self.data_dict['loanDetails'][loan]['startDate'],
                                     self.data_dict['loanDetails'][loan]['loanPaymentExtra'])
    
    def __init__(self, data_dict):
        """
        Intialisation of the simulation model
        """
        
        self.data_dict = data_dict   # holds simulation and profile information.
        
        # Init Profile
        Profile.__init__(self, self.data_dict['profileDetails']['name'], self.data_dict['profileDetails']['age'], \
                         self.data_dict['profileDetails']['retireAge'], self.data_dict['profileDetails']['deadAge'], \
                         self.data_dict['profileDetails']['incomePA'], self.data_dict['profileDetails']['expensesPM'], \
                         self.data_dict['profileDetails']['proportionSaved'])
        # Initialise profile for simulation
        self.init_user_profile()
    
    
    def simulate_one_step(self):
        """
        Simulates the financial situation of a user for one month.
        """
        # Duration of simulation (phase 1)
        dateStart = datetime.date(2020,1,1)
        dateStartTemp = dateStart

        # Iterate over life with month level granularity
        # Phase One - Working life
        logging.info('ENTERING PHASE ONE')

        while self.userProfile.age < self.userProfile.retireAge:
            # Current datetime of step
            logging.debug(f'Current DateTime: {dateStartTemp}')
            logging.debug(f'Monthly Income: ${self.userProfile.income:0.2f}')
            
            # Update earnings
            self.userProfile.employmentTransition() # Make a transition 
            logging.debug(f'Employement Status: {self.userProfile.employed} - Months of tenure: {self.userProfile.tenure} - Current Unemployment Risk: {self.userProfile.eduRiskLevel*100:0.2f}% - Current Earning (PA): ${self.userProfile.currentIncomePA:0.2f}')
            

            # Tax
            # Get taxable amount from income
            tax = self.userProfile.getTaxAmount(self.userProfile.income)
            logging.debug(f'Tax: ${tax:0.2f}')

            # Super
            # Contribute to superannuation from income
            self.userProfile.superContribution(1, self.userProfile.income)

            tempLoanCost = 0

            # Pay debts
            # An aggregation of loan costs is computed here over all active loans
            for loanID, loanInfo in self.userProfile.loanDict.items():    # Iterate through loans associated to the profile

                # If the start date of the loan of interest is before the current time stamp, calculate loan payment or make loan inactive if it's finished.
                if self.userProfile.loanDict[loanID].startDate <= dateStartTemp:

                    # TESTING: This step is currently simulating random increases to loan principal.
                    # This is used to emulate when income goes below zero and loans need to be increased to make up the difference.
                    # This only works if there are active loans, if no loan is active then another method for re-activating or creating a new loan need to be developed.
                    # NEED TO CONFIRM THAT THIS ISNT ATTRIBUTING EXTRA PRINCIPAL TO ALL LOANS... ONE MAY BE ENOUGH.
                    self.userProfile.loanDict[loanID].increasePrincipalRandomly()

                    # If balance remains on loans - make payment
                    if 0 < self.userProfile.loanDict[loanID].beginBalance:
                        # Raise payment against loan
                        self.userProfile.loanDict[loanID].makePayment()
                        # Print payment summary to console
#                         self.userProfile.loanDict[loanID].paymentSummary()    # shows summary of loan to console

                        # Capture loan history information for future analytics
                        self.userProfile.loanDict[loanID].getLoanHistory(dateStartTemp, self.userProfile.loanDict[loanID].beginBalance)

                        # If the loan payment makes the balance zero, make the loan in-active as it's paid off
                        if self.userProfile.loanDict[loanID].beginBalance == 0:
                            logging.debug(f'LOAN {loanID} PAID OFF!')
                            # Set loanFinished to True
                            self.userProfile.loanDict[loanID].loanFinished(dateStartTemp)

                        # Loan is not paid off but persists for the next period
                        else:
                            # Capture loanPayment for totalcost aggregation
#                             self.userProfile.loanDict[loanID].paymentSummary()    # shows summary of loan to console
                            
    #                         print(f'Loan {loanID} - Begin Balance: ${self.userProfile.loanDict[loanID].beginBalance:0.2f} Payment: {self.userProfile.loanDict[loanID].loanPayment:0.2f}')
    #                         logging.debug(f'Loan {loanID} - Begin Balance: ${self.userProfile.loanDict[loanID].beginBalance:0.2f} Payment: {self.userProfile.loanDict[loanID].loanPayment:0.2f}')
                            tempLoanCost += self.userProfile.loanDict[loanID].loanPayment

                    # No principal - either loan hasnt begun or its finished
                    else:
                        self.userProfile.loanDict[loanID].getLoanHistory(dateStartTemp, 0)

                # Too early - no loans are active
                else:
                    self.userProfile.loanDict[loanID].getLoanHistory(dateStartTemp, 0)
                    pass

            # Expenses
            # Currently randomly increasing expenses to emulate randomness
            # This has logic based on the phase of the user and some other salient information
            expenses =  self.userProfile.increaseExpenseRandomly(1)
            

            # Calculate income remaining after costs attributed to tax, expenses, etc.
            self.userProfile.incomeAfterCosts(tax + tempLoanCost + expenses)
            logging.debug(f'Income Remaining: ${self.userProfile.remainingIncome:0.2f}')
            # Capture income history for future analysis
            self.userProfile.getIncomeHistory(dateStartTemp, self.userProfile.remainingIncome)
            
            
            # If the amount of disposable income cannot service the loans and expenses, then 1. don't save any money.
            # If there is still not enough money, draw it out of savings...
            # NOTE: obviously there are lots of ways this deficiency can be tackled...
            if (self.userProfile.income - tax) < (tempLoanCost + expenses):
                savedAmt = self.userProfile.getSavedAmount(self.userProfile.remainingIncome)
                
                # capture savings history
                self.userProfile.getSavingHistory(dateStartTemp, savedAmt)
                
            else:
                # Savings
                # Calculate savings based on remaining income (can't save what you don't have)
                savedAmt = self.userProfile.getSavedAmount(self.userProfile.remainingIncome)
                logging.debug(f'Amount saved this month: ${savedAmt:0.2f}')
                
                # capture savings history
                self.userProfile.getSavingHistory(dateStartTemp, savedAmt)

            # Note: if more draw downs occur on the remaining income, then the savings need to be subtracted explicitly aswell.
            # As this is not the case, it doesn't matter that the savings amount isn't removed from this parameter.


            # Asset value
            # Compute asset value based on compounding period and interest rates 
    #         self.userProfile.getAssetValue(self.userProfile, compoundPeriod)

            # Create an ordered dictionary of information
            yield OrderedDict([('Date', dateStartTemp),
                              ('Income', self.userProfile.income),
                              ('Tax', self.userProfile.getTaxAmount(self.userProfile.income)),
                              ('SuperContrib', self.userProfile.superContrib),
                               ('SuperBalance', self.userProfile.superBalCumSum),
                               ('SuperValue', self.userProfile.superValCumSum),
                              ('LoanDebt', tempLoanCost),
                              ('Expenses', expenses),
                              ('RemainingIncome', self.userProfile.remainingIncome),
                              ('SavedAmt', savedAmt)])

            # Steps through time another month
            dateStartTemp += relativedelta(months=1)

            # if the current month of the year is January and we're not on the first year of the simulation
            # Add another year to the users profile, e.g. age them another year.
            if dateStartTemp.month == 1 and 0 < (dateStartTemp.year - dateStart.year):
                self.userProfile.ageStep(1)
                self.userProfile.dynamicEarnings()  # compute new earnings at the end of the year e.g. raise/promotion etc

        # Iterate over life with month level granularity
        # Phase Two - Retirement
        logging.info('ENTERING PHASE TWO')

        # While the users age is less than the age of death, run the simulation
        while self.userProfile.age < self.userProfile.deadAge:
            logging.debug(f'Current DateTime: {dateStartTemp}')

            # Super drawdown
            # Draw down super as this will act as a source of income
            # Need to review how this is used...
            self.userProfile.superDrawDown()

            # Expenses
            # Expenses in the retirement phase are treated differently to the 
            # working life phase
            expenses =  self.userProfile.increaseExpenseRandomly(2)

            # Create an ordered dictionary of information
            yield OrderedDict([('Date', dateStartTemp),
                              ('Income', 0),
                              ('Tax', 0),
                              ('SuperContrib', 0),
                              ('SuperBalance', self.userProfile.superBalCumSum),
                              ('SuperValue', self.userProfile.superValCumSum),
                              ('LoanDebt', 0),
                              ('Expenses', expenses),
                              ('RemainingIncome', 0),
                              ('SavedAmt', 0)])

            # Steps through time another month
            dateStartTemp += relativedelta(months=1)

            # if the current month of the year is January and we're not on the first year of the simulation
            # Add another year to the users profile, e.g. age them another year.
            if dateStartTemp.month == 1 and (dateStartTemp.year - dateStart.year) > 0:
                self.userProfile.ageStep(1)
                
                
    def simulate(self):
        """
        Simulates a users finance over their lifetime.
        """
        return pd.DataFrame(self.simulate_one_step())
        
                
    def monte_carlo_model(self, iterations):
        """
        Runs n iterations of the user life simulation and captures results for analysis.
        """
        
        self.simulationHistory = list()
        
        # Output information pertaining to to user profile summary and loan descriptions/information
        self.userProfile.summary()
        self.userProfile.loanDesc()
        self.userProfile.loanInfo()
        
        for iteration in tqdm(range(1, iterations+1, 1)):
#             print(f'\nIteration Number: {iteration}')
            self.simulationHistory.append(self.simulate())
            
            # Need to reinitialise user profile as the profile model believes the user is dead....
            self.init_user_profile()
    

    def statistical_analysis(self):
        """
        Performs a basic statistical analysis (mean, Q25, Q50, Q75) of the Monte Carlo simulation results. 
        """
        
        # Initialise empty dataframe instance - 'master dataframe'
        self.df_analytics = pd.DataFrame()
        
        for col_name in self.simulationHistory[0].drop('Date', axis=1).columns:    # iterate over columns except Date
            print(f'Processing: {col_name}')

            # column counter used for iteration columns for each type of column
            sim_column_count = 1

            df_temp_analytics = pd.DataFrame()    # used to create a temporary dataframe for each column type which then can have statistical analysis done. This is then concatenated to the master dataframe.
            for df in self.simulationHistory:

                # Expenses
                df_temp_analytics[f'{col_name}_{sim_column_count}'] = df[col_name]

                sim_column_count += 1

            self.df_analytics[f'{col_name}_Mean'] = df_temp_analytics.apply(lambda x: x.mean(), axis=1)
            self.df_analytics[f'{col_name}_Q25'] = df_temp_analytics.apply(lambda x: x.quantile(0.25), axis=1)
            self.df_analytics[f'{col_name}_Q50'] = df_temp_analytics.apply(lambda x: x.quantile(0.50), axis=1)
            self.df_analytics[f'{col_name}_Q75'] = df_temp_analytics.apply(lambda x: x.quantile(0.75), axis=1)
    