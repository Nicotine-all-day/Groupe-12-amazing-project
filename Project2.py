import pygame
import numpy as np
import random  # Import random module for random jumps
import time  # Import time module for timing hammer throws
from moviepy.editor import VideoFileClip
import sys

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

# Function to play the intro video with a skip button
def play_intro():
    clip = VideoFileClip('intro.mp4')

    # Set up a basic skip button
    skip_button_rect = pygame.Rect(SCREEN_WIDTH - 120, SCREEN_HEIGHT - 50, 100, 30)
    font = pygame.font.Font(None, 36)

    # Play video in a loop until the user skips it
    start_time = time.time()
    while True:
        screen.fill(BLACK)

        # Get current frame of the video
        current_time = time.time() - start_time
        if current_time < clip.duration:
            frame = clip.get_frame(current_time)
            frame = (frame * 255).astype(np.uint8)  # Ensure frame is in uint8 format
            frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
            screen.blit(frame_surface, (0, 0))
        else:
            clip.close()
            return

        # Draw the skip button
        pygame.draw.rect(screen, RED, skip_button_rect)
        skip_text = font.render("Skip", True, WHITE)
        screen.blit(skip_text, (SCREEN_WIDTH - 110, SCREEN_HEIGHT - 45))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if skip_button_rect.collidepoint(event.pos):
                    # Stop the video and return to the game
                    clip.close()
                    return

# Play the intro video with a skip button
play_intro()

# Game main loop
running = True
last_dash_time = 0  # Track the last time a dash was used
dash_cooldown = 2  # Cooldown time in seconds for dash
dash_distance = 100  # Distance covered in dash
last_dash_time = 0  # Track the last time a dash was used
dash_cooldown = 1  # Cooldown time in seconds for dash
dash_distance = 100  # Distance covered in dash
invincible = False  # Flag to track if the player is invincible
facing_direction = "right"  # Track the direction the player is facing
level = 1  # Start at level one
while running:
    screen.fill(WHITE)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update display
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
    if level == 2 and keys[pygame.K_s] and (small_platform_x < player_x + player_width and player_x < small_platform_x + small_platform_width) and (player_y + player_height == small_platform_y):
        player_velocity_y = 10  # Increase player velocity to drop down quickly to the main platform
        player_y += 15  # Move the player down quickly to drop through the platform
        

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
    if not invincible and (player_x < enemy_x + enemy_width and
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

    # Control frame rate
    clock.tick(60)

pygame.quit()