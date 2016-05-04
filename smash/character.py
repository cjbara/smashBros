import sys
sys.path.append('/afs/nd.edu/user37/cmc/Public/paradigms/python/local/lib/python2.6/site-packages/pygame-1.9.1release-py2.6-linux-x86_64.egg')
import os
import pygame
from pygame.locals import *
from pygame import font
from labels import *
from projectile import *
from attack import *

class Character(pygame.sprite.Sprite):
	def __init__(self, userNumber, game=None, user=False):
		# make labels
		self.livesLabel = Label() 
		self.damageLabel = Label() 
		self.playerNameLabel = Label() # the one that hovers over the character 
		self.playerLabel = Label() # the static label at top of screen

		# Is this the user?
		self.user = user

		# starts facing left
		self.isFacingLeft = True

		# make array of projectiles
		self.projectiles = []

		# set player name
		self.playerName = userNumber

		#initialize sprite object
		pygame.sprite.Sprite.__init__(self)
		self.game = game

		#create the images
		self.image = pygame.image.load("smash/media/mario.png")
		if self.playerName == 'p1':
			self.imageLeft = pygame.image.load("smash/media/mario.png")
			self.imageRight = pygame.transform.flip(self.imageLeft, True, False)
		else:
			self.imageRight = pygame.image.load("smash/media/link.png")
			self.imageLeft = pygame.transform.flip(self.imageRight, True, False)
		self.rect = self.image.get_rect()

		# Reset variables
		self.startPos = (self.game.width/2, self.game.height/3)
		self.startVel = (0, 0)
		self.startDamage = 0
		self.userWasHit = False
		self.resetCharacter()

		# Data variable to send to server
		self.dataToSend = {}

		# General Variables
		self.lives = 3
		self.friction = 10 # this depends on platform
		self.damage = self.startDamage

		# Character specific variables
		# These will change depening on the character
		self.gravity = 5
		self.maxJumps = 2
		self.jumpVelocity = 40

		# Create a delay for every attack
		# You can only do a particular attack  seconds
		self.Adelay = 0
		self.Bdelay = 0
		self.maxAdelay = 20
		self.maxBdelay = 20

		# Create the physics engine for this character
		self.offLeft = False
		self.offRight = False

		(self.xpos, self.ypos) = self.startPos
		(self.xvel, self.yvel) = self.startVel

		self.jumpsRemaining = self.maxJumps
		self.isOnGround = False

#================== Getters and Setters =================

	def getProjectiles(self):
		return self.projectiles

# ================== Display Functions ==================
	def displayProjectiles(self):
		# loop through this player's projectiles
		updatedProjectiles = [] 
		for p in self.projectiles:
			if p.isOnScreen():
				p.tick()
				self.game.screen.blit(p.image, p.getRect())
				updatedProjectiles.append(p) # dealloc unnecessary projectiles
		self.projectiles = updatedProjectiles

	def displayLabels(self):
		if self.user:
			self.u = 'You'
		else:
			self.u = 'Enemy'
		self.displayPlayerName()
		self.displayLives()
		self.attack = Attack(self)
		self.attack.show()

	def displayPlayerName(self):
		# label hovering over each character
		self.playerNameLabel.display(str(self.playerName), 45) 
		newRect = pygame.Rect(self.rect.centerx - self.rect.width*.5, self.rect.centery - (5/5.)*self.rect.height, 200, 100)
		self.game.screen.blit(self.playerNameLabel.image, newRect)
		
		# static label at top of window
		if self.playerName == 'p1':
			self.playerLabel.display(str(self.playerName), 55) 
			self.game.screen.blit(self.playerLabel.image, pygame.Rect(75, 0, 100, 100))
		else:
			self.playerLabel.display(str(self.playerName), 55) 
			self.game.screen.blit(self.playerLabel.image, pygame.Rect(1000-130, 0, 100, 100))

	def displayLives(self):
		if self.playerName == 'p1':
			self.livesLabel.display('Lives: ' + str(self.lives), 55) 
			self.game.screen.blit(self.livesLabel.image, pygame.Rect(75, 60, 100, 100))
		else:
			self.livesLabel.display('Lives: ' + str(self.lives), 55) 
			self.game.screen.blit(self.livesLabel.image, pygame.Rect(850-175, 60, 100, 100))

	def displayDamage(self):
		if self.playerName == 'p1':
			self.damageLabel.display(str(self.damage) + '%', 55) 
			self.game.screen.blit(self.damageLabel.image, pygame.Rect(75, 120, 100, 100))
		else:
			self.damageLabel.display(str(self.damage) + '%', 55) 
			self.game.screen.blit(self.damageLabel.image, pygame.Rect(1000-130, 120, 100, 100))
		
		#self.livesLabel.display('Lives: ' + str(self.lives), 30) 
		#self.livesLabel.display(self.u+'\nLives: '+str(self.lives)+'\n'+str(self.damage)+'%', 45) 
		#if self.user:
		#	self.game.screen.blit(self.livesLabel.image, pygame.Rect(75, 60, 100, 100))
		#else:
		#	self.game.screen.blit(self.livesLabel.image, pygame.Rect(600, 60, 100, 100))

	#ef displayDamage(self):
		#elf.damageLabel.display(str(self.damage) + '%', 30) 
		#elf.game.screen.blit(self.damageLabel.image, pygame.Rect(75, 120, 100, 100))

	def updateImageDirection(self):
		if self.isFacingLeft:
			self.image = self.imageLeft    
		else:
			self.image = self.imageRight    

