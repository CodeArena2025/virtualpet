import pygame
import sys

# --- Setup ---
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Virtual Pet - Episode 1")

# Colors (RGB)
WHITE = (255, 255, 255)

# --- Load Assets ---
background = pygame.image.load("sunny background.png")
pet = pygame.image.load("kitty.png")

# Optional: scale images to fit nicely
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
pet = pygame.transform.scale(pet, (200, 200))

# Pet position (centered)
pet_x = WIDTH // 2 - pet.get_width() // 2
pet_y = HEIGHT // 2 - pet.get_height() // 2 + 100 


# --- Button Setup ---
button_width, button_height = 100, 40
button_x = WIDTH - button_width - 20  
button_y = 20  # 20px from top edge
button_color = (200, 50, 50)
button_hover_color = (255, 80, 80)
font = pygame.font.SysFont(None, 32)
button_text = font.render("Quit", True, WHITE)

# --- Game Loop ---
running = True
while running:
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if (button_x <= mouse_pos[0] <= button_x + button_width and
                button_y <= mouse_pos[1] <= button_y + button_height):
                running = False

    # Draw background
    screen.blit(background, (0, 0))

    # Draw pet
    screen.blit(pet, (pet_x, pet_y))

    # Draw quit button
    if button_x <= mouse_pos[0] <= button_x + button_width and button_y <= mouse_pos[1] <= button_y + button_height:
        color = button_hover_color
    else:
        color = button_color
    pygame.draw.rect(screen, color, (button_x, button_y, button_width, button_height), border_radius=8)
    text_rect = button_text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
    screen.blit(button_text, text_rect)

    # Update display
    pygame.display.flip()

# --- Cleanup ---
pygame.quit()
sys.exit()
