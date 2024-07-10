#from tensorflow import *
from tensorflow.python.keras.models import load_model
import os
import numpy as np

def load_lstm():
    actual_path = os.getcwd()
    model_path = os.path.join(actual_path, 'LSTM\LSTM_Model.h5')
    weights_path = os.path.join(actual_path, 'LSTM\LSTM_Model_Weights.h5')
    model = load_model(model_path)
    model.load_weights(weights_path)
    return model

def make_predictions(model, input_value=[]):
    prediccion = model.predict(np.expand_dims(input_value, axis=0))[0]
    return prediccion

def map_predictions(predictions):
    map_dictionary = {0 : "Bancos", 1 : "Banios", 2 : "Comidas", 3 : "Juegos Infantiles", 4:"Parqueaderos"}
    class_predicted = map_dictionary[predictions]
    return class_predicted