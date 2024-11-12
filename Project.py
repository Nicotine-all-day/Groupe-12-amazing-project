# Importing modules and initializing constants

import pygame
import random
import sys
from pygame.locals import *

# Constants for screen dimensions, colors, and game properties
WINDOW_WIDTH, WINDOW_HEIGHT = 880, 660
FPS = 60
TEXT_COLOR = (0, 0, 0)
BACKGROUND_COLOR = (135, 206, 235)
PLAYER_MOVE_RATE = 5
HAMMER_SPEED = 10
HAMMER_FREQUENCY = 30
MAX_HEALTH = 3
SCALE_FACTOR_PLAYER = 0.25
SCALE_FACTOR_ENEMY = 0.5
ENEMY_MOVE_RATE = 3
ENEMY_DODGE_CHANCE = 0.02

# Colors and visuals
LEVEL_COLORS = [(135, 206, 250), (60, 179, 113), (255, 182, 193)]
LEVEL_TITLES = ['Level 1: The Princess Challenge', 'Level 2: Luigi Showdown', 'Level 3: Mario Finale']

# Level configurations
LEVELS = [
    {'name': 'Princess', 'health': 10, 'fireball_speed': 4, 'fireball_rate': 90, 'move_pattern': 'random'},
    {'name': 'Luigi', 'health': 20, 'fireball_speed': 6, 'fireball_rate': 100, 'move_pattern': 'random_jump'},
    {'name': 'Mario', 'health': 40, 'fireball_speed': 8, 'fireball_rate': 110, 'move_pattern': 'aggressive'}
]

# Initialize pygame
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Hammer Bro: Power of Vengeance')

# Load resources
font = pygame.font.SysFont(None, 48)
hammerImage = pygame.image.load('hammer.png').convert_alpha()
hammerImage = pygame.transform.scale(hammerImage, (int(30 * SCALE_FACTOR_PLAYER), int(20 * SCALE_FACTOR_PLAYER)))
fireballImage = pygame.image.load('fireball.png').convert_alpha()
fireballImage = pygame.transform.scale(fireballImage, (20, 20))

playerImage = pygame.image.load('hammer_bro.png').convert_alpha()
playerImage = pygame.transform.scale(playerImage, (int(100 * SCALE_FACTOR_PLAYER), int(120 * SCALE_FACTOR_PLAYER)))

# Loading enemy images and scaling
enemyImages = {}
for level in LEVELS:
    enemyImages[level['name']] = {
        'stand': pygame.image.load(f'{level["name"].lower()}_idle.png').convert_alpha(),
        'throw': pygame.image.load(f'{level["name"].lower()}_throw.png').convert_alpha(),
        'dead': pygame.image.load(f'{level["name"].lower()}_dead.png').convert_alpha()
    }
    enemyImages[level['name']]['stand'] = pygame.transform.scale(enemyImages[level['name']]['stand'], (int(100 * SCALE_FACTOR_ENEMY), int(120 * SCALE_FACTOR_ENEMY)))
    enemyImages[level['name']]['throw'] = pygame.transform.scale(enemyImages[level['name']]['throw'], (int(100 * SCALE_FACTOR_ENEMY), int(120 * SCALE_FACTOR_ENEMY)))
    enemyImages[level['name']]['dead'] = pygame.transform.scale(enemyImages[level['name']]['dead'], (WINDOW_WIDTH, WINDOW_HEIGHT))

# Utility functions
def terminate():
    pygame.quit()
    sys.exit()

def draw_text(text, x, y, color=TEXT_COLOR):
    text_obj = font.render(text, True, color)
    windowSurface.blit(text_obj, (x, y))

def wait_for_key_press():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
                return

