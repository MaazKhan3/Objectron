import cv2
import numpy as np

# Load the pre-trained object detection model
# Replace 'PATH_TO_MODEL' with the path to your model file
net = cv2.CascadeClassifier('stop_data.xml')

# Initialize webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Preprocess the frame (resize, normalize, etc.)
    blob = cv2.dnn.blobFromImage(frame, scalefactor=1.0/255.0, size=(300, 300), mean=(0, 0, 0), swapRB=True, crop=False)

    # Pass the blob through the network to obtain detections
    net.setInput(blob)
    detections = net.forward()

    # Process detections
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.5:  # Adjust confidence threshold as needed
            # Extract bounding box coordinates
            box = detections[0, 0, i, 3:7] * np.array([frame.shape[1], frame.shape[0], frame.shape[1], frame.shape[0]])
            (startX, startY, endX, endY) = box.astype("int")

            # Draw bounding box around the detected object
            cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)

    # Display the annotated frame
    cv2.imshow('Object Detection', frame)

    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close all windows
cap.release()
cv2.destroyAllWindows()
