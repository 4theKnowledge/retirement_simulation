"""
Expenses: The Expenses class is used to capture expenses relating to life in general. This is currently modelled as being stochastic within certain limits based on living costs.
"""

import numpy as np

class Expenses():
    """
    Model for general expenses.
    """
    
    def __init__(self, expenses):
        """
        
        """
        
        # Everything is on a monthly basis in the model...
        self.expenses = expenses
        
    def increaseExpenseRandomly(self, phase):
        """
        Increase principal by a random amount to simulate expense tranfers.
        This can only occur if the loan is still active. 
        TODO: integrate expenses and ability for profile to override 'active' status to ressurect their paid off loans...
        """

        expensesTemp = 0
        if (0.5 < np.random.uniform(0,1)):
            if phase == 2:
                increaseAmt = np.random.uniform(0.8, 1.2)*(self.expenses / 2)
            else:
                increaseAmt = np.random.uniform(0.8, 1.2)*(self.expenses)
            
#             print(f'Expense balance: ${increaseAmt:0.2f}')
            return increaseAmt
        else:
#             print(f'Expenses remain unchanged at: ${self.expenses:0.2f}', )
            if phase == 2:
                return self.expenses / 2
            else:
                return self.expenses
            
if __name__ == '__main__':
    pass