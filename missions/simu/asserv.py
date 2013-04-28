from missions.mission import Mission
from math import cos, sin
from mathutils.types import Vertex
from math import pi as PI

class AsservMission(Mission):

    def __init__(self):
        super().__init__(__name__)
    
    def post_init(self):
        self.pos = self.robot.pos
        self.rot = self.robot.rot
        self.broadcast = True
        self.odoBroadDelay = 500
        self.asservDelay = 500
        self.state = "repo"

    def process_event(self, e):

        if e.proto == "asserv" and e.name == "getId":
            self.asserv.id(5)
        elif e.proto == "sensor" and e.name == "getId":
            self.sensor.id(2)

        elif e.proto == "asserv" and e.name == "getPos":
            self.asserv.pos(self.robot.pos.x, self.robot.pos.y, self.robot.rot)

        elif e.proto == "asserv" and e.name == "odoBroadcastOn":
            self.broadcast = True
            self.create_timer(self.odoDelay, "odo")
        elif e.proto == "asserv" and e.name == "odoBroadcastOff":
            self.broadcast = False
        elif e.proto == "asserv" and e.name == "odoBroadcastSetDelay":
            self.odoBroadDelay = e.args["delay"]
        elif self.broadcast and e.proto == "internal" and e.name == "timeout" \
                and e.timername == 'speed':
            self.asserv.pos(self.robot.pos.x, self.robot.pos.y, self.robot.rot)
            self.create_timer(self.odoDelay, "odo")

        elif e.proto == "asserv" and e.name == "setPos":
            self.robot.pos = Vertex(e.x, e.y)
            self.robot.rot = e.theta

        elif e.proto == "asserv" and e.name == "setSpeed":
            self.v = e.args['v']
            self.omega = e.args['omega']
            if self.state != "speed":
                self.create_timer(self.asservDelay, "speed")
            self.state = "speed"
        elif e.proto == "asserv" and e.name == "stop":
            self.state = "repo"

        elif self.state == "speed" \
                and e.proto == "internal" and e.name == "timeout" \
                and e.timername == 'speed':
            dt = self.asservDelay/1000
            x = self.v * cos(self.robot.rot/180*PI) * dt
            y = self.v * sin(self.robot.rot/180*PI) * dt
            rot = self.omega * dt
            self.robot.pos += Vertex(x, y)
            self.robot.rot += rot % 360
            print(self.robot.pos, self.robot.rot)
            self.create_timer(self.asservDelay, "speed")

        #elif e.proto == "asserv" and e.name == "forward":
        #    self.state = 10
        #    self.create_timer(e.args["dist"]*2)
        elif self.state == "repo" and e.proto == "asserv" and e.name == "goTo":
            self.logger.info("En avant !")
            self.state = "goTo"
            self.create_timer(2000)
        elif self.state == "goTo" and e.proto == "internal" and e.name == "timeout":
            self.logger.info("Stop !")
            self.state = "repo"
            self.asserv.done()