# Main game setup and play function
def main_game():
    level_index = 0
    player_health = MAX_HEALTH

    while level_index < len(LEVELS):
        # Game setup for current level
        level = LEVELS[level_index]
        enemy_health = level['health']
        score = 0

        # Display level start title
        windowSurface.fill(LEVEL_COLORS[level_index])
        draw_text(LEVEL_TITLES[level_index], WINDOW_WIDTH // 2 - 150, WINDOW_HEIGHT // 2, color=(255, 255, 255))
        pygame.display.update()
        pygame.time.wait(3000)

        # Set up player and enemy positions
        playerRect = playerImage.get_rect(midbottom=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 20))
        current_enemy_images = enemyImages[level['name']]
        enemyRect = current_enemy_images['stand'].get_rect(midtop=(WINDOW_WIDTH // 2, 50))

        # Initialize animation timer and hammer list
        throw_animation_timer = 0
        hammers = []
        fireballs = []
        move_left = move_right = shooting = False
        hammer_counter = 0
        fireball_counter = 0
        enemy_direction = random.choice([-1, 1])  # Enemy starts by moving left or right

        # Main game loop for current level
        while True:
            windowSurface.fill(LEVEL_COLORS[level_index])
            draw_text(f'Score: {score}', 10, 10)
            draw_text(f'Health: {player_health}', WINDOW_WIDTH - 150, 10)
            draw_text(f'Enemy Health: {max(0, enemy_health)}', WINDOW_WIDTH // 2 - 50, 10)
            windowSurface.blit(playerImage, playerRect)
            windowSurface.blit(current_enemy_images['stand'], enemyRect)

            # Draw hammers
            for hammer in hammers:
                windowSurface.blit(hammerImage, hammer)

            # Draw fireballs
            for fireball in fireballs:
                windowSurface.blit(fireballImage, fireball)

            pygame.display.update()

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        terminate()
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        move_left = True
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        move_right = True
                    if event.key == pygame.K_SPACE:
                        shooting = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        move_left = False
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        move_right = False
                    if event.key == pygame.K_SPACE:
                        shooting = False

            # Player movement
            if move_left and playerRect.left > 0:
                playerRect.move_ip(-PLAYER_MOVE_RATE, 0)
            if move_right and playerRect.right < WINDOW_WIDTH:
                playerRect.move_ip(PLAYER_MOVE_RATE, 0)

            # Shooting mechanic
            hammer_counter += 1
            if shooting and hammer_counter >= HAMMER_FREQUENCY:
                hammer_rect = hammerImage.get_rect(midbottom=(playerRect.centerx, playerRect.top))
                hammers.append(hammer_rect)
                hammer_counter = 0

            # Move hammers
            for hammer in hammers[:]:
                hammer.top -= HAMMER_SPEED
                if hammer.top < 0:
                    hammers.remove(hammer)

            # Enemy movement - dodging hammers
            enemyRect.x += enemy_direction * ENEMY_MOVE_RATE
            if enemyRect.left <= 0 or enemyRect.right >= WINDOW_WIDTH:
                enemy_direction *= -1

            # Random chance for the enemy to change direction to dodge hammers
            if random.random() < ENEMY_DODGE_CHANCE:
                enemy_direction *= -1

            # Enemy shooting fireballs
            fireball_counter += 1
            if fireball_counter >= level['fireball_rate']:
                fireball_rect = fireballImage.get_rect(midtop=(enemyRect.centerx, enemyRect.bottom))
                fireballs.append(fireball_rect)
                fireball_counter = 0

            # Move fireballs
            for fireball in fireballs[:]:
                fireball.top += level['fireball_speed']
                if fireball.top > WINDOW_HEIGHT:
                    fireballs.remove(fireball)

            # Check for hammer collision with enemy
            for hammer in hammers[:]:
                if hammer.colliderect(enemyRect):
                    hammers.remove(hammer)
                    enemy_health -= 1
                    score += 10
                    if enemy_health <= 0:
                        draw_text(f'Level {level_index + 1} Cleared!', WINDOW_WIDTH // 3, WINDOW_HEIGHT // 3)
                        pygame.display.update()
                        pygame.time.wait(2000)
                        level_index += 1
                        if level_index >= len(LEVELS):
                            draw_text('You Win!', WINDOW_WIDTH // 3, WINDOW_HEIGHT // 3)
                            pygame.display.update()
                            wait_for_key_press()
                            return
                        break

            # Check for fireball collision with player
            for fireball in fireballs[:]:
                if fireball.colliderect(playerRect):
                    fireballs.remove(fireball)
                    player_health -= 1
                    if player_health <= 0:
                        draw_text('Game Over', WINDOW_WIDTH // 3, WINDOW_HEIGHT // 3)
                        pygame.display.update()
                        wait_for_key_press()
                        return

            mainClock.tick(FPS)

# Start the game
main_game()
