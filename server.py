#coding:utf-8
from ts.internet import protocol,factory
from ts.internet.reactor import reactor


class EchoProtocol(protocol.Protocol):
    def dataReceived(self, data):
        # As soon as any data is received, write it back
        self.transport.write(data)

class EchoFactory(factory.Factory):
    name = 'echo'
    def buildProtocol(self, addr):
        return EchoProtocol()

#reactor global variable
# reactor.listenTCP(9000, EchoFactory())
# reactor.run()