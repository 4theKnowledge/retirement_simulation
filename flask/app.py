from flask import Flask, render_template, url_for, jsonify
app = Flask(__name__)

@app.route('/')
def hello_world():
    title = 'Our Website'
    return render_template('test.html', title=title)

@app.route('/data')
def data():
    my_data = {
        'title': 'Tyler',
        'badges': ['one', 'two', 'three']
    }
    
    return jsonify(my_data)