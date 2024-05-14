import socket


# Function to send a command to the server
def send_command(command):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 65432))
    client_socket.sendall(command.encode())
    client_socket.close()


# Pygame and GUI code (simplified for clarity)
import pygame

# Initialize Pygame
pygame.init()

# Define colors
WHITE = (0, 60, 67)
BLACK = (119, 176, 170)
GRAY = (19, 93, 102)

# Define screen dimensions
SCREEN_WIDTH = 1366
SCREEN_HEIGHT = 768

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
    MenuButton("Detect Shoes", (SCREEN_WIDTH // 2 - 100, 300)),
    MenuButton("Detect Cups", (SCREEN_WIDTH // 2 - 100, 400)),
    MenuButton("Detect Cameras", (SCREEN_WIDTH // 2 - 100, 500)),
    MenuButton("Exit", (SCREEN_WIDTH // 2 - 100, 600))
]

# Main loop
running = True
while running:
    screen.fill(WHITE)

    # Draw border
    pygame.draw.rect(screen, BLACK, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 40)

    for button in main_menu_buttons:
        button.draw(screen)

    # Draw heading
    font_heading = pygame.font.SysFont(None, 72)
    text_heading = font_heading.render("Objectron", True, BLACK)
    text_heading_rect = text_heading.get_rect(center=(SCREEN_WIDTH // 2, 150))
    screen.blit(text_heading, text_heading_rect)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for button in main_menu_buttons:
                if button.rect.collidepoint(mouse_pos):
                    if button.text == "Detect Shoes":
                        send_command('shoes')
                    elif button.text == "Detect Cups":
                        send_command('cups')
                    elif button.text == "Detect Cameras":
                        send_command('cameras')
                    elif button.text == "Exit":
                        send_command('exit')
                        running = False

    pygame.display.flip()

pygame.quit()
