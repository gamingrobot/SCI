from bin.shared.protostream import ProtoStreamHandler
from twisted.internet.protocol import ClientFactory, Protocol
from twisted.protocols.basic import LineReceiver
import time


class ProtoBufProtocol(LineReceiver):
    MAX_LENGTH = 204800 #200kb
    def __init__(self):
        self.authkey = ""
        self.authtoken = ""
        self.handler = ProtoStreamHandler()

    def connectionMade(self): #needed for server only
        if self.factory.isServer:
            peer_addr = self.transport.getPeer()
            if peer_addr.host in self.factory.blacklist: #TODO add to blacklist
                self.transport.loseConnection()
                return
            #send some auth stuff
            print peer_addr
            self.authtoken = self.handler.getToken(peer_addr)
            self.sendLine(self.handler.packToken(self.authtoken))

    def lineReceived(self, data):
        print "dataReceived"
        if self.authkey == "": #must be auth response/request
            response = self.handleAuth(data)
            if response is not None:
                self.sendLine(response)
        else:
            response = self.handleProtoStream(data)
            if response is not None:
                self.sendLine(response)

    def handleAuth(self, data):
        try:
            protoauth = self.handler.unpackAuth(data)
        except:
            self.transport.loseConnection() #whoa what kind of request you sending
            return
        #do 3 auth_type checks
        print protoauth
        #got a token, compute a hash, send hash
        if protoauth.auth_type == protoauth.TOKEN: #server.TOKEN -> client
            passhash = self.handler.getHash(self.factory.password, protoauth.data)
            return self.handler.packHash(passhash) #client.HASH -> server
        #got a hash, double check hash, generate key, send key
        elif protoauth.auth_type == protoauth.HASH: #client.HASH -> server
            if protoauth.data == self.handler.getHash(self.factory.password, self.authtoken):
                peer_addr = self.transport.getPeer()
                self.authkey = self.handler.getKey(peer_addr)
                return self.handler.packKey(self.authkey) #server.KEY -> client
        #got key, store key
        elif protoauth.auth_type == protoauth.KEY: #server.KEY -> client
            self.authkey = protoauth.data
            self.factory.fireConnect()

    def handleProtoStream(self, data):
        header, message = self.handler.unpackProtoStream(data, self.factory.isRegistered)
        if header.key == self.authkey:
            try:
                response = self.factory.processMessage(header, message)
                return self.handler.packProtoStream(self.authkey, response)
            except:
                return ""
        else:
            print "bro you aint from around here"


class ProtoBufFactory(ClientFactory):
    protocol = ProtoBufProtocol
    def __init__(self, isServer, password, isRegistered, processMessage, blacklist, fireconnect):
        self.protocols = []
        self.password = password
        self.isServer = isServer
        self.isRegistered = isRegistered
        self.processMessage = processMessage
        self.blacklist = blacklist
        self.fireConnect = fireconnect

    def buildProtocol(self, addr):
        p = self.protocol()
        p.factory = self
        self.protocols.append(p)
        return p

    def dropAllConnections(self):
        for protocol in self.protocols:
            protocol.transport.loseConnection()

    def clientConnectionLost(self, connector, reason):
        print "lost connection:", reason
        time.sleep(1)
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "connection failed:", reason
        time.sleep(1)
        connector.connect()