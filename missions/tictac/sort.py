# -*-coding:UTF-8 -*

from missions.mission import Mission
from events.internal import InternalEvent
from math import pi

class Sort1Mission(Mission):
    """
    On sort, et on va taper dans les verres
    
    76cm entre 2
    """
    
    # dist1 = 0.63
    # chope1
    # timer
    # dist2 = 0.3
    # chope2
    # timer
    # dist3 = 0.170
    # angle = -1.57
    # dist4 = 330
    # chope3
    # timer
    # dist5 = 170
    # angle = -1.57
    # dist  = 0.13
    # chope4
    # timer
    # angle = -45°
    # dist = 950
    # depose

    def __init__(self):
        super().__init__(__name__)
    
    def process_event(self, e):
        if self.state == 0 and e.proto == "internal" and e.name == "sort1Start":
            # ON avance de 0.73m
            self.state = 1
            self.send_event(InternalEvent("forward", dist=0.63))
            
        elif self.state == 1 and e.proto == "internal" and e.name == "forwardDone":
            # On choppe un verre
            self.mother.chopperVerre()
            self.create_timer(9, "pince1")
            self.state = 2
            
        elif self.state == 2 and e.proto == "internal" and e.name == "timeout" and e.args["timername"] == "pince1":
            self.send_event(InternalEvent("forward", dist=0.3))
            self.state = 3
            
        elif self.state == 3 and e.proto == "internal" and e.name == "fowardDone":
            # on choppe un 2e verre
            self.mother.chopperVerre()
            self.create_timer(9, "pince2")
            self.state = 4
            
        elif self.state == 4 and e.proto == "internal" and e.name == "timeout" and e.args["timername"] == "pince2":
            # On continue
            self.send_event(InternalEvent("forward", dist=0.17))
            self.state = 5
       
            
        elif self.state == 5 and e.proto == "internal" and e.name == "forwardDone":
            # on tourne
            self.asserv.rot(-1.57)
            self.state = 6
            
        elif self.state == 6 and e.proto == "asserv" and e.name == "done":
            self.send_event(InternalEvent("forward", dist=0.33))
            self.state = 7
            
        elif self.state == 7 and e.proto == "internal" and e.name == "forwardDone":
            # On choppe un 3e verre
            self.mother.chopperVerre()
            self.create_timer(9, "pince3")
            self.state = 8
            
        elif self.state == 8 and e.proto == "internal" and e.name == "timeout" and e.args["timername"] == "pince3":
            self.send_event(InternalEvent("forward", dist=0.17))
            self.state = 9
        
            
        elif self.state == 9 and e.proto == "internal" and e.name == "forwardDone":
            # on tourne
            self.asserv.rot(3.14)
            self.state = 10
            
        elif self.state == 10 and e.proto == "asserv" and e.name == "done":
            self.send_event(InternalEvent("forward", dist=0.13))
            self.state = 11
            
        elif self.state == 11 and e.proto == "internal" and e.name == "fowardDone":
            # on choppe un 4e verre
            self.mother.chopperVerre()
            self.create_timer(9, "pince4")
            self.state = 12
            
        elif self.state == 12 and e.proto == "internal" and e.name == "timeout" and e.args["timername"] == "pince4":
            # On continue
            self.asserv.rot(3*pi/4)
            self.state = 13
            
        elif self.state == 13 and e.proto == "asserv" and e.name == "done":
            self.send_event(InternalEvent("forward", dist=0.95))
            self.state = 14
        
            
        elif self.state == 14 and e.proto == "internal" and e.name == "forwardDone":
            self.mother.lacherVerres()
            
