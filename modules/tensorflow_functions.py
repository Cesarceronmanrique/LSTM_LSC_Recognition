#from tensorflow import *
from tensorflow.keras.models import load_model
import os
import numpy as np

def load_lstm():
    actual_path = os.getcwd()
    model_path = os.path.join(actual_path, 'LSTM_Model.keras')
    model = load_model(model_path, compile = False)
    return model

def make_predictions(model, input_value=[]):
    prediccion = model.predict(np.expand_dims(input_value, axis=0))[0]
    return prediccion

def map_predictions(predictions):
    map_dictionary = {0 : "bancos", 1 : "banios", 2 : "comidas", 3 : "juegos infantiles", 4:"parqueaderos"}
    class_predicted = map_dictionary[predictions]
    return class_predicted