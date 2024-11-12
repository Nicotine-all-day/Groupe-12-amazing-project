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

        # Set up player and enemy positions
        playerRect = playerImage.get_rect(midbottom=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 20))
        current_enemy_images = enemyImages[level['name']]
        enemyRect = current_enemy_images['stand'].get_rect(midtop=(WINDOW_WIDTH // 2, 50))

        # Initialize animation timer
        throw_animation_timer = 0

        # Main game loop for current level
        while True:
            windowSurface.fill(BACKGROUND_COLOR)
            draw_text(f'Score: {score}', 10, 10)
            draw_text(f'Health: {player_health}', WINDOW_WIDTH - 150, 10)
            draw_text(f'Enemy Health: {max(0, enemy_health)}', WINDOW_WIDTH // 2 - 50, 10)
            windowSurface.blit(playerImage, playerRect)
            windowSurface.blit(current_enemy_images['stand'], enemyRect)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        terminate()

            # Decrease animation timer if active
            if throw_animation_timer > 0:
                throw_animation_timer -= 1

            mainClock.tick(FPS)

# Start the game
main_game()
