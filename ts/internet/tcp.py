import socket
class Port(object):
    # An externally initialized socket that we will use, rather than creating
    # our own.
    _preexistingSocket = None

    def __init__(self, port, factory, backlog=50, interface='', reactor=None):
        self.reactor = reactor
        print("Port init")

    def test(self):
        print("Port test")

    def startReading(self):
        """Start waiting for read availability.
        """
        self.reactor.addReader(self)

    def startListening(self):
        print("Port startListening")
        if self._preexistingSocket is None:
            # Create a new socket and make it listen
            try:
                skt = socket.socket(self.addressFamily, self.socketType)
                skt.setblocking(0)
                # fdesc._setCloseOnExec(s.fileno())
                #S.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1) 这里value设置为1，表示将SO_REUSEADDR标记为TRUE，操作系统会在服务器socket被关闭或服务器进程终止后马上释放该服务器的端口，否则操作系统会保留几分钟该端口。
                skt.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                addr = (self.interface, self.port)
                skt.bind(addr)
            except socket.error as le:
                print("CannotListenError")
                exit()
            skt.listen(self.backlog)
        else:
            # Re-use the externally specified socket
            skt = self._preexistingSocket
            self._preexistingSocket = None

        # Make sure that if we listened on port 0, we update that to
        # reflect what the OS actually assigned us.
        self._realPortNumber = skt.getsockname()[1]
        print("%s starting on %s")
        print("%s starting on %s" % (
                self._getLogPrefix(self.factory), self._realPortNumber))
        # log.msg("%s starting on %s" % (
        #         self._getLogPrefix(self.factory), self._realPortNumber))

        # The order of the next 5 lines is kind of bizarre.  If no one
        # can explain it, perhaps we should re-arrange them.
        self.factory.doStart()
        self.connected = True
        self.socket = skt
        self.fileno = self.socket.fileno
        self.numberAccepts = 100

        self.startReading()
