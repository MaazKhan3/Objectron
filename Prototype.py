import cv2
from matplotlib import pyplot as plt

# Load the stop sign cascade classifier
stop_data = cv2.CascadeClassifier('CP_OFF_1_jpg.rf.75addc61c77442373471eac3895766db.xml')

# Initialize the webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect stop signs in the frame
    found = stop_data.detectMultiScale(gray, minSize=(20, 20))

    # Draw bounding boxes around detected stop signs
    for (x, y, width, height) in found:
        cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 255, 0), 5)

    # Display the annotated frame
    cv2.imshow('Stop Sign Detection', frame)

    # Check for the 'q' key to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture
cap.release()
cv2.destroyAllWindows()

