import pygame
import numpy as np
import random
import time
import os
import sys
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Common settings
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

# Game state
GAME_STATE_LEVEL1 = 1
GAME_STATE_LEVEL2 = 2
current_game_state = GAME_STATE_LEVEL2

<<<<<<< HEAD
# Level 1 settings (from Project-Copy.py)
def init_level1():
=======
<<<<<<<< HEAD:ProjectMerge1.py
# Level 1 settings (from Project-Copy.py)
========
# Level 1 settings from the dodger code
>>>>>>>> dc2866410a9c2783ac6dc6fc428be2c5533de2c9:ProjectMerge1_Test.py
def init_level1():
    global TEXTCOLOR, BACKGROUNDCOLOR, FPS, BADDIEMINSIZE, BADDIEMAXSIZE
    global BADDIEMINSPEED, BADDIEMAXSPEED, ADDNEWBADDIERATE, PLAYERMOVERATE
    global playerRect, baddies, score, moveLeft, moveRight, moveUp, moveDown
    global reverseCheat, slowCheat, baddieAddCounter, topScore
    
    # Initialize all dodger.py settings
    TEXTCOLOR = (0, 0, 0)
    BACKGROUNDCOLOR = (255, 255, 255)
    FPS = 60
    BADDIEMINSIZE = 10
    BADDIEMAXSIZE = 40
    BADDIEMINSPEED = 1
    BADDIEMAXSPEED = 8
    ADDNEWBADDIERATE = 6
    PLAYERMOVERATE = 5
    
    # Set up player and game state
    playerRect = pygame.Rect(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 50, 20, 20)
    baddies = []
    score = 0
    moveLeft = moveRight = moveUp = moveDown = False
    reverseCheat = slowCheat = False
    baddieAddCounter = 0
    topScore = 0

# Level 2 settings from our initial game code - Nico's innovative creation
def init_level2():
>>>>>>> dc2866410a9c2783ac6dc6fc428be2c5533de2c9
    global player_width, player_height, player_x, player_y, player_velocity_x, player_velocity_y
    global player_color, player_lives, gravity, jump_strength, is_jumping
    global platform_width, platform_height, platform_x, platform_y
    global small_platform_width, small_platform_height, small_platform_x, small_platform_y
    global enemy_width, enemy_height, enemy_x, enemy_y, enemy_velocity_x, enemy_color, enemy_lives
    global enemy_gravity, enemy_jump_strength, enemy_velocity_y, enemy_is_jumping
    global jump_timer, jump_sequence, sequence_index, hammers
    global hammer_width, hammer_height, hammer_velocity_x, hammer_velocity_y_initial
    global last_hammer_time, hammer_cooldown, button_width, button_height, button_x, button_y
    global button_color, button_text_color, last_dash_time, dash_cooldown
    global dash_distance, invincible, facing_direction, level

    # Copy all the original settings from Project-Copy.py here
    player_width = 30
    player_height = 30
    player_x = 100
    player_y = SCREEN_HEIGHT - player_height - 100
    player_velocity_x = 6
    player_velocity_y = 0
    player_color = GREEN
    player_lives = 3
    gravity = 1
    jump_strength = -20
    is_jumping = False
    platform_width = SCREEN_WIDTH
    platform_height = 20
    platform_x = 0
    platform_y = SCREEN_HEIGHT - 100
    small_platform_width = 150
    small_platform_height = 20
    small_platform_x = SCREEN_WIDTH // 2 - small_platform_width // 2
    small_platform_y = SCREEN_HEIGHT - 250
    enemy_width = 60
    enemy_height = 60
    enemy_x = 300
    enemy_y = platform_y - enemy_height
    enemy_velocity_x = 5
    enemy_color = RED
    enemy_lives = 10
    enemy_gravity = 1
    enemy_jump_strength = -20
    enemy_velocity_y = 0
    enemy_is_jumping = False
    jump_timer = 0
    jump_sequence = [60, 60, 90]
    sequence_index = 0
    hammers = []
    hammer_width = 10
    hammer_height = 10
    hammer_velocity_x = 7
    hammer_velocity_y_initial = -15
    last_hammer_time = 0
    hammer_cooldown = 0.3
    button_width = 150
    button_height = 35
    button_x = SCREEN_WIDTH - button_width - 10
    button_y = 10
    button_color = GREEN
    button_text_color = WHITE
    last_dash_time = 0
    dash_cooldown = 1
    dash_distance = 100
    invincible = False
    facing_direction = "right"
<<<<<<< HEAD
=======
<<<<<<<< HEAD:ProjectMerge1.py
>>>>>>> dc2866410a9c2783ac6dc6fc428be2c5533de2c9
    level = 1

