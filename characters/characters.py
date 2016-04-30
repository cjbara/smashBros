import sys
import os
import pygame
from pygame.locals import *
from pygame import font
from labels import *
from projectile import *

class Character(pygame.sprite.Sprite):
    def __init__(self, game=None):
        # make labels
        self.livesLabel = Label() 
        self.damageLabel = Label() 
        self.playerNameLabel = Label() 

        # make array of projectiles
        self.projectiles = []

        # set player name
        self.playerName = 'Player 1'

        #initialize sprite object
        pygame.sprite.Sprite.__init__(self)
        self.game = game

        #create the images
        self.red = pygame.image.load("media/red.png")
        self.blue = pygame.image.load("media/blue.png")
        self.green = pygame.image.load("media/green.png")

        self.image = pygame.image.load("media/mario.png")
        self.rect = self.image.get_rect()

        # Reset variables
        self.startPos = (self.game.width/2, self.game.height/3)
        self.startVel = (0, 0)
        self.startDamage = 0
        self.resetCharacter()

        # General Variables
        self.lives = 3
        self.damage = self.startDamage

        # Character specific variables
        # These will change depening on the character
        self.maxJumps = 2
        self.jumpVelocity = 40

        # Create the physics engine for this character
        self.offLeft = False
        self.offRight = False

        (self.xpos, self.ypos) = self.startPos
        (self.xvel, self.yvel) = self.startVel

        self.jumpsRemaining = self.maxJumps
        self.isOnGround = False

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
            print 'Jumping'
            self.yvel = -1 * self.jumpVelocity
            self.ypos += self.yvel
            self.jumpsRemaining -= 1

    def Aattack(self):
        print 'A attack'

    def Battack(self):
        print 'B attack'
        newProjectile = Projectile(self.rect.center)
        self.projectiles.append(newProjectile)

    def mapCollision(self):
        c = self.rect
        m = self.game.platform.rect

        topCollision = leftCollision = rightCollision = False
        above = below = left = right = False

        if c.top > m.bottom: below = True
        if c.bottom < m.top:
            above = True
            self.offRight = self.offLeft = False
        if c.left > m.right: right = True
        if c.right < m.left: left = True
        if above or below or left or right:
            if left:
                self.offLeft = True
            if right:
                self.offRight = True
            return False # There is no collision
        
        if c.bottom >= m.top and c.top < m.top and self.offRight == False and self.offLeft == False:
            self.jumpsRemaining = self.maxJumps
            self.ypos = m.top - c.height/2
            self.yvel = 0
            topCollision = True

        if c.left <= m.right and c.right > m.left and topCollision == False:
            if self.offRight:
                self.xpos +=10
            rightCollision = True

        if c.right >= m.left and c.left < m.right and topCollision == False:
            if self.offLeft:
                self.xpos -= 10
            leftCollision = True

    def gravity(self):
        #Apply gravity
        gravity = 5
        if not self.mapCollision():
            self.yvel += gravity
            self.ypos += self.yvel
        
    def checkDeath(self):
        """Chacks if a user is dead or not"""
        if not self.game.screenRect.contains(self.rect):
            print 'Death'
            self.lives -= 1
            if self.lives < 1:
                sys.exit()
            self.resetCharacter()

    def resetCharacter(self):
        """Resets the character to the starting spot"""
        (self.xpos, self.ypos) = self.startPos
        (self.xvel, self.yvel) = self.startVel
        self.rect.center = (self.xpos, self.ypos)
        self.damage = self.startDamage
        self.offRight = self.offLeft = False
        
    def moveRight(self, right):
        if right == True:
            self.xpos += 10
        else:
            self.xpos -= 10

    def displayProjectiles(self):
        # loop through projectiles
        for p in self.projectiles:
            p.tick()
            self.game.screen.blit(p.image, p.getRect())
            #pygame.display.flip()


    def tick(self):
        #Get the right/left movement
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] and keys[K_RIGHT]:
            pass
        elif keys[K_LEFT]:
            self.moveRight(False)
        elif keys[K_RIGHT]:
            self.moveRight(True)

        self.gravity()

        #Get the attacks/jumping movement
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                #If this is true, jump
                if event.key == pygame.K_SPACE:
                    self.jump()
                elif event.key == pygame.K_a:
                    self.Aattack()
                elif event.key == pygame.K_s:
                    self.Battack()
                elif event.key == pygame.K_q:
                    sys.exit()
        
        self.rect.center = (self.xpos, self.ypos)
        self.checkDeath()
