class Event:
    def __init__(self, proto, name, args, dests=[], **kwargs):
        self.proto = proto
        self.name = name
        self.args = args
        self.dests = dests

    def __getattr__(self, attr):
        return self.args[attr]
        #return getattr(self.args, attr)
