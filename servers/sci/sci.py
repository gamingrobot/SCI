import socket
import json
import md5
import struct
import urllib
import httplib2


class SCIServer:
    def __init__(self, server_key, config):
        log.debug("server_key:", server_key)
        self._config = config
        log.info(self._config)
        self._key = server_key
        self.httplib = httplib2.Http()
        self._tags = self.sendcommand("get_tags")
        log.info(server_key, "tags are", self._tags)

    def restart(self):
        self.sendcommand(self, "restart_sci")

    def status(self):
        pass

    def sendcommand(self, command, args=[]):
        log.info("sending command", command, "to", self._key)
        rlogin = {'type': 3, 'hash': md5.new(self._config['password']).hexdigest()}
        loginencoded = urllib.urlencode(rlogin)
        url = "http://%s:%d/?%s" % (self._config['ip'], int(self._config['port']), loginencoded)
        print url
        header, response = self.httplib.request(url)
        print response
        resp = json.loads(response)
        if 'key' in resp:
            rcommand = {'type': 2, 'key': resp['key'], 'command': str(command), 'args': " ".join(args)}
            commandencoded = urllib.urlencode(rcommand)
            url = "http://%s:%d/?%s" % (self._config['ip'], int(self._config['port']), commandencoded)
            print url
            header, response = self.httplib.request(url)
            data = json.loads(response)
            print data
            if 'message' in data:
                return data['result'], data['message']
            else:
                return data['result']
        else:
            return False, data['error']

    def gettags(self):
        return self._tags

    def gettag(self):
        return self._key

    def getaddress(self):
        return self._config['ip'], self._config['port']

    def getlog(self, lines):
        return self.sendcommand("get_log", lines)
