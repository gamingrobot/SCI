from rconproto import SourceRCONProtocolFactory
from twisted.internet import reactor


class InterfaceRcon:
    def __init__(self, xml):
        #get rconcfg from main config
        rconcfg = manager.config.getConfig('rconcfg')

        #failedtries
        failed = int(manager.config.getValue(xml, 'failedattemps', default=5))

        #ip
        ip = manager.config.getValue(rconcfg, 'ip', default='0.0.0.0')
        #port
        port = int(manager.config.getValue(rconcfg, 'port', default=37015))

        rconpwd = manager.config.getValue(rconcfg, 'password')
        if rconpwd is None:
            log.warning("NO RCON PASSWORD SET")

        self.rconfactory = SourceRCONProtocolFactory(rconpwd, failed, manager.blacklist.blacklist, manager.blacklist.add, self.processCommand)

        log.info("Setting up rcon server on", ip, ":", port)

        self.rconport = reactor.listenTCP(port, self.rcon, interface=ip)

    def processCommand(self, source, data):
        ret = manager.commandmanager.processCommand(source, data)
        #process return data
        if isinstance(ret, tuple):
            return str(ret[1]) + "\n" + str(ret[0])
        else:
            return str(ret)

    def destroy(self, callback):
        self.rconfactory.dropAllConnections()
        d = self.rconport.stopListening()
        d.addCallback(callback, "ircon")
        return True
