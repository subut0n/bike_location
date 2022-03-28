from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route('/')
@app.route('/index/')
def index():
     return render_template('index.html')

@app.route('/predict/')
def predict():
    return render_template('predict.html')
