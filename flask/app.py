import pandas as pd
import json

from flask import Flask, render_template, url_for, jsonify, request
app = Flask(__name__)

def basic_function():
    return [1,2,3,4,5,6,7,8,9,10]


@app.route("/", methods=['GET'])
def index():
    name = request.args.get("name", "World")    # user, default

    print(f'METHOD: {request.method}')

    if request.method=='GET':
        array = basic_function()
        json_array = json.dumps(array)
        return render_template('index.html', name=name, data=json_array)
    
    return render_template('index.html', name=name)

if __name__ == '__main__':
    app.run(debug=True)