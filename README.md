# LSTM_LSC_Recognition

Este repositorio proporciona una implementación de un modelo para el reconocimiento de señas en la Lengua de Señas Colombiana (LSC) utilizando redes neuronales Long Short-Term Memory (LSTM).

## Descripción

El objetivo de este proyecto es desarrollar un sistema capaz de reconocer las señas en LSC a partir de secuencias de datos de movimiento. El modelo LSTM es particularmente adecuado para esta tarea debido a su habilidad para capturar dependencias a largo plazo en datos secuenciales.

## Dependencias

Para instalar las dependencias necesarias, se proporcionan dos archivos de requisitos para diferentes entornos:

- **`requirements_train.txt`**: Contiene las librerías necesarias para el entrenamiento del modelo.
- **`requirements_detections.txt`**: Incluye las librerías requeridas para realizar pruebas en tiempo real con el modelo entrenado.

Puedes instalar las dependencias ejecutando los siguientes comandos en tu terminal:

```bash
pip install -r requirements_train.txt
pip install -r requirements_detections.txt

## Gestión de archivos

Se contiene una carpeta de modulos que contienen todas las funciones usadas para ejecutar el código de detección en tiempo real; estos modulos reunen y ejecutan funciones de librerías como Opencv, Tensorflow y Mediapipe.

## Archivos para obtención de datos

Los archivos correspondientes a frame_extractor.ipynb y keypoint_extractor.ipynb son usados para generar el conjunto de datos para el entrenamiento de la red.