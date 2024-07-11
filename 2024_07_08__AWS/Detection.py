import os
import numpy as np
import cv2
import mediapipe as mp
from tensorflow.keras.models import load_model
mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh
mp_hands = mp.solutions.hands
mp_pose = mp.solutions.pose

class Detection:

    def __init__(self):
        self.model = load_model(r"LSTM_Model_CPU.keras", compile = False)

    def load_images(self,path):
        images = []
        files = os.listdir(path)
        for counter in range(1, len(files))+1: # NUEVO CODIGO
            #file_path = os.path.join(path, file)
            file_path = os.path.join(path, str(counter) + ".jpg") # NUEVO CODIGO
            image = cv2.imread(file_path)
            print("URL Imagen:",file_path)
        if image is None:
            print("No se pudo cargar la imagen ", file_path, ".")
        else:
            images.append(image)
        return images

    def detection(self,path):
        array_of_images = self.load_images(path)
        flag = True
        holistic_model = mp_holistic.Holistic(min_detection_confidence = 0.5, min_tracking_confidence = 0.5)
        sequence, predictions, min_value = [], [], 0.7
        map_dictionary = {0 : "bancos", 1 : "banios", 2 : "comidas", 3 : "juegos infantiles", 4:"parqueaderos"}
        class_predicted = ""
        print("Cantidad de imagenes:",len(array_of_images))
        for image in array_of_images:
            results = holistic_model.process(image)
            if results is not None:
                pose = np.array([[res.x, res.y, res.z, res.visibility] for res in results.pose_landmarks.landmark]).flatten() if results.pose_landmarks else np.zeros(33*4)
                face = np.array([[res.x, res.y, res.z] for res in results.face_landmarks.landmark]).flatten() if results.face_landmarks else np.zeros(468*3)
                lh = np.array([[res.x, res.y, res.z] for res in results.left_hand_landmarks.landmark]).flatten() if results.left_hand_landmarks else np.zeros(21*3)
                rh = np.array([[res.x, res.y, res.z] for res in results.right_hand_landmarks.landmark]).flatten() if results.right_hand_landmarks else np.zeros(21*3)
                data = np.concatenate([pose, face, lh, rh])
                sequence.append(data)
        if len(sequence) >= 30 and flag == True:
            sequence = sequence[-30:]
            predictec_value = self.model.predict(np.expand_dims(sequence, axis=0))[0]
            predictions = np.argmax(predictec_value)
            class_predicted = map_dictionary[predictions]
        return class_predicted