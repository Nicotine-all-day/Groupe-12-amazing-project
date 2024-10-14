import pygame
import sys

# Initialize pygame
pygame.init()

# Set up the game window
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Simple Spaceship Game')

# Define colors
black = (0, 0, 0)
white = (255, 255, 255)

# Set up FPS (frames per second)
clock = pygame.time.Clock()

# Define spaceship properties
spaceship_width = 40
spaceship_height = 60
spaceship_x = screen_width // 2 - spaceship_width // 2
spaceship_y = screen_height - spaceship_height - 10
spaceship_speed = 5

# Game loop flag
running = True

# Main game loop
while running:
    screen.fill(black)  # Fill screen with black
    
    # Event handling (e.g., closing window)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Get key presses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and spaceship_x > 0:
        spaceship_x -= spaceship_speed
    if keys[pygame.K_RIGHT] and spaceship_x < screen_width - spaceship_width:
        spaceship_x += spaceship_speed

    # Draw the spaceship
    pygame.draw.rect(screen, white, (spaceship_x, spaceship_y, spaceship_width, spaceship_height))

    # Update the display
    pygame.display.flip()

    # Control frame rate
    clock.tick(60)

# Quit the game
pygame.quit()
