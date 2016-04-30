import sys
import os
import pygame
from pygame.locals import *
from pygame import font
from labels import *

class Projectile(pygame.sprite.Sprite):
    def __init__(self, startPos, isFacingLeft, game=None):
        # initialize sprite object
        pygame.sprite.Sprite.__init__(self)
        self.game = game
       
        # remember direction
        self.isFacingLeft = isFacingLeft

        # create the images
        fireball = pygame.image.load("media/fireball.png")
        self.image = pygame.transform.scale(fireball, (60, 60))
        self.rect = pygame.Rect(0, 0, 60, 60)

        # Reset variables
        self.startPos = startPos
        self.startVel = (0, 0)

        (self.xpos, self.ypos) = self.startPos
        (self.xvel, self.yvel) = self.startVel

    def getRect(self):
        return self.rect

    def moveRight(self):
        self.xpos += 40
    
    def moveLeft(self):
        self.xpos -= 40

    def tick(self):
        if self.isFacingLeft:
            self.moveLeft()
        else:
            self.moveRight()
        self.rect.center = (self.xpos, self.ypos)
