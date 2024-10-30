import pygame
import random
import sys
import cv2
from ffpyplayer.player import MediaPlayer
from pygame.locals import *

# Constants for screen dimensions, colors, and game properties
WINDOW_WIDTH, WINDOW_HEIGHT = 880, 660  # 10% larger on both width and height
FPS = 60
TEXT_COLOR = (0, 0, 0)
BACKGROUND_COLOR = (135, 206, 235)
PLAYER_MOVE_RATE = 5
HAMMER_SPEED = 10  # Slightly faster
HAMMER_FREQUENCY = 30
MAX_HEALTH = 3
SCALE_FACTOR = 0.4  # Adjusted scale factor for enemy and player images

# Level configurations
LEVELS = [
    {'name': 'Princess', 'health': 10, 'fireball_speed': 4, 'fireball_rate': 70, 'move_pattern': 'random'},
    {'name': 'Luigi', 'health': 20, 'fireball_speed': 6, 'fireball_rate': 80, 'move_pattern': 'jump'},
    {'name': 'Mario', 'health': 40, 'fireball_speed': 8, 'fireball_rate': 90, 'move_pattern': 'aggressive'}
]

# Initialize pygame
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Hammer Bro: Power of Vengeance')

# Load resources
font = pygame.font.SysFont(None, 48)
hammerImage = pygame.image.load('hammer.png')
hammerImage = pygame.transform.scale(hammerImage, (int(hammerImage.get_width() * 0.2), int(hammerImage.get_height() * 0.2)))  # Smaller hammer
fireballImage = pygame.image.load('fireball.png')
fireballImage = pygame.transform.scale(fireballImage, (20, 20))  # Removed background

playerImage = pygame.image.load('hammer_bro.png')
playerImage = pygame.transform.scale(playerImage, (int(playerImage.get_width() * SCALE_FACTOR), int(playerImage.get_height() * SCALE_FACTOR)))

enemyImages = {
    'Princess': {
        'stand': pygame.transform.scale(pygame.image.load('princess_idle.png'), (int(playerImage.get_width() * SCALE_FACTOR * 2), int(playerImage.get_height() * SCALE_FACTOR * 2))),
        'throw': pygame.transform.scale(pygame.image.load('princess_throw.png'), (int(playerImage.get_width() * SCALE_FACTOR * 2), int(playerImage.get_height() * SCALE_FACTOR * 2))),
        'dead': pygame.transform.scale(pygame.image.load('princess_dead.png'), (WINDOW_WIDTH, WINDOW_HEIGHT))
    },
    'Luigi': {
        'stand': pygame.transform.scale(pygame.image.load('luigi_idle.png'), (int(playerImage.get_width() * SCALE_FACTOR * 2), int(playerImage.get_height() * SCALE_FACTOR * 2))),
        'throw': pygame.transform.scale(pygame.image.load('luigi_throw.png'), (int(playerImage.get_width() * SCALE_FACTOR * 2), int(playerImage.get_height() * SCALE_FACTOR * 2))),
        'hit': pygame.transform.scale(pygame.image.load('luigi_hit.png'), (int(playerImage.get_width() * SCALE_FACTOR * 2), int(playerImage.get_height() * SCALE_FACTOR * 2))),
        'dead': pygame.transform.scale(pygame.image.load('luigi_dead.png'), (WINDOW_WIDTH, WINDOW_HEIGHT))
    },
    'Mario': {
        'stand': pygame.transform.scale(pygame.image.load('mario_idle.png'), (int(playerImage.get_width() * SCALE_FACTOR * 2), int(playerImage.get_height() * SCALE_FACTOR * 2))),
        'throw': pygame.transform.scale(pygame.image.load('mario_throw.png'), (int(playerImage.get_width() * SCALE_FACTOR * 2), int(playerImage.get_height() * SCALE_FACTOR * 2))),
        'dead': pygame.transform.scale(pygame.image.load('mario_dead.png'), (WINDOW_WIDTH, WINDOW_HEIGHT))
    }
}

def terminate():
    pygame.quit()
    sys.exit()

def draw_text(text, x, y, color=TEXT_COLOR):
    text_obj = font.render(text, True, color)
    windowSurface.blit(text_obj, (x, y))

def wait_for_key_press():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                return

