# -*-coding:UTF-8 -*
from robots.robot import Robot
from mathutils.types import Vertex

class TictacRobot(Robot):
    
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
        self.transmitter = "arm"
        self.devices = { "asserv": 1305, "mother": 1306, "turret": 1308 }
        
        self.sensor_id_front_left  = 0
        self.sensor_id_front_right = 1
        self.sensor_id_back        = 2
