from cProfile import label
from flask_wtf import FlaskForm
from wtforms import PasswordField, EmailField, SubmitField, StringField, TextAreaField, FloatField, SelectField, IntegerField
from wtforms.fields import DateField, SelectField
from wtforms.validators import Length, DataRequired, Email, EqualTo, ValidationError, NumberRange, Regexp

class AddPrediction(FlaskForm):
    date = DateField(label='Date', validators=[DataRequired()]) #1 temporel
    # year = StringField(label='Année')
    # month = StringField(label='Mois')
    # weekday = StringField(label='Jour de la semaine')
    hour = IntegerField(label='Heure', validators=[DataRequired(), NumberRange(min=0, max=23)]) #2 condition
    # season = SelectField(label='Saison')
    weather = SelectField(label='Conditions météorologiques',
                          choices=[(1, 'Clear, few clouds, partly cloudy'),
                                   (2, 'Mist + cloudy, mist + broken clouds, mist + few clouds, mist'),
                                   (3, 'Light snow, light rain + thunderstorm + scattered clouds, light rain + scattered clouds'),
                                   (4, 'Heavy rain + ice pallets + thunderstorm + mist, snow + fog')], validators=[DataRequired()])
    holiday = SelectField(label='Vacances', choices=[(0, 'Hors vacances scolaire'), (1, 'Vacances scolaires')])
    workingday = SelectField(label='Journée de travail', choices=[(0, 'Jour de congé'), (1, 'Jour de travail')], validators=[DataRequired()])
    temperature = FloatField(label='Température', validators=[DataRequired(), NumberRange(min=-80,max=100,
                             message="La température doit être comprise entre -80 et 100 °C")]) #3 mesure
    # atemperature = FloatField(label='Température ressentie', validators=[DataRequired(), NumberRange(min=80,max=100)])
    humidity = IntegerField(label='Humidité', validators=[DataRequired(), NumberRange(min=0,max=100,
                            message="L'humidité doit être comprise entre 0 et 100.")])
    windspeed = StringField(label='Force du vent en km/h', validators=[DataRequired(),
                           Regexp('^\d+\.?\d*$', message='La vitesse du vent doit être un nombre décimal positif.')])
    submit = SubmitField(label="Prédiction")