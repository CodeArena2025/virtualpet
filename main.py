import pygame
import sys
import math

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

# --- Load (optional) run animation frames ---
run_frame_paths = [
    "assets/kitty_run_side/kitty_run_1.png",
    "assets/kitty_run_side/kitty_run_2.png"
]
run_frames = []
for p in run_frame_paths:
    try:
        f = pygame.image.load(p)
        f = pygame.transform.scale(f, (200, 200))
        run_frames.append(f)
    except Exception:
        # Silently ignore missing files; we'll fallback later
        pass
# --- Fallback logic so animation is always visible ---
if len(run_frames) == 0:
    # no external frames -> just use the same sprite twice (animation will be visible via movement and bob)
    run_frames = [pet, pet]
    print("[RUN] No run sprite frames found. Using same sprite for both frames (animation visible via movement). Add kitty_run_1.png & kitty_run_2.png to assets/kitty_run_side/")
elif len(run_frames) == 1:
    # only one frame -> just duplicate it
    run_frames.append(run_frames[0])
    print("[RUN] Only one run frame found. Duplicated for animation. Add the second file for smoother animation.")


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

# --- RUN Button Setup ---
run_button_width, run_button_height = 140, 50
run_button_x = speak_button_x - run_button_width - 20
run_button_y = speak_button_y
run_button_color = (40, 170, 90)
run_button_hover_color = (70, 220, 130)
run_button_text = font.render("RUN", True, WHITE)

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

# --- Run animation state ---
is_running = False
run_start_time = 0
run_duration = 2400  # ms total running time (3 stages x 800ms)
current_run_frame = 0
last_run_frame_switch = 0
run_frame_interval = 120  # ms between frames

# --- Running movement ---
run_origin_x = 0
run_center_x = 0  # center position to return to
run_stage = 0  # 0=to left, 1=to right, 2=back to center
run_stage_start_time = 0
run_stage_duration = 800  # ms per stage
run_current_start_x = 0
run_current_target_x = 0

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
            # RUN button
            if (run_button_x <= mouse_pos[0] <= run_button_x + run_button_width and
                run_button_y <= mouse_pos[1] <= run_button_y + run_button_height):
                if not is_running:  # start only if not already running
                    pet_width = pet.get_width()
                    
                    # Store center position to return to
                    run_center_x = pet_x
                    
                    # Initialize 3-stage run: left → right → center
                    run_stage = 0
                    run_stage_start_time = pygame.time.get_ticks()
                    run_start_time = run_stage_start_time
                    
                    # Stage 0: Go to left edge
                    run_current_start_x = pet_x
                    run_current_target_x = 0
                    
                    is_running = True
                    current_run_frame = 0
                    last_run_frame_switch = run_stage_start_time
                    
                    print(f"[RUN] Started 3-stage run sequence: left→right→center with {len(run_frames)} frame(s)")

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

    # --- Decide which pet frame to draw ---
    pet_image = pet
    pet_draw_x = pet_x
    pet_draw_y = pet_y
    if is_running:
        now_time = pygame.time.get_ticks()
        elapsed = now_time - run_start_time
        stage_elapsed = now_time - run_stage_start_time
        
        # switch frames
        if now_time - last_run_frame_switch >= run_frame_interval:
            current_run_frame = (current_run_frame + 1) % len(run_frames)
            last_run_frame_switch = now_time
        pet_image = run_frames[current_run_frame]

        # Check if current stage is complete
        if stage_elapsed >= run_stage_duration:
            # Move to next stage
            pet_x = run_current_target_x  # snap to target
            run_stage += 1
            run_stage_start_time = now_time
            run_current_start_x = pet_x
            
            pet_width = pet.get_width()
            if run_stage == 1:
                # Stage 1: Go to right edge
                run_current_target_x = WIDTH - pet_width
                print("[RUN] Stage 1: Moving to right edge")
            elif run_stage == 2:
                # Stage 2: Go back to center
                run_current_target_x = run_center_x
                print("[RUN] Stage 2: Returning to center")
            else:
                # All stages complete
                pet_x = run_center_x
                is_running = False
                print("[RUN] 3-stage sequence completed!")
                
        if is_running:
            # Calculate movement within current stage
            stage_progress = min(1.0, stage_elapsed / run_stage_duration)
            stage_distance = run_current_target_x - run_current_start_x
            pet_draw_x = int(run_current_start_x + stage_distance * stage_progress)

            # subtle vertical bob for life
            pet_draw_y = pet_y - int(6 * math.sin(elapsed / 110))

    # Draw pet (current frame)
    screen.blit(pet_image, (pet_draw_x, pet_draw_y))

    # Draw quit button
    if quit_button_x <= mouse_pos[0] <= quit_button_x + quit_button_width and quit_button_y <= mouse_pos[1] <= quit_button_y + quit_button_height:
        color = quit_button_hover_color
    else:
        color = quit_button_color
    pygame.draw.rect(screen, color, (quit_button_x, quit_button_y, quit_button_width, quit_button_height), border_radius=8)
    text_rect = quit_button_text.get_rect(center=(quit_button_x + quit_button_width // 2, quit_button_y + quit_button_height // 2))
    screen.blit(quit_button_text, text_rect)

    # Draw RUN button
    if run_button_x <= mouse_pos[0] <= run_button_x + run_button_width and run_button_y <= mouse_pos[1] <= run_button_y + run_button_height:
        rb_color = run_button_hover_color
    else:
        rb_color = run_button_color
    pygame.draw.rect(screen, rb_color, (run_button_x, run_button_y, run_button_width, run_button_height), border_radius=8)
    run_text_rect = run_button_text.get_rect(center=(run_button_x + run_button_width // 2, run_button_y + run_button_height // 2))
    screen.blit(run_button_text, run_text_rect)

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
            bubble_x = pet_draw_x + pet_image.get_width()//2 - bubble_w//2
            bubble_y = pet_draw_y - bubble_h - 20
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