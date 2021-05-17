class Target:
    name = ''
    bandwith = 0
    location = ''
    def __init__(self, name, bandwith, location):
        self.name = name
        self.bandwith = bandwith
        self.location = location

    def attacks(self):
        return "Attack launched at %s with %s mbps bandwith at %s"%(self.name,self.bandwith,self.location)

class Website(Target):
    address = ''

    def __init__(self, name, bandwith, location, address):
        Target.__init__((self), name, bandwith, location)
        self.address = address

    def attacks(self):
        return "Attack launched at %s with %s mbps bandwith with url %s located at %s\n"%(self.name,self.bandwith,self.address,self.location)

class Server(Target):
    spec = ''
    ip = ''

    def __init__(self, name, bandwith, location, spec, ip):
        Target.__init__((self), name, bandwith, location)
        self.spec = spec
        self.ip = ip
    
    def attacks(self):
        return "Attack launched at %s with %s mbps bandwith with type %s located at %s with ip %s\n"%(self.name,self.bandwith,self.spec,self.location,self.ip)

