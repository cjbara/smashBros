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

        # starts facing left
        self.isFacingLeft = True

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
        self.marioImageLeft = pygame.image.load("media/mario.png")
        self.marioImageRight = pygame.transform.flip(self.marioImageLeft, True, False)
        self.rect = self.image.get_rect()

        # Reset variables
        self.startPos = (self.game.width/2, self.game.height/3)
        self.startVel = (0, 0)
        self.startDamage = 0
        self.resetCharacter()

        # Data variable to send to server
        self.dataToSend = {}

        # General Variables
        self.lives = 3
        self.damage = self.startDamage

        # Character specific variables
        # These will change depening on the character
        self.gravity = 5
        self.maxJumps = 2
        self.jumpVelocity = 40

        # Create the physics engine for this character
        self.offLeft = False
        self.offRight = False

        (self.xpos, self.ypos) = self.startPos
        (self.xvel, self.yvel) = self.startVel

        self.jumpsRemaining = self.maxJumps
        self.isOnGround = False

# ================== Display Functions ==================
    def displayProjectiles(self):
        # loop through projectiles
        newProjectiles = [] 
        for p in self.projectiles:
            if p.isOnScreen():
                p.tick()
                self.game.screen.blit(p.image, p.getRect())
                newProjectiles.append(p) # dealloc unnecessary projectiles
        self.projectiles = newProjectiles

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

    def updateImageDirection(self):
        if self.isFacingLeft:
            self.image = self.marioImageLeft    
        else:
            self.image = self.marioImageRight    

# ================= Movement functions ====================
    
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
        newProjectile = Projectile(self.rect.center, self.isFacingLeft)
        self.projectiles.append(newProjectile)

    def platformCollision(self):
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
            if left and not above:
                self.offLeft = True
            if right and not above:
                self.offRight = True
            self.ypos += self.yvel

        self.rect.center = (self.xpos, self.ypos)
        c = self.rect
        
        # Check if the character is on the platform
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

    def moveVertical(self):
        # Apply gravity
        self.yvel += self.gravity
        
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

    def getKeysPressed(self):
        # Reset the sendToServer
        self.sendToServer = {'a': 0, 'b': 0, 'j': 0, 'l': 0, 'r': 0, 'u': 0, 'd': 0}    

        # Get the right/left movement
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] and keys[K_RIGHT]:
            pass
        elif keys[K_LEFT]:
            self.sendToServer['l'] = 1
        elif keys[K_RIGHT]:
            self.sendToServer['r'] = 1
        elif keys[K_UP]:
            self.sendToServer['u'] = 1
        elif keys[K_DOWN]:
            self.sendToServer['d'] = 1

        #Get the attacks/jumping movement
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                #If this is true, jump
                if event.key == pygame.K_SPACE:
                    self.sendToServer['j'] = 1
                elif event.key == pygame.K_a:
                    self.sendToServer['a'] = 1
                elif event.key == pygame.K_s:
                    self.sendToServer['b'] = 1
                elif event.key == pygame.K_q:
                    sys.exit()

        # Return the dictionary to send to server
        return self.sendToServer

    def tick(self, dataReceived):
        # Get the right/left movement
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] and keys[K_RIGHT]:
            pass
        elif keys[K_LEFT]:
            self.isFacingLeft = True
            self.moveRight(False)
        elif keys[K_RIGHT]:
            self.isFacingLeft = False
            self.moveRight(True)

        self.updateImageDirection() # TODO doesn't really have to be updated every tick

        self.moveVertical()
        self.platformCollision()

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
