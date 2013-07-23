from protobufproto import ProtoBufFactory
from twisted.internet import reactor


class InterfaceProtoStream:
    def __init__(self, xml):
        #get protobufcfg from main config
        protostreamcfg = manager.config.getConfig('iprotostream')

        #ip
        ip = manager.config.getValue(protostreamcfg, 'ip', default='0.0.0.0')
        #port
        port = int(manager.config.getValue(protostreamcfg, 'port', default=37014))
        #password
        password = manager.config.getValue(protostreamcfg, 'password')
        if password is None:
            log.warning("NO SCI PASSWORD SET")

        self.protofactory = ProtoBufFactory(manager.isMaster, password, manager.messagemanager.isRegistered, manager.messagemanager.proccessMessage, manager.blacklist.blacklist, self.fireConnect)
        if manager.isMaster:
            log.info("setting up protostream server on ", ip, ":", port)
            self.protoport = reactor.listenTCP(port, self.protofactory, interface=ip)
        else:
            log.info("connecting to protostream server on ", ip, ":", port)
            self.protoport = reactor.connectTCP(ip, port, self.protofactory)

        self.connectcallbacks = []


    def registerConnect(self, method):
        self.connectcallbacks.append(callback)

    def fireConnect(self):
        for callback in self.connectcallbacks:
            return callback()  


    def destroy(self, callback):
        self.protofactory.dropAllConnections()
        d = self.protoport.stopListening()
        d.addCallback(callback, "iprotostream")
        return True
