from flask import render_template
from ..forms import AddPrediction


@app.route('/predict', methods=['GET','POST'])
def predict():
    form = AddPrediction()
    future_prediction = future_prediction()

    if form.validate_on_submit():

        if 