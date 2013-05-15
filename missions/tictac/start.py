# -*-coding:UTF-8 -*

from missions.mission import Mission
from events.internal import InternalEvent


class StartMission(Mission):

    def __init__(self):
        super().__init__(__name__)
    
    def process_event(self, e):
        if self.state == 0 and e.proto == "internal" and e.name == "start":
            self.state = 2
            self.asserv.setDistLimits(0.12, 0.12, 5)
            self.asserv.setDistLimits(0.12, 0.12, 5)
            self.asserv.setOdoX(0)
            self.asserv.setOdoY(0)
            self.asserv.setOdoTheta(0)
            
            self.turret.on()
            
        # Si switch2, alors commencer le recalage après timer
            
        ##if self.state == 2 and e.proto == "mother" and e.name == "StartLaisseState" and e.args["state"] == 0:
            # On déploie la pince
            #self.asserv.SICKChangeOn()
            #~ self.asserv.SICKFloodOn()
            self.mother.sortirPince()
            
            # Lance la mission funny (qui commence dans 90 min)
            #self.send_event(InternalEvent("startFunny"))
            
            
            #~ self.internal.positioning()
            #~ self.send_event(InternalEvent("forward", dist=3000*1e-2))
            self.send_event(InternalEvent("forward", dist=2.5))
            #self.send_event(InternalEvent("sort1Start"))
            
        #~ if self.state == 1 and e.proto == "internal" and e.name == "positionned":
            #~ self.state = 2
            #~ self.send_event(InternalEvent("forward", dist=1))
            
        
            
        
        
        # TODO: vérifier le state == 1 pour laisse retirée
        
            
