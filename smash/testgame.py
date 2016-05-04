import sys
import os
import math
import json
sys.path.append('/afs/nd.edu/user37/cmc/Public/paradigms/python/local/lib/python2.6/site-packages/pygame-1.9.1release-py2.6-linux-x86_64.egg')
import pygame
from pygame.locals import *
from pygame import font
from character import *
from ground import *

class TestGame(object):
	def __init__(self):
		#1 Initialize game space
		self.size = self.width, self.height = (1000,750)
		self.black = (0,0,0)
		self.screen = pygame.display.set_mode(self.size)
		self.clock = pygame.time.Clock()
		self.screenRect = pygame.Rect(-100, -100, self.width + 200, self.height + 200)

		#2 Initialize game objects
		self.user = Character(1, self, True)
		self.other = Character(2, self, False)
		self.platform = Ground(self)

	def main(self):
		#3 Start game loop
		while(1):
			#4 Tick regulation
			self.clock.tick(60)
		
			#5 Handle user input
			dataToSend = self.user.getKeysPressed()
			self.doAfterServerResponse(dataToSend)
			# Send this data to the server
			#self.twisted.outgoing_data_queue.put(dataToSend)
	
	def doAfterServerResponse(self, dataReceived):
			#self.twisted.incoming_data_queue.get().addCallback(self.doAfterServerResponse)
			data = dataReceived

			#6 Tick all objects
			self.user.tick(data, self.other.getProjectiles())
			other = {'a': 0, 'b': 0, 'd': 0, 'j': 0, 'l': 0, 'r': 0, 'u': 0}
			self.other.tick(other, self.user.getProjectiles())
			
			#7 Update screen display
			self.updateScreen()

			#4 Tick regulation
			#self.clock.tick(60)
		
			#5 Handle user input
			#dataToSend = self.user.getKeysPressed()
			# Send this data to the server
			#self.twisted.outgoing_data_queue.put(dataToSend)

	def updateScreen(self):
			self.screen.fill(self.black)
			pygame.draw.rect(self.screen, (0,0, 255), self.platform.rect)
			self.user.displayProjectiles()
			self.other.displayProjectiles()
			self.user.displayLabels()
			self.other.displayLabels()
			self.screen.blit(self.user.image, self.user.rect)
			self.screen.blit(self.other.image, self.other.rect)
			pygame.display.flip()
		

if __name__ == '__main__':
	game = TestGame()
	game.main()
