import requests
import json
from datetime import datetime
import pickle as pkl
from sklearn.compose import make_column_transformer
from sklearn.preprocessing import OneHotEncoder
import pandas as pd
import ast

def load_dataAPI(lat, long, api_key):
     url = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&appid={}'.format(lat, long, api_key)
     req = requests.get(url)
     req = req.content.decode("utf-8")
     return json.loads(req)

def get_48h_data(dataAPI, feature_names):
    dataAPI = [dataAPI[i] for i in range(len(dataAPI))]
    data = []
    for i, dict in enumerate(dataAPI):
        data.append(data_formatting(dict, feature_names))
    return f'{data}'

def get_encoded_features_name(data, features_to_encode):
    data = data.drop(['Unnamed: 0', 'casual', 'registered', 'count', 'HI'], axis=1)
    ohe = make_column_transformer((OneHotEncoder(), features_to_encode), remainder='passthrough')
    ohe.fit(data)
    data_ohe = ohe.transform(data)
    data = pd.DataFrame(data_ohe)
    # On récupère le nom des colonnes après avoir OneHotEncoder
    features_name = {}
    for i in range(data.shape[1]):
        features_name[i] = ohe.get_feature_names_out()[i].replace("onehotencoder__","").replace("remainder__","")
    data = data.rename(columns=features_name)
    return data.columns

def data_formatting(currentDataAPI, feature_names):
    # keys correspond aux clés du dataset après onehotencodage

    # On extrait les données nécessaires pour la prédiction
    time_stamp = currentDataAPI['dt']
    currentDataAPI['dt'] = datetime.fromtimestamp(currentDataAPI['dt'])
    currentDataAPI['weather'] = currentDataAPI['weather'][0]['id']

    # Création d'un dictionnaire avec les clés correspondant aux noms des features utilisées
    # lors de la modélisation donc encodées.
    current_dict = {}
    for name in feature_names:
        current_dict[name] = 0

    keys = ['dt', 'temp', 'feels_like', 'humidity', 'wind_speed', 'weather']
    new_keys = ['dt', 'temp', 'atemp', 'humidity', 'windspeed', 'weather']
    current = {}
    for key, new_key in zip(keys, new_keys):
        current[new_key] = currentDataAPI[key]
    current['temp'] = current['temp'] - 273.15
    current['atemp'] = current['atemp'] - 273.15

    for key in current.keys():
        current_dict[key] = current[key]

    weather_1 = [800, 801, 802]
    weather_2 = [701, 711, 721, 803, 804]
    weather_3 = [200, 201, 300, 301, 310,
                500, 501, 520, 600, 601, 611, 612, 615, 620,
                731, 741, 751]
    weather_4 = [202, 210, 211, 212, 221, 230, 231, 232,
                301, 302, 311, 312, 313, 314, 321,
                502, 503, 504, 511, 520, 521, 522, 531,
                602, 613, 616, 621, 622, 761, 762, 771, 781]
    weathers = [weather_1, weather_2, weather_3, weather_4]
    weather_labels = ['weather_1', 'weather_2', 'weather_3', 'weather_4']
    for i, weather in enumerate(weathers):
        if current_dict['weather'] in weather:
            current_dict[weather_labels[i]] = i+1
    current_dict.pop('weather')

    current_dict['hours'] = current_dict['dt'].hour
    current_dict['years'] = current_dict['dt'].year

    month = current_dict['dt'].month
    month_label = 'months_' + str(month)
    current_dict[month_label] = 1

    week_day = datetime.fromtimestamp(time_stamp).weekday()+1
    week_day_label = 'week_days_' + str(week_day)
    current_dict[week_day_label] = 1

    seasons = ['06-21', '09-21', '12-21']
    for i, season in enumerate(seasons):
        if (current_dict['dt'].strftime('%m-%d') < '03-21'):
            current_dict['season_4'] = 1
            break
        if ((current_dict['dt'].strftime('%m-%d') < season) & (current_dict['dt'].strftime('%m-%d') >= '03-21')):
            current_dict['season_' + str(i+1)] = 1
            break
    
    if (week_day >= 6):
        current_dict['holiday'] = 0
        current_dict['workingday'] = 0
    else:
        current_dict['holiday'] = 0
        current_dict['workingday'] = 1
    current_dict.pop('dt')
    return current_dict

def prediction(pickle_uri, data):
     with open(pickle_uri, 'rb') as pickle_file:
          model = pkl.load(pickle_file)
     data = pd.DataFrame(ast.literal_eval(data))
     return f'{model.predict(data)}'
