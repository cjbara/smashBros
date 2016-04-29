import sys
import os
import pygame
from pygame.locals import *
from pygame import font
from labels import *

class Projectile(pygame.sprite.Sprite):
    def __init__(self, startPos, game=None):
        #initialize sprite object
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        
        print 'init of projectile'

        #create the images
        self.green = pygame.image.load("media/green.png")
        self.image = self.green
        self.rect = self.image.get_rect()

        # Reset variables
        self.startPos = startPos
        self.startVel = (0, 0)

        (self.xpos, self.ypos) = self.startPos
        (self.xvel, self.yvel) = self.startVel

    def getRect(self):
        print 'returning self.rect =', self.rect
        return self.rect

    def moveRight(self):
        print 'moving right'
        self.xpos += 10

    def tick(self):
        self.moveRight()
        self.rect.center = (self.xpos, self.ypos)
