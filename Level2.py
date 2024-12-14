import pygame
import os
import numpy as np
import random  # Import random module for random jumps
import time  # Import time module for timing hammer throws

# Initialize Pygame
pygame.init()

# Set up the game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("The Revenge of the Hammer Bros: Power of Vengeance")

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
DARK_GRAY = (50, 50, 50)  # Updated platform color to match the background

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Player settings
player_width = 40  # Increased size for the player
player_height = 60  # Increased size for the player
player_x = 100
player_y = SCREEN_HEIGHT - player_height - 100  # Start position
player_velocity_x = 6
player_velocity_y = 0
player_color = GREEN

# Player lives
player_lives = 3

# Gravity settings
gravity = 1
jump_strength = -20
is_jumping = False
jump_cooldown = 0.3  # Cooldown time in seconds for jumping
last_jump_time = 0  # Last jump time

# Platform settings
platform_width = SCREEN_WIDTH
platform_height = 20
platform_x = 0
platform_y = SCREEN_HEIGHT - 100

# Additional platforms
platforms = [
    {"x": 50, "y": SCREEN_HEIGHT - 200, "width": 150, "height": 20},  # Left platform
    {"x": SCREEN_WIDTH - 200, "y": SCREEN_HEIGHT - 200, "width": 150, "height": 20},  # Right platform
    {"x": SCREEN_WIDTH // 2 - 100, "y": SCREEN_HEIGHT - 300, "width": 200, "height": 20},  # Center platform
]

# Enemy settings
enemy_width = 60  # Increased size for the enemy
enemy_height = 100  # Increased size for the enemy
enemy_x = 300
enemy_y = platform_y - enemy_height
enemy_velocity_x = 5  # Increase enemy speed to 5
enemy_color = RED
enemy_lives = 30  # Start with 30 health points for level three

# Enemy jump settings
enemy_gravity = 1
enemy_jump_strength = -20  # Increase jump strength to make enemy jump higher
enemy_velocity_y = 0
enemy_is_jumping = False
jump_timer = 0  # Used to trigger enemy jumps in a sequence
jump_sequence = [random.randint(60, 90) for _ in range(5)]  # Random jump sequence for level three
sequence_index = 0

# Hammer settings
hammers = []  # List to store active hammers
hammer_velocity_x = 7
hammer_velocity_y_initial = -15
last_hammer_time = 0  # Track the last time a hammer was thrown
hammer_cooldown = 0.3  # Cooldown time in seconds between throws

# Get current directory
current_dir = os.getcwd()
print(f"Current working directory: {current_dir}")

# Load player GIFs
idle_gif = pygame.image.load(os.path.join(current_dir, 'Turtle.gif'))
right_gif = pygame.image.load(os.path.join(current_dir, 'Turtle Right.gif'))
left_gif = pygame.image.load(os.path.join(current_dir, 'Turtle Left.gif'))
jump_gif = pygame.image.load(os.path.join(current_dir, 'Turtle jump.gif'))

# Resize player GIFs to match hitbox
idle_gif = pygame.transform.scale(idle_gif, (player_width, player_height))
right_gif = pygame.transform.scale(right_gif, (player_width, player_height))
left_gif = pygame.transform.scale(left_gif, (player_width, player_height))
jump_gif = pygame.transform.scale(jump_gif, (player_width, player_height))

# Load hammer GIF
hammer_gif = pygame.image.load(os.path.join(current_dir, 'Hammer in the AIR.gif'))

# Load background image
background_img = pygame.image.load(os.path.join(current_dir, 'Background Mario Game.jpeg'))
background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load and play music
pygame.mixer.music.load(os.path.join(current_dir, 'Mario Music Final Boss.mp3'))
pygame.mixer.music.play(-1)  # Loop the music indefinitely

# Load enemy GIFs
enemy_right_gif = pygame.image.load(os.path.join(current_dir, 'Mario Right.gif'))
enemy_left_gif = pygame.image.load(os.path.join(current_dir, 'Mario Left.gif'))
enemy_hurt_gif = pygame.image.load(os.path.join(current_dir, 'Mario Hurt.gif'))

# Resize enemy GIFs to match hitbox
enemy_right_gif = pygame.transform.scale(enemy_right_gif, (enemy_width, enemy_height))
enemy_left_gif = pygame.transform.scale(enemy_left_gif, (enemy_width, enemy_height))
enemy_hurt_gif = pygame.transform.scale(enemy_hurt_gif, (enemy_width, enemy_height))

# Player state
player_state = "idle"
# Enemy state
enemy_state = "right"

def show_start_screen():
    screen.blit(background_img, (0, 0))
    font = pygame.font.Font(None, 72)
    text = font.render("LEVEL 2", True, WHITE)
    tutorial_font = pygame.font.Font(None, 36)
    tutorial_text = [
        "Controls:",
        "A/D: Move Left/Right",
        "SPACE: Jump",
        "W: Throw Hammer",
        "R: Dash",
    ]
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 4))
    for i, line in enumerate(tutorial_text):
        tutorial_line = tutorial_font.render(line, True, WHITE)
        screen.blit(tutorial_line, (SCREEN_WIDTH // 2 - tutorial_line.get_width() // 2, SCREEN_HEIGHT // 2 + i * 40))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False

def show_game_over_screen():
    screen.blit(background_img, (0, 0))
    font = pygame.font.Font(None, 72)
    text = font.render("GAME OVER", True, WHITE)
    retry_font = pygame.font.Font(None, 36)
    retry_text = retry_font.render("Press SPACE to Retry", True, WHITE)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 4))
    screen.blit(retry_text, (SCREEN_WIDTH // 2 - retry_text.get_width() // 2, SCREEN_HEIGHT // 2))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False

def show_victory_screen():
    screen.blit(background_img, (0, 0))
    font = pygame.font.Font(None, 72)
    text = font.render("CONGRATULATIONS!", True, WHITE)
    subtext_font = pygame.font.Font(None, 36)
    subtext = subtext_font.render("You avenged your brother!", True, WHITE)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 4))
    screen.blit(subtext, (SCREEN_WIDTH // 2 - subtext.get_width() // 2, SCREEN_HEIGHT // 2))
    pygame.display.flip()
    pygame.time.wait(5000)  # Show the victory screen for 5 seconds

# Show the start screen
show_start_screen()

# Main game loop
running = True
last_dash_time = 0  # Track the last time a dash was used
dash_cooldown = 1  # Cooldown time in seconds for dash
dash_distance = 100  # Distance covered in dash
invincible = False  # Flag to track if the player is invincible
facing_direction = "right"  # Track the direction the player is facing

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get keys pressed
    keys = pygame.key.get_pressed()

    # Dash movement
    current_time = time.time()
    if keys[pygame.K_r] and current_time - last_dash_time > dash_cooldown:
        if facing_direction == "left":
            player_x -= dash_distance
        elif facing_direction == "right":
            player_x += dash_distance
        last_dash_time = current_time

    # Activate invincibility if 'i' is pressed
    if keys[pygame.K_i]:
        invincible = True

    # Horizontal movement
    if keys[pygame.K_a]:
        player_x -= player_velocity_x
        facing_direction = "left"
        player_state = "left"
    elif keys[pygame.K_d]:
        player_x += player_velocity_x
        facing_direction = "right"
        player_state = "right"
    else:
        player_state = "idle"

    # Prevent player from going outside the screen boundaries
    if player_x < 0:
        player_x = 0
    if player_x + player_width > SCREEN_WIDTH:
        player_x = SCREEN_WIDTH - player_width

    # Jumping
    if keys[pygame.K_SPACE] and not is_jumping and current_time - last_jump_time > jump_cooldown:
        player_velocity_y = jump_strength
        is_jumping = True
        player_state = "jump"
        last_jump_time = current_time

    # Throw hammer with cooldown
    if keys[pygame.K_w] and current_time - last_hammer_time > hammer_cooldown:
        hammer = {
            "x": player_x + (player_width // 2),
            "y": player_y,
            "vx": hammer_velocity_x if facing_direction == "right" else -hammer_velocity_x,
            "vy": hammer_velocity_y_initial,
            "angle": 0  # Initialize rotation angle
        }
        hammers.append(hammer)
        last_hammer_time = current_time

    # Apply gravity
    player_velocity_y += gravity
    player_y += player_velocity_y

    # Collision with main platform
    if player_y + player_height >= platform_y:
        player_y = platform_y - player_height
        player_velocity_y = 0
        is_jumping = False

    # Collision with additional platforms
    for platform in platforms:
        if (platform["x"] < player_x + player_width and
            player_x < platform["x"] + platform["width"] and
            player_y + player_height >= platform["y"] and
            player_y + player_height <= platform["y"] + platform["height"]):
            player_y = platform["y"] - player_height
            player_velocity_y = 0
            is_jumping = False

    # Move the enemy
    enemy_x += enemy_velocity_x
    if enemy_velocity_x > 0:
        enemy_state = "right"
    else:
        enemy_state = "left"

    # Reverse direction if enemy reaches the edge of the platform
    if enemy_x < 0 or enemy_x + enemy_width > SCREEN_WIDTH:
        enemy_velocity_x *= -1

    # Trigger enemy jumps in a specific loop pattern
    jump_timer += 1
    if jump_timer >= jump_sequence[sequence_index]:
        if not enemy_is_jumping:
            enemy_velocity_y = enemy_jump_strength
            enemy_is_jumping = True
            jump_timer = 0
            sequence_index = (sequence_index + 1) % len(jump_sequence)

    # Apply gravity to the enemy
    enemy_velocity_y += enemy_gravity
    enemy_y += enemy_velocity_y

    # Collision with main platform for enemy
    if enemy_y + enemy_height >= platform_y:
        enemy_y = platform_y - enemy_height
        enemy_velocity_y = 0
        enemy_is_jumping = False

    # Collision with additional platforms for enemy
    for platform in platforms:
        if (platform["x"] < enemy_x + enemy_width and
            enemy_x < platform["x"] + platform["width"] and
            enemy_y + enemy_height >= platform["y"] and
            enemy_y + enemy_height <= platform["y"] + platform["height"]):
            enemy_y = platform["y"] - enemy_height
            enemy_velocity_y = 0
            enemy_is_jumping = False

    # Update hammers
    for hammer in hammers[:]:
        hammer["x"] += hammer["vx"]
        hammer["y"] += hammer["vy"]
        hammer["vy"] += gravity
        hammer["angle"] += 10  # Rotate hammer

        # Remove hammers that go off-screen
        if hammer["x"] < 0 or hammer["x"] > SCREEN_WIDTH or hammer["y"] > SCREEN_HEIGHT:
            hammers.remove(hammer)

    # Check hammer collision with enemy
    for hammer in hammers[:]:
        if (enemy_x < hammer["x"] < enemy_x + enemy_width and
            enemy_y < hammer["y"] < enemy_y + enemy_height):
            enemy_lives -= 1
            hammers.remove(hammer)
            enemy_state = "hurt"
            break

    # Check for victory condition
    if enemy_lives <= 0:
        show_victory_screen()
        running = False

    # Collision with enemy
    if not invincible and (player_x < enemy_x + enemy_width and
        player_x + player_width > enemy_x and
        player_y < enemy_y + enemy_height and
        player_y + player_height > enemy_y):
        player_lives -= 1
        if player_lives > 0:
            # Respawn player at the opposite side of the enemy
            if enemy_x < SCREEN_WIDTH / 2:
                player_x = SCREEN_WIDTH - player_width - 10
            else:
                player_x = 10
            player_y = SCREEN_HEIGHT - player_height - 100
        else:
            show_game_over_screen()
            player_lives = 3
            enemy_lives = 30
            player_x = 100
            player_y = SCREEN_HEIGHT - player_height - 100
            enemy_x = 300
            enemy_y = platform_y - enemy_height

    # Fill screen with background image
    screen.blit(background_img, (0, 0))

    # Draw the main platform
    pygame.draw.rect(screen, DARK_GRAY, (platform_x, platform_y, platform_width, platform_height))

    # Draw additional platforms
    for platform in platforms:
        pygame.draw.rect(screen, DARK_GRAY, (platform["x"], platform["y"], platform["width"], platform["height"]))

    # Draw the enemy using GIFs
    if enemy_state == "right":
        screen.blit(enemy_right_gif, (enemy_x, enemy_y))
    elif enemy_state == "left":
        screen.blit(enemy_left_gif, (enemy_x, enemy_y))
    elif enemy_state == "hurt":
        screen.blit(enemy_hurt_gif, (enemy_x, enemy_y))

    # Draw enemy life bar at the top of the screen
    pygame.draw.rect(screen, BLACK, (10, 50, SCREEN_WIDTH - 20, 20))  # Background of health bar
    pygame.draw.rect(screen, RED, (10, 50, (SCREEN_WIDTH - 20) * (enemy_lives / 30), 20))  # Health bar in red

    # Draw the player using GIFs
    if player_state == "idle":
        screen.blit(idle_gif, (player_x, player_y))
    elif player_state == "right":
        screen.blit(right_gif, (player_x, player_y))
    elif player_state == "left":
        screen.blit(left_gif, (player_x, player_y))
    elif player_state == "jump":
        screen.blit(jump_gif, (player_x, player_y))

    # Draw hammers
    for hammer in hammers:
        rotated_hammer = pygame.transform.rotate(hammer_gif, hammer["angle"])
        screen.blit(rotated_hammer, (hammer["x"], hammer["y"]))

    # Font settings to display lives
    font = pygame.font.Font(None, 36)
    lives_text = font.render(f"Lives: {player_lives}", True, BLACK)
    screen.blit(lives_text, (10, 10))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)  # 60 FPS

# Quit Pygame
pygame.quit()
