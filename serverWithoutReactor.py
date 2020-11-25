#coding:utf-8
from ts.internet import protocol,factory
import socket,select

class Echo(protocol.Protocol):
    def dataReceived(self, data):
        # As soon as any data is received, write it back
        print("dataReceived:",data)
        self.transport.write(data)

class EchoFactory(factory.Factory):
    name = 'echo'
    def buildProtocol(self, addr):
        return Echo()



reads = set()
writes = set()

# Create a new socket and make it listen
# 创建并绑定套接字，开始监听。
skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
skt.setblocking(0)
skt.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
addr = ('127.0.0.1', 10000)
# print("addr:",addr)
# 绑定
skt.bind(addr)
# 监听
skt.listen(5)

factory=EchoFactory()
factory.doStart()

reads.add(skt)

# self.startRunning()

# self.mainLoop()
while 1:
    # Advance simulation time in delayed event
    # processors.
    # 把self.threadCallQueue   和self.pendingTimedCalls
    # 里的对象执行一遍
    # self.runUntilCurrent()

    # t2 = self.timeout()
    # timeout = self.running and t2
    # self.doSelect(t)
    r, w, ignored = select.select(reads, writes,[])