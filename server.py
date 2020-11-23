#coding:utf-8
from ts.internet import protocol,factory
from ts.internet.reactor import reactor

class Echo(protocol.Protocol):
    def dataReceived(self, data):
        # As soon as any data is received, write it back
        print("dataReceived:",data)
        self.transport.write(data)

class EchoFactory(factory.Factory):
    name = 'echo'
    def buildProtocol(self, addr):
        return Echo()




#reactor global variable
reactor.listenTCP(9000, EchoFactory())
reactor.run()