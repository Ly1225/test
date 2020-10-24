class Factory(object):
    def doStart(self):
        self.startFactory()

    def startFactory(self):
        pass

class BaseProtocol:
    """
    This is the abstract superclass of all protocols.

    Some methods have helpful default implementations here so that they can
    easily be shared, but otherwise the direct subclasses of this class are more
    interesting, L{Protocol} and L{ProcessProtocol}.
    """
    connected = 0
    transport = None

    def makeConnection(self, transport):
        """
        Make a connection to a transport and a server.

        This sets the 'transport' attribute of this Protocol, and calls the
        connectionMade() callback.
        """
        self.connected = 1
        self.transport = transport
        self.connectionMade()


    def connectionMade(self):
        """
        Called when a connection is made.

        This may be considered the initializer of the protocol, because
        it is called when the connection is completed.  For clients,
        this is called once the connection to the server has been
        established; for servers, this is called after an accept() call
        stops blocking and a socket has been received.  If you need to
        send any greeting or initial message, do it here.
        """

class Protocol(BaseProtocol):
    """
    This is the base class for streaming connection-oriented protocols.

    If you are going to write a new connection-oriented protocol for Twisted,
    start here.  Any protocol implementation, either client or server, should
    be a subclass of this class.

    The API is quite simple.  Implement L{dataReceived} to handle both
    event-based and synchronous input; output can be sent through the
    'transport' attribute, which is to be an instance that implements
    L{twisted.internet.interfaces.ITransport}.  Override C{connectionLost} to be
    notified when the connection ends.

    Some subclasses exist already to help you write common types of protocols:
    see the L{twisted.protocols.basic} module for a few of them.
    """

    def logPrefix(self):
        """
        Return a prefix matching the class name, to identify log messages
        related to this protocol instance.
        """
        return self.__class__.__name__


    def dataReceived(self, data):
        """
        Called whenever data is received.

        Use this method to translate to a higher-level message.  Usually, some
        callback will be made upon the receipt of each complete protocol
        message.

        @param data: a string of indeterminate length.  Please keep in mind
            that you will probably need to buffer some data, as partial
            (or multiple) protocol messages may be received!  I recommend
            that unit tests for protocols call through to this method with
            differing chunk sizes, down to one byte at a time.
        """

    def connectionLost(self, reason=connectionDone):
        """
        Called when the connection is shut down.

        Clear any circular references here, and any external references
        to this Protocol.  The connection has been closed.

        @type reason: L{twisted.python.failure.Failure}
        """