# ================= Attack functions ====================
	def jump(self):
		if self.jumpsRemaining > 0:
			#print 'Jumping'
			self.yvel = -1 * self.jumpVelocity
			self.ypos += self.yvel
			self.jumpsRemaining -= 1

	def Aattack(self):
		#print 'A attack'
		if self.Adelay == 0:
			self.attack = Attack(self)
			self.attack.show()

	def Battack(self):
		#print 'B attack'
		if self.Bdelay == 0:
			newProjectile = Projectile(self.rect.center, self.isFacingLeft)
			self.projectiles.append(newProjectile)
			self.Bdelay = self.maxBdelay

# ================= Movement functions ====================
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

	def handleProjectileCollision(self, othersProjectiles):
		""" Loop through other player's projectiles because impossible to get
		hit by your own projectiles"""
		c = self
		for p in othersProjectiles:
			if pygame.sprite.collide_rect(p, c):
				if not p.alreadyHit:
					p.disappear()
					p.alreadyHit = True
					self.userWasHit = True
					self.userWasHitToLeft = p.getDirection()
					self.damage += p.getDamage()
					self.xvel = .5 * self.damage

	def handleHit(self, goLeft):
		self.xvel -= self.friction
		if self.xvel > 0: # xvel is actually xspeed, non-directional
			if goLeft:
				self.xpos -= self.xvel 
			else:
				self.xpos += self.xvel
		else:
			self.userWasHit = False
			self.xvel = 0

	def moveVertical(self):
		""" Apply gravity """
		self.yvel += self.gravity

	def checkDeath(self):
		""" Checks if a user is dead or not """
		if not self.game.screenRect.contains(self.rect):
			if self.lives > 0:
				print 'Death'
				self.lives -= 1
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
		if keys[K_UP] and keys[K_DOWN]:
			pass
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

		# Return the dictionary to send to server
		return self.sendToServer

	def tick(self, data, othersProjectiles):
		# decrement the delays after attacks
		if self.Adelay > 0:
			self.Adelay -= 1
		if self.Bdelay > 0:
			self.Bdelay -= 1

		# Get the right/left movement
		keys = pygame.key.get_pressed()
		if data['l']:
			self.isFacingLeft = True
			self.moveRight(False)
		elif data['r']:
			self.isFacingLeft = False
			self.moveRight(True)
		if data['u']:
			pass
		elif data['d']:
			pass
		self.updateImageDirection() # TODO doesn't really have to be updated every tick
		self.moveVertical()
		self.platformCollision()
		self.handleProjectileCollision(othersProjectiles)
		
		if self.userWasHit:	
			self.handleHit(self.userWasHitToLeft)

		if data['a']:
			self.Aattack()
		if data['b']:
			self.Battack()
		if data['j']:
			self.jump()
		self.rect.center = (self.xpos, self.ypos)
		self.checkDeath()
