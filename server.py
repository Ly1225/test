from twisted.internet import protocol, reactor

class Echo(protocol.Protocol):
    def dataReceived(self, data):
        # As soon as any data is received, write it back
        self.transport.write(data)


class EchoFactory(protocol.Factory):
    name = 'echo'
    def buildProtocol(self, addr):
        return Echo()

print("reactor")
print(reactor)
reactor.listenTCP(8000, EchoFactory())
reactor.run()

