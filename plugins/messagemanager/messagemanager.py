import bin.shared.protobufs.serveraction_pb2 as serveraction_pb2

class MessageManager:
    def __init__(self, xml):
        self._registered = {'serveraction_pb2.ServerAction': serveraction_pb2.ServerAction}

    def proccessMessage(self, header, message):
        print message
        return self.testData()

    def testData(self):
        entry = serveraction_pb2.ServerAction
        entry.action = serveraction_pb2.ServerAction.RCON_SEND
        entry.tag = "tacos"
        return entry

    def isRegistered(self, messagestr):
        if messagestr in self._registered.keys():
            return self._registered[messagestr]
        return None