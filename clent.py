from twisted.internet import reactor, protocol

print("server line 3 ===============")

class EchoClient(protocol.Protocol):
    def connectionMade(self):
        self.transport.write("hello, world!")

    def dataReceived(self, data):
        print "Server said:", data
        self.transport.loseConnection()

    def connectionLost(self, reason):
        print "connection lost"


class EchoFactory(protocol.ClientFactory):
    def buildProtocol(self, addr):
        return EchoClient()


    def clientConnectionFailed(self, connector, reason):
        print "Connection failed - goodbye!"
        reactor.stop()


    def clientConnectionLost(self, connector, reason):
        print "Connection lost - goodbye!"
        reactor.stop()


reactor.connectTCP("localhost", 8000, EchoFactory())
reactor.run()