# Level 2 settings (from dodger.py)
def init_level2():
    global TEXTCOLOR, BACKGROUNDCOLOR, FPS, BADDIEMINSIZE, BADDIEMAXSIZE
    global BADDIEMINSPEED, BADDIEMAXSPEED, ADDNEWBADDIERATE, PLAYERMOVERATE
    global playerRect, baddies, score, moveLeft, moveRight, moveUp, moveDown
    global reverseCheat, slowCheat, baddieAddCounter, topScore
    
    # Initialize all dodger.py settings
    TEXTCOLOR = (0, 0, 0)
    BACKGROUNDCOLOR = (255, 255, 255)
    FPS = 60
    BADDIEMINSIZE = 10
    BADDIEMAXSIZE = 40
    BADDIEMINSPEED = 1
    BADDIEMAXSPEED = 8
    ADDNEWBADDIERATE = 6
    PLAYERMOVERATE = 5
    
    # Set up player and game state
    playerRect = pygame.Rect(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 50, 20, 20)
    baddies = []
    score = 0
    moveLeft = moveRight = moveUp = moveDown = False
    reverseCheat = slowCheat = False
    baddieAddCounter = 0
    topScore = 0
<<<<<<< HEAD
=======
========
    level = 2
>>>>>>>> dc2866410a9c2783ac6dc6fc428be2c5533de2c9:ProjectMerge1_Test.py
>>>>>>> dc2866410a9c2783ac6dc6fc428be2c5533de2c9

# Import all functions from both games
def draw_button():
    font = pygame.font.Font(None, 23)
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
    pygame.draw.rect(screen, button_color, button_rect)
    button_text = font.render("Skip to Next Level", True, BLACK)
    text_rect = button_text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
    screen.blit(button_text, text_rect)

def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def playerHasHitBaddie(playerRect, baddies):
    for b in baddies:
        if playerRect.colliderect(b['rect']):
            return True
    return False

def terminate():
    pygame.quit()
    sys.exit()

def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # Pressing ESC quits.
                    terminate()
                return

# Function to display victory screen
def victory_screen():
    screen.fill(WHITE)
    font = pygame.font.Font(None, 74)
    text = font.render("Congratulations!", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))

<<<<<<< HEAD
=======
<<<<<<<< HEAD:ProjectMerge1.py
>>>>>>> dc2866410a9c2783ac6dc6fc428be2c5533de2c9
    # font = pygame.font.Font(None, 36)
    # text = font.render("Press SPACE to Start Level Two", True, BLACK)
    # screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 + 20))

<<<<<<< HEAD
=======
========
>>>>>>>> dc2866410a9c2783ac6dc6fc428be2c5533de2c9:ProjectMerge1_Test.py
>>>>>>> dc2866410a9c2783ac6dc6fc428be2c5533de2c9
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False

# Function to display game over screen

def game_over_screen():
    screen.fill(WHITE)
    font = pygame.font.Font(None, 74)
    text = font.render("Game Over!", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))

    font = pygame.font.Font(None, 36)
    text = font.render("Press SPACE to Restart Level Two", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 + 20))

<<<<<<< HEAD
=======
<<<<<<<< HEAD:ProjectMerge1.py
>>>>>>> dc2866410a9c2783ac6dc6fc428be2c5533de2c9
    # font = pygame.font.Font(None, 36)
    # text = font.render("Press S to Skip Level", True, BLACK)
    # screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 + 60))

<<<<<<< HEAD
=======
========
>>>>>>>> dc2866410a9c2783ac6dc6fc428be2c5533de2c9:ProjectMerge1_Test.py
>>>>>>> dc2866410a9c2783ac6dc6fc428be2c5533de2c9
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                init_level1()
                run_level1()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                init_level2()
                run_level2()

def is_button_clicked(mouse_pos):
    return button_x <= mouse_pos[0] <= button_x + button_width and button_y <= mouse_pos[1] <= button_y + button_height

def start_screen():
    screen.fill(WHITE)
    font = pygame.font.Font(None, 74)
    text = font.render("Level Two", True, BLACK)
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
<<<<<<< HEAD
        "Throw Hammer: W"
=======
        "Throw Hammer: W",
        "ENJOY THE GAME!"
>>>>>>> dc2866410a9c2783ac6dc6fc428be2c5533de2c9
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

def level2_start_screen():
    screen.fill(WHITE)
    font = pygame.font.Font(None, 74)
    text = font.render("Level One: Dodger", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
    
    font = pygame.font.Font(None, 36)
    text = font.render("Press any key to start", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 + 20))
    
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                waiting = False


