from twisted.internet import reactor
from test import Test


class Base:
    def __init__(self, xml):
        manager.commandmanager.registerCommand("about", self.aboutCommand)
        manager.commandmanager.registerCommand("plugins", self.pluginsCommand)
        manager.commandmanager.registerCommand("restart_sci", self.restartSCI)
        manager.commandmanager.registerCommand("echo", self.echoCommand)
        Test()

    def aboutCommand(self, command, args):
        return "SCI (Server Control Interface) %s\nCreated by agent86\nRewritten by GamingRobot32\nMaintained by spidEY & Spray" % (manager.getVersion())

    def pluginsCommand(self, command, args):
        plugins = manager.getPluginsInfo()
        ret = "List of plugins: \n"
        ret += "\n".join(plugins)
        return plugins, ret

    def restartSCI(self, command, args):
        reactor.callLater(1, manager.restartSCI)
        return True, "Restarting SCI"

    def echoCommand(self, command, args):
        return args, " ".join(args)
