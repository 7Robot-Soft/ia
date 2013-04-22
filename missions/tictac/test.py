from missions.mission import Mission

class TestMission(Mission):

    def __init__(self):
        super().__init__(__name__)
    
    def process_event(self, e):
        if self.state == 0 and e.proto == "internal" and e.name == "start":
            self.logger.info("C’est partie !")
            self.asserv.goTo(123, 23, 43)
            self.state = 1
        elif self.state == 1 and e.proto == "asserv" and e.name == "done":
            self.logger.info("On est arrivé !")
            self.state = 2
