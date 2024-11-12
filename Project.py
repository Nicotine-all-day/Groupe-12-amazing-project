# Importing modules and initializing constants

import pygame
import random
import sys
import cv2
from ffpyplayer.player import MediaPlayer
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

# Function to play intro video with skip button
def play_intro_video(video_path):
    cap = cv2.VideoCapture(video_path)
    player = MediaPlayer(video_path)
    skip_button_rect = pygame.Rect(WINDOW_WIDTH - 100, WINDOW_HEIGHT - 50, 80, 30)

    while cap.isOpened():
        ret, frame = cap.read()
        audio_frame, val = player.get_frame()
        if not ret:
            break
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = pygame.surfarray.make_surface(frame)
        frame = pygame.transform.rotate(frame, 180)  # Rotate the frame 180 degrees to the right
        frame = pygame.transform.scale(frame, (WINDOW_WIDTH, WINDOW_HEIGHT))

        windowSurface.blit(frame, (0, 0))
        pygame.draw.rect(windowSurface, (0, 0, 0), skip_button_rect)
        draw_text("Skip", WINDOW_WIDTH - 90, WINDOW_HEIGHT - 45, color=(255, 255, 255))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN and skip_button_rect.collidepoint(event.pos):
                cap.release()
                player.close()
                return
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                cap.release()
                player.close()
                return
            if event.type == QUIT:
                terminate()
        if audio_frame is not None:
            img, t = audio_frame
    cap.release()
    player.close()

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
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                return

# Main game setup and play function (to be corrected further)
def main_game():
    level_index = 0
    player_health = MAX_HEALTH
    play_intro_video("intro.mp4")

    while level_index < len(LEVELS):
        # Additional corrections will be applied here
        pass

# Start the game
main_game()
