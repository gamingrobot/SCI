class SRCDSServerBase:
    def __init__(self, server_key, config):
        self._key = server_key
        self._config = config
        self._game = config["game"]

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
