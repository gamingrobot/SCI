from srcds_base import SRCDSServerBase
from srcds_gs import SRCDSServerGS
from twisted.internet import reactor
from twisted.internet.protocol import ProcessProtocol
from twisted.internet.defer import Deferred
from twisted.python.runtime import platform

if platform.isWindows():
    from srcds_win32 import SRCDSServerProcessWin32
    from srcds_svcwin32 import SRCDSServerServiceWin32

import json
import urllib
import urllib2
import os
import time
import ast

import SourceLog
import SourceRcon


class SRCDSUpdate(ProcessProtocol):
    def __init__(self, server_key,):
        self.deferred = Deferred()
        self.server_key = server_key

    def childDataReceived(self, childFD, data):
        data = data.replace("\r", "")
        data_lines = data.split("\n")
        for line in data_lines:
            line = line.strip()
            if(len(line) == 0):
                continue
            #log.info("%s, %s" % (self.server_key, line))  # TODO

    def processEnded(self, status):
        #print("process ended!")
        if(self.deferred):
            self.deferred.callback(self)


class SRCDSServer:
    def __init__(self, server_key, config):
        self._subtype = config["subtype"].lower()
        self._server_key = server_key
        self._config = config

        #setup logging
        self.logdata = []
        self.lastlogtime = time.time()
        self.loggingport = 0

        self._dediids = {'tf': 232250, 'dod': 232290, 'css': 232330}

        #setup rcon
        self.rcon = SourceRcon.SourceRcon(self._config["ip"], int(self._config["port"]), self._config["rcon_password"])

        if self._subtype == "":
            self._subtype = None

        log.debug("server_key:", server_key, "self._subtype:", self._subtype)
        if self._subtype is None:
            if platform.isWindows():
                self._server = SRCDSServerProcessWin32(server_key, config)
            else:
                self._server = SRCDSServerBase(server_key, config)

        elif self._subtype == "svc":
            if platform.isWindows():
                self._server = SRCDSServerServiceWin32(server_key, config)
            else:
                self._server = SRCDSServerBase(server_key, config)

        elif self._subtype == "gs":
            self._server = SRCDSServerGS(server_key, config)

    def start(self):
        self._server.start()
        sourcelog = SourceLog.SourceLogListener(self.logaction)
        self.loggingport = sourcelog.getlogport()

    def stop(self):
        self._server.stop()

    def restart(self):
        self._server.stop()
        self._server.start()

    def status(self):
        pass

    def update(self):
        if self.checkupdate():
            self.sendcommand("sm_say", "[SCI] Game update has been detected, server will shut down for updates.")
            self.stop()
            update_obj = SRCDSUpdate(self._server_key)
            update_obj.deferred.addCallback(self.updateComplete)
            update_exe = self._config['update_exe']
            if os.path.basename(update_exe) == "hldsupdatetool.exe":
                #OLD_SYSTEM
                arg_list = [os.path.basename(update_exe), "-command", "update", "-game", self._config['game'], "-dir", self._config['dir']]
            else:
                #steamcmd.exe +login anonymous +force_install_dir ../server +app_update 232290+quit
                arg_list = [os.path.basename(update_exe), "+login", "anonymous", "+force_install_dir", self._config['dir'], "+app_update", str(self._dediids[self._config['game']]), "+quit"]
            print arg_list
            reactor.spawnProcess(update_obj, update_exe, arg_list, env=None)
            return True, "Updating %s" % self._server_key
        else:
            return False, "Server is up to date"

    def updateComplete(self, data):
        self.start()

    def sendcommand(self, command, args):
        if isinstance(args, list) or isinstance(args, tuple):
            return self.rcon.sendrcon(command + "" + " ".join(args))
        else:
            return self.rcon.sendrcon(command + " " + args)

    def getlog(self, lines):
        return self.logdata[-lines:]

    def checkupdate(self):
        if self._subtype == "gs":
            return False
        else:
            gamename, version, appid = self._readSteamInf()
            updateret = self.steamAPICall('ISteamApps/UpToDateCheck/v0001', {'appid': appid, 'version': version})
            if (updateret is False or updateret['success'] is not True):
                return False
            elif updateret['up_to_date'] is True:
                return False
            else:
                return True

    def checkserver(self):
        if (time.time() - self.lastlogtime) >= 60:
            #send logaddress_add ip:port
            self.sendcommand("logaddress_add", "%s:%s" % (self._config["ip"], str(self.loggingport)))

    def logaction(self, remote, timestamp, key, value, properties):
        self.lastlogtime = time.time()
        value = ast.literal_eval(str(value).encode('utf-8', 'replace'))
        properties = ast.literal_eval(str(properties).encode('utf-8', 'replace'))
        self.logdata.append({'remote': remote, 'timestamp': timestamp, 'key': key, 'value': value, 'properties': properties})

    def steamAPICall(self, path, rawargs={}):
        args = rawargs
        args = '?%s' % (urllib.urlencode(args))

        url = "%s/%s/%s" % ('https://api.steampowered.com', path, args)
        try:
            raw = urllib2.urlopen(url).read()
        except Exception:
            return False

        return json.loads(raw)['response']

    def _readSteamInf(self):
        gamename = None
        version = None
        appid = None
        try:
            # open file
            basedir = self._config["dir"]
            steaminf = os.path.join(basedir, self._config["game"], "steam.inf")
            if not os.path.isfile(steaminf):
                #must be the old system #OLD_SYSTEM
                steaminf = os.path.join(basedir, "orangebox", self._config["game"], "steam.inf")
            inffile = open(steaminf, "r")

            for line in inffile:
                (key, value) = line.split("=")
                if(key == "PatchVersion"):
                    version = value.strip()
                elif(key == "ProductName"):
                    gamename = value.strip()
                elif(key == "appID"):
                    appid = value.strip()
        except:
            log.error("Error while reading steam.inf file")

        if(gamename is None or version is None or appid is None):
            log.warning("Can't read steam.inf!" % (self._server_key))

        return gamename, version, appid
