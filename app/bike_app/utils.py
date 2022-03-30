import requests
import json
from datetime import datetime

def load_dataAPI(lat, long, api_key):
     url = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&appid={}'.format(lat, long, api_key)
     req = requests.get(url)
     req = req.content.decode("utf-8")
     return json.loads(req)

def get_48h_data(dataAPI):
    dataAPI = [dataAPI[i] for i in range(len(dataAPI))]
    data = []
    for i, dict in enumerate(dataAPI):
        data.append(data_formating(dict))
    return f'{data}'


def data_formating(currentDataAPI):

    # On extrait les données nécessaires pour la prédiction
    time_stamp = currentDataAPI['dt']
    currentDataAPI['dt'] = datetime.fromtimestamp(currentDataAPI['dt'])

    currentDataAPI['weather'] = currentDataAPI['weather'][0]['id']
    keys = ['dt', 'temp', 'feels_like', 'humidity', 'wind_speed', 'weather']
    new_keys = ['dt', 'temp', 'atemp', 'humidity', 'windspeed', 'weather']
    current = {}
    for key, new_key in zip(keys, new_keys):
        current[new_key] = currentDataAPI[key]

    current['temp'] = current['temp'] - 273.15
    current['atemp'] = current['atemp'] - 273.15

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
    
    for i, weather in enumerate(weathers):
        if current['weather'] in weather:
            current['weather'] = i+1

    current['hours'] = current['dt'].hour
    current['week_days'] = datetime.fromtimestamp(time_stamp).weekday() + 1
    current['months'] = current['dt'].month
    current['years'] = current['dt'].year

    seasons = ['06-21', '09-21', '12-21']
    for i, season in enumerate(seasons):
        if (current['dt'].strftime('%m-%d') < '03-21'):
            current['season'] = 4
            break
        if ((current['dt'].strftime('%m-%d') < season) & (current['dt'].strftime('%m-%d') >= '03-21')):
            current['season'] = i+1
            break
    
    if (current['week_days'] >= 6):
        current['holiday'] = 0
        current['workingday'] = 0
    else:
        current['holiday'] = 0
        current['workingday'] = 1

    return current