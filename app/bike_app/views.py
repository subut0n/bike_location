from flask import Flask, render_template, url_for, request
from .utils import get_season, load_dataAPI, data_formatting, get_48h_data, \
                   prediction, get_encoded_features_name, feels_like_temperature, \
                   prediction_segmentation, get_48h_data_segmentation
from .forms import AddPrediction
import pandas as pd
import numpy as np
import os

app = Flask(__name__)

basedir = os.getcwd()
db = pd.read_csv(os.path.join(basedir, '../csv/train_modifie.csv'))

app.config.from_object('config')

@app.route('/')
@app.route('/index/')
def index():
     api_key = app.config['API_KEY_OPENWEATHERMAP']
     lat = app.config['LAT'] # latitude de Lille
     long = app.config['LONG'] # longitude de Lille
     dataAPI = load_dataAPI(lat, long, api_key)

     # On réalise la segmentation des 48h de données de l'API

     data_seg = get_48h_data_segmentation(dataAPI['hourly'])

     cwd = os.getcwd()
     pickle_segmentation = cwd + '/model_segmentation.pkl'  
     clusters = prediction_segmentation(pickle_segmentation, data_seg)

     # On encode les colonnes catégorielles et on récupère la liste des noms de ces colonnes
     features_to_encode = ['season', 'weather', 'week_days', 'months']
     feature_names = get_encoded_features_name(db, features_to_encode)

     data = get_48h_data(dataAPI['hourly'], feature_names)
<<<<<<< HEAD
     cwd = os.getcwd()
=======
>>>>>>> 09144a9ba745e9974657320f120cab46c98dc51c

     pickle_registered = cwd + '/model_registered.pkl'
     pred_registered = eval(prediction(pickle_registered, data))
     # pred_registered = list(np.round(pred_registered))

     pickle_casual = cwd + '/model_casual.pkl'
     pred_casual = eval(prediction(pickle_casual, data))
     # pred_casual = list(np.round(pred_casual))

<<<<<<< HEAD
     pred_count = pred_registered + pred_casual

=======
     pred = {'registered': pred_registered, 'casual': pred_casual, 'count': pred_registered + pred_casual}
>>>>>>> 09144a9ba745e9974657320f120cab46c98dc51c
     data = eval(data)

     return render_template('index.html', data=data, pred=pred, clusters=clusters)

@app.route('/predict/', methods=['GET', 'POST'])
def predict():
     form = AddPrediction()
     pred = {'registered': '', 'casual': '', 'count': ''}
     if form.validate_on_submit():
          # On encode les colonnes catégorielles et on récupère la liste des noms de ces colonnes
          features_to_encode = ['season', 'weather', 'week_days', 'months']
          feature_names = get_encoded_features_name(db, features_to_encode)

          # Création d'un dictionnaire avec les clés correspondant aux noms des features utilisées
          # lors de la modélisation donc encodées.
          dict = {}
          for name in feature_names:
               dict[name] = 0

          dict['dt'] = form.date.data
          dict['years'] = dict['dt'].year
          month = dict['dt'].month
          dict['months_' + str(month)] = 1
          weekday = dict['dt'].weekday()+1
          dict['week_days_' + str(weekday)] = 1
          dict['holiday'] = float(form.holiday.data)
          dict['workingday'] = float(form.holiday.data)
          weather = form.weather.data
          dict['weather_' + str(weather)] = 1
          dict['temp'] = form.temperature.data
          dict['humidity'] = form.humidity.data
          dict['windspeed'] = float(form.windspeed.data)
          dict['atemp'] = round(feels_like_temperature(dict['temp'],dict['humidity']),2)
          dict = get_season(dict)
          dict.pop('dt')

          cwd = os.getcwd()
          pickle_segmentation = cwd + '/model_segmentation.pkl'
          keys = ['temp', 'atemp', 'humidity', 'windspeed']
          dict_seg = { key: dict[key] for key in keys }
          dict_seg = f'{[dict_seg]}'

          clusters = eval(prediction_segmentation(pickle_segmentation, dict_seg))

          dict = [dict]
          dict = f'{dict}'

          pickle_registered = cwd + '/model_registered.pkl'
          pred_registered = eval(prediction(pickle_registered, dict))

          pickle_casual = cwd + '/model_casual.pkl'
          pred_casual = eval(prediction(pickle_casual, dict))

          pred = {'registered': pred_registered, 'casual': pred_casual, 'count': pred_registered[0] + pred_casual[0]}

          return render_template('predict.html', form=form, clusters=clusters, pred=pred)

     return render_template('predict.html', form=form, clusters='', pred=pred)
