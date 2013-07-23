from twisted.internet.protocol import Factory, Protocol
from struct import pack, unpack
from binascii import hexlify


""" https://developer.valvesoftware.com/wiki/Source_RCON_Protocol """


class SourceRCONProtocol(Protocol):
    def __init__(self):
        self.auth = False

    def connectionMade(self):
        peer_addr = self.transport.getPeer()
        host = peer_addr.host
        attempts = self.factory.attempts

        if host in self.factory.blacklist:
            self.transport.loseConnection()
            return

        elif host in attempts:
            if attempts[host] >= self.factory.failedattempts:
                #add to blacklist
                self.factory.addToBlacklist(host)
                del attempts[host]

    def dataReceived(self, data):
        debug = False
        peer_addr = self.transport.getPeer()
        host = peer_addr.host
        attempts = self.factory.attempts

        if debug:
            log.info(host, hexlify(data), data)
        #kick them off if they are on the blacklist
        if host in self.factory.blacklist:
            self.transport.loseConnection()
            return
        minpacketsize = 10
        if len(data) < minpacketsize:  # Anything shorter than this is not a valid request!
            self.transport.loseConnection()
            return
        reqsize, reqid, reqtype = unpack("<iii", data[0:12])
        if debug:
            print hexlify(data)
            print "reqsize: %d, reqid: %d, reqtype: %d" % (reqsize, reqid, reqtype)
        if self.auth == False or reqtype == 3:
            resid = 2  # SERVERDATA_AUTH_RESPONSE
            ressize = minpacketsize
            resid = -1
            resstatus = 2
            if reqtype == 3:  # SERVERDATA_AUTH
                client_pwd = data[12:-2]
                if client_pwd == self.factory.rcon_pwd:
                    if debug:
                        print "Successful authorization."
                    resid = reqid
                    self.auth = True
                else:
                    if host in attempts:
                        attempts[host] += 1
                    else:
                        attempts[host] = 1
                    if debug:
                        print "failed authorization, '%s' != '%s'" % (client_pwd, self.factory.rcon_pwd)

            response = pack("<iiibb", ressize, resid, resstatus, 0, 0)
            self.transport.write(response)
        else:
            if reqsize == minpacketsize:
                data = data[8:]
            else:
                data = data[12:]
            while(len(data) != 0):
                next_cmd_end_idx = data.find("\x00\x00")
                if(next_cmd_end_idx <= 0):
                    return
                client_cmd = data[:next_cmd_end_idx]
                data = data[next_cmd_end_idx + 2 + 12:]
                if self.factory.processCommand:
                    try:
                        str_output = self.factory.processCommand((peer_addr.host, peer_addr.port), client_cmd)
                    except:
                        str_output = "An internal error occurred while processing your command."
                        ressize = minpacketsize + len(str_output)
                        resstatus = 0  # SERVERDATA_RESPONSE_VALUE
                        response = "".join((pack("<iii", ressize, reqid, resstatus), str_output, pack("<bb", 0, 0)))
                        self.transport.write(response)
                        raise

                    if str_output is None:
                        str_output = "Command complete."
                else:
                    str_output = "".join("Request: %s" % (client_cmd))
                ressize = minpacketsize + len(str_output)
                resstatus = 0  # SERVERDATA_RESPONSE_VALUE
                response = "".join((pack("<iii", ressize, reqid, resstatus), str_output, pack("<bb", 0, 0)))
                if debug:
                    print "Command response: %s" % (hexlify(response))
                self.transport.write(response)
            if debug:
                print "Transaction complete.\n"


class SourceRCONProtocolFactory(Factory):
    protocol = SourceRCONProtocol
    def __init__(self, rcon_pwd, failedattempts, blacklist, addblacklist, processCommand=None):
        self.protocols = []
        self.rcon_pwd = rcon_pwd
        self.processCommand = processCommand
        self.attempts = {}
        self.blacklist = blacklist
        self.addToBlacklist = addblacklist
        self.failedattempts = failedattempts

    def buildProtocol(self, addr):
        p = self.protocol()
        p.factory = self
        self.protocols.append(p)
        return p

    def dropAllConnections(self):
        for protocol in self.protocols:
            protocol.transport.loseConnection()
