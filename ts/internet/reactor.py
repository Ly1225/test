#coding:utf-8
import socket,select

class Reactor(object):
    # Actual port number being listened on, only set to a non-None
    # value when we are actually listening.
    _realPortNumber = None

    # An externally initialized socket that we will use, rather than creating
    # our own.
    _preexistingSocket = None

    def __init__(self):
        self._reads = set()
        self._writes = set()
        # posixbase.PosixReactorBase.__init__(self)

    def test(self):
        print("reactor test")

    def doSelect(self, timeout):
        """
        Run one iteration of the I/O monitor loop.

        This will run all selectables who had input or output readiness
        waiting for them.
        """
        # 调用select方法监控读写集合，返回准备好读写的描述符
        r, w, ignored = select.select(self._reads,self._writes,[], timeout)

        _drdw = self._doReadOrWrite
        for selectables, method, fdset in ((r, "doRead", self._reads),
                                           (w,"doWrite", self._writes)):
            for selectable in selectables:
                # if this was disconnected in another thread, kill it.
                # ^^^^ --- what the !@#*?  serious!  -exarkun
                if selectable not in fdset:
                    continue

    def listenTCP(self, port, factory, backlog=50, interface=''):
        # Create a new socket and make it listen
        # 创建并绑定套接字，开始监听。
        skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        skt.setblocking(0)
        skt.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        addr = (interface, port)
        # print("addr:",addr)
        # 绑定
        skt.bind(addr)
        #监听
        skt.listen(backlog)

        factory.doStart()

        self._reads.add(skt)

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
            exit()
        self._started = True
        self._stopped = False

    def runUntilCurrent(self):
        """
        Run all pending timed calls.
        """

    def mainLoop(self):
        #mianLoop就是最终的主循环了，在循环中，调用doIteration方法监控读写描述符的集合，
        # 一旦发现有描述符准备好读写，就会调用相应的事件处理程序。
        while self._started:
            try:
                while self._started:
                    # Advance simulation time in delayed event
                    # processors.
                    self.runUntilCurrent()
                    t2 = self.timeout()
                    t = self.running and t2
                    #关键
                    self.doSelect(t)
            except:
                print("Unexpected error in main loop.")
            else:
                print('Main loop terminated.')

    def run(self):
        self.startRunning()
        self.mainLoop()

#单例模式
reactor = Reactor()