"""
Savings: The Savings class is used for capturing user savings based on proportions saved which vary over time. 
Savings also work as a buffer for rare events that cannot be directly covered by income.

"""


class Savings():
    """
    Model for savings.
    """
    
    def __init__(self, proportionSaved):
        """
        
        """
        self.proportionSaved = proportionSaved
        
        # data capture
        self.dataHistory = []
        self.savingHistory = []
        self.amtSaved = sum(self.savingHistory)
        
    def getSavedAmount(self, remainingIncome):
        """
        Gets amount saved from remainingIncome
        """
        if 0 < remainingIncome:
            return remainingIncome*self.proportionSaved
        elif remainingIncome < 0:
            # if negative income then take out of savings the amount required.
            # Need to be able to check the current balance of savings and compare that there is enough...
            return remainingIncome
        else:
            return 0
        
    # Data Capture Functions
    def getSavingHistory(self, date, savingInfo):
        """
        Used to capture temporal data for plotting and analysis.
        """
        self.dateHistory.append(date)
        self.savingHistory.append(savingInfo)
        
if __name__ == '__main__':
    pass