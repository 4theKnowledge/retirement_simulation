"""
Personal Financial Modelling

Author: Tyler Bikaun
Last Modified: 22.03.2020
"""


from simulation import Simulation 

def main(sim_details):

    
    # Initialse simulation class
    sim = Simulation(data_dict=sim_details)
    
    # Review user profile has the correct attributes
    print(sim.userProfile.eduLevel)
    
    # Run monte carlo model for two simulation iterations
    df_store = sim.monte_carlo_model(10)
    
    # Execute statistical analysis
    sim.statistical_analysis()
    
    # Review analysis results
    sim.df_analytics.head()
    
    # Review analysis results
    sim.df_analytics.loc[90,:].T

def test(sim_details):
    
    sim = Simulation(data_dict=sim_details)
    
    # print(sim.userProfile.employed)
    print(sim.userProfile.eduLevel)


if __name__ == '__main__':
    # RUNNING USER SIMULATION MODEL
    
    # Simulation and user profile information
    sim_details = {'profileDetails': {'name': 'Tyler',
                                    'age': 26,
                                    'retireAge': 65,
                                    'deadAge': 80,
                                    'incomePA': 52000,
                                    'expensesPM': 1000,
                                    'proportionSaved': 0.25
                                    },
                    'loanDetails': {
                        'loan_1': {'type': 'Home',
                                    'description': 'Home loan...',
                                    'principal':300000,
                                    'interestRate': 0.04,
                                    'annualPayments': 12,
                                    'duration': 25,
                                    'startDate': '01-01-2021',
                                    'loanPaymentExtra': 0},
                        'loan_2': {'type': 'Car',
                                    'description': 'Car loan 1',
                                    'principal':50000,
                                    'interestRate': 0.12,
                                    'annualPayments': 12,
                                    'duration': 10,
                                    'startDate': '01-01-2025',
                                    'loanPaymentExtra': 50},
                        'loan_3': {'type': 'Car',
                                    'description': 'Car loan 2',
                                    'principal':7000,
                                    'interestRate': 0.08,
                                    'annualPayments': 12,
                                    'duration': 5,
                                    'startDate': '01-06-2027',
                                    'loanPaymentExtra': 250}
                    }}
    main(sim_details)
    
    # test(sim_details)
    
    