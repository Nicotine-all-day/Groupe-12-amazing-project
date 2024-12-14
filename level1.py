import pygame, random, sys
from pygame.locals import *
import time

WINDOWWIDTH = 600
WINDOWHEIGHT = 600
TEXTCOLOR = (0, 0, 0)
BACKGROUNDCOLOR = (255, 255, 255)
PLATFORMCOLOR = (51, 103, 78)  # ForestGreen to match the new background
FPS = 60
BADDIEMINSIZE = 10
BADDIEMAXSIZE = 40
BADDIEMINSPEED = 1
BADDIEMAXSPEED = 8
ADDNEWBADDIERATE = 6
PLAYERMOVERATE = 5
JUMP_HEIGHT = 100
GRAVITY = 6
PLATFORMHEIGHT = 20
OPPONENTSPEED = 3
OPPONENTTHROWRATE = 25
HAMMER_SPEED = -10
HAMMER_COOLDOWN = 0.3
LUIGI_LIFE = 10
TURTLE_LIFE = 3

def terminate():
    pygame.quit()
    sys.exit()

def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # Pressing ESC quits.
                    terminate()
                return

def playerHasHitBaddie(playerRect, baddies):
    for b in baddies:
        if playerRect.colliderect(b['rect']):
            baddies.remove(b)
            return True
    return False

def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def hammerHitsOpponent(hammerRect, opponentRect):
    return hammerRect.colliderect(opponentRect)

# Set up pygame, the window, and the mouse cursor.
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Dodger')
pygame.mouse.set_visible(False)

# Set up the fonts.
font = pygame.font.SysFont(None, 48)

# Set up sounds.
gameOverSound = pygame.mixer.Sound('gameover.wav')
winMusic = pygame.mixer.Sound('Winning level transition music.mp3')
pygame.mixer.music.load('Luigi Music.mp3')

