from flask import Flask
import pandas as pd

from .views import app

data = pd.read_csv('..\\csv\\train_modifie.csv')