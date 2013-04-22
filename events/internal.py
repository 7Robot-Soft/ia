from events.event import Event

class InternalEvent(Event):

    def __init__(self, name, **kwargs):
        super().__init__("internal", name, kwargs)
