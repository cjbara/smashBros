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
		self.conn_queue = DeferredQueue()
		self.data_queue = DeferredQueue()
		self.playersConnected = 0

		#Create an array that will contain dictionaries
		self.data_array = {'p1': [], 'p2': []}
		self.data_received = {'p1': False, 'p2': False}

	def listen(self):
		reactor.listenTCP(self.port_1, CommandConnFactory(self, 1))
		reactor.listenTCP(self.port_2, CommandConnFactory(self, 2))
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
		self.server.conn_queue.get().addCallback(self.tellPlayerAboutConn)
		if self.server.playersConnected == 2:
			print 'Two connections made, sending data connections'
			# Create the two data connections
			reactor.listenTCP(self.server.data_port_1, DataConnFactory(self.server, 1))
			reactor.listenTCP(self.server.data_port_2, DataConnFactory(self.server, 2))
			self.transport.write('Make data connection')
			self.server.conn_queue.put('Make data connection')

	def connectionLost(self, reason):
		print 'Command connection lost from player', self.player

	def tellPlayerAboutConn(self, data):
		self.transport.write(data)

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
		self.player = 'p'+str(player)

	def connectionMade(self):
		print 'Data connection received from player', self.player

	def connectionLost(self, reason):
		print 'Data connection lost from WORK'

	def dataReceived(self, data):
		"""Data received back from player"""
		#print 'Received data from ', self.player, data
		self.server.data_array[self.player] = json.loads(data)
		self.server.data_received[self.player] = True
		if self.server.data_received['p1'] == self.server.data_received['p2'] == True:
			#Received data from both players, send back to the players
			self.sendToPlayer(self.server.data_array)
			self.server.data_queue.put(self.server.data_array)
		else:
			self.server.data_queue.get().addCallback(self.sendToPlayer)

	def sendToPlayer(self, data):
		self.transport.write(json.dumps(data))
		self.server.data_received[self.player] = False

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
