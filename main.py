import sys
import os
import math
import pygame
from pygame.locals import *
from characters import *

class Game(object):
    def __init__(self):
        #1 Initialize game space
        self.size = self.width, self.height = (1000,750)
        self.black = (0,0,0)
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()
        self.screenRect = pygame.Rect(-100, -100, self.width + 200, self.height + 200)

        #2 Initialize game objects
        self.character = Character(self)
        self.platform = Ground(self)
        
    def main(self):
        #3 Start game loop
        while(1):
            #4 Tick regulation
            self.clock.tick(60)
        
            #5 Handle user input
            #self.character.handleInput()
    
            #6 Tick all objects
            self.character.tick()
            
            #7 Update screen display
            self.screen.fill(self.black)
            self.screen.blit(self.platform.image, pygame.Rect(0,500,self.width, 20))
            self.screen.blit(self.character.image, self.character.rect)
            pygame.display.flip()

if __name__ == '__main__':
    game = Game()
    game.main()