# Set up images.
backgroundImage = pygame.image.load('Background Luigi Game.jpeg')
backgroundImage = pygame.transform.scale(backgroundImage, (WINDOWWIDTH, WINDOWHEIGHT))
playerImageLeft = pygame.image.load('Turtle Left.gif')
playerImageLeft = pygame.transform.scale(playerImageLeft, (50, 50))
playerImageRight = pygame.image.load('Turtle Right.gif')
playerImageRight = pygame.transform.scale(playerImageRight, (50, 50))
playerImage = playerImageRight
playerRect = playerImage.get_rect()
baddieImage = pygame.image.load('Fireball .gif')
baddieImage = pygame.transform.scale(baddieImage, (30, 30))
opponentImageLeft = pygame.image.load('Luigi Left.gif')
opponentImageLeft = pygame.transform.scale(opponentImageLeft, (100, 100))
opponentImageRight = pygame.image.load('Luigi Right.gif')
opponentImageRight = pygame.transform.scale(opponentImageRight, (100, 100))
opponentImageHurt = pygame.image.load('Luigi Hurt.gif')
opponentImageHurt = pygame.transform.scale(opponentImageHurt, (100, 100))
opponentImage = opponentImageRight
opponentRect = opponentImage.get_rect()
opponentRect.midtop = (WINDOWWIDTH // 2, 100)
opponentDirection = 1 # 1 for moving right, -1 for moving left
hammerImage = pygame.image.load('Hammer in the AIR.gif')
hammerImage = pygame.transform.scale(hammerImage, (30, 30))
hammers = []
hammerRotations = []
lastHammerTime = 0
opponentHurtCooldown = 0

# Jumping variables
isJumping = False
jumpStartY = 0
onGround = True

# Show the "Start" screen.
windowSurface.blit(backgroundImage, (0, 0))
drawText('Dodger', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
drawText('Press a key to start.', font, windowSurface, (WINDOWWIDTH / 3) - 30, (WINDOWHEIGHT / 3) + 50)
pygame.display.update()
waitForPlayerToPressKey()

def resetGame():
    global luigiLife, turtleLife, baddies, hammers, hammerRotations, score, opponentRect, playerRect, opponentImage, playerImage, opponentHurtCooldown, isJumping, onGround
    luigiLife = LUIGI_LIFE
    turtleLife = TURTLE_LIFE
    baddies = []
    hammers = []
    hammerRotations = []
    score = 0
    playerRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - PLATFORMHEIGHT - playerRect.height)
    opponentRect.midtop = (WINDOWWIDTH // 2, 100)
    opponentImage = opponentImageRight
    playerImage = playerImageRight
    opponentHurtCooldown = 0
    isJumping = False
    onGround = True

resetGame()

def gameOver():
    pygame.mixer.music.stop()
    gameOverSound.play()
    drawText('GAME OVER', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
    drawText('Press a key to play again.', font, windowSurface, (WINDOWWIDTH / 3) - 80, (WINDOWHEIGHT / 3) + 50)
    pygame.display.update()
    pygame.time.wait(2000)  # Ensure sound finishes playing
    gameOverSound.stop()
    waitForPlayerToPressKey()
    resetGame()
    pygame.mixer.music.play(-1, 0.0)

while True:
    moveLeft = moveRight = False
    reverseCheat = slowCheat = False
    baddieAddCounter = 0
    opponentThrowCounter = 0
    pygame.mixer.music.play(-1, 0.0)

    while True: # The game loop runs while the game part is playing.
        current_time = time.time()

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                if event.key == K_z:
                    reverseCheat = True
                if event.key == K_x:
                    slowCheat = True
                if event.key == K_LEFT or event.key == K_a:
                    moveRight = False
                    moveLeft = True
                    playerImage = playerImageLeft
                if event.key == K_RIGHT or event.key == K_d:
                    moveLeft = False
                    moveRight = True
                    playerImage = playerImageRight
                if event.key == K_SPACE and onGround:  # Initiate jump
                    isJumping = True
                    jumpStartY = playerRect.y
                    onGround = False
                if event.key == K_w and current_time - lastHammerTime >= HAMMER_COOLDOWN: # Throw hammer with cooldown
                    hammerRect = pygame.Rect(playerRect.centerx - 15, playerRect.top - 30, 30, 30)
                    hammers.append(hammerRect)
                    hammerRotations.append(0)  # Add initial rotation angle
                    lastHammerTime = current_time

            if event.type == KEYUP:
                if event.key == K_z:
                    reverseCheat = False
                if event.key == K_x:
                    slowCheat = False
                if event.key == K_ESCAPE:
                    terminate()

                if event.key == K_LEFT or event.key == K_a:
                    moveLeft = False
                if event.key == K_RIGHT or event.key == K_d:
                    moveRight = False

        # Handle jumping
        if isJumping:
            if playerRect.y > jumpStartY - JUMP_HEIGHT:
                playerRect.y -= GRAVITY
            else:
                isJumping = False
        else:
            if playerRect.y < WINDOWHEIGHT - PLATFORMHEIGHT - playerRect.height:
                playerRect.y += GRAVITY
            else:
                onGround = True

        # Add new baddies at the top of the screen, if needed.
        opponentThrowCounter += 1
        if opponentThrowCounter >= OPPONENTTHROWRATE:
            opponentThrowCounter = 0
            baddieSize = random.randint(BADDIEMINSIZE, BADDIEMAXSIZE)
            newBaddie = {'rect': pygame.Rect(opponentRect.centerx - baddieSize // 2, opponentRect.bottom, baddieSize, baddieSize),
                        'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                        'surface':pygame.transform.scale(baddieImage, (baddieSize, baddieSize)),
                        }
            baddies.append(newBaddie)

        # Move the opponent left and right.
        if opponentHurtCooldown > 0:
            opponentHurtCooldown -= 1
        else:
            opponentRect.x += opponentDirection * OPPONENTSPEED
            if opponentDirection == 1:
                opponentImage = opponentImageRight
            else:
                opponentImage = opponentImageLeft

            if opponentRect.right >= WINDOWWIDTH or opponentRect.left <= 0:
                opponentDirection *= -1

        # Move the hammers.
        for i in range(len(hammers) - 1, -1, -1):
            hammers[i].y += HAMMER_SPEED
            hammerRotations[i] += 15  # Increment rotation angle
            if hammerRotations[i] >= 360:
                hammerRotations[i] -= 360
            if hammers[i].bottom < 0:
                del hammers[i]
                del hammerRotations[i]
            elif hammerHitsOpponent(hammers[i], opponentRect):
                del hammers[i]
                del hammerRotations[i]
                luigiLife -= 1
                opponentImage = opponentImageHurt
                opponentHurtCooldown = FPS // 2  # Hurt state lasts 0.5 seconds

        # Check if player is hit by baddie.
        for b in baddies[:]:
            if playerRect.colliderect(b['rect']):
                baddies.remove(b)
                turtleLife -= 1

        # End game if Luigi's life reaches 0.
        if luigiLife <= 0:
            pygame.mixer.music.stop()
            winMusic.play()
            drawText('You Win!', font, windowSurface, WINDOWWIDTH / 3, WINDOWHEIGHT / 3)
            pygame.display.update()
            pygame.time.wait(5000)  # Allow the win music to play completely
            winMusic.stop()
            gameOver()
            break

        # End game if Turtle's life reaches 0.
        if turtleLife <= 0:
            drawText('GAME OVER', font, windowSurface, WINDOWWIDTH / 3, WINDOWHEIGHT / 3)
            pygame.display.update()
            pygame.time.wait(2000)
            gameOver()
            break

        # Move the player around.
        if moveLeft and playerRect.left > 0:
            playerRect.move_ip(-1 * PLAYERMOVERATE, 0)
        if moveRight and playerRect.right < WINDOWWIDTH:
            playerRect.move_ip(PLAYERMOVERATE, 0)

        # Move the baddies down.
        for b in baddies:
            if not reverseCheat and not slowCheat:
                b['rect'].move_ip(0, b['speed'])
            elif reverseCheat:
                b['rect'].move_ip(0, -5)
            elif slowCheat:
                b['rect'].move_ip(0, 1)

        # Delete baddies that have fallen past the bottom.
        for b in baddies[:]:
            if b['rect'].top > WINDOWHEIGHT:
                baddies.remove(b)

        # Draw the game world on the window.
        windowSurface.blit(backgroundImage, (0, 0))

        # Draw the platform for the opponent.
        pygame.draw.rect(windowSurface, PLATFORMCOLOR, (0, 190, WINDOWWIDTH, 10))

        # Draw the platform for the player.
        pygame.draw.rect(windowSurface, PLATFORMCOLOR, (0, WINDOWHEIGHT - PLATFORMHEIGHT, WINDOWWIDTH, PLATFORMHEIGHT))

        # Draw Luigi's life bar.
        pygame.draw.rect(windowSurface, (255, 0, 0), (opponentRect.x, opponentRect.top - 20, 100, 10))
        pygame.draw.rect(windowSurface, (0, 255, 0), (opponentRect.x, opponentRect.top - 20, luigiLife * 10, 10))

        # Draw Turtle's life bar.
        pygame.draw.rect(windowSurface, (255, 0, 0), (10, WINDOWHEIGHT - PLATFORMHEIGHT - 30, 100, 10))
        pygame.draw.rect(windowSurface, (0, 255, 0), (10, WINDOWHEIGHT - PLATFORMHEIGHT - 30, turtleLife * 33, 10))

        # Draw the player's rectangle.
        windowSurface.blit(playerImage, playerRect)

        # Draw the opponent.
        windowSurface.blit(opponentImage, opponentRect)

        # Draw each baddie.
        for b in baddies:
            windowSurface.blit(b['surface'], b['rect'])

        # Draw each hammer with rotation.
        for i, hammer in enumerate(hammers):
            rotatedHammer = pygame.transform.rotate(hammerImage, hammerRotations[i])
            windowSurface.blit(rotatedHammer, hammer.topleft)

        pygame.display.update()

        mainClock.tick(FPS)

