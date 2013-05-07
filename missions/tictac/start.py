# -*-coding:UTF-8 -*

from missions.mission import Mission
from events.internal import InternalEvent


class StartMission(Mission):

    def __init__(self):
        super().__init__(__name__)
    
    def process_event(self, e):
        if self.state == 0 and e.proto == "internal" and e.name == "start":
            self.state = 1
            self.internal.positioning()
