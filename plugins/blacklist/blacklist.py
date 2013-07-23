class Blacklist:
    def __init__(self, xml):
        manager.commands.registerCommand("blacklist", self.blacklistCommand, help="blacklist <add|remove|update> <ip>")
        self._file = manager.config.getValue(xml, 'blacklist', subkey='file', default='ip_blacklist.cfg')
        self.blacklist = self.readBlacklistFile(self._file)

    def blacklistCommand(self, command, args):
        numargs = len(args)
        if numargs < 2:
            if len(self.blacklist) == 0:
                return self.blacklist, "Blacklist is empty"
            else:
                return self.blacklist, ",".join(self.blacklist)
        elif numargs == 2:
            if args[0] == 'add':
                self.add(args[1])
                return True, "Added %s to blacklist" % (args[1])
            elif args[0] == 'update':
                self.blacklist = self.readBlacklistFile(self._file)
                return True, "Updated blacklist from file"
            elif args[0] == 'remove':
                if self.remove(args[1]):
                    return True, "Removed %s from blacklist" % (args[1])
                else:
                    return False, "%s was not on the blacklist" % (args[1])

    def add(self, ip):
        log.info("Added", ip, "to blacklist")
        if ip not in self.blacklist:
            self.blacklist.append(ip)
            self.writeBlacklistFile(self._file, self.blacklist)

    def remove(self, ip):
        if ip in self.blacklist:
            del self.blacklist[ip]
            self.writeBlacklistFile(self._file, self.blacklist)
            log.info("Removed", ip, "from blacklist")
            return True
        else:
            return False

    def writeBlacklistFile(self, file_, blacklist):
        log.info("Updated Blacklist", blacklist)
        try:
            thefile = open(file_, "w")
            for item in blacklist:
                thefile.write("%s\n" % item)
        except IOError:
            log.error("Could not save blacklist")

    def readBlacklistFile(self, file_):
        try:
            with open(file_, "r") as f:
                ips = f.read().splitlines()
            return ips
        except IOError:
            log.warning("Could not find blacklist file:", self.blacklistfile, "creating it")
            return []
