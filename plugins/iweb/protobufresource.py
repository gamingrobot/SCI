from bin.shared.protostream import ProtoStreamHandler
from twisted.web.resource import Resource


class ProtoBufResource(Resource):
    def __init__(self, isRegistered, processMessage):
        self.handler = ProtoStreamHandler()
        self.isRegistered = isRegistered
        self.processMessage = processMessage

    isLeaf = True
    def render_GET(self, request):
        print "getReceived", request
        if "protoStream" in request.args.keys(): #just a normal stream
            data = request.args['protoStream'][0]
            response = self.handleProtoStream(data)
            if response is not None:
                return response
        return ""

    def handleProtoStream(self, data):
        header, message = self.handler.unpackProtoStream(data, self.isRegistered)
        if header.key == "800e6e356840e38362ae625307437261035db6ed08277159ab7499c1a29e7db9": #TODO
            try:
                response = self.processMessage(header, message)
                return self.handler.packProtoStream(header.key, response)
            except:
                return ""
        else:
            print "bro you aint from around here"