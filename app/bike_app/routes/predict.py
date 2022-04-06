from flask import render_template, flash
from ..forms import AddPrediction


# @app.route('/predict', methods=['GET','POST'])
# def predict():
#     form = AddPrediction()
#     future_prediction = future_prediction()

    # if form.validate_on_submit():

    #     future_prediction.date = form.date
    #     future_prediction.weather = form.weather
    #     future_prediction.holiday = form.holiday
    #     future_prediction.workingday = form.workingday
    #     future_prediction.temperature = form.temperature
    #     future_prediction.atemperature = form.atemperature
    #     future_prediction.humidity = form.humidity
    #     future_prediction.windspeed = form.windspeed

    #     flash(f"Les variables pour la prediction ont bien ete pris en compte.")
    # return render_template('results.html', form=form, future_prediction=future_prediction())
