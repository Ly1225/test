from select import  epoll, EPOLLHUP,EPOLLIN, EPOLLOUT
from tcp import Port

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

    def listenTCP(self, port, factory, backlog=50, interface=''):
        p = Port(port, factory, backlog, interface, self)
        p.startListening()
        return p

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
            print( e.__dict__ )