import sys
import __builtin__
from threading import Timer

import bin.log
import bin.manager

from twisted.internet import reactor


class SCI:
    def __init__(self, config):
        self.config = config
        self.start()
        reactor.run(installSignalHandlers=1)

    def start(self):
        #make logger global
        __builtin__.log = bin.log.Log(self.config)

        # Create the manager
        pluginmanager = bin.manager.Manager(self.config)

        #make manager global
        __builtin__.manager = pluginmanager

        pluginmanager.loadPlugins()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        config = sys.argv[1]
    else:
        config = 'sci_config.xml'

    #start up SCI
    SCI(config)
