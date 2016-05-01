# Cory Jbara
import json
from twisted.internet.protocol import Factory
from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
from twisted.internet.tcp import Port
from twisted.internet import reactor
from twisted.internet.defer import DeferredQueue

#======================================================================
class Server(object):
	def __init__(self):
		self.port_1 = 40062
		self.port_2 = 40063
		self.data_port_1 = 41062
		self.data_port_2 = 41063
		self.queue = DeferredQueue()
		self.p2_queue = DeferredQueue()
		self.playersConnected = 0

	def listen(self):
		self.player1 = CommandConnFactory(self, 1)
		self.player2 = CommandConnFactory(self, 2)
		reactor.listenTCP(self.port_1, self.player1)
		reactor.listenTCP(self.port_2, self.player2)
		reactor.run()

#======================================================================
class CommandConn(Protocol):
	def __init__(self, addr, server, player):
		self.addr = addr
		self.server = server
		self.player = player

	def connectionMade(self):
		print 'Connection made to player', self.player
		# Add callback
		self.server.playersConnected += 1
		if self.server.playersConnected == 2:
			print 'Two connections made, sending data connections'
			# Create the two data connections
			reactor.listenTCP(self.server.data_port_1, DataConnFactory(self.server, 1))
			reactor.listenTCP(self.server.data_port_2, DataConnFactory(self.server, 2))
			self.transport.write(data)
			self.server.player1.transport.write(data)

	def connectionLost(self, reason):
		print 'Command connection lost from player', self.player

#======================================================================
class CommandConnFactory(Factory):
	def __init__(self, server, player):
		self.server = server
		self.player = player

	def buildProtocol(self, addr):
		return CommandConn(addr, self.server, self.player)

#======================================================================
class DataConn(Protocol):
	def __init__(self, addr, server, player):
		self.addr = addr
		self.server = server
		self.player = player

	def connectionMade(self):
		print 'Data connection received from player', self.player
		self.server.data_queue.get().addCallback(self.server.sendToPlayers)

	def connectionLost(self, reason):
		print 'Data connection lost from WORK'

	def dataReceived(self, data):
		"""Data received back from player"""
		print 'Received data from ', self.player
		print data
		#self.server.data_queue.put(data)

	def sendToPlayers(self, data):
		self.transport.write(data)
		self.server.data_queue.get().addCallback(self.sendToPlayers)

#======================================================================
class DataConnFactory(ClientFactory):
	def __init__(self, server, player):
		self.server = server
		self.player = player

	def buildProtocol(self, addr):
		return DataConn(addr, self.server, self.player)

#======================================================================
if __name__ == '__main__':
	server = Server()
	server.listen()
