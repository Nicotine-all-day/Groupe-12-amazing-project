import pygame, random, sys
from pygame.locals import *  # Import necessary constants like K_LEFT, QUIT, etc.

# Constants for game setup
WINDOWWIDTH = 600
WINDOWHEIGHT = 600
TEXTCOLOR = (0, 0, 0)
BACKGROUNDCOLOR = (135, 206, 235)  # Sky blue background
FPS = 60
ENEMY_MINSIZE = 10
ENEMY_MAXSIZE = 40
ENEMY_MINSPEED = 1
ENEMY_MAXSPEED = 8
ADDNEWENEMYRATE = 6
PLAYERMOVERATE = 5
HAMMER_SPEED = 10

# Initialize pygame
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Hammer Bro: Power of Vengeance')
pygame.mouse.set_visible(False)

# Fix Hammer Image
hammerImage = pygame.Surface((10, 20))  # Create a 10x20 pixel surface as placeholder
hammerImage.fill((0, 0, 255))  # Fill it with blue color to simulate a hammer

# Load assets
font = pygame.font.SysFont(None, 48)
playerImage = pygame.image.load('hammer_bro.png')  # Placeholder image for Hammer Bro
playerRect = playerImage.get_rect()
enemyImage = pygame.image.load('enemy.png')        # Placeholder image for Mario's allies

# Utility functions
def terminate():
    pygame.quit()
    sys.exit()

def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                return

def playerHasHitEnemy(playerRect, enemies):
    for e in enemies:
        if playerRect.colliderect(e['rect']):
            return True
    return False

def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# Main game loop
def main_game():
    topScore = 0
    while True:
        # Set up the game start state
        enemies = []
        hammers = []
        score = 0
        playerRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 50)
        moveLeft = moveRight = moveUp = moveDown = False
        shooting = False
        enemyAddCounter = 0

        while True:  # The game loop
            score += 1  # Increase score
            for event in pygame.event.get():
                if event.type == QUIT:
                    terminate()

                if event.type == KEYDOWN:
                    if event.key == K_LEFT or event.key == K_a:
                        moveRight = False
                        moveLeft = True
                    if event.key == K_RIGHT or event.key == K_d:
                        moveLeft = False
                        moveRight = True
                    if event.key == K_UP or event.key == K_w:
                        moveDown = False
                        moveUp = True
                    if event.key == K_DOWN or event.key == K_s:
                        moveUp = False
                        moveDown = True
                    if event.key == K_SPACE:
                        shooting = True

                if event.type == KEYUP:
                    if event.key == K_LEFT or event.key == K_a:
                        moveLeft = False
                    if event.key == K_RIGHT or event.key == K_d:
                        moveRight = False
                    if event.key == K_UP or event.key == K_w:
                        moveUp = False
                    if event.key == K_DOWN or event.key == K_s:
                        moveDown = False
                    if event.key == K_SPACE:
                        shooting = False

            # Add new enemies
            enemyAddCounter += 1
            if enemyAddCounter == ADDNEWENEMYRATE:
                enemyAddCounter = 0
                enemySize = random.randint(ENEMY_MINSIZE, ENEMY_MAXSIZE)
                newEnemy = {
                    'rect': pygame.Rect(random.randint(0, WINDOWWIDTH - enemySize), 0 - enemySize, enemySize, enemySize),
                    'speed': random.randint(ENEMY_MINSPEED, ENEMY_MAXSPEED),
                    'surface': pygame.transform.scale(enemyImage, (enemySize, enemySize)),
                }
                enemies.append(newEnemy)

            # Move the player
            if moveLeft and playerRect.left > 0:
                playerRect.move_ip(-1 * PLAYERMOVERATE, 0)
            if moveRight and playerRect.right < WINDOWWIDTH:
                playerRect.move_ip(PLAYERMOVERATE, 0)
            if moveUp and playerRect.top > 0:
                playerRect.move_ip(0, -1 * PLAYERMOVERATE)
            if moveDown and playerRect.bottom < WINDOWHEIGHT:
                playerRect.move_ip(0, PLAYERMOVERATE)

            # Throw hammer if shooting
            if shooting:
                hammerRect = pygame.Rect(playerRect.centerx, playerRect.top, 10, 20)
                hammers.append(hammerRect)

            # Move the hammers
            for h in hammers[:]:
                h.top -= HAMMER_SPEED
                if h.top < 0:
                    hammers.remove(h)

            # Move the enemies down
            for e in enemies:
                e['rect'].move_ip(0, e['speed'])
            for e in enemies[:]:
                if e['rect'].top > WINDOWHEIGHT:
                    enemies.remove(e)

            # Check for hammer collisions with enemies
            for h in hammers[:]:
                for e in enemies[:]:
                    if h.colliderect(e['rect']):
                        hammers.remove(h)
                        enemies.remove(e)
                        score += 10  # Increase score for hitting an enemy
                        break

            # Draw the game world
            windowSurface.fill(BACKGROUNDCOLOR)
            drawText('Score: %s' % score, font, windowSurface, 10, 0)
            drawText('Top Score: %s' % topScore, font, windowSurface, 10, 40)

            # Draw the player and projectiles
            windowSurface.blit(playerImage, playerRect)
            for h in hammers:
                windowSurface.blit(hammerImage, h)

            # Draw each enemy
            for e in enemies:
                windowSurface.blit(e['surface'], e['rect'])

            pygame.display.update()

            # Check if any enemies have hit the player
            if playerHasHitEnemy(playerRect, enemies):
                if score > topScore:
                    topScore = score
                break

            mainClock.tick(FPS)

        # Game over screen
        drawText('GAME OVER', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
        drawText('Press a key to play again.', font, windowSurface, (WINDOWWIDTH / 3) - 80, (WINDOWHEIGHT / 3) + 50)
        pygame.display.update()
        waitForPlayerToPressKey()

main_game()