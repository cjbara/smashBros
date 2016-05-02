# Paradigms Twisted Primer
# Cory Jbara
# player 1

import json
from main import *
import sys
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
		self.port_1 = 40062
		self.data_port_1 = 41062
		self.incoming_data_queue = DeferredQueue()
		self.outgoing_data_queue = DeferredQueue()
		self.game = Game(self)

	def connect(self):
		reactor.connectTCP(self.server, self.port_1, CommandConnFactory(self, 1))
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
		print 'Received data, making data connection', data
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
		self.player.outgoing_data_queue.get().addCallback(self.sendToServer)
		self.player.incoming_data_queue.get().addCallback(self.player.game.doAfterServerResponse)
		self.player.game.main()

	def connectionLost(self, reason):
		print 'Data connection lost to HOME'

	def dataReceived(self, data):
		"""Data received from server, put it on queue"""
		self.player.incoming_data_queue.put(data)

	def sendToServer(self, data):
		self.transport.write(json.dumps(data))
		self.player.outgoing_data_queue.get().addCallback(self.sendToServer)

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
