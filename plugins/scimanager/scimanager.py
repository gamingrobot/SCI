class Tag:
    none = None
    server = 1 #server of the current instance 
    sci = 2 #sci instance
    sciserver = 3 #server that belongs to another sci instance
    group = 4 



class SCIManager:
    def __init__(self, xml):
        pass


    """general functions"""
    def destroy(self, callback):
        self.servercheckerloop.stop()

    def checkServer(self):
        #do ping checks

        #call sub servers checkserver
        for server_tag in self._servers.keys():
            server = self._servers[server_tag]["instance"]
            if hasattr(server, "checkserver"):
                server.checkserver()

    def sendTagData(self):
        name = manager.getName()
        print name


    """used to do tag checking"""
    def tagCommand(self, command, args):
        server_tag = args[0]
        istag, result = self.isTag(server_tag)
        if not istag:
            return istag, result

        #call the function
        return getattr(self, command)(server_tag, result, args[1:])

    """commands"""
    def getTagsCommand(self, command, args):
        tags = self._servers.keys()
        for server in self._servers.keys():
            if self._servers[server]["type"] == "sci":
                tags += self._servers[server]["instance"].gettags()
        return tags

    def serverTagCommand(self, command, args):
        ip = args[0]
        port = args[1]
        for tag in self._servers.keys():
            cfg = self._servers[tag]["config"]
            testip = cfg['ip']
            testport = cfg['port']
            if testip == ip and testport == port:
                return tag
        #no server found
        return False

    """tag based commands"""
    def rcon_send(self, tag, tagtype, args):
        if tagtype == Tag.server:
            return self.serverForTag(tag).sendcommand(args[0], args[1:])
        elif tagtype == Tag.sci:
            sci = self.sciForTag(tag)
            return sci.sendcommand(args[0], args[1:])
        elif tagtype == Tag.sciserver:
            sci = self.sciServerForTag(tag)
            cmdargs = [tag] + args
            return sci.sendcommand("rcon_send", cmdargs)
        elif tagtype == Tag.group:
            return True  # TODO

    def start(self, tag, tagtype, args):
        if tagtype == Tag.server:
            log.info("Starting server", tag)
            response = self.serverForTag(tag).start()
            log.info("Started server", tag)
            return response
        elif tagtype == Tag.sci:
            return False, "Sci %s cannot be started" % tag
        elif tagtype == Tag.sciserver:
            sci = self.sciServerForTag(tag)
            return sci.sendcommand("start", tag)
        elif tagtype == Tag.group:
            return True  # TODO

    def stop(self, tag, tagtype, args):
        if tagtype == Tag.server:
            log.info("Stopping server", tag)
            response = self.serverForTag(tag).stop()
            log.info("Stopped server", tag)
            return response
        elif tagtype == Tag.sci:
            return False, "Sci %s cannot be stopped" % tag
        elif tagtype == Tag.sciserver:
            sci = self.sciServerForTag(tag)
            return sci.sendcommand("stop", tag)
        elif tagtype == Tag.group:
            return True  # TODO

    def restart(self, tag, tagtype, args):
        if tagtype == Tag.server:
            log.info("Restarting server", tag)
            response = self.serverForTag(tag).restart()
            log.info("Restarted server", tag)
            return response
        elif tagtype == Tag.sci:
            sci = self.sciForTag(tag)
            return sci.restart()
        elif tagtype == Tag.sciserver:
            sci = self.sciServerForTag(tag)
            return sci.sendcommand("restart", tag)
        elif tagtype == Tag.group:
            return True  # TODO

    def update(self, tag, tagtype, args):
        if tagtype == Tag.server:
            log.info("Updating server", tag)
            response = self.serverForTag(tag).update()
            log.info("Updated server", tag)
            return response
        elif tagtype == Tag.sci:
            return False, "Sci updating currently unavailable"  # TODO
        elif tagtype == Tag.sciserver:
            sci = self.sciServerForTag(tag)
            return sci.sendcommand("update", tag)
        elif tagtype == Tag.group:
            return True  # TODO

    def checkupdate(self, tag, tagtype, args):
        if tagtype == Tag.server:
            return self.serverForTag(tag).checkupdate()
        elif tagtype == Tag.sci:
            return False, "Sci checkupdate currently unavailable"  # TODO
        elif tagtype == Tag.sciserver:
            sci = self.sciServerForTag(tag)
            return sci.sendcommand("checkupdate", tag)
        elif tagtype == Tag.group:
            return True  # TODO

    def status(self, tag, tagtype, args):
        pass  # TODO

    def get_server_log(self, tag, tagtype, args):
        if len(args) == 0:
            lines = 50
        else:
            lines = int(args[0])

        if tagtype == Tag.server:
            return self.serverForTag(tag).getlog(lines)
        elif tagtype == Tag.sci:
            sci = self.sciForTag(tag)
            return sci.getlog(lines)
        elif tagtype == Tag.sciserver:
            sci = self.sciServerForTag(tag)
            return sci.sendcommand("get_server_log", [tag, lines])
        elif tagtype == Tag.group:
            return True  # TODO

    """tag stuff"""
    def isTag(self, server_tag):
        #do tag checking
        isservertag = self.isServerTag(server_tag)
        isgrouptag = self.isGroupTag(server_tag)
        isscitag = self.isSciTag(server_tag)
        issciservertag = self.isSciServerTag(server_tag)

        tagtype = Tag.none
        if isservertag:
            tagtype = Tag.server
        elif isgrouptag:
            tagtype = Tag.group
        elif isscitag:
            tagtype = Tag.sci
        elif issciservertag:
            tagtype = Tag.sciserver

        if tagtype != Tag.none:
            return True, tagtype

        return False, "Tag %s doesn't exist" % server_tag

    def isServerTag(self, server_tag):
        if server_tag in self._servers.keys():
            if self._servers[server_tag]["type"] != "sci":
                return True
        return False

    def isSciTag(self, server_tag):
        if server_tag in self._servers:
            if self._servers[server_tag]["type"] == "sci":
                return True
        return False

    def isSciServerTag(self, server_tag):
        issciserver = self.sciServerForTag(server_tag)
        if issciserver is None:
            return False
        return True

    def isGroupTag(self, server_tag):
        return False  # TODO

    def sciForTag(self, server_tag):
        if server_tag in self._servers.keys():
            return self._servers[server_tag]["instance"]

    def serverForTag(self, server_tag):
        if server_tag in self._servers.keys():
            return self._servers[server_tag]["instance"]

    def sciServerForTag(self, server_tag):
        for sci_server in self._servers.keys():
            if self._servers[sci_server]["type"] == "sci":
                if server_tag in self._servers[sci_server]["instance"].gettags():
                    return self._servers[sci_server]["instance"]
