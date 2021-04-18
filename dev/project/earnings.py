"""
Earnings: Employment for users is not constant but rather dependent on various latent factors such as 1. 2. 3. 4. 5. etc. 
This dictates the amount of income of the user.<br> Note: Earnings dictate monthly income
"""

import numpy as np

class Earnings():

    def __init__(self, eduLevel, age, retireAge):
        """
        Something...
        """
    
        self.renumerationType = 'salary'
        self.employmentType = 'FT'    # FT (sal), PT (sal), CAS (wage), TEMP (wage)
        self.employmentStatus = 'Working'    # Working, temp. laid off, unemployed, retired, disabled, housewife, student, other (only first 3 are included in the paper 'Modeling Earning Dynamics')
        self.employed = True    # will be inhierited by profile class...
        self.tenure = 0  # months
        self.tenureBeforeJobLoss = 0    # Months
        self.maxTenure = (retireAge-age)*12   # months
        self.currentIncomePA = 50000
        self.maximumIncomePA = 200000
        
        self.jobTransitions = 0
        
        
        eduRisk = {1:0.05, 2:0.04, 3: 0.03, 4: 0.02, 5: 0.01, 6: 0.0075, 7: 0.005}   # eduLevel : bernoulli risk probability correction...
        self.eduRiskLevel = eduRisk[eduLevel]
            
        
    def captureTenure(self):
        """
        Amount of tenure accumulated over time. This is proportional to experience...
        """
        
        if self.employed:
            self.tenure += 1
            
    def countJobTransitions(self):
        """
        """
        
        self.jobTransitions += 1
    
    def employmentTransition(self):
        """
        Employment transitions, including whether profile becomes unemployed or not. Furthermore, this may also be related to getting better roles.
        Job searching, labor supply...
        Job offer...
        Job in similar domain -> offer based on similar earnings
        Job type/industry -> change... 
        Unemployment and Job shocks...
        Job specific hour shocks...
        Job shopping...
        Job tenure...
        
        Discrete events... job changes, employment loss, interactions between job changes and wages
        Temporary / Permanent layoffs
        
        Account for persons who come out of retirement and include observations following a retirement spell if the individual is working, temporarily laid off, or unemployed.
        
        Assumes that tenure dictates likelihood of unemployment (doesn't take job specific roles into account). For example: If a job is lost and regained, the risk level doesn't reset but rather starts lowering again from a new tenure.
        """
    
        # the risk of job loss reduces with increasing tenure... using an inverse relationship... this could probably be changed to a natural log or similar in the future.
        if self.employed:
            
            # Capture tenure for being employed.
            self.captureTenure()
            
            # Compute unemployment risk based on education level and tenure...
            self.eduRiskLevel = self.eduRiskLevel * (1 - ((self.tenure/self.maxTenure)/100))
            
            # First logic is the chance of becoming unemployed.
            if np.random.binomial(n = 1, p = self.eduRiskLevel):
                print('Job lost')
                self.jobTransitions += 1   # not working...
                self.employed = False
                self.tenureBeforeJobLoss = self.tenure   # Used to weight the reemployment calculation
                print(self.tenureBeforeJobLoss)
                self.tenure = 0   # reset tenure...
            
        # If not employed...
        # Need to try and get job back and restart tenure...
        if not self.employed:
            print('Not employed')
            
            
            # Current probability is random, however, this should be weighted on education level and tenure...This isn't the best logic but it's something.
            if np.random.binomial(n = 1, p = 0.25):
                print('Got a job...')
                self.employed = True
    
    
    def dynamicEarnings(self):
        """
        Model for changes in earnings based on latent factors such as education, experience, productivity, etc.
        """
        
        self.currentIncomePA = (self.maximumIncomePA - self.currentIncomePA)*(self.tenure/self.maxTenure)+self.currentIncomePA
        
        
if __name__ == '__main__':
    
    import datetime
    from dateutil.relativedelta import relativedelta
    import numpy as np
    
    dateStart = datetime.date(2020,1,1)
    dateStartTemp = dateStart

    userAge = 26
    retireAge = 65

    # Initialise education
    # edu = Education()

    # Initialise an 'earnings' class for someone with education level 2, who is 26 years old and wants to retire at 27...
    earning = Earnings(eduLevel=2, age=userAge, retireAge=retireAge)

    while userAge <= retireAge:
        
        
        # Earnings model
        earning.employmentTransition()    # Make a transition...


        # Debug Output
        print(f'{dateStartTemp} - Employement Status {earning.employed} - Months of tenure {earning.tenure} - Current Unemployment Risk {earning.eduRiskLevel*100:0.2f}% - Current Earning (PA) ${earning.currentIncomePA:0.2f}')
        
        
        # Steps through time another month
        dateStartTemp += relativedelta(months=1)

        
        # if the current month of the year is January and we're not on the first year of the simulation
        # Add another year to the users profile, e.g. age them another year.
        if dateStartTemp.month == 1 and 0 < (dateStartTemp.year - dateStart.year):
            userAge += 1
            earning.dynamicEarnings()   # compute new earnings at end of year...