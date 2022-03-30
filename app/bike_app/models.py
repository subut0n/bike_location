from sklearn.compose import make_column_transformer
from sklearn.preprocessing import OneHotEncoder
import pandas as pd

class FuturePrediction():
    """Create a table Prediction on the database
    Args:
    """
    # date = 
    # weather = 
    # registered =
    # casual =
    # count =

class TodayPrediction():
    """Create Prediction from """

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

