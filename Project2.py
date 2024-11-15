import pygame
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

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Player settings
player_width = 30
player_height = 30
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

# Platform settings
platform_width = SCREEN_WIDTH
platform_height = 20
platform_x = 0
platform_y = SCREEN_HEIGHT - 100

# Small platform settings
small_platform_width = 150
small_platform_height = 20
small_platform_x = SCREEN_WIDTH // 2 - small_platform_width // 2
small_platform_y = SCREEN_HEIGHT - 250

# Enemy settings
enemy_width = 60
enemy_height = 60
enemy_x = 300
enemy_y = platform_y - enemy_height
enemy_velocity_x = 5  # Increase enemy speed to 5
enemy_color = RED
enemy_lives = 10  # Start with 10 health points for level one

# Enemy jump settings
enemy_gravity = 1
enemy_jump_strength = -20  # Increase jump strength to make enemy jump higher
enemy_velocity_y = 0
enemy_is_jumping = False
jump_timer = 0  # Used to trigger enemy jumps in a sequence
jump_sequence = [60, 60, 90]  # Frames equivalent to 1 second, 1 second, and 1.5 seconds at 60 FPS
sequence_index = 0

# Hammer settings
hammers = []  # List to store active hammers
hammer_width = 10
hammer_height = 10
hammer_velocity = 10
last_hammer_time = 0  # Track the last time a hammer was thrown
hammer_cooldown = 0.3  # Cooldown time in seconds between throws

# Function to display start screen
def start_screen():
    screen.fill(WHITE)
    font = pygame.font.Font(None, 74)
    text = font.render("Level One", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))

    font = pygame.font.Font(None, 36)
    text = font.render("Press SPACE to Start", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 + 20))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False

# Function to display victory screen
def victory_screen():
    screen.fill(WHITE)
    font = pygame.font.Font(None, 74)
    text = font.render("Congratulations!", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))

    font = pygame.font.Font(None, 36)
    text = font.render("Press SPACE to Start Level Two", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 + 20))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False

# Display the start screen
start_screen()

