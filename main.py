import pygame
import random
from abc import ABC, abstractmethod
from characters import Pacman, Ghosts, convertGhosts, whiteGhostHit, resetGhosts
from dots import SmallDot, BigDot, checkDotPoint

pygame.init()

SCREENWIDTH = 600
SCREENHEIGHT = 700
win = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
clock = pygame.time.Clock()

#title
titleImage = pygame.image.load('images/title.png')

#game over
gameOverImage = pygame.image.load('images/gameOver.png')

#maps
bg = pygame.image.load('images/map.png')
dotimage = pygame.image.load('images/pacmandotmap.png')

#dot images
smallDotImage = [pygame.image.load('images/dot.png')]
bigDotImage = [pygame.image.load('images/bigdot.png')]

#pacman animation images
moveRight = [pygame.image.load('images/pacman_openR.png'), pygame.image.load('images/pacman_closeR.png')]
moveLeft = [pygame.image.load('images/pacman_openL.png'), pygame.image.load('images/pacman_closeL.png')]
moveUp = [pygame.image.load('images/pacman_openU.png'), pygame.image.load('images/pacman_closeU.png')]
moveDown = [pygame.image.load('images/pacman_openD.png'), pygame.image.load('images/pacman_closeD.png')]

#ghost animation images
blueGhostImage = [pygame.image.load('images/blueGhostL.png'), pygame.image.load('images/blueGhostR.png')]
redGhostImage = [pygame.image.load('images/redGhostL.png'), pygame.image.load('images/redGhostR.png')]
purpleGhostImage = [pygame.image.load('images/purpleGhostL.png'), pygame.image.load('images/purpleGhostR.png')]
checkerGhostImage = [pygame.image.load('images/checkerGhostL.png'), pygame.image.load('images/checkerGhostR.png')]
whiteGhostImage = [pygame.image.load('images/whiteGhostL.png'), pygame.image.load('images/whiteGhostR.png')]

def redrawGameWindow(ghosts):
    global moveCount
    global dotsLeft
    global gameover
    global dt
    global timeEaten
    win.fill((0,0,0))
    win.blit(bg, (0,0))
    win.blit(titleImage, (150, 610))
    
    #pacman
    pacman.draw(win)
    
    #small dots
    dotsLeft = 0
    for i in range(len(pacDots)):
        if pacDots[i].status == 0:
            pacDots[i].draw(win, smallDotImage)
            dotsLeft += 1
        if checkCollision(pacDots[i]):
            pacDots[i].status = 1
            
    for i in range(len(bigPacDots)):
        if bigPacDots[i].status == 0:
            bigPacDots[i].draw(win, bigDotImage)
        if checkCollision(bigPacDots[i]) and bigPacDots[i].status == 0:
            timeEaten = pygame.time.get_ticks() / 1000.0
            bigPacDots[i].status = 1
            convertGhosts(ghosts)            

    for ghost in ghosts:
        ghost.draw(win)

    for i in range(pacman.lives-1):
        win.blit(moveRight[0], (10 + 40*i, 650))

    if gameover:
        win.blit(gameOverImage, (225, 287))
        pygame.display.update()
        pygame.time.wait(4000)
    
    pygame.display.update()

def checkCollision(obj): 
    #pacman left object right
    midEdge = 16

    if pacman.y + midEdge < obj.hitbox[1] + obj.hitbox[3] and pacman.y + midEdge > obj.hitbox[1]:
        if pacman.x + pacman.width < obj.hitbox[0] + obj.hitbox[2] and pacman.x + pacman.width > obj.hitbox[0]:
            return True
    #pacman right object left
    elif pacman.y + midEdge < obj.hitbox[1] + obj.hitbox[3] and pacman.y + midEdge > obj.hitbox[1]:
        if pacman.x > obj.hitbox[0] and pacman.x < obj.hitbox[0] + obj.hitbox[2]:
            return True
    #pacman up object down
    elif pacman.y + pacman.height < obj.hitbox[1] + obj.hitbox[3] and pacman.y + pacman.height > obj.hitbox[1]:
        if pacman.x + midEdge < obj.hitbox[0] + obj.hitbox[2] and pacman.x + midEdge > obj.hitbox[0]:
            return True
    #pacman down object up
    elif pacman.y + 10 > obj.hitbox[1] and pacman.y + 10 < obj.hitbox[1] + obj.hitbox[3]:
        if pacman.x + midEdge < obj.hitbox[0] + obj.hitbox[2] and pacman.x + midEdge > obj.hitbox[0]:
            return True

    return False

