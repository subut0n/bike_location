import requests
import json
from datetime import datetime
import pickle as pkl
from sklearn.compose import make_column_transformer
from sklearn.preprocessing import OneHotEncoder
import pandas as pd

def load_dataAPI(lat, long, api_key):
     url = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&appid={}'.format(lat, long, api_key)
     req = requests.get(url)
     req = req.content.decode("utf-8")
     return json.loads(req)

def get_48h_data(dataAPI, feature_names):
    dataAPI = [dataAPI[i] for i in range(len(dataAPI))]
    data = []

    for dict in dataAPI:
        data.append(data_formatting(dict, feature_names))
    return f'{data}'

def get_encoded_features_name(data, features_to_encode):
    data = data.drop(['casual', 'registered'], axis=1)
    ohe = make_column_transformer((OneHotEncoder(), features_to_encode), remainder='passthrough')
    ohe.fit(data)
    data_ohe = ohe.transform(data)
    data = pd.DataFrame(data_ohe)
    # On récupère le nom des colonnes après avoir OneHotEncodé
    features_name = {}
    for i in range(data.shape[1]):
        features_name[i] = ohe.get_feature_names_out()[i].replace("onehotencoder__","").replace("remainder__","")
    data = data.rename(columns=features_name)
    return data.columns


def data_formatting(data_1h_API, feature_names):
    # keys correspond aux clés du dataset après onehotencodage

    # On extrait les données nécessaires pour la prédiction
    timestamp = data_1h_API['dt']
    data_1h_API['dt'] = datetime.fromtimestamp(data_1h_API['dt'])
    data_1h_API['weather'] = data_1h_API['weather'][0]['id']

    # Reformatage des données issues de l'API en une forme qui nous convient
    keys = ['dt', 'temp', 'feels_like', 'humidity', 'wind_speed', 'weather']
    new_keys = ['dt', 'temp', 'atemp', 'humidity', 'windspeed', 'weather']
    data = {}
    for key, new_key in zip(keys, new_keys):
        data[new_key] = data_1h_API[key]
    data['temp'] = round(data['temp'] - 273.15, 2)
    data['atemp'] = round(data['atemp'] - 273.15, 2)

    # Création d'un dictionnaire avec les clés correspondant aux noms des features utilisées
    # lors de la modélisation donc encodées.
    data_1h_dict = {}
    for name in feature_names:
        data_1h_dict[name] = 0

    for key in data.keys():
        data_1h_dict[key] = data[key]

    data_1h_dict = get_weather(data_1h_dict)

    data_1h_dict['hours'] = data_1h_dict['dt'].hour
    data_1h_dict['years'] = data_1h_dict['dt'].year
    data_1h_dict = get_months(data_1h_dict)
    data_1h_dict, weekday = get_week_day(data_1h_dict, timestamp)

    data_1h_dict = get_season(data_1h_dict)
    data_1h_dict = get_workingday(data_1h_dict, weekday)
    data_1h_dict['dt'] = data_1h_dict['dt'].strftime("%A, %Y-%m-%d, %H:%M:%S")

    return data_1h_dict

def prediction(pickle_uri, data):
     with open(pickle_uri, 'rb') as pickle_file:
          model = pkl.load(pickle_file)
    #  data = ast.literal_eval(data)
     data = pd.DataFrame(eval(data))
     pred = list(model.predict(data))
     return f'{pred}'

def feels_like_temperature(temp,humidity):
    # Heat index (indice de chaleur) ; en degré celsius
    c1 = -8.78469475556
    c2 = 1.61139411
    c3 = 2.33854883889
    c4 = -0.14611605
    c5 = -0.012308094
    c6 = -0.0164248277778
    c7 = 2.211732e-3
    c8 = 7.2546e-4
    c9 = 3.582e-6
    T = temp
    R = humidity
    if (humidity > 40) & (temp > 27):
        return c1 + c2*T + c3*R + c4*T*R + c5*pow(T,2) + c6*pow(R,2) + c7*pow(T,2)*R + c8*T*pow(R,2) + c9*pow(T,2)*pow(R,2)
    else:
        return temp

def get_weather(data_1h_dict):
    weather_1 = [800, 801, 802]
    weather_2 = [701, 711, 721, 803, 804]
    weather_3 = [200, 201, 300, 301, 310, 500, 501, 520,
                 600, 601, 611, 612, 615, 620, 731, 741, 751]
    weather_4 = [202, 210, 211, 212, 221, 230, 231, 232,
                 301, 302, 311, 312, 313, 314, 321, 502,
                 503, 504, 511, 520, 521, 522, 531, 602,
                 613, 616, 621, 622, 761, 762, 771, 781]
    weathers = [weather_1, weather_2, weather_3, weather_4]
    weather_labels = ['weather_1', 'weather_2', 'weather_3', 'weather_4']
    for i, weather in enumerate(weathers):
        if data_1h_dict['weather'] in weather:
            data_1h_dict[weather_labels[i]] = 1
    data_1h_dict.pop('weather')
    return data_1h_dict

def get_season(data_1h_dict):
    seasons = ['06-21', '09-21', '12-21']
    for i, season in enumerate(seasons):
        if (data_1h_dict['dt'].strftime('%m-%d') < '03-21'):
            data_1h_dict['season_4'] = 1
            return data_1h_dict
        if ((data_1h_dict['dt'].strftime('%m-%d') < season) & (data_1h_dict['dt'].strftime('%m-%d') >= '03-21')):
            data_1h_dict['season_' + str(i+1)] = 1
            return data_1h_dict

def get_months(data_1h_dict):
    month = data_1h_dict['dt'].month
    month_label = 'months_' + str(month)
    data_1h_dict[month_label] = 1
    return data_1h_dict

def get_week_day(data_1h_dict, timestamp):
    weekday = datetime.fromtimestamp(timestamp).weekday()+1
    weekday_label = 'week_days_' + str(weekday)
    data_1h_dict[weekday_label] = 1
    return data_1h_dict, weekday

def get_workingday(data_1h_dict, weekday):
    if (weekday >= 6):
        data_1h_dict['workingday'] = 0
    else:
        data_1h_dict['workingday'] = 1
    return data_1h_dict
