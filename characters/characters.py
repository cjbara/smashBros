import sys
import os
import pygame
from pygame.locals import *
from pygame import font
from labels import *

class Character(pygame.sprite.Sprite):
    def __init__(self, game=None):
        # make labels
        self.livesLabel = Label() 
        self.damageLabel = Label() 
        self.playerNameLabel = Label() 

        # set player name
        self.playerName = 'Player 1'

        #initialize sprite object
        pygame.sprite.Sprite.__init__(self)
        self.game = game

        #create the images
        self.red = pygame.image.load("media/red.png")
        self.blue = pygame.image.load("media/blue.png")
        self.green = pygame.image.load("media/green.png")

        self.image = self.blue
        self.rect = self.image.get_rect()

        # Reset variables
        self.startPos = (self.game.width/2, self.game.height/2)
        self.startVel = (0, 0)
        self.startDamage = 0

        # General Variables
        self.lives = 3
        self.damage = self.startDamage

        # Character specific variables
        # These will change depening on the character
        self.maxJumps = 2
        self.jumpVelocity = 40

        # Create the physics engine for this character
        (self.xpos, self.ypos) = self.startPos
        (self.xvel, self.yvel) = self.startVel

        self.onGround = False
        self.jumpsRemaining = self.maxJumps

    def displayPlayerName(self):
        self.playerNameLabel.display(str(self.playerName), 45) 
        newRect = pygame.Rect(self.rect.centerx - self.rect.width*.5, self.rect.centery - (4/5.)*self.rect.height, 200, 100)
        self.game.screen.blit(self.playerNameLabel.image, newRect)
    
    def displayLives(self):
        self.livesLabel.display('Lives: ' + str(self.lives), 55) 
        self.game.screen.blit(self.livesLabel.image, pygame.Rect(75, 60, 100, 100))
    
    def displayDamage(self):
        self.damageLabel.display(str(self.damage) + '%', 55) 
        self.game.screen.blit(self.damageLabel.image, pygame.Rect(75, 120, 100, 100))

    def move(self, button):
        """Function to handle movement from input"""
        pass

    def jump(self):
        if self.jumpsRemaining > 0:
            self.yvel = -1 * self.jumpVelocity
            self.jumpsRemaining -= 1

    def Aattack(self):
        print 'A attack'

    def Battack(self):
        print 'B attack'

    def gravity(self):
        #Check if the user is above 500
        platform = 500 

        #Apply gravity
        gravity = 5
        if self.onGround == False:
            self.yvel += gravity

        if self.ypos > platform:
            self.yvel = 0
            self.ypos = platform
            self.onGround = True
            self.jumpsRemaining = self.maxJumps
        else:
            self.onGround = False
        
    def checkDeath(self):
        """Chacks if a user is dead or not"""
        if not self.game.screenRect.contains(self.rect):
            print 'Death'
            self.lives -= 1
            self.resetCharacter()

    def resetCharacter(self):
        """Resets the character to the starting spot"""
        (self.xpos, self.ypos) = self.startPos
        (self.xvel, self.yvel) = self.startVel
        self.damage = self.startDamage
        

    def tick(self):
        
        delta = 10

        keys = pygame.key.get_pressed()
        if keys[K_LEFT] and keys[K_RIGHT]:
            print "Nothing"
        elif keys[K_LEFT]:
            self.xpos -= delta
        elif keys[K_RIGHT]:
            self.xpos += delta

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                #If this is true, jump
                if event.key == pygame.K_SPACE:
                    self.jump()
                elif event.key == pygame.K_a:
                    self.Aattack()
                elif event.key == pygame.K_s:
                    self.Battack()
                    
        self.ypos += self.yvel
        self.gravity()

        self.rect.center = (self.xpos, self.ypos)
        self.checkDeath()
