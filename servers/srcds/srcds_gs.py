from srcds_base import SRCDSServerBase


class SRCDSServerGS(SRCDSServerBase):
    def __init__(self, server_key, config):
        SRCDSServerBase.__init__(self, server_key, config)
        self._gs_username = config["gs_username"]
        self._gs_password = config["gs_password"]

    def start(self):
        pass

    def stop(self):
        pass

    def restart(self):
        pass

    def status(self):
        pass

    def update(self):
        pass
