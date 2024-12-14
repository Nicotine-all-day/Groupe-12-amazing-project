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
pygame.mouse.set_visible(False)

font = pygame.font.SysFont(None, 48)
current_dir = os.getcwd()
TEXTCOLOR = (0, 0, 0)


# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
DARK_GRAY = (50, 50, 50)  # Updated platform color to match the background


# Clock for controlling frame rate
clock = pygame.time.Clock()

# Game state
GAME_STATE_LEVEL1 = 1
GAME_STATE_LEVEL2 = 2
current_game_state = GAME_STATE_LEVEL1

# Level 2 settings (from Project-Copy.py)
def init_level2():
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

def playerHasHitBaddie(playerRect, baddies):
    for b in baddies:
        if playerRect.colliderect(b['rect']):
            baddies.remove(b)
            return True
    return False

def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def hammerHitsOpponent(hammerRect, opponentRect):
    return hammerRect.colliderect(opponentRect)


# Import all functions from both games
def draw_button():
    font = pygame.font.Font(None, 23)
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
    pygame.draw.rect(screen, button_color, button_rect)
    button_text = font.render("Skip to Next Level", True, BLACK)
    text_rect = button_text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
    screen.blit(button_text, text_rect)

def show_victory_screen():
    # Load background image
    winMusic = pygame.mixer.Sound('Winning level transition music.mp3')
    winMusic.play()
    background_img = pygame.image.load(os.path.join(current_dir, 'Background Mario Game.jpeg'))
    background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(background_img, (0, 0))
    font = pygame.font.Font(None, 72)
    text = font.render("CONGRATULATIONS!", True, WHITE)
    subtext_font = pygame.font.Font(None, 36)
    subtext = subtext_font.render("You avenged your brother!", True, WHITE)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 4))
    screen.blit(subtext, (SCREEN_WIDTH // 2 - subtext.get_width() // 2, SCREEN_HEIGHT // 2))
    pygame.display.flip()
    pygame.time.wait(5000) 
    winMusic.stop()

def show_game_over_screen():
    gameOverSound = pygame.mixer.Sound('gameover.wav')
    gameOverSound.play()
    background_img = pygame.image.load(os.path.join(current_dir, 'Background Mario Game.jpeg'))
    background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(background_img, (0, 0))
    font = pygame.font.Font(None, 72)
    text = font.render("GAME OVER", True, WHITE)
    retry_font = pygame.font.Font(None, 36)
    retry_text = retry_font.render("Press SPACE to Retry", True, WHITE)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 4))
    screen.blit(retry_text, (SCREEN_WIDTH // 2 - retry_text.get_width() // 2, SCREEN_HEIGHT // 2))
    pygame.display.flip()
    pygame.time.wait(5000)
    gameOverSound.stop()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                pygame.mixer.music.play()
                waiting = False

def is_button_clicked(mouse_pos):
    return button_x <= mouse_pos[0] <= button_x + button_width and button_y <= mouse_pos[1] <= button_y + button_height

def start_screen():
    # Load background image
    background_img = pygame.image.load(os.path.join(current_dir, 'Background Mario Game.jpeg'))
    background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
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
   
def run_level2():
    global current_game_state, player_x, player_y, player_velocity_y, is_jumping
    global enemy_x, enemy_y, enemy_velocity_y, enemy_is_jumping, enemy_lives, enemy_velocity_x
    global jump_timer, sequence_index, hammers, last_hammer_time, last_dash_time
    global player_velocity_x, player_width, player_height, platform_x, platform_y
    global platform_width, platform_height, enemy_width, enemy_height
    global player_lives, invincible, facing_direction, player_color, enemy_color
    global gravity, jump_strength, enemy_gravity, enemy_jump_strength


    background_img = pygame.image.load(os.path.join(current_dir, 'Background Mario Game.jpeg'))
    background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

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


    jump_cooldown = 0.3  # Cooldown time in seconds for jumping
    last_jump_time = 0  # Last jump time

    # Additional platforms
    platforms = [
    {"x": 50, "y": SCREEN_HEIGHT - 200, "width": 150, "height": 20},  # Left platform
    {"x": SCREEN_WIDTH - 200, "y": SCREEN_HEIGHT - 200, "width": 150, "height": 20},  # Right platform
    {"x": SCREEN_WIDTH // 2 - 100, "y": SCREEN_HEIGHT - 300, "width": 200, "height": 20},  # Center platform
    ]
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
            pygame.mixer.music.stop()
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
                pygame.mixer.music.stop()
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
        lives_text = font.render(f"Lives: {player_lives}", True, WHITE)
        screen.blit(lives_text, (10, 10))

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)  # 60 FPS


def run_level1():

    BACKGROUNDCOLOR = (255, 255, 255)
    PLATFORMCOLOR = (51, 103, 78)  # ForestGreen to match the new background
    FPS = 60
    BADDIEMINSIZE = 10
    BADDIEMAXSIZE = 40
    BADDIEMINSPEED = 1
    BADDIEMAXSPEED = 8
    ADDNEWBADDIERATE = 6
    PLAYERMOVERATE = 5
    JUMP_HEIGHT = 100
    GRAVITY = 6
    PLATFORMHEIGHT = 20
    OPPONENTSPEED = 3
    OPPONENTTHROWRATE = 25
    HAMMER_SPEED = -10
    HAMMER_COOLDOWN = 0.3
    LUIGI_LIFE = 10
    TURTLE_LIFE = 3
    # Set up sounds.
    gameOverSound = pygame.mixer.Sound('gameover.wav')
    winMusic = pygame.mixer.Sound('Winning level transition music.mp3')
    pygame.mixer.music.load('Luigi Music.mp3')

    # Set up images.
    backgroundImage = pygame.image.load('Background Luigi Game.jpeg')
    backgroundImage = pygame.transform.scale(backgroundImage, (SCREEN_WIDTH,SCREEN_HEIGHT))
    playerImageLeft = pygame.image.load('Turtle Left.gif')
    playerImageLeft = pygame.transform.scale(playerImageLeft, (50, 50))
    playerImageRight = pygame.image.load('Turtle Right.gif')
    playerImageRight = pygame.transform.scale(playerImageRight, (50, 50))
    playerImage = playerImageRight
    playerRect = playerImage.get_rect()
    baddieImage = pygame.image.load('Fireball .gif')
    baddieImage = pygame.transform.scale(baddieImage, (30, 30))
    opponentImageLeft = pygame.image.load('Luigi Left.gif')
    opponentImageLeft = pygame.transform.scale(opponentImageLeft, (100, 100))
    opponentImageRight = pygame.image.load('Luigi Right.gif')
    opponentImageRight = pygame.transform.scale(opponentImageRight, (100, 100))
    opponentImageHurt = pygame.image.load('Luigi Hurt.gif')
    opponentImageHurt = pygame.transform.scale(opponentImageHurt, (100, 100))
    opponentImage = opponentImageRight
    opponentRect = opponentImage.get_rect()
    opponentRect.midtop = (SCREEN_WIDTH // 2, 100)
    opponentDirection = 1 # 1 for moving right, -1 for moving left
    hammerImage = pygame.image.load('Hammer in the AIR.gif')
    hammerImage = pygame.transform.scale(hammerImage, (30, 30))
    hammers = []
    hammerRotations = []
    lastHammerTime = 0
    opponentHurtCooldown = 0

    # Jumping variables
    isJumping = False
    jumpStartY = 0
    onGround = True

    luigiLife = LUIGI_LIFE
    turtleLife = TURTLE_LIFE
    baddies = []
    hammers = []
    hammerRotations = []
    score = 0
    playerRect.topleft = (SCREEN_WIDTH / 2, SCREEN_HEIGHT - PLATFORMHEIGHT - playerRect.height)
    opponentRect.midtop = (SCREEN_WIDTH // 2, 100)
    opponentImage = opponentImageRight
    playerImage = playerImageRight
    opponentHurtCooldown = 0
    isJumping = False
    onGround = True
    

    # Show the "Start" screen.
    screen.blit(backgroundImage, (0, 0))
    drawText('Dodger', font, screen, (SCREEN_WIDTH / 2)-50, (SCREEN_HEIGHT / 2)-50)
    drawText('Press a key to start.', font, screen, (SCREEN_WIDTH / 3) - 25, (SCREEN_HEIGHT / 3) + 100)
    pygame.display.update()
    waitForPlayerToPressKey()


    while True:
        moveLeft = moveRight = False
        reverseCheat = slowCheat = False
        baddieAddCounter = 0
        opponentThrowCounter = 0
        pygame.mixer.music.play(-1, 0.0)

        while True: # The game loop runs while the game part is playing.
            current_time = time.time()

            for event in pygame.event.get():
                if event.type == QUIT:
                    terminate()

                if event.type == KEYDOWN:
                    if event.key == K_z:
                        reverseCheat = True
                    if event.key == K_x:
                        slowCheat = True
                    if event.key == K_LEFT or event.key == K_a:
                        moveRight = False
                        moveLeft = True
                        playerImage = playerImageLeft
                    if event.key == K_RIGHT or event.key == K_d:
                        moveLeft = False
                        moveRight = True
                        playerImage = playerImageRight
                    if event.key == K_SPACE and onGround:  # Initiate jump
                        isJumping = True
                        jumpStartY = playerRect.y
                        onGround = False
                    if event.key == K_w and current_time - lastHammerTime >= HAMMER_COOLDOWN: # Throw hammer with cooldown
                        hammerRect = pygame.Rect(playerRect.centerx - 15, playerRect.top - 30, 30, 30)
                        hammers.append(hammerRect)
                        hammerRotations.append(0)  # Add initial rotation angle
                        lastHammerTime = current_time

                if event.type == KEYUP:
                    if event.key == K_z:
                        reverseCheat = False
                    if event.key == K_x:
                        slowCheat = False
                    if event.key == K_ESCAPE:
                        terminate()

                    if event.key == K_LEFT or event.key == K_a:
                        moveLeft = False
                    if event.key == K_RIGHT or event.key == K_d:
                        moveRight = False

            # Handle jumping
            if isJumping:
                if playerRect.y > jumpStartY - JUMP_HEIGHT:
                    playerRect.y -= GRAVITY
                else:
                    isJumping = False
            else:
                if playerRect.y < SCREEN_HEIGHT - PLATFORMHEIGHT - playerRect.height:
                    playerRect.y += GRAVITY
                else:
                    onGround = True

            # Add new baddies at the top of the screen, if needed.
            opponentThrowCounter += 1
            if opponentThrowCounter >= OPPONENTTHROWRATE:
                opponentThrowCounter = 0
                baddieSize = random.randint(BADDIEMINSIZE, BADDIEMAXSIZE)
                newBaddie = {'rect': pygame.Rect(opponentRect.centerx - baddieSize // 2, opponentRect.bottom, baddieSize, baddieSize),
                            'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                            'surface':pygame.transform.scale(baddieImage, (baddieSize, baddieSize)),
                            }
                baddies.append(newBaddie)

            # Move the opponent left and right.
            if opponentHurtCooldown > 0:
                opponentHurtCooldown -= 1
            else:
                opponentRect.x += opponentDirection * OPPONENTSPEED
                if opponentDirection == 1:
                    opponentImage = opponentImageRight
                else:
                    opponentImage = opponentImageLeft

                if opponentRect.right >= SCREEN_WIDTH or opponentRect.left <= 0:
                    opponentDirection *= -1

            # Move the hammers.
            for i in range(len(hammers) - 1, -1, -1):
                hammers[i].y += HAMMER_SPEED
                hammerRotations[i] += 15  # Increment rotation angle
                if hammerRotations[i] >= 360:
                    hammerRotations[i] -= 360
                if hammers[i].bottom < 0:
                    del hammers[i]
                    del hammerRotations[i]
                elif hammerHitsOpponent(hammers[i], opponentRect):
                    del hammers[i]
                    del hammerRotations[i]
                    luigiLife -= 1
                    opponentImage = opponentImageHurt
                    opponentHurtCooldown = FPS // 2  # Hurt state lasts 0.5 seconds

            # Check if player is hit by baddie.
            for b in baddies[:]:
                if playerRect.colliderect(b['rect']):
                    baddies.remove(b)
                    turtleLife -= 1

            # End game if Luigi's life reaches 0.
            if luigiLife <= 0:
                pygame.mixer.music.stop()
                winMusic.play()
                drawText('You Win!', font, screen, (SCREEN_WIDTH / 2) - 20, (SCREEN_HEIGHT / 2)-20)
                pygame.display.update()
                pygame.time.wait(5000)  # Allow the win music to play completely
                winMusic.stop()
                init_level2()
                start_screen()
                run_level2()
                break

            # End game if Turtle's life reaches 0.
            if turtleLife <= 0:
                drawText('GAME OVER', font, screen, (SCREEN_WIDTH / 2)-70, (SCREEN_HEIGHT / 3)+7)
                pygame.display.update()
                pygame.time.wait(2000)
                pygame.mixer.music.stop()
                gameOverSound.play()

                drawText('Press SPACE to Restart Level', font, screen, (SCREEN_WIDTH / 3) - 80, (SCREEN_HEIGHT / 3) + 50)
                drawText('Press S to Skip Level', font, screen, (SCREEN_WIDTH / 3) - 30, (SCREEN_HEIGHT / 3) + 90)
                pygame.display.update()
                waiting = True
                while waiting:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            exit()
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                            run_level1()
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                            init_level2()
                            start_screen()
                            run_level2()
                    
                pygame.time.wait(2000)  # Ensure sound finishes playing
                gameOverSound.stop()
                # resetGame()
                pygame.mixer.music.play(-1, 0.0)
                break

            # Move the player around.
            if moveLeft and playerRect.left > 0:
                playerRect.move_ip(-1 * PLAYERMOVERATE, 0)
            if moveRight and playerRect.right < SCREEN_WIDTH:
                playerRect.move_ip(PLAYERMOVERATE, 0)

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
            screen.blit(backgroundImage, (0, 0))

            # Draw the platform for the opponent.
            pygame.draw.rect(screen, PLATFORMCOLOR, (0, 190, SCREEN_WIDTH, 10))

            # Draw the platform for the player.
            pygame.draw.rect(screen, PLATFORMCOLOR, (0, SCREEN_HEIGHT - PLATFORMHEIGHT, SCREEN_WIDTH, PLATFORMHEIGHT))

            # Draw Luigi's life bar.
            pygame.draw.rect(screen, (255, 0, 0), (opponentRect.x, opponentRect.top - 20, 100, 10))
            pygame.draw.rect(screen, (0, 255, 0), (opponentRect.x, opponentRect.top - 20, luigiLife * 10, 10))

            # Draw Turtle's life bar.
            pygame.draw.rect(screen, (255, 0, 0), (10, SCREEN_HEIGHT - PLATFORMHEIGHT - 30, 100, 10))
            pygame.draw.rect(screen, (0, 255, 0), (10, SCREEN_HEIGHT - PLATFORMHEIGHT - 30, turtleLife * 33, 10))

            # Draw the player's rectangle.
            screen.blit(playerImage, playerRect)

            # Draw the opponent.
            screen.blit(opponentImage, opponentRect)

            # Draw each baddie.
            for b in baddies:
                screen.blit(b['surface'], b['rect'])

            # Draw each hammer with rotation.
            for i, hammer in enumerate(hammers):
                rotatedHammer = pygame.transform.rotate(hammerImage, hammerRotations[i])
                screen.blit(rotatedHammer, hammer.topleft)

            pygame.display.update()

            clock.tick(FPS)

# Main game loop
def main():
    global current_game_state
    
    while True:
        if current_game_state == GAME_STATE_LEVEL2:
            init_level2()
            start_screen()
            run_level2()
        elif current_game_state == GAME_STATE_LEVEL1:
            run_level1()

if __name__ == "__main__":
    main()