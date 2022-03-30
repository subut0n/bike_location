from flask import Flask, render_template, url_for
from .utils import load_dataAPI, data_formatting, get_48h_data, prediction
from .forms import AddPrediction
from .models import get_encoded_features_name
import pandas as pd
import os

app = Flask(__name__)

basedir = os.getcwd()
db = pd.read_csv(os.path.join(basedir, '..\\csv\\train_modifie.csv'))

app.config.from_object('config')

@app.route('/')
@app.route('/index/')
def index():
     api_key = app.config['API_KEY_OPENWEATHERMAP']
     lat = app.config['LAT'] # latitude de Lille
     long = app.config['LONG'] # longitude de Lille
     dataAPI = load_dataAPI(lat, long, api_key)

     # On encode les colonnes catégorielles et on récupère la liste des noms de ces colonnes
     features_to_encode = ['season', 'weather', 'week_days', 'months']
     feature_names = get_encoded_features_name(db, features_to_encode)

     data = get_48h_data(dataAPI['hourly'], feature_names)
     cwd = os.getcwd()
     pickle_uri = cwd + '\\model_test.pkl'
     pred = prediction(pickle_uri, data)
     return pred #render_template('index.html', data=data)

@app.route('/predict/')
def predict():
     form = AddPrediction()
     return render_template('predict.html', form=form)
