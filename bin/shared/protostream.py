import protoStream_pb2
import hashlib
import time

class ProtoStreamHandler:
    def __init__(self):
        pass

    def getToken(self, peer):
        host = "%s:%s" % (peer.host, peer.port)
        creationtime = time.time()
        authtoken = hashlib.sha256(host + str(creationtime)).hexdigest()
        return authtoken

    def packToken(self, token):
        prototoken = protoStream_pb2.ProtoStreamAuth()
        prototoken.data = token
        prototoken.auth_type = prototoken.TOKEN
        return self.encodeProto(prototoken)

    def getHash(self, password, token):
        return hashlib.sha256(password + token).hexdigest()

    def packHash(self, passhash):
        protoresponse = protoStream_pb2.ProtoStreamAuth()
        protoresponse.data = passhash 
        protoresponse.auth_type = protoresponse.HASH
        return self.encodeProto(protoresponse)

    def getKey(self, peer):
        host = "%s:%s" % (peer.host, peer.port)
        creationtime = time.time()
        return hashlib.sha256(host + str(creationtime)).hexdigest()

    def packKey(self, key):
        protoresponse = protoStream_pb2.ProtoStreamAuth()
        protoresponse.data = key
        protoresponse.auth_type = protoresponse.KEY
        return self.encodeProto(protoresponse)

    def packProtoStream(self, authkey, message):
        header = protoStream_pb2.ProtoStreamHeader()
        header.key = authkey
        header.module = message.__class__.__module__.split('.')[-1][:-4] #remove plugins.pluginname.*****_pb2
        header.message = message.__class__.__name__

        request = []
        request.append(self.encodeProto(header))
        request.append(self.encodeProto(message))
        return ",".join(request)

    def unpackProtoStream(self, data, getProto):
        data = data.split(",")
        #header protobuf
        header = protoStream_pb2.ProtoStreamHeader()
        self.decodeProto(data[0], header)
        #message protobuf
        print header
        messagepath = "%s_pb2.%s" % (header.module, header.message)
        registered = getProto(messagepath)
        if registered is not None:
            entry = registered()
            self.decodeProto(data[1], entry)
            return header, entry
        else:
            return None

    def unpackAuth(self, data):
        protoauth = protoStream_pb2.ProtoStreamAuth()
        self.decodeProto(data, protoauth)
        return protoauth

    def encodeProto(self, proto):
        return proto.SerializeToString().encode('base64','strict')

    def decodeProto(self, data, proto):
        return proto.ParseFromString(data.decode('base64','strict'))