# Main Game
def main_game():
    level_index = 0
    player_health = MAX_HEALTH

    while level_index < len(LEVELS):
        level = LEVELS[level_index]
        enemy_health = level['health']
        fireball_speed = level['fireball_speed']
        fireball_rate = level['fireball_rate']
        move_pattern = level['move_pattern']
        score = 0
        throw_animation_timer = 0

        current_enemy_images = enemyImages[level['name']]
        current_enemy_image = current_enemy_images['stand']
        enemyRect = current_enemy_image.get_rect()
        enemyRect.midtop = (WINDOW_WIDTH // 2, 50)
        fireballs = []
        enemy_direction = 1
        enemy_jump_counter = 0

        playerRect = playerImage.get_rect()
        playerRect.midbottom = (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 20)
        hammers = []
        move_left = move_right = shooting = False
        hammer_counter = 0

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    terminate()
                if event.type == KEYDOWN:
                    if event.key in (K_LEFT, K_a):
                        move_left = True
                    elif event.key in (K_RIGHT, K_d):
                        move_right = True
                    elif event.key == K_SPACE:
                        shooting = True
                if event.type == KEYUP:
                    if event.key in (K_LEFT, K_a):
                        move_left = False
                    elif event.key in (K_RIGHT, K_d):
                        move_right = False
                    elif event.key == K_SPACE:
                        shooting = False

            if move_left and playerRect.left > 0:
                playerRect.move_ip(-PLAYER_MOVE_RATE, 0)
            if move_right and playerRect.right < WINDOW_WIDTH:
                playerRect.move_ip(PLAYER_MOVE_RATE, 0)

            hammer_counter += 1
            if shooting and hammer_counter >= HAMMER_FREQUENCY:
                hammer_rect = hammerImage.get_rect(midbottom=(playerRect.centerx, playerRect.top))
                hammers.append(hammer_rect)
                hammer_counter = 0

            for hammer in hammers[:]:
                hammer.top -= HAMMER_SPEED
                if hammer.top < 0:
                    hammers.remove(hammer)

            if random.randint(1, fireball_rate) == 1:
                fireball_rect = fireballImage.get_rect(midtop=(enemyRect.centerx, enemyRect.bottom))
                fireballs.append(fireball_rect)
                current_enemy_image = current_enemy_images['throw']
                throw_animation_timer = 10

            if throw_animation_timer > 0:
                throw_animation_timer -= 1
            else:
                current_enemy_image = current_enemy_images['stand']

            for fireball in fireballs[:]:
                fireball.top += fireball_speed
                if fireball.top > WINDOW_HEIGHT:
                    fireballs.remove(fireball)

            for hammer in hammers[:]:
                if hammer.colliderect(enemyRect):
                    hammers.remove(hammer)
                    enemy_health -= 1
                    score += 10
                    current_enemy_image = current_enemy_images.get('hit', current_enemy_image)
                    if enemy_health <= 0:
                        windowSurface.fill(BACKGROUND_COLOR)
                        windowSurface.blit(current_enemy_images['dead'], (0, 0))
                        draw_text(f'Level {level_index + 1} passed!', WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2)
                        pygame.display.update()
                        pygame.time.wait(5000)
                        level_index += 1
                        break

            for fireball in fireballs[:]:
                if fireball.colliderect(playerRect):
                    fireballs.remove(fireball)
                    player_health -= 1
                    if player_health <= 0:
                        draw_text('Game Over', WINDOW_WIDTH // 3, WINDOW_HEIGHT // 3)
                        pygame.display.update()
                        wait_for_key_press()
                        return

            windowSurface.fill(BACKGROUND_COLOR)
            draw_text(f'Score: {score}', 10, 10)
            draw_text(f'Health: {player_health}', WINDOW_WIDTH - 150, 10)
            draw_text(f'Enemy Health: {max(0, enemy_health)}', WINDOW_WIDTH // 2 - 50, 10)
            windowSurface.blit(playerImage, playerRect)
            windowSurface.blit(current_enemy_image, enemyRect)

            for hammer in hammers:
                windowSurface.blit(hammerImage, hammer)
            for fireball in fireballs:
                windowSurface.blit(fireballImage, fireball)

            pygame.display.update()
            mainClock.tick(FPS)

    windowSurface.fill(BACKGROUND_COLOR)
    draw_text('You Win!', WINDOW_WIDTH // 3, WINDOW_HEIGHT // 3)
    pygame.display.update()
    wait_for_key_press()

# Start the game
main_game()
