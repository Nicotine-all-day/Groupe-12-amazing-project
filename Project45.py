# main.py

import pygame
import numpy as np
import random  # Import random module for random jumps
import time  # Import time module for timing hammer throws
import os  # Import os for file path handling
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
TEXTCOLOR = (0, 0, 0)

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Player settings for Level 1
player_width = 30
player_height = 30
player_x = 100
player_y = SCREEN_HEIGHT - player_height - 100  # Start position
player_velocity_x = 6
player_velocity_y = 0
player_color = GREEN

# Player lives
player_lives = 3

# Gravity settings for Level 1
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

# Enemy settings for Level 1
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

# Hammer settings for Level 1
hammers = []  # List to store active hammers
hammer_width = 10
hammer_height = 10
hammer_velocity_x = 7
hammer_velocity_y_initial = -15
last_hammer_time = 0  # Track the last time a hammer was thrown
hammer_cooldown = 0.3  # Cooldown time in seconds between throws

# Level 2 Dodger Game Settings
WINDOWWIDTH = 800
WINDOWHEIGHT = 600
BADDIEMINSIZE = 10
BADDIEMAXSIZE = 40
BADDIEMINSPEED = 1
BADDIEMAXSPEED = 8
ADDNEWBADDIERATE = 6
PLAYERMOVERATE = 5
baddies = []
score = 0
topScore = 0

# Function to terminate the game
def terminate():
    pygame.quit()
    sys.exit()

# Function to wait for player to press a key
def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Pressing ESC quits.
                    terminate()
                return

# Function to check collision with baddies
def playerHasHitBaddie(playerRect, baddies):
    for b in baddies:
        if playerRect.colliderect(b['rect']):
            return True
    return False

# Function to draw text on screen
def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

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
last_dash_time = 0  # Track the last time a dash was used
dash_cooldown = 1  # Cooldown time in seconds for dash
dash_distance = 100  # Distance covered in dash
invincible = False  # Flag to track if the player is invincible
facing_direction = "right"  # Track the direction the player is facing
level = 1  # Start at level one

while running:
    if level == 1:
        # Level 1 logic
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Get keys pressed
        keys = pygame.key.get_pressed()

        # Dash movement
        current_time = time.time()
        if keys[pygame.K_e] and current_time - last_dash_time > dash_cooldown:
            if facing_direction == "left":
                player_x -= dash_distance
            elif facing_direction == "right":
                player_x += dash_distance
            last_dash_time = current_time

        # Toggle invincibility if 'i' is pressed
        if keys[pygame.K_i]:
            invincible = not invincible

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

        # Throw hammer with cooldown
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
            # Move to level two
            level = 2
            continue

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
        pygame.draw.rect(screen, RED, (10, 50, (SCREEN_WIDTH - 20) * (enemy_lives / 10), 20))  # Health bar in red

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

    elif level == 2:
        # Level 2: Dodger game logic
        baddies = []
        score = 0
        playerRect = pygame.Rect(WINDOWWIDTH / 2, WINDOWHEIGHT - 50, player_width, player_height)
        moveLeft = moveRight = moveUp = moveDown = False
        baddieAddCounter = 0
        
        while running and level == 2:
            score += 1  # Increase score.

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        moveRight = False
                        moveLeft = True
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        moveLeft = False
                        moveRight = True
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        moveDown = False
                        moveUp = True
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        moveUp = False
                        moveDown = True

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        moveLeft = False
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        moveRight = False
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        moveUp = False
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        moveDown = False

            # Add new baddies at the top of the screen, if needed.
            baddieAddCounter += 1
            if baddieAddCounter == ADDNEWBADDIERATE:
                baddieAddCounter = 0
                baddieSize = random.randint(BADDIEMINSIZE, BADDIEMAXSIZE)
                newBaddie = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH - baddieSize), 0 - baddieSize, baddieSize, baddieSize),
                            'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED)}
                baddies.append(newBaddie)

            # Move the player around.
            if moveLeft and playerRect.left > 0:
                playerRect.move_ip(-1 * PLAYERMOVERATE, 0)
            if moveRight and playerRect.right < WINDOWWIDTH:
                playerRect.move_ip(PLAYERMOVERATE, 0)
            if moveUp and playerRect.top > 0:
                playerRect.move_ip(0, -1 * PLAYERMOVERATE)
            if moveDown and playerRect.bottom < WINDOWHEIGHT:
                playerRect.move_ip(0, PLAYERMOVERATE)

            # Move the baddies down.
            for b in baddies:
                b['rect'].move_ip(0, b['speed'])

            # Delete baddies that have fallen past the bottom.
            for b in baddies[:]:
                if b['rect'].top > WINDOWHEIGHT:
                    baddies.remove(b)

            # Fill screen with white background
            screen.fill(WHITE)

            # Draw the player's rectangle
            pygame.draw.rect(screen, GREEN, playerRect)

            # Draw each baddie
            for b in baddies:
                pygame.draw.rect(screen, RED, b['rect'])

            # Draw the score
            font = pygame.font.Font(None, 36)
            drawText(f'Score: {score}', font, screen, 10, 0)
            drawText(f'Top Score: {topScore}', font, screen, 10, 40)

            pygame.display.update()

            # Check if any of the baddies have hit the player.
            if playerHasHitBaddie(playerRect, baddies):
                if score > topScore:
                    topScore = score  # Set new top score
                break

            clock.tick(FPS)  # Cap the frame rate

        # Game over logic for level 2
        font = pygame.font.Font(None, 74)
        drawText('GAME OVER', font, screen, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
        drawText('Press a key to play again.', font, screen, (WINDOWWIDTH / 3) - 80, (WINDOWHEIGHT / 3) + 50)
        pygame.display.update()
        waitForPlayerToPressKey()

# Quit Pygame 
pygame.quit()
