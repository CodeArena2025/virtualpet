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

# --- Game Loop ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw background
    screen.blit(background, (0, 0))

    # Draw pet
    screen.blit(pet, (pet_x, pet_y))

    # Update display
    pygame.display.flip()

# --- Cleanup ---
pygame.quit()
sys.exit()
