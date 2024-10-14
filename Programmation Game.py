import pygame
import random

# Initialize pygame
pygame.init()

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Create the screen object
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Define player attributes
player_size = 50
player_x = SCREEN_WIDTH // 2
player_y = SCREEN_HEIGHT - 2 * player_size
player_speed = 5

# Define block attributes
block_width = 50
block_height = 50
block_speed = 5
block_list = []

def create_block():
    x_pos = random.randint(0, SCREEN_WIDTH - block_width)
    y_pos = -block_height
    return [x_pos, y_pos]

def update_blocks(block_list):
    for block in block_list:
        block[1] += block_speed
    block_list = [block for block in block_list if block[1] < SCREEN_HEIGHT]
    return block_list

def detect_collision(player_x, player_y, block):
    block_x, block_y = block
    if (player_x < block_x + block_width and player_x + player_size > block_x and
        player_y < block_y + block_height and player_y + player_size > block_y):
        return True
    return False

# Game loop
game_over = False
score = 0

while not game_over:
    screen.fill(WHITE)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    # Move player with arrow keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - player_size:
        player_x += player_speed

    # Update blocks
    if random.random() < 0.05:
        block_list.append(create_block())

    block_list = update_blocks(block_list)

    # Draw blocks
    for block in block_list:
        pygame.draw.rect(screen, RED, (block[0], block[1], block_width, block_height))

    # Draw player
    pygame.draw.rect(screen, BLACK, (player_x, player_y, player_size, player_size))

    # Collision detection
    for block in block_list:
        if detect_collision(player_x, player_y, block):
            game_over = True

    # Update screen
    pygame.display.flip()

    # Set frame rate
    clock.tick(30)

# Quit the game
pygame.quit()


