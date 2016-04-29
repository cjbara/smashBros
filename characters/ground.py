import sys
import os
import pygame
from pygame.locals import *

class Ground(pygame.sprite.Sprite):
    def __init__(self, game=None):
        pygame.sprite.Sprite.__init__(self)
        self.game = game

        self.image = pygame.image.load("media/platform.png")
        self.rect = self.image.get_rect()

    def tick(self):
        pass
