import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("The Revenge of the Hammer Bros: Power of Vengeance")

# Colors
WHITE = (255, 255, 255)

# Player settings
player_size = 50
player_color = (0, 128, 255)
player_x = SCREEN_WIDTH // 2
player_y = SCREEN_HEIGHT - player_size - 10
player_speed = 5

# Hammer settings
hammer_color = (200, 0, 0)
hammer_size = 20
hammers = []
hammer_speed = 10

# Enemy settings
enemy_size = 50
enemy_color = (0, 255, 0)
enemies = []
enemy_speed = 2
enemy_spawn_rate = 100  # Frames between new enemy spawns

# Game loop variables
running = True
clock = pygame.time.Clock()
enemy_spawn_counter = 0

# Font settings for score
font = pygame.font.Font(None, 36)
score = 0

while running:
    screen.fill(WHITE)  # Fill the screen with white to clear it each frame
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Throw a hammer
                hammer_rect = pygame.Rect(player_x + player_size // 2 - hammer_size // 2, player_y, hammer_size, hammer_size)
                hammers.append(hammer_rect)
    
    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
    if keys[pygame.K_UP]:
        player_y -= player_speed
    if keys[pygame.K_DOWN]:
        player_y += player_speed

    # Keep player within screen bounds
    player_x = max(0, min(SCREEN_WIDTH - player_size, player_x))
    player_y = max(0, min(SCREEN_HEIGHT - player_size, player_y))

    # Update hammers
    for hammer in hammers[:]:
        hammer.y -= hammer_speed
        if hammer.y < 0:
            hammers.remove(hammer)

    # Spawn enemies
    enemy_spawn_counter += 1
    if enemy_spawn_counter >= enemy_spawn_rate:
        enemy_spawn_counter = 0
        enemy_x = pygame.Rect(0, 0, SCREEN_WIDTH - enemy_size, enemy_size).x
        enemy_rect = pygame.Rect(enemy_x, 0, enemy_size, enemy_size)
        enemies.append(enemy_rect)

    # Update enemies
    for enemy in enemies[:]:
        enemy.y += enemy_speed
        if enemy.y > SCREEN_HEIGHT:
            enemies.remove(enemy)

    # Check for collisions between hammers and enemies
    for hammer in hammers[:]:
        for enemy in enemies[:]:
            if hammer.colliderect(enemy):
                hammers.remove(hammer)
                enemies.remove(enemy)
                score += 10
                break

    # Draw the player
    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
    pygame.draw.rect(screen, player_color, player_rect)
    
    # Draw hammers
    for hammer in hammers:
        pygame.draw.rect(screen, hammer_color, hammer)
    
    # Draw enemies
    for enemy in enemies:
        pygame.draw.rect(screen, enemy_color, enemy)

    # Draw score
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    # Update the display
    pygame.display.flip()

    # Frame rate
    clock.tick(60)