# Main game loop
running = True
facing_direction = "right"  # Track the direction the player is facing
level = 1  # Start at level one

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get keys pressed
    keys = pygame.key.get_pressed()

    # Horizontal movement
    if keys[pygame.K_LEFT]:
        player_x -= player_velocity_x
        facing_direction = "left"
    if keys[pygame.K_RIGHT]:
        player_x += player_velocity_x
        facing_direction = "right"

    # Prevent player from going outside the screen boundaries
    if player_x < 0:
        player_x = 0
    if player_x + player_width > SCREEN_WIDTH:
        player_x = SCREEN_WIDTH - player_width

    # Jumping
    if keys[pygame.K_SPACE] and not is_jumping:
        player_velocity_y = jump_strength
        is_jumping = True

    # Drop down through small platform (only in level two)
    if level == 2 and keys[pygame.K_DOWN] and (small_platform_x < player_x < small_platform_x + small_platform_width) and (player_y + player_height == small_platform_y):
        player_y += 5  # Move the player down slightly to allow dropping through the platform

    # Throw hammer with cooldown
    current_time = time.time()
    if keys[pygame.K_v] and current_time - last_hammer_time > hammer_cooldown:
        if facing_direction == "left":
            hammers.append({"x": player_x, "y": player_y + player_height // 2, "vx": -hammer_velocity, "vy": 0})
        elif facing_direction == "right":
            hammers.append({"x": player_x + player_width, "y": player_y + player_height // 2, "vx": hammer_velocity, "vy": 0})
        last_hammer_time = current_time

    # Throw hammer upward with cooldown
    if keys[pygame.K_b] and current_time - last_hammer_time > hammer_cooldown:
        hammers.append({"x": player_x + player_width // 2, "y": player_y, "vx": 0, "vy": -hammer_velocity})
        last_hammer_time = current_time

    # Apply gravity
    player_velocity_y += gravity
    player_y += player_velocity_y

    # Collision with main platform
    if player_y + player_height >= platform_y:
        player_y = platform_y - player_height
        player_velocity_y = 0
        is_jumping = False

    # Collision with small platform (only in level two)
    if level == 2 and (small_platform_x < player_x + player_width and player_x < small_platform_x + small_platform_width and
        player_y + player_height >= small_platform_y and player_y + player_height <= small_platform_y + small_platform_height and player_velocity_y >= 0):
        player_y = small_platform_y - player_height
        player_velocity_y = 0
        is_jumping = False

    # Move the enemy
    enemy_x += enemy_velocity_x

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

    # Collision with small platform for enemy (only in level two)
    if level == 2 and (small_platform_x < enemy_x + enemy_width and enemy_x < small_platform_x + small_platform_width and
        enemy_y + enemy_height >= small_platform_y and enemy_y + enemy_height <= small_platform_y + small_platform_height and enemy_velocity_y >= 0):
        enemy_y = small_platform_y - enemy_height
        enemy_velocity_y = 0
        enemy_is_jumping = False

    # Update hammers
    for hammer in hammers:
        hammer["x"] += hammer["vx"]
        hammer["y"] += hammer["vy"]

    # Remove hammers that go off-screen
    hammers = [hammer for hammer in hammers if 0 <= hammer["x"] <= SCREEN_WIDTH and 0 <= hammer["y"] <= SCREEN_HEIGHT]

    # Check hammer collision with enemy
    for hammer in hammers:
        if (enemy_x < hammer["x"] < enemy_x + enemy_width and
            enemy_y < hammer["y"] < enemy_y + enemy_height):
            enemy_lives -= 1
            hammers.remove(hammer)
            break

    # Check for victory condition
    if enemy_lives <= 0:
        victory_screen()
        # Reset for level two
        level = 2
        enemy_lives = 20  # Increased health for level two
        player_lives = 3  # Reset player lives for level two
        player_x = 10  # Respawn player on the left side of the screen
        player_y = SCREEN_HEIGHT - player_height - 100
        enemy_x = SCREEN_WIDTH - enemy_width - 10  # Respawn enemy on the right side of the screen
        enemy_y = platform_y - enemy_height
        jump_timer = 0
        sequence_index = 0

    # Collision with enemy
    if (player_x < enemy_x + enemy_width and
        player_x + player_width > enemy_x and
        player_y < enemy_y + enemy_height and
        player_y + player_height > enemy_y):
        player_lives -= 1
        if player_lives > 0:
            # Respawn player at the opposite side of the enemy
            if enemy_x < SCREEN_WIDTH / 2:
                player_x = SCREEN_WIDTH - player_width - 10  # Respawn on the right side
            else:
                player_x = 10  # Respawn on the left side
            player_y = SCREEN_HEIGHT - player_height - 100
        else:
            running = False  # End the game when no lives are left

    # Fill screen with white background
    screen.fill(WHITE)

    # Draw the main platform
    pygame.draw.rect(screen, BLACK, (platform_x, platform_y, platform_width, platform_height))

    # Draw the small platform (only in level two)
    if level == 2:
        pygame.draw.rect(screen, BLACK, (small_platform_x, small_platform_y, small_platform_width, small_platform_height))

    # Draw the enemy
    pygame.draw.rect(screen, enemy_color, (enemy_x, enemy_y, enemy_width, enemy_height))

    # Draw enemy life bar at the top of the screen
    pygame.draw.rect(screen, BLACK, (10, 50, SCREEN_WIDTH - 20, 20))  # Background of health bar
    pygame.draw.rect(screen, RED, (10, 50, (SCREEN_WIDTH - 20) * (enemy_lives / (20 if level == 2 else 10)), 20))  # Health bar in red

    # Draw the player (as a green square for now)
    pygame.draw.rect(screen, player_color, (player_x, player_y, player_width, player_height))

    # Draw hammers
    for hammer in hammers:
        pygame.draw.rect(screen, BLACK, (hammer["x"], hammer["y"], hammer_width, hammer_height))

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





# main.py

import pygame
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

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Player settings
player_width = 30
player_height = 30
player_x = 100
player_y = SCREEN_HEIGHT - player_height - 100  # Start position
player_velocity_x = 6
player_velocity_y = 0
player_color = GREEN

# Player lives
player_lives = 3

# Gravity settings
gravity = 1
jump_strength = -25
is_jumping = False

# Platform settings
platform_width = SCREEN_WIDTH
platform_height = 20
platform_x = 0
platform_y = SCREEN_HEIGHT - 100

# Small platform settings
small_platform_width = 150
small_platform_height = 20
small_platform_x = SCREEN_WIDTH // 2 - small_platform_width // 2
small_platform_y = SCREEN_HEIGHT - 250

# Enemy settings
enemy_width = 60
enemy_height = 60
enemy_x = 300
enemy_y = platform_y - enemy_height
enemy_velocity_x = 5  # Increase enemy speed to 5
enemy_color = RED
enemy_lives = 10  # Start with 10 health points for level one

# Enemy jump settings
enemy_gravity = 1
enemy_jump_strength = -20  # Increase jump strength to make enemy jump higher
enemy_velocity_y = 0
enemy_is_jumping = False
jump_timer = 0  # Used to trigger enemy jumps in a sequence
jump_sequence = [60, 60, 90]  # Frames equivalent to 1 second, 1 second, and 1.5 seconds at 60 FPS
sequence_index = 0

# Hammer settings
hammers = []  # List to store active hammers
hammer_width = 10
hammer_height = 10
hammer_velocity_x = 7
hammer_velocity_y_initial = -15
last_hammer_time = 0  # Track the last time a hammer was thrown
hammer_cooldown = 0.5  # Cooldown time in seconds between throws

# Function to display start screen
def start_screen():
    screen.fill(WHITE)
    font = pygame.font.Font(None, 74)
    text = font.render("Level One", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))

    font = pygame.font.Font(None, 36)
    text = font.render("Press SPACE to Start", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 + 20))

    font = pygame.font.Font(None, 28)
    commands_text = [
        "Commands:",
        "Move Left: A",
        "Move Right: D",
        "Jump: SPACE",
        "Drop Down (Level 2): S",
        "Throw Hammer: W"
    ]
    for i, line in enumerate(commands_text):
        text = font.render(line, True, BLACK)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 + 60 + i * 30))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False

# Function to display victory screen
def victory_screen():
    screen.fill(WHITE)
    font = pygame.font.Font(None, 74)
    text = font.render("Congratulations!", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))

    font = pygame.font.Font(None, 36)
    text = font.render("Press SPACE to Start Level Two", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 + 20))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False

