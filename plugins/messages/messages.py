import bin.shared.protobufs.serveraction_pb2 as serveraction_pb2
from bin.shared.protostream import ProtoStreamHandler


class Messages:
    def __init__(self, xml):
        self._registered = {}

    def proccessMessage(self, header, message):
        module = self._formatModule(message.__module__, message.__class__.__name__)
        return self.getCallback(module)(message)

    def registerMessage(self, message, callback):
        path = self._formatModule(message.__module__, message.__name__)
        self._registered[path] = {'message': message, 'callback': callback}

    def getCallback(self, messagestr):
        if messagestr in self._registered.keys():
            return self._registered[messagestr]['callback']
        return None

    def getProto(self, messagestr):
        if messagestr in self._registered.keys():
            return self._registered[messagestr]['message']
        return None

    def _formatModule(self, module, classname):
        module = module.split('.')[-1]
        return "%s.%s" % (module, classname)