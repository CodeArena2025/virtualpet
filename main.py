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
# Replace with your own images
background = pygame.image.load("sunny background.png")
pet = pygame.image.load("kitty.png")

# Optional: scale images to fit nicely
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
pet = pygame.transform.scale(pet, (200, 200))

# Pet position (centered)
pet_x = WIDTH // 2 - pet.get_width() // 2
pet_y = HEIGHT // 2 - pet.get_height() // 2 + 100 



# --- Quit Button Setup ---
quit_button_width, quit_button_height = 100, 40
quit_button_x = WIDTH - quit_button_width - 20  
quit_button_y = 20  
quit_button_color = (200, 50, 50)
quit_button_hover_color = (255, 80, 80)
font = pygame.font.SysFont(None, 32)
quit_button_text = font.render("Quit", True, WHITE)

# --- SPEAK Button Setup ---
speak_button_width, speak_button_height = 120, 50
speak_button_x = WIDTH // 2 - speak_button_width // 2
speak_button_y = HEIGHT - speak_button_height - 30  # 30px from bottom
speak_button_color = (50, 120, 200)
speak_button_hover_color = (80, 180, 255)
speak_button_text = font.render("SPEAK", True, WHITE)

# --- Speech Bubble Setup ---
bubble_font = pygame.font.SysFont(None, 36)
bubble_text = bubble_font.render("MEOW", True, (0,0,0))
bubble_show = False
bubble_timer = 0

# --- Game Loop ---
running = True
clock = pygame.time.Clock()
while running:
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Quit button
            if (quit_button_x <= mouse_pos[0] <= quit_button_x + quit_button_width and
                quit_button_y <= mouse_pos[1] <= quit_button_y + quit_button_height):
                running = False
            # SPEAK button
            if (speak_button_x <= mouse_pos[0] <= speak_button_x + speak_button_width and
                speak_button_y <= mouse_pos[1] <= speak_button_y + speak_button_height):
                bubble_show = True
                bubble_timer = pygame.time.get_ticks()

    # Draw background
    screen.blit(background, (0, 0))

    # Draw pet
    screen.blit(pet, (pet_x, pet_y))

    # Draw quit button
    if quit_button_x <= mouse_pos[0] <= quit_button_x + quit_button_width and quit_button_y <= mouse_pos[1] <= quit_button_y + quit_button_height:
        color = quit_button_hover_color
    else:
        color = quit_button_color
    pygame.draw.rect(screen, color, (quit_button_x, quit_button_y, quit_button_width, quit_button_height), border_radius=8)
    text_rect = quit_button_text.get_rect(center=(quit_button_x + quit_button_width // 2, quit_button_y + quit_button_height // 2))
    screen.blit(quit_button_text, text_rect)

    # Draw SPEAK button
    if speak_button_x <= mouse_pos[0] <= speak_button_x + speak_button_width and speak_button_y <= mouse_pos[1] <= speak_button_y + speak_button_height:
        speak_color = speak_button_hover_color
    else:
        speak_color = speak_button_color
    pygame.draw.rect(screen, speak_color, (speak_button_x, speak_button_y, speak_button_width, speak_button_height), border_radius=8)
    speak_text_rect = speak_button_text.get_rect(center=(speak_button_x + speak_button_width // 2, speak_button_y + speak_button_height // 2))
    screen.blit(speak_button_text, speak_text_rect)

    # Draw speech bubble if needed
    if bubble_show:
        # Show for 1 second
        if pygame.time.get_ticks() - bubble_timer < 1000:
            bubble_w, bubble_h = 120, 60
            bubble_x = pet_x + pet.get_width()//2 - bubble_w//2
            bubble_y = pet_y - bubble_h - 20
            pygame.draw.ellipse(screen, (255,255,255), (bubble_x, bubble_y, bubble_w, bubble_h))
            pygame.draw.ellipse(screen, (0,0,0), (bubble_x, bubble_y, bubble_w, bubble_h), 2)
            bubble_text_rect = bubble_text.get_rect(center=(bubble_x + bubble_w//2, bubble_y + bubble_h//2))
            screen.blit(bubble_text, bubble_text_rect)
        else:
            bubble_show = False

    # Update display
    pygame.display.flip()
    clock.tick(60)

# --- Cleanup ---
pygame.quit()
sys.exit()
