from events.event import Event

class InternalChannel:

    def __init__(self, dispatcher):
        self.dispatcher = dispatcher

    def __getattr__(self, name):
        def fnct(args = dict()):
            e = Event("internal", name, args)
            self.dispatcher.add_event(e)
        return fnct
