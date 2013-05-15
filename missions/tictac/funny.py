# -*-coding:UTF-8 -*

from missions.mission import Mission
from events.internal import InternalEvent

import time

class FunnyMission(Mission):

    def __init__(self):
        super().__init__(__name__)
    
    def process_event(self, e):
        if self.state == 0 and e.proto == "internal" and e.name == "startFunny":
            self.state = 2
            #self.send_event(InternalEvent("forward", dist=30*1e-2))
            self.mother.sortirPince()
            self.create_timer(90000, "finMatch") 
            
        
        elif self.state == 2 and e.proto == "internal" and e.name == "timeout" and e.args["timername"] == "finMatch":
            self.state = 3
            self.logger.debug("Starting funny")
            self.mother.FunnyAction()
            self.create_timer(7000, "finFunny")
            
        elif self.state == 3 and e.proto == "internal" and e.name == "timeout" and e.args["timername"] == "finFunny":
            self.logger.debug("Stop funny")
            self.mother.StopFunnyAction()
            self.state = 4
