from missions.mission import Mission

class AsservMission(Mission):

    def __init__(self):
        super().__init__(__name__)
    
    def post_init(self):
        self.pos = self.robot.pos
        self.rot = self.robot.rot

    def process_event(self, e):
        if e.proto == "asserv" and e.name == "getId":
            self.asserv.id(5)
        elif e.proto == "sensor" and e.name == "getId":
            self.sensor.id(2)
        elif self.state == 0 and e.proto == "asserv" and e.name == "goTo":
            self.logger.info("En avant !")
            self.state = 1
            self.create_timer(1000)
        elif self.state == 1 and e.proto == "internal" and e.name == "timer":
            self.logger.info("Stop !")
            self.asserv.done()
            self.state = 2
