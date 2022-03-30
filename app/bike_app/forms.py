from cProfile import label
from flask_wtf import FlaskForm
from wtforms import PasswordField, EmailField, SubmitField, StringField, TextAreaField, FileField
from wtforms.fields import DateField, SelectField
from wtforms.validators import Length, DataRequired, Email, EqualTo, ValidationError

class AddPrediction(FlaskForm):
    date = DateField(label='Date') #1 temporel
    # year = StringField(label='Année')
    # month = StringField(label='Mois')
    # weekday = StringField(label='Jour de la semaine')
    # hour = StringField(label='Heure')
    season = StringField(label='Saison') #2 condition
    weather = StringField(label='Conditions météorologiques')
    holiday = StringField(label='Vacances')
    workingday = StringField(label='Journée de travail')
    temperature = StringField(label='Température') #3 mesure
    atemperature = StringField(label='Température ressentie')
    humidity = StringField(label='Humidité')
    windspeed = StringField(label='Force du vent en km/h')