import cv2

def real_time_detector():
    detector = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not detector.isOpened():
        print("Sin conexión a la cámara")
        return None
    else:
        print("Conexión realizada")
        return detector
    
def wait_keys_detector(captura):
    if cv2.waitKey(1) & 0xFF == ord('q'):
        captura.release()
        cv2.destroyAllWindows()
        return True

def show_window(name_window = "Real Time", video = None):
    cv2.imshow(name_window, video)
    return None