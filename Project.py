import pygame
import random
import sys
import cv2
from ffpyplayer.player import MediaPlayer
from pygame.locals import *

{
    "cSpell.words": [
        "pygame", "cv2", "ffpyplayer", "blit", "KEYDOWN", "KEYUP",
        "colliderect", "centerx", "midtop", "midbottom", "surfarray"
    ]
}


# Constants for screen dimensions, colors, and game properties
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
FPS = 60
TEXT_COLOR = (0, 0, 0)
BACKGROUND_COLOR = (135, 206, 235)
PLAYER_MOVE_RATE = 5
HAMMER_SPEED = 15
MAX_HEALTH = 3

# Level configurations
LEVELS = [
    {'name': 'Princess', 'health': 10, 'fireball_speed': 4, 'fireball_rate': 100, 'move_pattern': 'slow'},
    {'name': 'Luigi', 'health': 20, 'fireball_speed': 8, 'fireball_rate': 70, 'move_pattern': 'jump'},
    {'name': 'Mario', 'health': 30, 'fireball_speed': 12, 'fireball_rate': 50, 'move_pattern': 'aggressive'}
]

# Initialize pygame
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Hammer Bro: Power of Vengeance')

# Load resources
font = pygame.font.SysFont(None, 48)
hammerImage = pygame.Surface((10, 20))
hammerImage.fill((0, 0, 255))
fireballImage = pygame.Surface((10, 10))
fireballImage.fill((255, 0, 0))
playerImage = pygame.image.load('hammer_bro.png')
enemyImages = {
    'Princess': {
        'idle': pygame.image.load('princess_idle.png'),
        'throw': pygame.image.load('princess_throw.png'),
        'hit': pygame.image.load('princess_hit.png'),
        'dead': pygame.image.load('princess_dead.png')
    },
    'Luigi': {
        'idle': pygame.image.load('luigi_idle.png'),
        'throw': pygame.image.load('luigi_throw.png'),
        'hit': pygame.image.load('luigi_hit.png'),
        'dead': pygame.image.load('luigi_dead.png')
    },
    'Mario': {
        'idle': pygame.image.load('mario_idle.png'),
        'throw': pygame.image.load('mario_throw.png'),
        'hit': pygame.image.load('mario_hit.png'),
        'dead': pygame.image.load('mario_dead.png')
    }
}
healthImage = pygame.Surface((20, 20))
healthImage.fill((0, 255, 0))

# Function to play intro video
def play_intro_video(video_path):
    cap = cv2.VideoCapture(video_path)
    player = MediaPlayer(video_path)
    while cap.isOpened():
        ret, frame = cap.read()
        audio_frame, val = player.get_frame()
        if not ret:
            break
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.transpose(frame)
        frame = pygame.surfarray.make_surface(frame)
        frame = pygame.transform.scale(frame, (WINDOW_WIDTH, WINDOW_HEIGHT))
        windowSurface.blit(frame, (0, 0))
        pygame.display.update()
        if cv2.waitKey(20) & 0xFF == ord('q'):
            break
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                cap.release()
                return
            if event.type == QUIT:
                cap.release()
                terminate()
        if audio_frame is not None:
            img, t = audio_frame
    cap.release()
    player.close()

# Utility functions
def terminate():
    pygame.quit()
    sys.exit()

def draw_text(text, x, y):
    text_obj = font.render(text, True, TEXT_COLOR)
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
    play_intro_video("intro.mp4")

    while level_index < len(LEVELS):
        level = LEVELS[level_index]
        enemy_health = level['health']
        fireball_speed = level['fireball_speed']
        fireball_rate = level['fireball_rate']
        move_pattern = level['move_pattern']
        score = 0

        # Enemy setup
        enemyImageSet = enemyImages[level['name']]
        current_enemy_image = enemyImageSet['idle']
        enemyRect = current_enemy_image.get_rect()
        enemyRect.midtop = (WINDOW_WIDTH // 2, 50)
        fireballs = []

        # Player setup
        playerRect = playerImage.get_rect()
        playerRect.midbottom = (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 20)
        hammers = []
        move_left = move_right = shooting = False

        # Game loop for current level
        while True:
            # Event handling
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

            # Player movement
            if move_left and playerRect.left > 0:
                playerRect.move_ip(-PLAYER_MOVE_RATE, 0)
            if move_right and playerRect.right < WINDOW_WIDTH:
                playerRect.move_ip(PLAYER_MOVE_RATE, 0)

            # Shooting mechanic
            if shooting:
                hammer_rect = pygame.Rect(playerRect.centerx, playerRect.top - 20, 10, 20)
                hammers.append(hammer_rect)

            # Move hammers
            for hammer in hammers[:]:
                hammer.top -= HAMMER_SPEED
                if hammer.top < 0:
                    hammers.remove(hammer)

            # Enemy fireball shooting logic
            if random.randint(1, fireball_rate) == 1:
                fireball_rect = pygame.Rect(enemyRect.centerx, enemyRect.bottom, 10, 10)
                fireballs.append(fireball_rect)

            # Move fireballs
            for fireball in fireballs[:]:
                fireball.top += fireball_speed
                if fireball.top > WINDOW_HEIGHT:
                    fireballs.remove(fireball)

            # Check for hammer collisions with enemy
            for hammer in hammers[:]:
                if hammer.colliderect(enemyRect):
                    hammers.remove(hammer)
                    current_enemy_image = enemyImageSet['hit']
                    enemy_health -= 1
                    score += 10
                    if enemy_health <= 0:
                        current_enemy_image = enemyImageSet['dead']
                        level_index += 1
                        break

            # Check if player is hit by fireball
            for fireball in fireballs[:]:
                if fireball.colliderect(playerRect):
                    fireballs.remove(fireball)
                    player_health -= 1
                    if player_health <= 0:
                        draw_text('Game Over', WINDOW_WIDTH // 3, WINDOW_HEIGHT // 3)
                        pygame.display.update()
                        wait_for_key_press()
                        return

            # Draw game elements
            windowSurface.fill(BACKGROUND_COLOR)
            draw_text(f'Score: {score}', 10, 10)
            draw_text(f'Health: {player_health}', WINDOW_WIDTH - 150, 10)
            draw_text(f'Enemy Health: {enemy_health}', WINDOW_WIDTH // 2 - 50, 10)
            windowSurface.blit(playerImage, playerRect)
            windowSurface.blit(current_enemy_image, enemyRect)

            for hammer in hammers:
                windowSurface.blit
