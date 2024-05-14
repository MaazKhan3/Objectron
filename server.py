import socket
import cv2
import mediapipe as mp
import time

# Initialize MediaPipe
mp_objectron = mp.solutions.objectron
mp_drawing = mp.solutions.drawing_utils

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Function to detect objects (generic)
def detect_object(model_name):
    with mp_objectron.Objectron(static_image_mode=False,
                                max_num_objects=2,
                                min_detection_confidence=0.5,
                                min_tracking_confidence=0.8,
                                model_name=model_name) as objectron:
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                break

            start = time.time()
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = objectron.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            if results.detected_objects:
                for detected_objects in results.detected_objects:
                    mp_drawing.draw_landmarks(image, detected_objects.landmarks_2d, mp_objectron.BOX_CONNECTIONS)
                    mp_drawing.draw_axis(image, detected_objects.rotation, detected_objects.translation)

            end = time.time()
            totaltime = end - start
            fps = 1 / totaltime
            cv2.putText(image, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2)
            cv2.imshow('MediaPipe Objectron', image)

            key = cv2.waitKey(1)
            if key == 27:  # ESC key
                break

        cap.release()
        cv2.destroyAllWindows()

# Create socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 65432))
server_socket.listen(1)

print("Server is waiting for connections...")

while True:
    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address}")

    while True:
        data = client_socket.recv(1024).decode()
        if not data:
            break
        print(f"Received command: {data}")

        if data == 'shoes':
            detect_object('Shoe')
        elif data == 'cups':
            detect_object('Cup')
        elif data == 'cameras':
            detect_object('Camera')
        elif data == 'exit':
            break

    client_socket.close()
    if data == 'exit':
        break

server_socket.close()
