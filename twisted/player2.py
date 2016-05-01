# Paradigms Twisted Primer
# Cory Jbara

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
		self.port_1 = 40080
		self.data_port_1 = 41080
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
		# Add callback
		self.player.home_queue.get().addCallback(self.sendToHome)
		reactor.connectTCP(self.player.student_server, self.player.student_port, ConnToStudentFactory(self.player, self))

	def connectionLost(self, reason):
		print 'Data connection lost to HOME'

	def dataReceived(self, data):
		"""Data received from home connection, forward to student"""
		self.player.student_queue.put(data)

	def sendToHome(self, data):
		print 'Sending data to HOME'
		self.transport.write(data)
		self.player.home_queue.get().addCallback(self.sendToHome)

#======================================================================
class DataConnFactory(ClientFactory):
	def __init__(self, player, number):
		self.player = player
		self.number = number

	def buildProtocol(self, addr):
		return DataConnToHome(addr, self.player, self.number)

#======================================================================
if __name__ == '__main__':
	player = Player()
	player.connect()
