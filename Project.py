import pygame
import random
import sys
import cv2
from ffpyplayer.player import MediaPlayer
from pygame.locals import *

# Constants for screen dimensions, colors, and game properties
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
FPS = 60
TEXT_COLOR = (0, 0, 0)
BACKGROUND_COLOR = (135, 206, 235)
PLAYER_MOVE_RATE = 5
HAMMER_SPEED = 7  # Slowed down
HAMMER_FREQUENCY = 30  # Slowed down
MAX_HEALTH = 3
SCALE_FACTOR = 0.25  # Scale images to 25% of their original size

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
hammerImage = pygame.image.load('hammer.png')
hammerImage = pygame.transform.scale(hammerImage, (int(hammerImage.get_width() * SCALE_FACTOR), int(hammerImage.get_height() * SCALE_FACTOR)))
fireballImage = pygame.image.load('fireball.png')  # Load fireball image
fireballImage = pygame.transform.scale(fireballImage, (20, 20))  # Resize fireball

playerImage = pygame.image.load('hammer_bro.png')
playerImage = pygame.transform.scale(playerImage, (int(playerImage.get_width() * SCALE_FACTOR), int(playerImage.get_height() * SCALE_FACTOR)))

enemyImages = {
    'Princess': {
        'stand': pygame.transform.scale(pygame.image.load('princess_idle.png'), (int(playerImage.get_width() * SCALE_FACTOR), int(playerImage.get_height() * SCALE_FACTOR))),
        'throw': pygame.transform.scale(pygame.image.load('princess_throw.png'), (int(playerImage.get_width() * SCALE_FACTOR), int(playerImage.get_height() * SCALE_FACTOR))),
        'dead': pygame.transform.scale(pygame.image.load('princess_dead.png'), (int(playerImage.get_width() * SCALE_FACTOR), int(playerImage.get_height() * SCALE_FACTOR)))
    },
    'Luigi': {
        'stand': pygame.transform.scale(pygame.image.load('luigi_idle.png'), (int(playerImage.get_width() * SCALE_FACTOR), int(playerImage.get_height() * SCALE_FACTOR))),
        'throw': pygame.transform.scale(pygame.image.load('luigi_throw.png'), (int(playerImage.get_width() * SCALE_FACTOR), int(playerImage.get_height() * SCALE_FACTOR))),
        'dead': pygame.transform.scale(pygame.image.load('luigi_dead.png'), (int(playerImage.get_width() * SCALE_FACTOR), int(playerImage.get_height() * SCALE_FACTOR)))
    },
    'Mario': {
        'stand': pygame.transform.scale(pygame.image.load('mario_idle.png'), (int(playerImage.get_width() * SCALE_FACTOR), int(playerImage.get_height() * SCALE_FACTOR))),
        'throw': pygame.transform.scale(pygame.image.load('mario_throw.png'), (int(playerImage.get_width() * SCALE_FACTOR), int(playerImage.get_height() * SCALE_FACTOR))),
        'dead': pygame.transform.scale(pygame.image.load('mario_dead.png'), (int(playerImage.get_width() * SCALE_FACTOR), int(playerImage.get_height() * SCALE_FACTOR)))
    }
}

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
        frame = cv2.transpose(frame)
        frame = pygame.surfarray.make_surface(frame)
        frame = pygame.transform.scale(frame, (WINDOW_WIDTH, WINDOW_HEIGHT))
        
        windowSurface.blit(frame, (0, 0))
        pygame.draw.rect(windowSurface, (0, 0, 0), skip_button_rect)
        draw_text("Skip", WINDOW_WIDTH - 90, WINDOW_HEIGHT - 45, color=(255, 255, 255))

        pygame.display.update()
        
        if cv2.waitKey(20) & 0xFF == ord('q'):
            break
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                cap.release()
                return
            elif event.type == MOUSEBUTTONDOWN and skip_button_rect.collidepoint(event.pos):
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
        enemy_throwing = False
        throw_animation_timer = 0

        # Enemy setup
        current_enemy_images = enemyImages[level['name']]
        current_enemy_image = current_enemy_images['stand']
        enemyRect = current_enemy_image.get_rect()
        enemyRect.midtop = (WINDOW_WIDTH // 2, 50)
        fireballs = []
        enemy_direction = 1  # Initial direction for left-right movement

        # Player setup
        playerRect = playerImage.get_rect()
        playerRect.midbottom = (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 20)
        hammers = []
        move_left = move_right = shooting = False
        hammer_counter = 0  # For controlling hammer frequency

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

            # Shooting mechanic with reduced frequency
            hammer_counter += 1
            if shooting and hammer_counter >= HAMMER_FREQUENCY:
                hammer_rect = hammerImage.get_rect(midbottom=(playerRect.centerx, playerRect.top))
                hammers.append(hammer_rect)
                hammer_counter = 0  # Reset counter

            # Move hammers
            for hammer in hammers[:]:
                hammer.top -= HAMMER_SPEED
                if hammer.top < 0:
                    hammers.remove(hammer)

            # Enemy movement (left-right)
            enemyRect.x += enemy_direction * 3  # Adjust speed as needed
            if enemyRect.left <= 0 or enemyRect.right >= WINDOW_WIDTH:
                enemy_direction *= -1  # Reverse direction at edges

            # Enemy throw animation and fireball shooting
            if random.randint(1, fireball_rate) == 1:
                fireball_rect = fireballImage.get_rect(midtop=(enemyRect.centerx, enemyRect.bottom))
                fireballs.append(fireball_rect)
                current_enemy_image = current_enemy_images['throw']
                throw_animation_timer = 10  # Show throw image for a few frames

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
                        # Show dead enemy image and level passed message
                        windowSurface.fill(BACKGROUND_COLOR)
                        windowSurface.blit(current_enemy_images['dead'], enemyRect)
                        draw_text(f'Level {level_index + 1} passed!', WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2)
                        pygame.display.update()
                        pygame.time.wait(5000)  # Wait 5 seconds
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
            draw_text(f'Enemy Health: {max(0, enemy_health)}', WINDOW_WIDTH // 2 - 50, 10)
            windowSurface.blit(playerImage, playerRect)
            windowSurface.blit(current_enemy_image, enemyRect)

            for hammer in hammers:
                windowSurface.blit(hammerImage, hammer)
            for fireball in fireballs:
                windowSurface.blit(fireballImage, fireball)

            pygame.display.update()
            mainClock.tick(FPS)

    # Victory screen
    windowSurface.fill(BACKGROUND_COLOR)
    draw_text('You Win!', WINDOW_WIDTH // 3, WINDOW_HEIGHT // 3)
    pygame.display.update()
    wait_for_key_press()

# Start the game
main_game()
