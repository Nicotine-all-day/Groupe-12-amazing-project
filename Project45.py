import pygame
import random
import sys
import time
import os
from pygame.locals import *

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
enemy_velocity_x = 5
enemy_color = RED
enemy_lives = 10

# Enemy jump settings
enemy_gravity = 1
enemy_jump_strength = -20
enemy_velocity_y = 0
enemy_is_jumping = False
jump_timer = 0
jump_sequence = [60, 60, 90]
sequence_index = 0

# Hammer settings
hammers = []
hammer_width = 10
hammer_height = 10
hammer_velocity_x = 7
hammer_velocity_y_initial = -15
last_hammer_time = 0
hammer_cooldown = 0.3

# Level 2 settings
BADDIEMINSIZE = 10
BADDIEMAXSIZE = 40
BADDIEMINSPEED = 1
BADDIEMAXSPEED = 8
ADDNEWBADDIERATE = 6
PLAYERMOVERATE = 5

# Load images
playerImage = pygame.image.load('player.png')
playerRect = playerImage.get_rect()
baddieImage = pygame.image.load('baddie.png')

# Load sounds
gameOverSound = pygame.mixer.Sound('gameover.wav')
pygame.mixer.music.load('background.mid')

# Font
font = pygame.font.Font(None, 36)

def draw_text(text, font, surface, x, y):
    text_obj = font.render(text, 1, BLACK)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

def start_screen():
    screen.fill(WHITE)
    draw_text("The Revenge of the Hammer Bros", font, screen, SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 100)
    draw_text("Press SPACE to Start", font, screen, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 20)
    
    commands_text = [
        "Commands:",
        "Move Left: A",
        "Move Right: D",
        "Jump: SPACE",
        "Drop Down (Level 2): S",
        "Throw Hammer: W"
    ]
    for i, line in enumerate(commands_text):
        draw_text(line, font, screen, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 60 + i * 30)
    
    # Draw skip button
    skip_button_text = font.render("Skip to Level 2", True, BLACK)
    skip_button_rect = skip_button_text.get_rect(bottomright=(SCREEN_WIDTH - 10, SCREEN_HEIGHT - 10))
    screen.blit(skip_button_text, skip_button_rect)
    
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if skip_button_rect.collidepoint(event.pos):
                    # Skip to level 2
                    victory_screen()
                    run_level_two()
                    return

def victory_screen():
    screen.fill(WHITE)
    draw_text("Congratulations!", font, screen, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 100)
    draw_text("Press SPACE to Start Level Two", font, screen, SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 20)
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False

def game_over_screen(score, top_score):
    screen.fill(WHITE)
    draw_text("GAME OVER", font, screen, SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2 - 100)
    draw_text(f"Score: {score}", font, screen, SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 50)
    draw_text(f"Top Score: {top_score}", font, screen, SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2)
    draw_text("Press SPACE to play again", font, screen, SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 50)
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False

def run_level_one():
    global player_x, player_y, player_velocity_y, is_jumping, enemy_x, enemy_y, enemy_velocity_y, enemy_is_jumping
    global jump_timer, sequence_index, enemy_lives, player_lives, hammers, last_hammer_time

    # Level one game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        # Player movement
        if keys[pygame.K_a] and player_x > 0:
            player_x -= player_velocity_x
        if keys[pygame.K_d] and player_x < SCREEN_WIDTH - player_width:
            player_x += player_velocity_x
        if keys[pygame.K_SPACE] and not is_jumping:
            player_velocity_y = jump_strength
            is_jumping = True

        # Apply gravity to player
        player_velocity_y += gravity
        player_y += player_velocity_y

        # Player collision with platform
        if player_y + player_height > platform_y:
            player_y = platform_y - player_height
            player_velocity_y = 0
            is_jumping = False

        # Enemy movement and jumping
        enemy_x += enemy_velocity_x
        if enemy_x <= 0 or enemy_x + enemy_width >= SCREEN_WIDTH:
            enemy_velocity_x *= -1

        jump_timer += 1
        if jump_timer >= jump_sequence[sequence_index]:
            if not enemy_is_jumping:
                enemy_velocity_y = enemy_jump_strength
                enemy_is_jumping = True
                jump_timer = 0
                sequence_index = (sequence_index + 1) % len(jump_sequence)

        # Apply gravity to enemy
        enemy_velocity_y += enemy_gravity
        enemy_y += enemy_velocity_y

        # Enemy collision with platform
        if enemy_y + enemy_height > platform_y:
            enemy_y = platform_y - enemy_height
            enemy_velocity_y = 0
            enemy_is_jumping = False

        # Hammer throwing
        current_time = time.time()
        if keys[pygame.K_w] and current_time - last_hammer_time > hammer_cooldown:
            hammers.append({"x": player_x, "y": player_y, "vx": hammer_velocity_x, "vy": hammer_velocity_y_initial})
            last_hammer_time = current_time

        # Update and remove hammers
        for hammer in hammers[:]:
            hammer["x"] += hammer["vx"]
            hammer["y"] += hammer["vy"]
            hammer["vy"] += gravity

            if hammer["y"] > SCREEN_HEIGHT:
                hammers.remove(hammer)

            # Check for collision with enemy
            if (enemy_x < hammer["x"] < enemy_x + enemy_width and
                enemy_y < hammer["y"] < enemy_y + enemy_height):
                enemy_lives -= 1
                hammers.remove(hammer)

        # Check for player-enemy collision
        if (player_x < enemy_x + enemy_width and player_x + player_width > enemy_x and
            player_y < enemy_y + enemy_height and player_y + player_height > enemy_y):
            player_lives -= 1
            if player_lives <= 0:
                return False  # Game over
            # Respawn player
            player_x = 100
            player_y = SCREEN_HEIGHT - player_height - 100

        # Draw everything
        screen.fill(WHITE)
        pygame.draw.rect(screen, BLACK, (platform_x, platform_y, platform_width, platform_height))
        pygame.draw.rect(screen, player_color, (player_x, player_y, player_width, player_height))
        pygame.draw.rect(screen, enemy_color, (enemy_x, enemy_y, enemy_width, enemy_height))
        for hammer in hammers:
            pygame.draw.rect(screen, BLACK, (hammer["x"], hammer["y"], hammer_width, hammer_height))

        # Draw health bars
        pygame.draw.rect(screen, RED, (10, 10, (SCREEN_WIDTH - 20) * (enemy_lives / 10), 20))
        pygame.draw.rect(screen, GREEN, (10, 40, (SCREEN_WIDTH - 20) * (player_lives / 3), 20))

        draw_text(f"Enemy Health: {enemy_lives}", font, screen, 10, 10)
        draw_text(f"Player Lives: {player_lives}", font, screen, 10, 40)

        pygame.display.flip()
        clock.tick(60)

        if enemy_lives <= 0:
            return True  # Level completed

    return False

