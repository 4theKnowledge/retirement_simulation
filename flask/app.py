"""
"""

import pandas as pd
import json


from flask import Flask, render_template, url_for, jsonify, request
app = Flask(__name__)


def basic_function():
    labels = [1,1,2,2,3,3,4,4,5,5]
    values = [2,3,11,5,4,33,2,2,2,9]
    return labels, values


@app.route("/", methods=['GET'])
def index():
    name = request.args.get("name", "World")    # user, default

    print(f'METHOD: {request.method}')

    if request.method=='GET':
        labels, values = basic_function()
        json_labels = json.dumps(labels)
        json_values = json.dumps(values)
        return render_template('index.html',
                               name=name,
                               data=[json_labels,json_values])
    return render_template('index.html', name=name)


if __name__ == '__main__':
    app.run(debug=True)