# Paradigms Twisted Primer
# Cory Jbara
# player 2

import json
from twisted.internet.protocol import Factory
from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
from twisted.internet.tcp import Port
from twisted.internet import reactor
from twisted.internet.defer import DeferredQueue

#======================================================================
class Player(object):
	def __init__(self):
		self.server = 'student00.cse.nd.edu'
		self.port_1 = 40063
		self.data_port_1 = 41063
		self.home_queue = DeferredQueue()
		self.student_queue = DeferredQueue()

	def connect(self):
		reactor.connectTCP(self.server, self.port_1, CommandConnFactory(self, 2))
		reactor.run()

#======================================================================
class CommandConn(Protocol):
	def __init__(self, addr, player, number):
		self.addr = addr
		self.player = player
		self.number = number

	def connectionMade(self):
		print 'Command connection made to SERVER, waiting for other player'

	def connectionLost(self, reason):
		print 'Command connection lost from SERVER'

	def dataReceived(self, data):
		"""Data received from server connection, this means two players have connected, so create a new DataConn"""
		print 'data received from command conn, making data connection now with data:', data
		reactor.connectTCP(self.player.server, self.player.data_port_1, DataConnFactory(self.player, self.number))

#======================================================================
class CommandConnFactory(ClientFactory):
	def __init__(self, player, number):
		self.player = player
		self.playerNumber = number

	def buildProtocol(self, addr):
		return CommandConn(addr, self.player, self.playerNumber)

#======================================================================
class DataConn(Protocol):
	def __init__(self, addr, player, number):
		self.addr = addr
		self.player = player
		self.number = number

	def connectionMade(self):
		print 'Data connection made to SERVER'
		self.sendToServer('sl;kf')

	def connectionLost(self, reason):
		print 'Data connection lost to HOME'

	def dataReceived(self, data):
		"""Data received from home connection, forward to student"""
		print 'data received:', data

	def sendToServer(self, data):
		print 'Sending data to server'
		data = {'a':1, 'b':0, 'j':0, 'l':0, 'r':0, 'u':1, 'd':0}
		self.transport.write(json.dumps(data))
		#self.player.server_queue.get().addCallback(self.sendToServer)

#======================================================================
class DataConnFactory(ClientFactory):
	def __init__(self, player, number):
		self.player = player
		self.number = number

	def buildProtocol(self, addr):
		return DataConn(addr, self.player, self.number)

#======================================================================
if __name__ == '__main__':
	player = Player()
	player.connect()