blueGhost = Ghosts(290, 280, 22, 22, 0)
redGhost = Ghosts(200, 200, 22, 22, 1)
purpleGhost = Ghosts(250, 280, 22, 22, 2)
checkerGhost = Ghosts(270, 280, 22, 22, 3)
ghosts = [blueGhost, redGhost, purpleGhost, checkerGhost]      

dotsLeft = 0
dt = 0
timeEaten = 0
pacDots = []
bigPacDots = []
index = x = bigIndex = 0
while x < 30:
    y = 0
    while y < 29:
        if checkDotPoint(10+x*20, 10+y*20):
            if (x == 1 and y == 1) or (x == 1 and y == 27) or (x == 28 and y == 1) or (x == 28 and y == 27):
                powerDot = BigDot(x*20, y*20)
                bigPacDots.append(powerDot)
                bigPacDots[bigIndex].status = 0
                bigIndex += 1
            else:
                dot = SmallDot(10+x*20, 9+y*20)
                pacDots.append(dot)
                pacDots[index].status = 0
                index += 1
        y += 1
    x += 1
    
pacman = Pacman(285,475,22,22,'',4)
gameover = False
doneWait = False

#mainloop
run = True
while run:
    clock.tick(32)
    dt = pygame.time.get_ticks() / 1000.0
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    pacman.velocity = 4.5

    for i in range(len(ghosts)):
        ghosts[i].move(pacman)

    for i in range(len(ghosts)):
        if checkCollision(ghosts[i]):
            if ghosts[i].ghostType == 4:
                whiteGhostHit(ghosts[i], i)
            elif ghosts[i].ghostType < 4:
                pacman.restartPacman()
                resetGhosts(ghosts)
                ghosts[i].x = 260
                ghosts[i].y = 280
                pygame.time.wait(1000)
                if pacman.lives == 0:
                    gameover = True
                    
    if dt - timeEaten > 10 and dt - timeEaten < 11:
        resetGhosts(ghosts)

    if keys[pygame.K_LEFT]:
        pacman.direction = 'left'
        pacman.verifyMove()
        pacman.x -= pacman.velocity
        pacman.left = True
        pacman.right = False
        pacman.up = False
        pacman.down = False
        pacman.stationary = False
        
    elif keys[pygame.K_RIGHT]:
        pacman.direction = 'right'
        pacman.verifyMove()
        pacman.x += pacman.velocity
        pacman.left = False
        pacman.right = True
        pacman.up = False
        pacman.down = False
        pacman.stationary = False

    elif keys[pygame.K_UP]:
        pacman.direction = 'up'
        pacman.verifyMove()
        pacman.y -= pacman.velocity
        pacman.left = False
        pacman.right = False
        pacman.up = True
        pacman.down = False
        pacman.stationary = False


    elif keys[pygame.K_DOWN]:
        pacman.direction = 'down'
        pacman.verifyMove()
        pacman.y += pacman.velocity
        pacman.left = False
        pacman.right = False
        pacman.up = False
        pacman.down = True
        pacman.stationary = False

    else:
        pacman.stationary = True
        pacman.moveCount = 0

    redrawGameWindow(ghosts)

    if dotsLeft == 0:
        print('YOU WON')
        run = False

    if gameover:
        run = False

pygame.quit()

    
    
