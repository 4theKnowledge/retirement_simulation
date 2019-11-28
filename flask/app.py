"""
"""

import pandas as pd
import numpy as np
import json
import time
import datetime

from state_model import phase_model

from flask import Flask, render_template, url_for, jsonify, request, redirect
app = Flask(__name__, template_folder='templates')


def load_sim_data():
    """
    Test function to emulate output of simulation data. For use in front-end dev.
    """
    df = pd.read_csv('simulation_results.csv')
    
    index = json.dumps(list(df.index))
    super_bal = json.dumps(list(df['Super_Balance_Value']))
    savings = json.dumps(list(df['Savings_Val']))
    loan_principal = json.dumps(list(df['Loan_Begin_Balance']))
    super_drawdown = json.dumps(list(df['Super_Drawdown']))
    disposable_income = json.dumps(list(df['Disposable_Income']))
       
    plot_data = {"plot1": {"labels": index, "values": super_bal},
                "plot2": {"labels": index, "values": savings},
                "plot3": {"labels": index, "values": loan_principal},
                "plot4": {"labels": index, "values": super_drawdown},
                "plot5": {"labels": index, "values": disposable_income}
                }
    
    return plot_data
    
    
def model_simulation(model_config, 
                     current_age = 20,
                     retire_age = 50,
                     income = 52000,
                     retire_income = 25000,
                     retirement_end_age = 82):
    
    start_date = start_date = datetime.date(2020,1,1)   
    
    df = pd.DataFrame(phase_model(model_config, start_date,
                                  current_age,
                                  retire_age,
                                  retirement_end_age,
                                  income,
                                  retire_income))
    
    index = json.dumps(list(df.index))
    super_bal = json.dumps(list(df['Super_Balance_Value']))
    savings = json.dumps(list(df['Savings_Val']))
    loan_principal = json.dumps(list(df['Loan_Begin_Balance']))
    super_drawdown = json.dumps(list(df['Super_Drawdown']))
    disposable_income = json.dumps(list(df['Disposable_Income']))
       
    plot_data = {"plot1": {"labels": index, "values": super_bal},
                "plot2": {"labels": index, "values": savings},
                "plot3": {"labels": index, "values": loan_principal},
                "plot4": {"labels": index, "values": super_drawdown},
                "plot5": {"labels": index, "values": disposable_income}
                }
    
    return plot_data
    
    
@app.route('/home', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        currentAge = int(request.form.get('currentAge'))
        retireAge = int(request.form.get('retireAge'))
        currentIncome = float(request.form.get('currentIncome'))
        retireIncome = float(request.form.get('retireIncome'))
        retireEndAge = int(request.form.get('retireEndAge'))
        
        # super init
        super_config = {'contrib_rate': float(request.form.get('superContribRate')) / 100,
                        'admin_fee_amt': float(request.form.get('superAdminFees')),
                        'investment_fee_rate': float(request.form.get('sueprInvestFee')) / 100,
                        'contrib_fee_rate': float(request.form.get('superContribFee')) / 100,
                        'insurance_premium_amt': float(request.form.get('superInsurePrem')),
                        'indirect_costs_rate': float(request.form.get('superIndirectFee')) / 100,
                        'super_return_rate': float(request.form.get('superReturnRate')) /100
                        }
        
        # saving init
        saving_config = {'proportion': 0.25,
                        'interest_rate': 0.03}
        # loan init
        loan_config = {'principal': 300000,
                        'interest_rate': 0.04,
                        'annual_payments': 12,
                        'years': 30}
        
        # expenses init

        # asset value init
        asset_config = {'interest_rate': 0.03}
        
        
        model_config = {'super_model': super_config,
                        'loan_model': loan_config,
                        'saving_model': saving_config,
                        'asset_model': asset_config}
                
        plot_data = model_simulation(model_config,
                                     currentAge,
                                     retireAge,
                                     currentIncome,
                                     retireIncome,
                                     retireEndAge)
        
        
        data = [currentAge, retireAge]
        return render_template('results.html', data=data, plot_data=plot_data)

    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)