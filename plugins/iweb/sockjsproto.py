from twisted.internet.protocol import Factory, Protocol

class WebSockProtocol(Protocol):
    def __init__(self):
        pass

    def connectionMade(self):
        print "connectionMade"
        self.transport.write("testing")

    def dataReceived(self, data):
        print "dataReceived"
        print data


class WebSockFactory(Factory):
    protocol = WebSockProtocol
    def __init__(self):
        self.protocols = []

    def buildProtocol(self, addr):
        print "building proto"
        p = self.protocol()
        p.factory = self
        self.protocols.append(p)
        return p
