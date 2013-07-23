import pickle
import sys
from srcds_win32 import SRCDSServerProcessWin32

import win32serviceutil
import win32event
import win32service
import win32api


class Service(win32serviceutil.ServiceFramework):
    _svc_name_ = '_unNamed'
    _svc_display_name_ = '_Service Template'

    def __init__(self, *args):
        #fix the name
        if(len(args) > 0):
            self._svc_name_ = args[0][0]
        win32serviceutil.ServiceFramework.__init__(self, *args)
        self.log('init')
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)

    def log(self, msg):
        import servicemanager
        servicemanager.LogInfoMsg(str(msg))

    def sleep(self, sec):
        win32api.Sleep(sec * 1000, True)

    def SvcDoRun(self):
        self.ReportServiceStatus(win32service.SERVICE_START_PENDING)
        try:
            self.ReportServiceStatus(win32service.SERVICE_RUNNING)
            self.log('starting')
            self.start()
            #self.log('wait')
            win32event.WaitForSingleObject(self.stop_event, win32event.INFINITE)
            self.log('started')
        except Exception, x:
            self.log('Exception : %s' % x)
            self.SvcStop()

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.log('stopping')
        self.stop()
        self.log('stopped')
        win32event.SetEvent(self.stop_event)
        self.ReportServiceStatus(win32service.SERVICE_STOPPED)

    # to be overridden
    def start(self):
        pass

    # to be overridden
    def stop(self):
        pass


class SRCDSSvc(Service):
    def start(self):
        self.runflag = True
        pickled_key = win32serviceutil.GetServiceCustomOption(self._svc_name_, "server_key")
        key = pickle.loads(pickled_key)
        pickled_config = win32serviceutil.GetServiceCustomOption(self._svc_name_, "config")
        config = pickle.loads(pickled_config)

        self.log("Starting Server")
        self.log(config)
        try:
            self.server_obj = SRCDSServerProcessWin32(key, config)
            self.server_obj.start()
        except Exception, x:
            self.log('Exception : %s' % x)
            self.SvcStop()

        self.log("Started Server")

    def stop(self):
        self.runflag = False
        self.log("Stopping Server")
        self.server_obj.stop()
        self.log("Stopped Server")