def run_level1():
    global current_game_state, player_x, player_y, player_velocity_y, is_jumping
    global enemy_x, enemy_y, enemy_velocity_y, enemy_is_jumping, enemy_lives, enemy_velocity_x
    global jump_timer, sequence_index, hammers, last_hammer_time, last_dash_time
    global player_velocity_x, player_width, player_height, platform_x, platform_y
    global platform_width, platform_height, enemy_width, enemy_height
    global player_lives, invincible, facing_direction, player_color, enemy_color
    global gravity, jump_strength, enemy_gravity, enemy_jump_strength
    
    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if is_button_clicked(event.pos):
                    current_game_state = GAME_STATE_LEVEL2
                    return

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

        # Move the enemy
        enemy_x += enemy_velocity_x

        # Reverse direction if enemy reaches the edge of the platform
        if enemy_x < 0 or enemy_x + enemy_width > SCREEN_WIDTH:
            enemy_velocity_x *= -1

        # Trigger enemy jumps
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
        for hammer in hammers[:]:  # Create a copy of the list to safely modify it
            hammer["x"] += hammer["vx"]
            hammer["y"] += hammer["vy"]
            hammer["vy"] += gravity

        # Remove hammers that go off-screen
        hammers = [hammer for hammer in hammers if 0 <= hammer["x"] <= SCREEN_WIDTH and 0 <= hammer["y"] <= SCREEN_HEIGHT]

        # Check hammer collision with enemy
        for hammer in hammers[:]:  # Create a copy of the list to safely modify it
            if (enemy_x < hammer["x"] < enemy_x + enemy_width and
                enemy_y < hammer["y"] < enemy_y + enemy_height):
                enemy_lives -= 1
                hammers.remove(hammer)
                if enemy_lives <= 0:
                    victory_screen()
                    current_game_state = GAME_STATE_LEVEL2
                    return

        # Check for collision with enemy
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
                game_over_screen()

        # Draw everything
        screen.fill(WHITE)
        pygame.draw.rect(screen, BLACK, (platform_x, platform_y, platform_width, platform_height))
        pygame.draw.rect(screen, enemy_color, (enemy_x, enemy_y, enemy_width, enemy_height))
        pygame.draw.rect(screen, player_color, (player_x, player_y, player_width, player_height))
        
        # Draw enemy life bar
        pygame.draw.rect(screen, BLACK, (10, 50, SCREEN_WIDTH - 20, 20))
        pygame.draw.rect(screen, RED, (10, 50, (SCREEN_WIDTH - 20) * (enemy_lives / 10), 20))
        
        # Draw hammers
        for hammer in hammers:
            pygame.draw.rect(screen, BLACK, (hammer["x"], hammer["y"], hammer_width, hammer_height))

        # Draw lives
        font = pygame.font.Font(None, 36)
        lives_text = font.render(f"Lives: {player_lives}", True, BLACK)
        screen.blit(lives_text, (10, 10))

        # Draw the button
        # draw_button()
        
        pygame.display.flip()
        clock.tick(60)

