#coding:utf-8
class Protocol(object):
    connected = 0
    transport = None

    def makeConnection(self, transport):
        self.connected = 1
        self.transport = transport
        self.connectionMade()

    def connectionMade(self):
        pass

    def dataReceived(self, data):
        pass

    def connectionLost(self, reason):
        pass
