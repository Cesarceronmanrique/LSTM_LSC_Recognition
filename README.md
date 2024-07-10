# LSTM_LSC_Recognition
Este repositorio contiene la implementación de un modelo de reconocimiento de señas en Lengua de Señas Colombiana (LSC) utilizando Long Short-Term Memory (LSTM).
***
El objetivo de este proyecto es desarrollar un sistema que pueda reconocer las señas de la LSC a partir de secuencias de datos de movimiento. El modelo LSTM es adecuado para este tipo de tareas debido a su capacidad para capturar dependencias a largo plazo en datos secuenciales.
***

## Dependencias

Para la instalación de dependencias se poseen 2 archivos en formato .txt que contienen las librerías correspondientes para 2 ambientes virtuales.

- requirements_train.txt : Que corresponde al ambiente usado para el entrenamiento del modelo.

'pip install -r requirements_detections.txt

- requirements_detections.txt : Que corresponde al ambiente usado para hacer pruebas en tiempo real del modelo entrenado.

'pip install -r requirements_detections.txt

## Gestión de archivos

Se contiene una carpeta de modulos que contienen todas las funciones usadas para ejecutar el código de detección en tiempo real; estos modulos reunen y ejecutan funciones de librerías como Opencv, Tensorflow y Mediapipe.

## Archivos para obtención de datos

Los archivos correspondientes a frame_extractor.ipynb y keypoint_extractor.ipynb son usados para generar el conjunto de datos para el entrenamiento de la red.