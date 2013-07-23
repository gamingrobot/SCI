from srcds_base import SRCDSServerBase
import os
import srcds_service

from servers.win32_service import service_install, service_start, service_stop


class SRCDSServerServiceWin32(SRCDSServerBase):
    def __init__(self, server_key, config):
        SRCDSServerBase.__init__(self, server_key, config)
        self._dir = config["dir"]
        self._args = config["launch_args"]
        self._cmd = os.path.join(self._dir, "srcds.exe")
        if not os.path.isfile(self._cmd):
            #must be the old system #OLD_SYSTEM
            self._cmd = os.path.join(self._dir, "orangebox", "srcds.exe")
        #install service
        service_install(srcds_service.SRCDSSvc, 'sci_srcds_%s' % self._key, 'SCI srcds(%s)' % self._key, server_key, config)

    def start(self):
        #start service
        service_start('sci_srcds_%s' % self._key)

    def stop(self):
        service_stop('sci_srcds_%s' % self._key)

    def restart(self):
        pass

    def status(self):
        pass

    def update(self):
        pass
