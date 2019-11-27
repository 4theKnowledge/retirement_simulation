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
    
    
def model_simulation(current_age = 20,
                     retire_age = 50,
                     income = 52000,
                     retire_income = 25000,
                     retirement_end_age = 82):
    
    start_date = start_date = datetime.date(2020,1,1)   
    
    df = pd.DataFrame(phase_model(start_date,
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
        currentIncome = int(request.form.get('currentIncome'))
        retireIncome = int(request.form.get('retireIncome'))
        retireEndAge = int(request.form.get('retireEndAge'))
        
        plot_data = model_simulation(currentAge,
                                     retireAge,
                                     currentIncome,
                                     retireIncome,
                                     retireEndAge)
        
        
        data = [currentAge, retireAge]
        return render_template('results.html', data=data, plot_data=plot_data)

    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)