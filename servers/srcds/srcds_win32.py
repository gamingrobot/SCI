import os
from twisted.internet import reactor
from srcds_base import SRCDSServerBase

import win32con
import win32process
import pywintypes
import win32api
import win32pipe


class SRCDSServerProcessWin32(SRCDSServerBase):
    def __init__(self, server_key, config):
        SRCDSServerBase.__init__(self, server_key, config)
        self._dir = config["dir"]
        self._args = config["launch_args"]
        self._cmd = os.path.join(self._dir, "srcds.exe")
        if not os.path.isfile(self._cmd):
            #must be the old system #OLD_SYSTEM
            self._cmd = os.path.join(self._dir, "orangebox", "srcds.exe")
        self.startupinfo = win32process.STARTUPINFO()
        self.startupinfo.dwFlags = 0  # win32con.STARTF_USESHOWWINDOW
        self.startupinfo.wShowWindow = win32con.SW_NORMAL
        self.r_pipe = None
        self.w_pipe = None
        self.process = None
        self.ended = 0

    def start(self):
        sec = pywintypes.SECURITY_ATTRIBUTES()
        sec.bInheritHandle = 1
        self.r_pipe, self.w_pipe = win32pipe.CreatePipe(sec, 64 * 1024)
        self.startupinfo.dwFlags = 0  # win32con.STARTF_USESTDHANDLES
        self.startupinfo.hStdOutput = self.w_pipe
        self.startupinfo.hStdError = self.w_pipe
        self.startupinfo.hStdInput = win32api.GetStdHandle(win32api.STD_INPUT_HANDLE)
        #flags = win32con.CREATE_NEW_CONSOLE
        flags = win32con.CREATE_NEW_PROCESS_GROUP

        cmd = self._cmd + " " + self._args
        print(cmd)

        try:
            (self.process, self.thread, self.process_id, self.thread_id) = win32process.CreateProcess(None, cmd, None, None, 1, flags, None, None, self.startupinfo)
        except win32api.error, details:
            # maul_proc_event
            # task_id, event_time, event_type, event_text
            #  event_type - 0 = info, 1 = warn, 2 = error
            log.error("Failed to launch process.  Error in function %s: %s (Windows error code %d)" % (details[1], details[2], details[0]))
            self.ended = 1
            #self.processEnded()
            return False

        return True

    def stop(self):
        if(self.process is None):
            if(self.ended == 0):
                self.ended = 1
                self.processEnded(-1)
            return False
        try:
            win32process.TerminateProcess(self.process, 1)
        except:
            pass
        self.process = None
        if(self.r_pipe is not None):
            self.r_pipe.close()
        if(self.w_pipe is not None):
            self.w_pipe.close()
        self.r_pipe = None
        self.w_pipe = None
        if(self.ended == 0):
            self.ended = 1
            #self.processEnded()
