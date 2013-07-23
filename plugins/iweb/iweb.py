from twisted.web.server import Site
from twisted.internet import reactor
from protobufresource import ProtoBufResource
from sockjsproto import WebSockFactory
from txsockjs.factory import SockJSFactory


class InterfaceWeb:
    def __init__(self, xml):
        #get protobufcfg from main config
        protostreamcfg = manager.config.getConfig('iweb')

        #ip
        ip = manager.config.getValue(protostreamcfg, 'ip', default='0.0.0.0')
        #port
        port = int(manager.config.getValue(protostreamcfg, 'port', default=37016))

        #sockjsport
        sockjsport = int(manager.config.getValue(protostreamcfg, 'sockjsport', default=37017))

        apicfg= protostreamcfg.find('apikeys').findall('key')
        apiKeys = []
        for apikeycfg in apicfg:
            apiKeys.append(apikeycfg.get("value"))

        proto = ProtoBufResource(manager.messages.getProto, manager.messages.proccessMessage, apiKeys)
        site = Site(proto)
        site.displayTracebacks = False
        reactor.listenTCP(port, site, 50)
        log.info("setting up protobufresource server on ", ip, ":", port)
        reactor.listenTCP(sockjsport, SockJSFactory(WebSockFactory()), interface=ip)
        log.info("setting up sockjs server on ", ip, ":", sockjsport)


    def destroy(self, callback):
        #do some clean up
        return None
