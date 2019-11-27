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
                "plot5": {"labels": index, "values": disposable_income},}
    
    return plot_data
    
    
def model_simulation(income = 18000,
                          retire_income = 20000,
                          current_age = 20,
                          retirement_age = 50,
                          retirement_end_age = 80):
    
    df = pd.DataFrame(phase_model(start_date,
                                  current_age,
                                  retire_age,
                                  retirement_end_age,
                                  income,
                                  retire_income))
    
    
    

def intermediate_function():
    """
    """
    current_age = int(current_age)
    retirement_age = int(retirement_age)
    
    x = list(range(current_age, retirement_age, 1))
    y = list(range(10, 10+len(x), 1))
    z = list(range(2, 2+len(x), 1))
    
    # time.sleep(15)
    
    x = json.dumps(x)
    y = json.dumps(y)
    z = json.dumps(z)
    
    plot_data = {"plot1": {"labels": x, "values": y},
                    "plot2": {"labels": x, "values": z}}
    
    return plot_data
    

@app.route('/home', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        currentAge = request.form.get('currentAge')
        retireAge = request.form.get('retireAge')
        
        # plot_data = intermediate_function(currentAge, retireAge)
        plot_data = load_sim_data()
        
        
        data = [currentAge, retireAge]
        # return f'<h1> Current Age: {currentAge} Retire Age: {retireAge} Income Amount: {incomeAmt}'
        return render_template('results.html', data=data, plot_data=plot_data)

    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)