import pandas as pd
import json

from flask import Flask, render_template, url_for, jsonify, request
app = Flask(__name__)

# import static data from retirement simulation
df = pd.read_csv('simulation_results.csv')

@app.route("/")
def chart():
    return render_template('chart.html')

# Start Simulation Functionality
SimButtonPressed = 0
@app.route('/', methods=['GET', 'POST'])
def simulate():
    print(request.method)
    if request.method == "POST":
        SimButtonPressed = 1
        df = pd.read_csv('simulation_results.csv')
        df_json = df.to_json(orient='columns')
        json_data = json.loads(df_json)
        print(json_data.keys())
        
        return render_template("chart.html", SimButtonPressed=SimButtonPressed)#, json_data=json_data)
    SimButtonPressed = 0
    return render_template("chart.html", SimButtonPressed=SimButtonPressed)


# @app.route("/")
# def chart_populated():
#     # legend = 'Monthly Data'
#     labels = df['Date']
#     super_bal_val = df['Super_Balance_Value']
#     savings_val = df['Savings_Val']
#     loan_principal = df['Loan_Begin_Balance']
#     super_drawdown = df['Super_Drawdown']
#     disposable_income = df['Disposable_Income']
    
#     return render_template('chart.html', 
#                            labels=labels, 
#                            super_bal_val=super_bal_val,
#                            savings_val=savings_val,
#                            loan_principal=loan_principal,
#                            super_drawdown=super_drawdown,
#                            disposable_income=disposable_income)


# @app.route('/', methods=['POST'])
# def chart_post():
#     text = request.form['text']
#     processed_text = text.upper()
#     return render_template('chart.html', title=processed_text)

# @app.route('/simulate_input_data', methods=['POST'])
# def simulate_data_input():
#     email = request.form['email']
#     name = request.form['name']
    
#     if name and email:
#         newName = name[::-1]
        
#         return jsonify({'name' : newName})
    
#     return jsonify({'error' : 'Missing data!'})


# @app.route('/simulate', methods=['POST'])
# def simulate():
#     # Simulate code
#     print('button pressed')
#     # import static data from retirement simulation
#     df = pd.read_csv('simulation_results.csv')
    
#     simBtn = request.form['simulate']
    
#     if simBtn:
#         print('You pressed the sim btn')
#         print(df.head(5))
    
#     return render_template('chart.html')

if __name__ == '__main__':
    app.run(debug=True)