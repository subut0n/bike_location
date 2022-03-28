from flask import Flask, render_template, url_for
import requests

app = Flask(__name__)

app.config.from_object('config')

@app.route('/')
@app.route('/index/')
def index():
     API_KEY_OPENWEATHERMAP = app.config['API_KEY_OPENWEATHERMAP']
     LAT = 50.62925
     LONG = 3.057256
     url = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&appid={}'.format(LAT, LONG, API_KEY_OPENWEATHERMAP)
     req = requests.get(url)
     data = req.content
     return render_template('index.html', data=data)

@app.route('/predict/')
def predict():
    return render_template('predict.html')
