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
# Function to play intro video with skip button
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

        if cv2.waitKey(20) & 0xFF == ord('q'):
            break
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN and skip_button_rect.collidepoint(event.pos):
                cap.release()
                return
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                cap.release()
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
        current_enemy_images = enemyImages[level['name']]
        current_enemy_image = current_enemy_images['stand']
        enemyRect = current_enemy_image.get_rect(midtop=(WINDOW_WIDTH // 2, 50))

        # Player setup
        playerRect = playerImage.get_rect(midbottom=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 20))
        hammers = []
        move_left = move_right = shooting = False
        hammer_counter = 0

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

            # Enemy movement
            if move_pattern == 'random':
                enemyRect.x += random.choice([-1, 1]) * (5 if not 'jump' in move_pattern else 0)  # Only move if not in jump mode
                if enemyRect.left < 0 or enemyRect.right > WINDOW_WIDTH:
                    enemy_direction *= -1
            elif move_pattern == 'random_jump' and random.randint(1, 100) <= 20:  # 20% chance to jump
                enemyRect.y -= 10  # Simple jump
                if enemyRect.bottom > WINDOW_HEIGHT:
                    enemyRect.bottom = WINDOW_HEIGHT

            # Fireball shooting and animations
            if random.randint(1, fireball_rate) == 1:
                fireball_rect = fireballImage.get_rect(midtop=(enemyRect.centerx, enemyRect.bottom))
                fireballs.append(fireball_rect)
                current_enemy_image = current_enemy_images['throw']
                throw_animation_timer = 10  # Frames to display throw animation

            if throw_animation_timer > 0:
                throw_animation_timer -= 1
            else:
                current_enemy_image = current_enemy_images['stand']

            # Move fireballs
            for fireball in fireballs[:]:
                fireball.top += fireball_speed
                if fireball.top > WINDOW_HEIGHT:
                    fireballs.remove(fireball)

            # Check for hammer collisions with enemy
            for hammer in hammers[:]:
                if hammer.colliderect(enemyRect):
                    hammers.remove(hammer)
                    enemy_health -= 1
                    score += 10
                    if enemy_health <= 0:
                        windowSurface.fill(BACKGROUND_COLOR)
                        windowSurface.blit(current_enemy_images['dead'], (0, 0))
                        draw_text(f'Level {level_index + 1} passed!', WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2)
                        pygame.display.update()
                        pygame.time.wait(5000)  # Wait 5 seconds before continuing
                        level_index += 1  # Move to next level
                        if level_index >= len(LEVELS):
                            draw_text('You Win!', WINDOW_WIDTH // 3, WINDOW_HEIGHT // 3)
                            pygame.display.update()
                            wait_for_key_press()
                            return
                        break  # Exit loop to load next level

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

            # Drawing game elements
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

# Start the game
main_game()
