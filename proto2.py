import cv2
import mediapipe as mp
import time
import pygame

# Initialize Pygame
pygame.init()

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)

# Define screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Initialize MediaPipe
mp_objectron = mp.solutions.objectron
mp_drawing = mp.solutions.drawing_utils

# Function to detect objects (generic)
def detect_object(model_name):
    with mp_objectron.Objectron(static_image_mode=False,
                                max_num_objects=2,
                                min_detection_confidence=0.5,
                                min_tracking_confidence=0.8,
                                model_name=model_name) as objectron:
        while cap.isOpened():
            success, image = cap.read()
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
            cv2.putText(image, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1.5, (0, 255, 0), 2)
            cv2.imshow('MediaPipe Objectron', image)

            key = cv2.waitKey(1)
            if key == 27:  # ESC key
                cv2.destroyAllWindows()  # Close cv2 window
                return  # Return to main loop

    return  # Optional: Code to run after closing cv2 window (outside the loop)

# Set up Pygame display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Object Detection")

# Main loop
running = True
while running:
    screen.fill(WHITE)

    # Draw buttons
    shoe_button = pygame.draw.rect(screen, GRAY, (50, 50, 200, 50))
    cup_button = pygame.draw.rect(screen, GRAY, (50, 150, 200, 50))
    camera_button = pygame.draw.rect(screen, GRAY, (50, 250, 200, 50))

    # Add text to buttons
    font = pygame.font.SysFont(None, 36)
    shoe_text = font.render("Detect Shoes", True, BLACK)
    cup_text = font.render("Detect Cups", True, BLACK)
    camera_text = font.render("Detect Cameras", True, BLACK)
    screen.blit(shoe_text, (70, 60))
    screen.blit(cup_text, (70, 160))
    screen.blit(camera_text, (70, 260))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if shoe_button.collidepoint(mouse_pos):
                detect_object('Shoe')  # Call generic function with model name
            elif cup_button.collidepoint(mouse_pos):
                detect_object('Cup')
            elif camera_button.collidepoint(mouse_pos):
                detect_object('Camera')

    pygame.display.flip()

