# Cory Jbara
# Madelyn Nelson
# Programming Paradigms final project
# Super Smash Bros

import sys
from smash import *

class Play(object):
    def __init__(self):
		if len(sys.argv) <= 1:
			print 'You must enter a player number'
			sys.exit()
		if sys.argv[1] == '1':
			self.player = Player(1, 62)
		elif sys.argv[1] == '2':
			self.player = Player(2, 63)
		else:
			print 'This is not a valid character'
			sys.exit()	
		self.player.connect()

if __name__ == '__main__':
    Play()