def run_level_two():
    global playerRect, player_lives

    baddies = []
    score = 0
    playerRect.topleft = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
    moveLeft = moveRight = moveUp = moveDown = False
    baddieAddCounter = 0
    pygame.mixer.music.play(-1, 0.0)

    while True:
        score += 1

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
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
                if event.key == K_LEFT or event.key == K_a:
                    moveLeft = False
                if event.key == K_RIGHT or event.key == K_d:
                    moveRight = False
                if event.key == K_UP or event.key == K_w:
                    moveUp = False
                if event.key == K_DOWN or event.key == K_s:
                    moveDown = False

        # Move the player
        if moveLeft and playerRect.left > 0:
            playerRect.move_ip(-1 * PLAYERMOVERATE, 0)
        if moveRight and playerRect.right < SCREEN_WIDTH:
            playerRect.move_ip(PLAYERMOVERATE, 0)
        if moveUp and playerRect.top > 0:
            playerRect.move_ip(0, -1 * PLAYERMOVERATE)
        if moveDown and playerRect.bottom < SCREEN_HEIGHT:
            playerRect.move_ip(0, PLAYERMOVERATE)

        # Add new baddies
        baddieAddCounter += 1
        if baddieAddCounter == ADDNEWBADDIERATE:
            baddieAddCounter = 0
            baddieSize = random.randint(BADDIEMINSIZE, BADDIEMAXSIZE)
            newBaddie = {'rect': pygame.Rect(random.randint(0, SCREEN_WIDTH - baddieSize), 0 - baddieSize, baddieSize, baddieSize),
                         'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                         'surface': pygame.transform.scale(baddieImage, (baddieSize, baddieSize))}
            baddies.append(newBaddie)

        # Move the baddies down
        for baddie in baddies:
            baddie['rect'].move_ip(0, baddie['speed'])

        # Delete baddies that have fallen past the bottom
        for baddie in baddies[:]:
            if baddie['rect'].top > SCREEN_HEIGHT:
                baddies.remove(baddie)

        # Draw the game world
        screen.fill(WHITE)
        screen.blit(playerImage, playerRect)
        for baddie in baddies:
            screen.blit(baddie['surface'], baddie['rect'])

        draw_text(f'Score: {score}', font, screen, 10, 0)
        draw_text(f'Lives: {player_lives}', font, screen, 10, 40)

        pygame.display.flip()

        # Check for collisions
        if playerHasHitBaddie(playerRect, baddies):
            player_lives -= 1
            if player_lives == 0:
                return score  # Game over, return the score
            else:
                playerRect.topleft = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)

        clock.tick(60)

def playerHasHitBaddie(playerRect, baddies):
    for baddie in baddies:
        if playerRect.colliderect(baddie['rect']):
            return True
    return False

def main():
    global player_lives

    top_score = 0

    while True:
        start_screen()
        player_lives = 3  # Reset lives at the start of each game

        # Level One
        level_one_completed = run_level_one()

        if level_one_completed:
            victory_screen()
            
            # Level Two
            score = run_level_two()
            
            if score > top_score:
                top_score = score
        else:
            score = 0

        game_over_screen(score, top_score)

if __name__ == "__main__":
    main()