def run_level2():
    # Initialize level 2 specific variables
    init_level2()

    # Set up sounds.
    gameOverSound = pygame.mixer.Sound('gameover.wav')
    # pygame.mixer.music.load('background.mid')

    mainClock = pygame.time.Clock()

    # Set up images.
    playerImage = pygame.image.load('player.png')
    playerRect = playerImage.get_rect()
    baddieImage = pygame.image.load('baddie.png')

    topScore = 0

    # Set up the start of the game.
    baddies = []
    score = 0
    playerRect.topleft = (SCREEN_WIDTH / 2, SCREEN_HEIGHT - 50)
    moveLeft = moveRight = moveUp = moveDown = False
    reverseCheat = slowCheat = False
    baddieAddCounter = 0
    windowSurface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    font = pygame.font.SysFont(None, 48)
    
    while True:
        # Set up the start of the game.
        baddies = []
        score = 0
        playerRect.topleft = (SCREEN_WIDTH / 2, SCREEN_HEIGHT - 50)
        moveLeft = moveRight = moveUp = moveDown = False
        reverseCheat = slowCheat = False
        baddieAddCounter = 0
        # pygame.mixer.music.play(-1, 0.0)

        while True: # The game loop runs while the game part is playing.
            score += 1 # Increase score.

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                    
                    
                if event.type == KEYDOWN:
                    if event.key == K_z:
                        reverseCheat = True
                    if event.key == K_x:
                        slowCheat = True
                    if event.key == K_LEFT or event.key == K_a:
                        moveRight = False
                        moveLeft = True
                    if event.key == K_RIGHT or event.key == K_d:
                        moveLeft = False
                        moveRight = True
                    if event.key == K_UP or event.key == K_w:
                        moveDown = False
                        moveUp = True
                    if event.key == K_DOWN or event.key == K_s:
                        moveUp = False
                        moveDown = True

                if event.type == KEYUP:
                    if event.key == K_z:
                        reverseCheat = False
                        score = 0
                    if event.key == K_x:
                        slowCheat = False
                        score = 0
                    if event.key == K_ESCAPE:
                            terminate()

                    if event.key == K_LEFT or event.key == K_a:
                        moveLeft = False
                    if event.key == K_RIGHT or event.key == K_d:
                        moveRight = False
                    if event.key == K_UP or event.key == K_w:
                        moveUp = False
                    if event.key == K_DOWN or event.key == K_s:
                        moveDown = False

                if event.type == MOUSEMOTION:
                    # If the mouse moves, move the player where to the cursor.
                    playerRect.centerx = event.pos[0]
                    playerRect.centery = event.pos[1]
            # Add new baddies at the top of the screen, if needed.
            if not reverseCheat and not slowCheat:
                baddieAddCounter += 1
            if baddieAddCounter == ADDNEWBADDIERATE:
                baddieAddCounter = 0
                baddieSize = random.randint(BADDIEMINSIZE, BADDIEMAXSIZE)
                newBaddie = {'rect': pygame.Rect(random.randint(0, SCREEN_WIDTH - baddieSize), 0 - baddieSize, baddieSize, baddieSize),
                            'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                            'surface':pygame.transform.scale(baddieImage, (baddieSize, baddieSize)),
                            }

                baddies.append(newBaddie)

            # Move the player around.
            if moveLeft and playerRect.left > 0:
                playerRect.move_ip(-1 * PLAYERMOVERATE, 0)
            if moveRight and playerRect.right < SCREEN_WIDTH:
                playerRect.move_ip(PLAYERMOVERATE, 0)
            if moveUp and playerRect.top > 0:
                playerRect.move_ip(0, -1 * PLAYERMOVERATE)
            if moveDown and playerRect.bottom < SCREEN_HEIGHT:
                playerRect.move_ip(0, PLAYERMOVERATE)

            # Move the baddies down.
            for b in baddies:
                if not reverseCheat and not slowCheat:
                    b['rect'].move_ip(0, b['speed'])
                elif reverseCheat:
                    b['rect'].move_ip(0, -5)
                elif slowCheat:
                    b['rect'].move_ip(0, 1)

            # Delete baddies that have fallen past the bottom.
            for b in baddies[:]:
                if b['rect'].top > SCREEN_HEIGHT:
                    baddies.remove(b)

            # Draw the game world on the window.
            windowSurface.fill(BACKGROUNDCOLOR)

            # Draw the score and top score.
            drawText('Score: %s' % (score), font, windowSurface, 10, 0)
            drawText('Top Score: %s' % (topScore), font, windowSurface, 10, 40)

            # Draw the player's rectangle.
            windowSurface.blit(playerImage, playerRect)

            # Draw each baddie.
            for b in baddies:
                windowSurface.blit(b['surface'], b['rect'])

            pygame.display.update()

            # Check if any of the baddies have hit the player.
            if playerHasHitBaddie(playerRect, baddies):
                if score > topScore:
                    topScore = score # set new top score
                break

            mainClock.tick(FPS)

        # Stop the game and show the "Game Over" screen.
        # pygame.mixer.music.stop()
        gameOverSound.play()

        drawText('GAME OVER', font, windowSurface, (SCREEN_WIDTH / 3), (SCREEN_HEIGHT / 3))
        drawText('Press SPACE to Restart Level', font, windowSurface, (SCREEN_WIDTH / 3) - 80, (SCREEN_HEIGHT / 3) + 50)
        drawText('Press S to Skip Level', font, windowSurface, (SCREEN_WIDTH / 3) - 80, (SCREEN_HEIGHT / 3) + 90)
        pygame.display.update()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    init_level2()
                    run_level2()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                    init_level1()
                    start_screen()
                    run_level1()
        
        # Draw the button
        draw_button()


        gameOverSound.stop()

# Main game loop
def main():
    global current_game_state
    
    while True:
        if current_game_state == GAME_STATE_LEVEL1:
            init_level1()
            start_screen()
            run_level1()
        elif current_game_state == GAME_STATE_LEVEL2:
            level2_start_screen()
            run_level2()

if __name__ == "__main__":
    main()