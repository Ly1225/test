from select import  epoll, EPOLLHUP,EPOLLIN, EPOLLOUT

class Reactor(object):
    def __init__(self):
        print("Reactor init")
        self._poller = epoll(1024)
        self._reads = set()
        self._writes = set()
        self._selectables = {}
        # self._continuousPolling = posixbase._ContinuousPolling(self)
        # posixbase.PosixReactorBase.__init__(self)

    def test(self):
        print("reactor test")

    def _add(self, xer, primary, other, selectables, event, antievent):
        """
        Private method for adding a descriptor from the event loop.

        It takes care of adding it if  new or modifying it if already added
        for another state (read -> read/write for example).
        """
        fd = xer.fileno()
        if fd not in primary:
            flags = event
            # epoll_ctl can raise all kinds of IOErrors, and every one
            # indicates a bug either in the reactor or application-code.
            # Let them all through so someone sees a traceback and fixes
            # something.  We'll do the same thing for every other call to
            # this method in this file.
            if fd in other:
                flags |= antievent
                self._poller.modify(fd, flags)
            else:
                self._poller.register(fd, flags)

            # Update our own tracking state *only* after the epoll call has
            # succeeded.  Otherwise we may get out of sync.
            primary.add(fd)
            selectables[fd] = xer

    def addReader(self, reader):
        """
        Add a FileDescriptor for notification of data available to read.
        """
        try:
            self._add(reader, self._reads, self._writes, self._selectables,
                      EPOLLIN, EPOLLOUT)
        except IOError as e:
            print(e.__dict__)

    def startReading(self):
        """Start waiting for read availability.
        """
        self.addReader(self)

    def listenTCP(self, port, factory, backlog=50, interface=''):
        print("Port startListening")
        if self._preexistingSocket is None:
            # Create a new socket and make it listen
            try:
                skt = socket.socket(self.addressFamily, self.socketType)
                skt.setblocking(0)
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

    def startRunning(self):
        """
        Method called when reactor starts: do some initialization and fire
        startup events.

        Don't call this directly, call reactor.run() instead: it should take
        care of calling this.

        This method is somewhat misnamed.  The reactor will not necessarily be
        in the running state by the time this method returns.  The only
        guarantee is that it will be on its way to the running state.
        """
        if self._started:
            raise error.ReactorAlreadyRunning()
        if self._startedBefore:
            raise error.ReactorNotRestartable()
        self._started = True
        self._stopped = False
        if self._registerAsIOThread:
            threadable.registerAsIOThread()
        self.fireSystemEvent('startup')

    def mainLoop(self):
        while self._started:
            try:
                print("self._started:")
                while self._started:
                    # Advance simulation time in delayed event
                    # processors.
                    self.runUntilCurrent()
                    t2 = self.timeout()
                    t = self.running and t2
                    self.doIteration(t)
            except:
                log.msg("Unexpected error in main loop.")
                log.err()
            else:
                log.msg('Main loop terminated.')

    def run(self, installSignalHandlers=True):
        print("===start run")
        self.startRunning(installSignalHandlers=installSignalHandlers)
        self.mainLoop()

#单例模式
reactor = Reactor()