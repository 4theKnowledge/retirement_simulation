import pandas as pd

from flask import Flask, render_template, url_for, jsonify, request
app = Flask(__name__)

# import static data from retirement simulation
df = pd.read_csv('simulation_results.csv')


@app.route('/')
def hello_world():
    title = 'Our Website'
    # return render_template('landing-page.html')
    return render_template('test.html')

@app.route('/data')
def data():
    my_data = {
        'title': 'Tyler',
        'badges': ['one', 'two', 'three']
    }
    return jsonify(my_data)

@app.route("/simple_chart")
def chart():
    # legend = 'Monthly Data'
    labels = df['Date']
    super_bal_val = df['Super_Balance_Value']
    savings_val = df['Savings_Val']
    loan_principal = df['Loan_Begin_Balance']
    super_drawdown = df['Super_Drawdown']
    disposable_income = df['Disposable_Income']
    
    return render_template('chart.html', 
                           labels=labels, 
                           super_bal_val=super_bal_val,
                           savings_val=savings_val,
                           loan_principal=loan_principal,
                           super_drawdown=super_drawdown,
                           disposable_income=disposable_income)

@app.route('/simple_chart', methods=['POST'])
def chart_post():
    text = request.form['text']
    processed_text = text.upper()
    return render_template('chart.html', title=processed_text)

@app.route('/simple_chart', methods=['GET', 'POST'])
def simulate():
    pass


if __name__ == '__main__':
    app.run(debug=True)