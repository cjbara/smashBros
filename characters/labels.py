import sys
import os
import pygame
from pygame.locals import *
from pygame import font

class Label(pygame.sprite.Sprite):
    def __init__(self, game=None):
        #initialize sprite object
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pygame.image.load("media/red.png")

        # Initialize font for labels
        pygame.font.init()
    
    def display(self, text, fontSize):
        myfont = pygame.font.SysFont("monospace", int(fontSize))
        label = myfont.render(str(text), 1, (255, 255, 255))
        self.image = label
