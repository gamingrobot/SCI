from bin.shared.protostream import ProtoStreamHandler
from twisted.web.resource import Resource


class ProtoBufResource(Resource):
    def __init__(self, getProto, processMessage, apikeys):
        self.handler = ProtoStreamHandler()
        self.getProto = getProto
        self.processMessage = processMessage
        self.apiKeys = apikeys

    isLeaf = True
    def render_GET(self, request):
        print "getReceived"
        if "protoStream" in request.args.keys(): #just a normal stream
            data = request.args['protoStream'][0]
            response = self.handleProtoStream(data)
            if response is not None:
                return response
        return ""

    def handleProtoStream(self, data):
        header, message = self.handler.unpackProtoStream(data, self.getProto)
        if header is None or message is None:
            return None
        if header.key in self.apiKeys:
            try:
                response = self.processMessage(header, message)
                if response is not None:
                    return self.handler.packProtoStream(header.key, response)
            except:
                return None
        else:
            print "bro you aint from around here"