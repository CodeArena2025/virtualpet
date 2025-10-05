import pygame
import sys

# --- Setup ---
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Virtual Pet")

# Colors (RGB)
WHITE = (255, 255, 255)

# --- Load Assets ---

background = pygame.image.load("sunny background.png")
pet = pygame.image.load("kitty.png")


background = pygame.transform.scale(background, (WIDTH, HEIGHT))
pet = pygame.transform.scale(pet, (200, 200))


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

# --- pet stats (0-100) ---
health = 100.0 
happiness = 80.0
energy = 90.0
hunger = 100.0

# --- time ticking for stat decay (1/sec) ---
last_stat_tick = pygame.time.get_ticks()

# --- simple helper function ---
def clamp(v):
    if v < 0: return 0.00
    if v > 100: return 100.00
    return v

def draw_stat_bar(target_surface, stat_label, stat_value, pos_x, pos_y, bar_width=160, bar_height=18):
    # --- Colors and Normalization ---
    BAR_BG = (35, 35, 35)
    BORDER = (0, 0, 0)
    LOW_COLOR = (220, 40, 40)
    MID_COLOR = (220, 200, 40)
    HIGH_COLOR = (60, 200, 90)

    fill_ratio = max(0.0, min(1.0, stat_value/ 100.00))

    # --- interpolation
    if fill_ratio < 0.5:
        phase = fill_ratio / 0.5
        color_r = int(LOW_COLOR[0] + (MID_COLOR[0] - LOW_COLOR[0]) * phase)
        color_g = int(LOW_COLOR[1] + (MID_COLOR[1] - LOW_COLOR[1]) * phase)
        color_b = int(LOW_COLOR[2] + (MID_COLOR[2] - LOW_COLOR[2]) * phase)
    else:
        phase = (fill_ratio - 0.5) / 0.5
        color_r = int(MID_COLOR[0] + (HIGH_COLOR[0] - MID_COLOR[0]) * phase)
        color_g = int(MID_COLOR[1] + (HIGH_COLOR[1] - MID_COLOR[1]) * phase)
        color_b = int(MID_COLOR[2] + (HIGH_COLOR[2] - MID_COLOR[2]) * phase)
    
    # --- Draw the background ---
    pygame.draw.rect(target_surface, BAR_BG, (pos_x, pos_y, bar_width, bar_height), border_radius=5)

    # --- draw filling ---
    filled_width = int(bar_width * fill_ratio)
    if filled_width > 0:
        pygame.draw.rect(target_surface, (color_r, color_g, color_b), (pos_x, pos_y, filled_width, bar_height), border_radius=5)

    # --- border ---
    pygame.draw.rect(target_surface, BORDER, (pos_x, pos_y, bar_width, bar_height), 2, border_radius=5)

    # --- label ---
    label_surface = font.render(f"{stat_label}: {int(stat_value)}", True, WHITE)
    target_surface.blit(label_surface, (pos_x, pos_y -22))

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

    # --- Update stats ---
    now = pygame.time.get_ticks()
    if now - last_stat_tick >=1000: 
        last_stat_tick = now

        # --- natural decay ---
        hunger -= 2.5 
        energy -= 1.2
        happiness -= 0.6 

        # --- conditional effects
        if hunger < 35:
            health -= 1.2
            happiness -= 0.8
        if energy < 25:
            happiness -= 0.7
        if hunger > 70 and energy > 60 and health < 100:
            health += 0.8 

        # --- clamp values ---
        health = clamp(health)
        happiness = clamp(happiness)
        energy = clamp(energy)
        hunger = clamp(hunger)


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

    # --- Draw pet stats ---
    stats_x = 40
    stats_top = 60
    gap = 60
    draw_stat_bar(screen, "Health", health, stats_x, stats_top)
    draw_stat_bar(screen, "Happiness", happiness, stats_x, stats_top + gap)
    draw_stat_bar(screen, "Energy", energy, stats_x, stats_top + gap * 2)
    draw_stat_bar(screen, "Hunger", hunger, stats_x, stats_top + gap * 3)

    # -- Flash red overlay ---
    if health < 25 and (now //400) % 2 == 0:
        warn = pygame.Surface((WIDTH,HEIGHT), pygame.SRCALPHA)
        warn.fill((255,0,0,35))
        screen.blit(warn, (0,0))

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