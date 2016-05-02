import sys
import os
import math
sys.path.append('/afs/nd.edu/user37/cmc/Public/paradigms/python/local/lib/python2.6/site-packages/pygame-1.9.1release-py2.6-linux-x86_64.egg')
import pygame
from pygame.locals import *
from pygame import font
from characters import *

class Game(object):
	def __init__(self, twisted):
		#0 Initialize the networking
		self.twisted = twisted

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
		#while(1):
			#4 Tick regulation
			self.clock.tick(1)
		
			#5 Handle user input
			dataToSend = self.character.getKeysPressed()
			# Send this data to the server
			self.twisted.outgoing_data_queue.put(dataToSend)
	
	def doAfterServerResponse(self, dataReceived):
			print 'dr',dataReceived
			#6 Tick all objects
			self.character.tick(dataReceived)
			
			#7 Update screen display
			self.screen.fill(self.black)
			pygame.draw.rect(self.screen, (0,0, 255), self.platform.rect)
			self.character.displayProjectiles()
			self.character.displayLives()
			self.character.displayDamage()
			self.character.displayPlayerName()
			self.screen.blit(self.character.image, self.character.rect)
			pygame.display.flip()
			print 'end function'

if __name__ == '__main__':
	game = Game()
	game.main()
