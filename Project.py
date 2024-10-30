import pygame
import random
import sys
from pygame.locals import *  # Import necessary constants like K_LEFT, QUIT, etc.

# Constants
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
TEXT_COLOR = (0, 0, 0)
BACKGROUND_COLOR = (135, 206, 235)
FPS = 60
ENEMY_MIN_SIZE = 10
ENEMY_MAX_SIZE = 40
ENEMY_MIN_SPEED = 1
ENEMY_MAX_SPEED = 8
ADD_NEW_ENEMY_RATE = 6
PLAYER_MOVE_RATE = 5
HAMMER_SPEED = 10

# Initialize pygame
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Hammer Bro: Power of Vengeance')
pygame.mouse.set_visible(False)

# Placeholder images
hammerImage = pygame.Surface((10, 20))
hammerImage.fill((0, 0, 255))  # Blue to simulate a hammer
font = pygame.font.SysFont(None, 48)
playerImage = pygame.image.load('hammer_bro.png')  # Placeholder for Hammer Bro
playerRect = playerImage.get_rect()
enemyImage = pygame.image.load('enemy.png')        # Placeholder for Mario's allies

# Functions
def terminate():
    pygame.quit()
    sys.exit()

def waitForPlayerToPressKey():
    """Wait for player to press any key to continue."""
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                terminate()
            if event.type == KEYDOWN:
                return

def playerHasHitEnemy(playerRect, enemies):
    """Check if player has collided with any enemy."""
    return any(playerRect.colliderect(e['rect']) for e in enemies)

def drawText(text, font, surface, x, y):
    """Draw text on the surface."""
    text_obj = font.render(text, True, TEXT_COLOR)
    text_rect = text_obj.get_rect(topleft=(x, y))
    surface.blit(text_obj, text_rect)

# Main game loop
def main_game():
    top_score = 0
    while True:
        # Game state initialization
        enemies, hammers = [], []
        score, enemy_add_counter = 0, 0
        playerRect.topleft = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 50)
        move_left = move_right = move_up = move_down = shooting = False

        while True:  # Main game loop
            score += 1
            for event in pygame.event.get():
                if event.type == QUIT:
                    terminate()
                
                # Refactored repeated KEYDOWN and KEYUP events
                if event.type in (KEYDOWN, KEYUP):
                    key_state = event.type == KEYDOWN
                    if event.key in (K_LEFT, K_a):
                        move_left = key_state
                        move_right = not key_state
                    elif event.key in (K_RIGHT, K_d):
                        move_right = key_state
                        move_left = not key_state
                    elif event.key in (K_UP, K_w):
                        move_up = key_state
                        move_down = not key_state
                    elif event.key in (K_DOWN, K_s):
                        move_down = key_state
                        move_up = not key_state
                    elif event.key == K_SPACE:
                        shooting = key_state

            # Add new enemies at intervals
            enemy_add_counter += 1
            if enemy_add_counter == ADD_NEW_ENEMY_RATE:
                enemy_add_counter = 0
                enemy_size = random.randint(ENEMY_MIN_SIZE, ENEMY_MAX_SIZE)
                new_enemy = {
                    'rect': pygame.Rect(random.randint(0, WINDOW_WIDTH - enemy_size), -enemy_size, enemy_size, enemy_size),
                    'speed': random.randint(ENEMY_MIN_SPEED, ENEMY_MAX_SPEED),
                    'surface': pygame.transform.scale(enemyImage, (enemy_size, enemy_size)),
                }
                enemies.append(new_enemy)

            # Move the player
            if move_left and playerRect.left > 0:
                playerRect.move_ip(-PLAYER_MOVE_RATE, 0)
            if move_right and playerRect.right < WINDOW_WIDTH:
                playerRect.move_ip(PLAYER_MOVE_RATE, 0)
            if move_up and playerRect.top > 0:
                playerRect.move_ip(0, -PLAYER_MOVE_RATE)
            if move_down and playerRect.bottom < WINDOW_HEIGHT:
                playerRect.move_ip(0, PLAYER_MOVE_RATE)

            # Shooting mechanic
            if shooting:
                hammer_rect = pygame.Rect(playerRect.centerx, playerRect.top, 10, 20)
                hammers.append(hammer_rect)

            # Move hammers
            for hammer in hammers[:]:
                hammer.top -= HAMMER_SPEED
                if hammer.top < 0:
                    hammers.remove(hammer)

            # Move enemies and check for off-screen
            for enemy in enemies:
                enemy['rect'].move_ip(0, enemy['speed'])
            enemies = [enemy for enemy in enemies if enemy['rect'].top <= WINDOW_HEIGHT]

            # Check for collisions between hammers and enemies
            for hammer in hammers[:]:
                for enemy in enemies[:]:
                    if hammer.colliderect(enemy['rect']):
                        hammers.remove(hammer)
                        enemies.remove(enemy)
                        score += 10
                        break

            # Draw game elements
            windowSurface.fill(BACKGROUND_COLOR)
            drawText(f'Score: {score}', font, windowSurface, 10, 0)
            drawText(f'Top Score: {top_score}', font, windowSurface, 10, 40)
            windowSurface.blit(playerImage, playerRect)

            for hammer in hammers:
                windowSurface.blit(hammerImage, hammer)

            for enemy in enemies:
                windowSurface.blit(enemy['surface'], enemy['rect'])

            pygame.display.update()

            # Check if player collides with any enemy
            if playerHasHitEnemy(playerRect, enemies):
                if score > top_score:
                    top_score = score  # Update top score
                break

            mainClock.tick(FPS)

        # Game over screen
        drawText('GAME OVER', font, windowSurface, (WINDOW_WIDTH // 3), (WINDOW_HEIGHT // 3))
        drawText('Press a key to play again.', font, windowSurface, (WINDOW_WIDTH // 3) - 80, (WINDOW_HEIGHT // 3) + 50)
        pygame.display.update()
        waitForPlayerToPressKey()

# Run the game
main_game()
