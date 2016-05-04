import sys
import os
import pygame
from pygame.locals import *

class Ground(pygame.sprite.Sprite):
    def __init__(self, game=None):
        pygame.sprite.Sprite.__init__(self)
        self.game = game

        #self.image = pygame.image.load("smash/media/platform.png")
        self.image = pygame.image.load("smash/media/finalDestPlatform-1.jpg")
        self.image = pygame.transform.scale(self.image, (2*self.game.width/3, self.game.height))
        self.rect = pygame.Rect(self.game.width/6, 550, 2*self.game.width/3, self.game.height)

    def tick(self):
        pass
