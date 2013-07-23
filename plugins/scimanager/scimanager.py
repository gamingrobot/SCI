import bin.shared.protobufs.serverinfo_pb2 as serverinfo_pb2
import bin.shared.protobufs.serveraction_pb2 as serveraction_pb2


class SCIManager:
    def __init__(self, xml):
        manager.messages.registerMessage(serverinfo_pb2.Server, self.messageServer)
        manager.messages.registerMessage(serverinfo_pb2.SCIServers, self.messageSCIServers)
        manager.messages.registerMessage(serveraction_pb2.ServerAction, self.messageServerAction)

    def messageServerAction(self, message):
        print message

    def messageServer(self, message):
        print message

    def messageSCIServers(self, message):
        print message
        
