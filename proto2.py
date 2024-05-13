import cv2
import mediapipe as mp
import time
import pygame

# Initialize Pygame
pygame.init()

# Define colors
WHITE = (100, 0, 0)
BLACK = (20, 20, 20)
GRAY = (220, 22, 60)

# Define screen dimensions
SCREEN_WIDTH = 1366
SCREEN_HEIGHT = 768

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
pygame.display.set_caption("Objectron")

# Main menu buttons
class MenuButton:
    def __init__(self, text, position):
        self.text = text
        self.position = position
        self.rect = pygame.Rect(position[0], position[1], 200, 50)

    def draw(self, screen):
        pygame.draw.rect(screen, GRAY, self.rect)
        font = pygame.font.SysFont(None, 36)
        text_render = font.render(self.text, True, BLACK)
        text_rect = text_render.get_rect(center=self.rect.center)
        screen.blit(text_render, text_rect)

# Main menu
main_menu_buttons = [
    MenuButton("Select Object", (SCREEN_WIDTH//2 - 100, 300)),
    MenuButton("Instructions", (SCREEN_WIDTH//2 - 100, 400)),
    MenuButton("Exit", (SCREEN_WIDTH//2 - 100, 500))
]

# Object selection buttons
object_buttons = [
    MenuButton("Detect Shoes", (SCREEN_WIDTH//2 - 100, 250)),
    MenuButton("Detect Cups", (SCREEN_WIDTH//2 - 100, 350)),
    MenuButton("Detect Cameras", (SCREEN_WIDTH//2 - 100, 450)),
]

# Display instructions
instructions = [
    "Instructions:",
    "- Press 'Select Object' to choose the object you want to detect.",
    "- After selecting the desired object, a webcam feed will pop open.",
    "- Hold your object steady in front of the webcam",
    "- To exit the webcam feed, press esc.",
    "- Press 'Backspace' to return to the main menu.",
    "- Press 'Exit' to close the program."
]

# Main loop
running = True
display_object_buttons = False
display_instructions = False
while running:
    screen.fill(WHITE)

    # Draw border
    pygame.draw.rect(screen, BLACK, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 40)

    if display_object_buttons:
        for button in object_buttons:
            button.draw(screen)
        # Draw heading
        font_heading = pygame.font.SysFont(None, 72)
        text_heading = font_heading.render("Objectron", True, BLACK)
        text_heading_rect = text_heading.get_rect(center=(SCREEN_WIDTH//2, 150))
        screen.blit(text_heading, text_heading_rect)
    elif display_instructions:
        # Draw heading
        font_heading = pygame.font.SysFont(None, 72)
        text_heading = font_heading.render("Objectron", True, BLACK)
        text_heading_rect = text_heading.get_rect(center=(SCREEN_WIDTH//2, 150))
        screen.blit(text_heading, text_heading_rect)
        # Draw instructions
        font_instructions = pygame.font.SysFont(None, 24)
        for i, instruction in enumerate(instructions):
            text_instructions = font_instructions.render(instruction, True, BLACK)
            text_instructions_rect = text_instructions.get_rect(left=50, top=200 + i * 30)
            screen.blit(text_instructions, text_instructions_rect)
    else:
        for button in main_menu_buttons:
            button.draw(screen)
        # Draw heading
        font_heading = pygame.font.SysFont(None, 72)
        text_heading = font_heading.render("Objectron", True, BLACK)
        text_heading_rect = text_heading.get_rect(center=(SCREEN_WIDTH//2, 150))
        screen.blit(text_heading, text_heading_rect)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if display_object_buttons:
                for button in object_buttons:
                    if button.rect.collidepoint(mouse_pos):
                        if button.text == "Detect Shoes":
                            detect_object('Shoe')
                        elif button.text == "Detect Cups":
                            detect_object('Cup')
                        elif button.text == "Detect Cameras":
                            detect_object('Camera')
            elif display_instructions:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
                    display_instructions = False
            else:
                for button in main_menu_buttons:
                    if button.rect.collidepoint(mouse_pos):
                        if button.text == "Select Object":
                            display_object_buttons = True
                        elif button.text == "Instructions":
                            display_instructions = True
                        elif button.text == "Exit":
                            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                if display_object_buttons or display_instructions:
                    display_object_buttons = False
                    display_instructions = False

    pygame.display.flip()