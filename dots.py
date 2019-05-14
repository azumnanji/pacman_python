import pygame

#dot map
dotimage = pygame.image.load('images/pacmandotmap.png')

#dot images
smallDotImage = [pygame.image.load('images/dot.png')]
bigDotImage = [pygame.image.load('images/bigdot.png')]

class SmallDot(object):
    def __init__(self, x, y):
        self.status = 0
        self.x = x
        self.y = y 
        self.width = 20
        self.height = 20
        self.hitbox = (self.x, self.y, self.width, self.height)

    def draw(self, win, image):
        win.blit(image[0], (self.x,self.y))

class BigDot(SmallDot):
    def __init__(self, x, y):
        self.width = 30
        self.height = 30
        SmallDot.__init__(self, x, y)

def checkDotPoint(x,y):
    global dotimage
    if (dotimage.get_at((int(x), int(y)))) == pygame.Color('black'):
        return True
    return False