import sys
import os
import math
import json
sys.path.append('/afs/nd.edu/user37/cmc/Public/paradigms/python/local/lib/python2.6/site-packages/pygame-1.9.1release-py2.6-linux-x86_64.egg')
import pygame
from pygame.locals import *
from pygame import font
from pygame import mixer
from character import *
from ground import *

class Game(object):
	def __init__(self, twisted):
		#0 Initialize the networking
		self.twisted = twisted

		#1 Initialize game space
		self.size = self.width, self.height = (1000,750)
		self.background = pygame.image.load("smash/media/finalDestBackground.png")
		self.background = pygame.transform.scale(self.background, (1000, 750))
		self.black = (0,0,0)
		self.screen = pygame.display.set_mode(self.size)
		self.clock = pygame.time.Clock()
		self.screenRect = pygame.Rect(-100, -100, self.width + 200, self.height + 200)

		#2 Initialize game objects
		self.user = Character(self.twisted.playerNumber, self, True)
		self.other = Character(self.twisted.otherNumber, self, False)
		self.platform = Ground(self)

		# Play music
		pygame.mixer.init()
		pygame.mixer.music.load("smash/media/backgroundMusic.wav")
		pygame.mixer.music.play()

	def main(self):
		#3 Start game loop
			#4 Tick regulation
			self.clock.tick(60)
		
			#5 Handle user input
			dataToSend = self.user.getKeysPressed()
			# Send this data to the server
			self.twisted.outgoing_data_queue.put(dataToSend)
	
	def doAfterServerResponse(self, dataReceived):
			self.twisted.incoming_data_queue.get().addCallback(self.doAfterServerResponse)
			data = json.loads(dataReceived)

			#6 Tick all objects
			self.user.tick(data[self.twisted.playerNumber], self.other.getProjectiles())
			self.other.tick(data[self.twisted.otherNumber], self.user.getProjectiles())
			
			#7 Update screen display
			self.updateScreen()

			#4 Tick regulation
			self.clock.tick(60)
		
			#5 Handle user input
			dataToSend = self.user.getKeysPressed()
			# Send this data to the server
			self.twisted.outgoing_data_queue.put(dataToSend)

	def updateScreen(self):
			self.screen.fill(self.black)
			self.screen.blit(self.background, pygame.Rect(0, 0, self.width, self.height))
			self.screen.blit(self.platform.image, self.platform.rect)
			#pygame.draw.rect(self.screen, (0,0, 255), self.platform.rect)
			self.user.displayProjectiles()
			self.other.displayProjectiles()
			self.user.displayLabels()
			self.other.displayLabels()
			#self.user.displayLives()
			#self.other.displayLives()
			#self.user.displayDamage()
			#self.other.displayDamage()
			#self.user.displayPlayerName()
			#self.other.displayPlayerName()
			self.screen.blit(self.user.image, self.user.rect)
			self.screen.blit(self.other.image, self.other.rect)
			pygame.display.flip()
		

if __name__ == '__main__':
	game = Game()
	game.main()
