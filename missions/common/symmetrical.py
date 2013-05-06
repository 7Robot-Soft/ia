from missions.mission import Mission
from math import cos, sin
from mathutils.types import Vertex
from math import pi as PI

class SymmetricalMission(Mission):

    def __init__(self):
        super().__init__(__name__)
    
    def post_init(self):
        pass

    def process_event(self, e):

        if e.proto == "asserv" and e.name == "sideX":
            self.dispatcher.symmetrical(False)
        elif e.proto == "sensor" and e.name == "sideY":
            self.dispatcher.symmetrical(True)
