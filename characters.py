import pygame
import random
from abc import ABC, abstractmethod

#movemap image
moveimage = pygame.image.load('images/pacmanmovemap.png')

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

CENTER = 12

#base class
class Character(ABC):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    #interface
    @abstractmethod
    def draw(self, win):
        pass

#child class
class Pacman(Character):

    def __init__(self, x, y, width, height, direction, lives):
        Character.__init__(self, x, y, width, height)
        self.stationary = True
        self.direction = direction
        self.velocity = 4.5
        self.left = False
        self.right = True
        self.up = False
        self.down = False
        self.moveCount = 0
        self.hitbox = (self.x + 16, self.y + 16, 32, 32)
        self.lives = lives

    def draw(self, win):
        if self.moveCount + 1 >= 8:
                self.moveCount = 0
                
        if not self.stationary:
            if self.left:
                win.blit(moveLeft[self.moveCount//4], (self.x,self.y))
                self.moveCount += 1

            elif self.right:
                win.blit(moveRight[self.moveCount//4], (self.x,self.y))
                self.moveCount += 1

            elif self.up:
                win.blit(moveUp[self.moveCount//4], (self.x,self.y))
                self.moveCount += 1

            elif self.down:
                win.blit(moveDown[self.moveCount//4], (self.x,self.y))
                self.moveCount += 1

            self.hitbox = (self.x, self.y, 32, 32)
            #pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

        else:
            if self.left:
                win.blit(moveLeft[0], (self.x,self.y))
            elif self.right:
                win.blit(moveRight[0], (self.x,self.y))
            elif self.up:
                win.blit(moveUp[0], (self.x,self.y))
            elif self.down:
                win.blit(moveDown[0], (self.x,self.y))

            #pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def verifyMove(self):
        global moveimage
        CENTER = 12
        if self.direction == 'right':
            if self.x + self.width + self.velocity > 599:
                self.x = self.x - 599
            if moveimage.get_at((int(self.x + self.width + self.velocity), int(self.y + CENTER))) != pygame.Color('black'):
                self.velocity = 0;

        elif self.direction == 'left':
            if self.x - self.velocity < 0:
                self.x = self.x + 600
            if moveimage.get_at((int(self.x - self.velocity), int(self.y + CENTER))) != pygame.Color('black'):
                self.velocity = 0;

        elif self.direction == 'up':
            if moveimage.get_at((int(self.x + CENTER), int(self.y - self.velocity))) != pygame.Color('black'):
                self.velocity = 0;

        elif self.direction == 'down':
            if moveimage.get_at((int(self.x + CENTER), int(self.y + self.height + self.velocity))) != pygame.Color('black'):
                self.velocity = 0;

    def restartPacman(self):
        self.lives -= 1
        self.x = 285
        self.y = 475

#child class
class Ghosts(Character):
    
    def __init__(self, x, y, width, height, ghostType):
        Character.__init__(self, x, y, width, height)
        self.previousDirection = 0
        self.animationDirection = 0
        self.validDirections = [0,0,0,0]
        self.velocity = 5
        self.ghostType = ghostType
        self.hitbox = (self.x + 16, self.y + 16, 32, 32)
        self.followDirections = [0,0,0,0]

    def ghostDirection(self):
        right = False
        left = False

        global moveimage
        self.validDirections = [0,0,0,0]
        if self.x - self.velocity < 0:
            self.x = self.x + 600
            left = True
        if self.x + self.width + self.velocity > 599:
            self.x = self.x - 599
            right = True
            
        #check for right direction
        if left == False:
            if moveimage.get_at((int(self.x + self.width + self.velocity), int(self.y + CENTER))) == pygame.Color('black'):
                self.validDirections[0] = 1
        #check for left direction
        if right == False:
            if moveimage.get_at((int(self.x - self.velocity), int(self.y + CENTER))) == pygame.Color('black'):
                self.validDirections[1] = 1
        #check for up direction
        if right == False and left == False:
            if moveimage.get_at((int(self.x + CENTER), int(self.y - self.velocity))) == pygame.Color('black'):
                self.validDirections[2] = 1
        #check for down direction
        if right == False and left == False:
            if moveimage.get_at((int(self.x + CENTER), int(self.y + self.height + self.velocity))) == pygame.Color('black'):
                self.validDirections[3] = 1
        if left == True:
            self.validDirections[1] = 1
        if right == True:
            self.validDirections[0] = 1

    def draw(self, win):
        # down/left = animationDirection of 0
        # up/right = animationDirection of 1
        if self.previousDirection == 0 or self.previousDirection == 2:
            self.animationDirection = 1
        else:
            self.animationDirection = 0

        if self.ghostType == 0:
            win.blit(blueGhostImage[self.animationDirection], (self.x,self.y))
        elif self.ghostType == 1:
            win.blit(redGhostImage[self.animationDirection], (self.x,self.y))
        elif self.ghostType == 2:
            win.blit(purpleGhostImage[self.animationDirection], (self.x,self.y))
        elif self.ghostType == 3:
            win.blit(checkerGhostImage[self.animationDirection], (self.x,self.y))
        elif self.ghostType == 4:
            win.blit(whiteGhostImage[self.animationDirection], (self.x,self.y))

        self.hitbox = (self.x, self.y, 32, 32)
        #pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)
                
    def move(self, pacman):
        self.ghostDirection()
        self.backTrack()
        count = 0
        if self.ghostType < 4:
            self.followPacman(pacman)
            for i in range(len(self.followDirections)):
                if (self.followDirections[i] == self.validDirections[i]):
                    count += 1
            if count > 1:
                for i in range(len(self.followDirections)):
                    if (self.followDirections[i] != self.validDirections[i]):
                        self.validDirections[i] = 0
        
        randProb = random.randint(0,1000)
        if self.validDirections[self.previousDirection] and randProb < 950:
            randInd = self.previousDirection

        else:
            randInd = random.randint(0,3)
            while not self.validDirections[randInd]:
                randInd = random.randint(0,3)

        #right
        if randInd == 0:
            self.x += self.velocity
        #left
        elif randInd == 1:
            self.x -= self.velocity
        #up
        elif randInd == 2:
            self.y -= self.velocity
        #down
        elif randInd == 3:
            self.y += self.velocity

        self.previousDirection = randInd

    def backTrack(self):
        if self.previousDirection == 0:
            self.validDirections[1] = 0
        elif self.previousDirection == 1:
            self.validDirections[0] = 0
        elif self.previousDirection == 2:
            self.validDirections[3] = 0
        elif self.previousDirection == 3:
            self.validDirections[2] = 0

    def followPacman(self, pacman):
        self.followDirections = [0,0,0,0]
        
        if pacman.x > self.x and pacman.y > self.y:
            self.followDirections = [1,0,0,1]
        elif pacman.x >self.x and pacman.y < self.y:
            self.followDirections = [1,0,1,0]
        elif pacman.x <self.x and pacman.y > self.y:
            self.followDirections = [0,1,0,1]
        else:
            self.followDirections = [0,1,1,0]

#convert all ghosts to white ghosts
def convertGhosts(ghosts):
    for i in range(len(ghosts)):
        ghosts[i].ghostType = 4
        ghosts[i].velocity = 3

#move white ghost to center and change back to original colour
def whiteGhostHit(ghost, i):
    ghost.ghostType = i
    ghost.velocity = 5
    ghost.x = 260
    ghost.y = 280

#reset all ghosts to original colour (after 10 second timer runs out)
def resetGhosts(ghosts):
    for i in range(len(ghosts)):
        ghosts[i].ghostType = i
        ghosts[i].velocity = 5