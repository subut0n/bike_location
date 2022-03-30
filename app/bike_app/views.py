from flask import Flask, render_template, url_for
from .utils import load_dataAPI, data_formating, get_48h_data

app = Flask(__name__)

app.config.from_object('config')

@app.route('/')
@app.route('/index/')
def index():
     api_key = app.config['API_KEY_OPENWEATHERMAP']
     # Latitude et longitude de Lille
     lat = app.config['LAT']
     long = app.config['LONG']
     dataAPI = load_dataAPI(lat, long, api_key)
     data = get_48h_data(dataAPI['hourly'])
     return data#render_template('index.html', data=dataAPI)

@app.route('/predict/')
def predict():
    return render_template('predict.html')
