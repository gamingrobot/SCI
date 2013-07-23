import xml.etree.ElementTree as et
import inspect
import datetime
import os
import sys
from twisted.python import log as twistedlog


class Log:
    def __init__(self, config):
        self.logcallbacks = []
        elem = et.parse(config)
        logger = elem.find('logger')
        #log file
        logdir = logger.find('logdir')
        if logdir is None:
            logdir = "logs"
        else:
            logdir = logdir.get('value')
        self._logdir = logdir
        #log level
        loglevel = logger.find('level')
        if loglevel is None:
            loglevel = "info"
            self.loglevel = 2
            self.warning('Logger: No loglevel set in config <logger> <level="info" /> <logger/> assuming info level')
        else:
            loglevel = loglevel.get('value')

        if loglevel == "error":
            self.loglevel = 4
        elif loglevel == "warning":
            self.loglevel = 3
        elif loglevel == "info":
            self.loglevel = 2
        elif loglevel == "debug":
            self.loglevel = 1
        elif loglevel == "manager":
            self.loglevel = 0

        self.debug("Level", loglevel)

        #err hook
        twistedlog.addObserver(self.excepthook)

    def _getName(self):
        retmod = "Module"
        frame, module, line, function, context, index = inspect.stack()[2]
        try:
            self_argument = frame.f_code.co_varnames[0]  # this should be self
            instance = frame.f_locals[self_argument]
            retmod = instance.__class__.__name__
        except IndexError:
            retmod = inspect.getmodulename(module)
        return retmod

    def _combine(self, message):
        return " ".join(map(str, message))

    def _format(self, level, name, message):
        return "[%s] <%s> %s" % (name, level, self._combine(message))

    def _log(self, logdata):
        print logdata
        timestamp = datetime.datetime.now().strftime("%m/%d/%Y - %H:%M:%S")
        timelogdata = "%s: %s" % (timestamp, logdata)
        self.file(timelogdata)
        for callback in self.logcallbacks:
            callback(timelogdata)

    def registerLogListener(self, callback):
        self.logcallbacks.append(callback)

    #extra logging
    def file(self, logdata):
        self._filewriter(".log", logdata)

    def fileerr(self, logdata):
        self._filewriter(".log.err", logdata)

    def _filewriter(self, ext, logdata):
        today = datetime.date.today().strftime("%d%m%y")
        filehandler = open(os.path.join(self._logdir, today + str(ext)), 'a', 0)  # 0 is buffer
        filehandler.write(logdata + "\n")
        filehandler.close()

    #message levels
    def error(self, *message):
        if self.loglevel <= 4:
            self._log(self._format("error", self._getName(), message))

    def warning(self, *message):
        if self.loglevel <= 3:
            self._log(self._format("warning", self._getName(), message))

    def info(self, *message):
        if self.loglevel <= 2:
            self._log(self._format("info", self._getName(), message))

    def debug(self, *message):
        if self.loglevel <= 1:
            self._log(self._format("debug", self._getName(), message))

    def manager(self, *message):
        if self.loglevel <= 0:
            self._log(self._format("manager", self._getName(), message))

    #stuff for stderr
    def excepthook(self, logEntryDict):
        if logEntryDict.get('isError'):
            #print logEntryDict
            timestamp = datetime.datetime.now().strftime("%m/%d/%Y - %H:%M:%S")
            if "failure" in logEntryDict.keys():
                logdata = timestamp + "\n" + str(logEntryDict) + "\n" + str(logEntryDict['failure'].getTraceback()) + "\n"
                self.fileerr(logdata)
                self.error("Exception %s: %s %s" % (logEntryDict['failure'].type, logEntryDict['failure'].value, logEntryDict['message']))
            else:
                logdata = timestamp + "\n" + str(logEntryDict) + "\n" + str(logEntryDict['message']) + "\n"
                self.fileerr(logdata)
                self.error("Exception %s %s" % (logEntryDict['system'], logEntryDict['message']))
