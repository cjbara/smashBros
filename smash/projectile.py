import sys
import os
import pygame
from pygame.locals import *
from pygame import font
from labels import *

class Projectile(pygame.sprite.Sprite):
	def __init__(self, startPos, isFacingLeft, game=None):
		# initialize sprite object
		pygame.sprite.Sprite.__init__(self)
		self.game = game

		# starts on screen, facing left
		self.onScreen = True
		self.isFacingLeft = isFacingLeft

		# damage level for this projectile
		self.damage = 7 # TODO make this a parameter

		# create the images
		fireball = pygame.image.load("smash/media/fireball.png")
		self.image = pygame.transform.scale(fireball, (60, 60))
		self.rect = pygame.Rect(0, 0, 60, 60)

		# Reset variables
		self.startPos = startPos
		self.startVel = (0, 0)
		self.alreadyHit = False

		(self.xpos, self.ypos) = self.startPos
		(self.xvel, self.yvel) = self.startVel

# ====================== Getters and Setters ====================

	def isOnScreen(self):
		return self.onScreen

	def getRect(self):
		return self.rect

	def getDamage(self):
		return self.damage

	def disappear(self):
		self.image = pygame.image.load("smash/media/empty.png")

	def getDirection(self):
		return self.isFacingLeft
# ====================== Movement functions ===================


	def rotate(self):
		pass

	def moveRight(self):
		self.xpos += 15

	def moveLeft(self):
		self.xpos -= 15

	def checkOnScreen(self):
		if (self.rect.centerx > 1000) or (self.rect.centerx < 0):
			self.onScreen = False
		elif (self.rect.centery > 750) or (self.rect.centery < 0):
			self.onScreen = False
		else:
			self.onScreen = True

	def tick(self):
		# check on screen
		self.checkOnScreen()

		# move in the correct direction
		if self.isFacingLeft:
			self.moveLeft()
		else:
			self.moveRight()
		self.rect.center = (self.xpos, self.ypos)
