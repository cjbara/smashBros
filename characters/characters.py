import sys
import os
import pygame
from pygame.locals import *

class Character(pygame.sprite.Sprite):
    def __init__(self, game=None):
        #initialize sprite object
        pygame.sprite.Sprite.__init__(self)
        self.game = game

        #create the images
        self.red = pygame.image.load("media/red.png")
        self.blue = pygame.image.load("media/blue.png")
        self.green = pygame.image.load("media/green.png")

        self.image = self.blue
        self.rect = self.image.get_rect()

    def move(self, button):
        """Function to handle movement from input"""
        pass

    def tick(self):
        (x, y) = self.rect.center
        delta = 10
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] and keys[K_RIGHT]:
            print "Nothing"
        elif keys[K_LEFT]:
            self.rect.center = (x - delta, y)
        elif keys[K_RIGHT]:
            self.rect.center = (x + delta, y)

        if keys[K_SPACE]:
            y +=

        self.rect.center = (x, y)
            
