class MinecraftServer:
    def __init__(self, server_key, config):
        subtype = config["subtype"]
        if subtype == "":
            subtype = None
        log.debug("server_key:", server_key, "subtype:", subtype)

        self._key = server_key

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
