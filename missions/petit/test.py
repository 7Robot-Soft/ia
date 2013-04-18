from missions.mission import Mission

class TestMission(Mission):

    def __init__(self):
        super().__init__()
    
    def process_event(self, e):
        print(e)
        if e.proto == "asserv" and e.name == "pos":
            print(e.x, e.y)
            self.asserv.getPos()
