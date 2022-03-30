from cProfile import label
from flask_wtf import FlaskForm
from wtforms import PasswordField, EmailField, SubmitField, StringField, TextAreaField, FileField
from wtforms.fields import DateField, SelectField
from wtforms.validators import Length, DataRequired, Email, EqualTo, ValidationError

class Prediction(FlaskForm):
    date = DateField(label='Date')
    hour = StringField(label='Hour')
    temperature = StringField(label='Temperature', validators=[Length(max=50)])
    humidity = StringField(label='Humidity', validators=[Length(max=100)])
    windforce = StringField(label='Wind force in km/h')
    holiday = StringField(label='Holiday')
    workingday = StringField(label='Working Day')
    