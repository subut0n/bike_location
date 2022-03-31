import requests
import json
from datetime import datetime

class FuturePrediction():
    """Create a table Prediction on the database"""
    date = 
    year =
    month =
    weekday =
    hour = 
    season =
    weather =
    holiday =
    workingday =
    temperature = 
    atemperature = 
    humidity =
    windspeed = 

class TodayPrediction():
    """Create Prediction from """
    date = 
    year =
    month =
    weekday =
    hour = 
    season =
    weather =
    holiday =
    workingday =
    temperature = 
    atemperature = 
    humidity =
    windspeed = 

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