from missions.mission import Mission
from math import cos, sin
from mathutils.types import Vertex
from math import pi as PI

class SymmetricalMission(Mission):

    def __init__(self):
        super().__init__(__name__)
    
    def post_init(self):
        self.mother.getSwitchOneState()

    def process_event(self, e):

        if e.proto == "asserv" and e.name == "switchOne":
            if e.args["state"] == 0:
                self.dispatcher.symmetrical(False)
            else:
                self.dispatcher.symmetrical(True)
        
