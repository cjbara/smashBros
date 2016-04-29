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

        # Create the physics engine for this character
        self.xpos = 200
        self.ypos = 200
        self.xvel = 0
        self.yvel = 0
        self.onGround = False

    def move(self, button):
        """Function to handle movement from input"""
        pass

    def tick(self):
        #Check if the user is above 500
        platform = 500
        (x, y) = self.rect.center

        #Apply gravity
        gravity = 5
        y += gravity

        if y > platform:
            y = platform
        
        
        

        delta = 10
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] and keys[K_RIGHT]:
            print "Nothing"
        elif keys[K_LEFT]:
            print 'Left'
            x -= delta
        elif keys[K_RIGHT]:
            print 'Right'
            x += delta
        if keys[K_SPACE]:
            y -= delta

        self.rect.center = (x, y)
            
