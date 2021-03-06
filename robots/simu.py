from robots.robot import Robot
from mathutils.types import Vertex

class SimuRobot(Robot):
    
    def __init__(self):
        
        super().__init__()

        # Zone de départ : red|blue
        self.side = "red"

        # Dimension du robot
        self.dimensions = { "left": 1290, "right": 1290,
                "front": 1190, "back": 920 }

        # Position initial du robot
        self.pos = Vertex(-12000, -7000)
        # Orientation initial du robot
        self.rot = 0

        # Périphérique
        self.transmitter = "pic"
        self.devices = { "asserv": 1305, "sensor": 1302 }
