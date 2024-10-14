import pygame
import random
import syspython3.13 --version


# Initialize pygame
pygame.init()

# Set up the game window
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Dodge the Blocks")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Set up the player
player_width = 50
player_height = 50
player_x = screen_width // 2 - player_width // 2
player_y = screen_height - player_height - 10
player_speed = 7

# Set up the blocks (obstacles)
block_width = 50
block_height = 50
block_speed = 5
block_list = []

# Font for score
font = pygame.font.SysFont(None, 35)

# Function to create a block
def create_block():
    x = random.randint(0, screen_width - block_width)
    y = -block_height
    block_list.append([x, y])

# Function to move blocks
def move_blocks():
    for block in block_list:
        block[1] += block_speed

# Function to draw player
def draw_player():
    pygame.draw.rect(screen, BLUE, (player_x, player_y, player_width, player_height))

# Function to draw blocks
def draw_blocks():
    for block in block_list:
        pygame.draw.rect(screen, RED, (block[0], block[1], block_width, block_height))

# Function to check collisions
def check_collision(player_x, player_y, block_list):
    for block in block_list:
        if (block[1] + block_height > player_y and
            block[1] < player_y + player_height and
            block[0] + block_width > player_x and
            block[0] < player_x + player_width):
            return True
    return False

# Function to display score
def display_score(score):
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, [10, 10])

# Main game loop
def game_loop():
    global player_x
    clock = pygame.time.Clock()
    score = 0
    block_spawn_time = 30
    block_spawn_counter = 0

    running = True
    while running:
        screen.fill(WHITE)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Move player using "J" and "L" keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_j] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_l] and player_x < screen_width - player_width:
            player_x += player_speed

        # Spawn blocks
        block_spawn_counter += 1
        if block_spawn_counter >= block_spawn_time:
            create_block()
            block_spawn_counter = 0

        # Move blocks
        move_blocks()

        # Remove blocks that are out of screen
        block_list[:] = [block for block in block_list if block[1] <= screen_height]

        # Draw player and blocks
        draw_player()
        draw_blocks()

        # Check for collisions
        if check_collision(player_x, player_y, block_list):
            running = False  # Game over if there's a collision

        # Update score
        score += 1

        # Display score
        display_score(score)

        # Update display
        pygame.display.flip()

        # Control frame rate
        clock.tick(60)

    # Game over screen
    screen.fill(WHITE)
    game_over_text = font.render(f"Game Over! Your Score: {score}", True, BLACK)
    screen.blit(game_over_text, [screen_width // 2 - 150, screen_height // 2 - 20])
    pygame.display.flip()
    pygame.time.wait(3000)

# Run the game loop
if __name__ == "__main__":
    game_loop()
    pygame.quit()
