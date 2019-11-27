"""
"""

import pandas as pd
import numpy as np
import json

from flask import Flask, render_template, url_for, jsonify, request, redirect
app = Flask(__name__, template_folder='templates')


def basic_function():
    labels = [1,1,2,2,3,3,4,4,5,5]
    values = [2,3,11,5,4,33,2,2,2,9]
    return labels, values

@app.route('/home', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        currentAge = request.form.get('currentAge')
        retireAge = request.form.get('retireAge')
        
        inputdata = [currentAge, retireAge]
        
        labels, values = basic_function()
        currentAge_out = [labels, values]
        retireAge_out = [labels, values]
        # return f'<h1> Current Age: {currentAge} Retire Age: {retireAge} Income Amount: {incomeAmt}'
        return render_template('index1.html', inputdata=data, 
                               currentAgeOut=currentAge_out,
                               retireAgeOut=retireAge_out)


    return '''<form method='POST'>
    Current Age: <input type="text" name="currentAge">
    Retirement Age: <input type="text" name="retireAge">
    <input type="submit">
    </form>
    '''


# @app.route("/", methods=['GET'])
# def index():
#     event_counter = 0

#     print(f'METHOD: {request.method}')
#     if (request.method=='GET') & (event_counter == 0):
#         print('basic method - get')
#         labels, values = basic_function()
#         json_labels = json.dumps(labels)
#         json_values = json.dumps(values)
#         event_counter += 1
        
#         return render_template('index.html',
#                                data=[json_labels,json_values])
        
#     return render_template('index.html')


@app.route('/postmethod', methods=['POST'])
def get_post_javascript_data():
    jsdata = request.form['javascript_data']    # JSON String
    jsdata = json.loads(jsdata) # JSON Object
    print(jsdata)
    print(jsdata['current_age'])
    print(jsdata['retirement_age'])
    print(jsdata['income_amount'])
    print('1', request.method)

    if request.method == 'POST':
        try:
            print('2', request.method)
            print('calling function')
            output = basic_function_1(jsdata['current_age'],
                            jsdata['retirement_age'],
                            jsdata['income_amount'])
            return output
        except:
            print('fucked it m8')
            return jsdata

def basic_function_1(current_age = 20, retirement_age = 50, income_amount = 2500):
    print('in some function...')
    x = list(range(current_age,retirement_age,1))
    y = list(range(10,10+len(x),1))
    labels = json.dumps(x)
    values = json.dumps(y)
    
    return [labels, values]
    

if __name__ == '__main__':
    app.run(debug=True)