# Display the start screen
start_screen()

# Main game loop
running = True
facing_direction = "right"  # Track the direction the player is facing
level = 1  # Start at level one

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get keys pressed
    keys = pygame.key.get_pressed()

    # Horizontal movement
    if keys[pygame.K_a]:
        player_x -= player_velocity_x
        facing_direction = "left"
    if keys[pygame.K_d]:
        player_x += player_velocity_x
        facing_direction = "right"

    # Prevent player from going outside the screen boundaries
    if player_x < 0:
        player_x = 0
    if player_x + player_width > SCREEN_WIDTH:
        player_x = SCREEN_WIDTH - player_width

    # Jumping
    if keys[pygame.K_SPACE] and not is_jumping:
        player_velocity_y = jump_strength
        is_jumping = True

    # Drop down through small platform (only in level two)
    if level == 2 and keys[pygame.K_s] and (small_platform_x < player_x < small_platform_x + small_platform_width) and (player_y + player_height == small_platform_y):
        player_y += 5  # Move the player down slightly to allow dropping through the platform

    # Throw hammer with cooldown
    current_time = time.time()
    if keys[pygame.K_w] and current_time - last_hammer_time > hammer_cooldown:
        if facing_direction == "left":
            hammers.append({"x": player_x, "y": player_y, "vx": -hammer_velocity_x, "vy": hammer_velocity_y_initial})
        elif facing_direction == "right":
            hammers.append({"x": player_x + player_width, "y": player_y, "vx": hammer_velocity_x, "vy": hammer_velocity_y_initial})
        last_hammer_time = current_time

    # Apply gravity
    player_velocity_y += gravity
    player_y += player_velocity_y

    # Collision with main platform
    if player_y + player_height >= platform_y:
        player_y = platform_y - player_height
        player_velocity_y = 0
        is_jumping = False

    # Collision with small platform (only in level two)
    if level == 2 and (small_platform_x < player_x + player_width and player_x < small_platform_x + small_platform_width and
        player_y + player_height >= small_platform_y and player_y + player_height <= small_platform_y + small_platform_height and player_velocity_y >= 0):
        player_y = small_platform_y - player_height
        player_velocity_y = 0
        is_jumping = False

    # Move the enemy
    enemy_x += enemy_velocity_x

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

    # Collision with small platform for enemy (only in level two)
    if level == 2 and (small_platform_x < enemy_x + enemy_width and enemy_x < small_platform_x + small_platform_width and
        enemy_y + enemy_height >= small_platform_y and enemy_y + enemy_height <= small_platform_y + small_platform_height and enemy_velocity_y >= 0):
        enemy_y = small_platform_y - enemy_height
        enemy_velocity_y = 0
        enemy_is_jumping = False

    # Update hammers
    for hammer in hammers:
        hammer["x"] += hammer["vx"]
        hammer["y"] += hammer["vy"]
        hammer["vy"] += gravity  # Apply gravity to the hammer for a parabolic arc

    # Remove hammers that go off-screen
    hammers = [hammer for hammer in hammers if 0 <= hammer["x"] <= SCREEN_WIDTH and 0 <= hammer["y"] <= SCREEN_HEIGHT]

    # Check hammer collision with enemy
    for hammer in hammers:
        if (enemy_x < hammer["x"] < enemy_x + enemy_width and
            enemy_y < hammer["y"] < enemy_y + enemy_height):
            enemy_lives -= 1
            hammers.remove(hammer)
            break

    # Check for victory condition
    if enemy_lives <= 0:
        victory_screen()
        # Reset for level two
        level = 2
        enemy_lives = 20  # Increased health for level two
        player_lives = 3  # Reset player lives for level two
        player_x = 10  # Respawn player on the left side of the screen
        player_y = SCREEN_HEIGHT - player_height - 100
        enemy_x = SCREEN_WIDTH - enemy_width - 10  # Respawn enemy on the right side of the screen
        enemy_y = platform_y - enemy_height
        jump_timer = 0
        sequence_index = 0

    # Collision with enemy
    if (player_x < enemy_x + enemy_width and
        player_x + player_width > enemy_x and
        player_y < enemy_y + enemy_height and
        player_y + player_height > enemy_y):
        player_lives -= 1
        if player_lives > 0:
            # Respawn player at the opposite side of the enemy
            if enemy_x < SCREEN_WIDTH / 2:
                player_x = SCREEN_WIDTH - player_width - 10  # Respawn on the right side
            else:
                player_x = 10  # Respawn on the left side
            player_y = SCREEN_HEIGHT - player_height - 100
        else:
            running = False  # End the game when no lives are left

    # Fill screen with white background
    screen.fill(WHITE)

    # Draw the main platform
    pygame.draw.rect(screen, BLACK, (platform_x, platform_y, platform_width, platform_height))

    # Draw the small platform (only in level two)
    if level == 2:
        pygame.draw.rect(screen, BLACK, (small_platform_x, small_platform_y, small_platform_width, small_platform_height))

    # Draw the enemy
    pygame.draw.rect(screen, enemy_color, (enemy_x, enemy_y, enemy_width, enemy_height))

    # Draw enemy life bar at the top of the screen
    pygame.draw.rect(screen, BLACK, (10, 50, SCREEN_WIDTH - 20, 20))  # Background of health bar
    pygame.draw.rect(screen, RED, (10, 50, (SCREEN_WIDTH - 20) * (enemy_lives / (20 if level == 2 else 10)), 20))  # Health bar in red

    # Draw the player (as a green square for now)
    pygame.draw.rect(screen, player_color, (player_x, player_y, player_width, player_height))

    # Draw hammers
    for hammer in hammers:
        pygame.draw.rect(screen, BLACK, (hammer["x"], hammer["y"], hammer_width, hammer_height))

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