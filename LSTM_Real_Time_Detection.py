from modules.mediapipe_functions import *
from modules.opencv_functions import *
from modules.tensorflow_functions import *

def real_time_conection(lstm_model):
    holistic_model = get_holistic_model(0.5, 0.5)
    captura = real_time_detector()
    sequence, predictions, min_value = [], [], 0.7
    try:
        while captura.isOpened():
            ret, frame = captura.read()
            if ret == True:
                flag = wait_keys_detector(captura)
                if flag == True:
                    break
                image, results = mediapipe_detector(frame, holistic_model)
                if results is not None:
                    draw_styled_landmarks(image, results)
                    hand_flag = hand_detector(results)
                    input_vector = keypoints_values(results)
                    print(input_vector)
                    sequence.append(input_vector)
                    sequence = sequence[-30:]
                    if len(sequence) == 30 and hand_flag == True:
                    #if len(sequence) == 30:
                        predictec_value = make_predictions(lstm_model, sequence)
                        class_predicted = map_predictions(np.argmax(predictec_value))
                        predictions.append(np.argmax(predictec_value))
                        if np.unique(predictions[-10:])[0] == np.argmax(predictec_value):
                            if predictec_value[np.argmax(predictec_value)] > min_value:
                                cv2.putText(image, class_predicted, (3,30),  cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                show_window('Captura original', frame)
    finally:
        holistic_model.close()

if __name__ == "__main__":
    lstm_model = load_lstm()
    real_time_conection(lstm_model)
    print("Ejecución finalizada...")