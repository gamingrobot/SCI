class ExamplePlugin:
    def __init__(self, xml):
        manager.commandmanager.registerCommand("echoexample", self.echoCommand)

    def echoCommand(self, command, args):
        return args, " ".join(args)
