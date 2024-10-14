import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set up the game window
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Dodge the Blocks")

# Colors (RGB format)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Player properties
player_width = 50
player_height = 50
player_x = screen_width // 2 - player_width // 2
player_y = screen_height - player_height - 10
player_speed = 5

# Block properties
block_width = 50
block_height = 50
block_speed = 5
block_list = []

# Set up the game clock
clock = pygame.time.Clock()

# Font for displaying score
font = pygame.font.SysFont(None, 36)

# Function to create a new block
def create_block():
    x = random.randint(0, screen_width - block_width)
    y = -block_height  # Start above the screen
    return [x, y]

# Function to display score
def display_score(score):
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

# Main game loop
def game_loop():
    global player_x

    # Initialize game variables
    running = True
    score = 0
    block_list.append(create_block())

    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Handle player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < screen_width - player_width:
            player_x += player_speed

        # Update blocks
        for block in block_list:
            block[1] += block_speed
            if block[1] > screen_height:  # Block is off the screen
                block_list.remove(block)
                block_list.append(create_block())  # Add a new block
                score += 1  # Increase score when dodging a block

        # Check for collisions
        for block in block_list:
            if (player_x < block[0] + block_width and
                player_x + player_width > block[0] and
                player_y < block[1] + block_height and
                player_y + player_height > block[1]):
                running = False  # End the game on collision

        # Fill the screen with white
        screen.fill(WHITE)

        # Draw the player
        pygame.draw.rect(screen, BLUE, (player_x, player_y, player_width, player_height))

        # Draw the blocks
        for block in block_list:
            pygame.draw.rect(screen, RED, (block[0], block[1], block_width, block_height))

        # Display the score
        display_score(score)

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

# Start the game
game_loop()
