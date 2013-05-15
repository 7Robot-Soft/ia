# -*-coding:UTF-8 -*

from missions.mission import Mission
from events.internal import InternalEvent
from math import pi
from mathutils.types import Vertex


SRECULE1 = 1
SWAIT1 = 2
SSTOP1 = 3
SAVANCE1 = 4
STOURNE1 = 5
SRECULE2 = 6
SWAIT2 = 7
SSTOP2 = 8
SAVANCE2 = 9


# REGLER LES DISTANCES !!!


class PositioningMission(Mission):

    def __init__(self):
        super().__init__(__name__)
    
    def process_event(self, e):
        if self.state == 0 and e.proto == "internal" and e.name == "positioning":
            # On démarre le recalage
            # On désactive les SICs ?
            #on recule1
            self.asserv.setOdoXYTheta(0,0.8-self.robot.dimensions["back"], -pi/2)
            self.asserv.setVit(-.15)
            #self.state = SRECULE1
            self.state = SWAIT1
            self.create_timer(5000, "recalage_y")
            
        #elif self.state == SRECULE1 and e.proto == "asserv" and e.name == "backBumperState":
        #    # on attend (recalage)
        #    self.create_timer(2, "recalage")
        #    self.state = SWAIT1
            
        elif self.state == SWAIT1 and e.proto == "internal" and e.name == "timeout" and e.args["timername"] == "recalage_y":
            # On s'arrête
            self.state = SSTOP1
            self.asserv.free()
            
        elif self.state == SSTOP1 and e.proto == "asserv" and e.name == "done":
            # Set odo, avance
            #self.asserv.setOdoX = 0 # x=0
            #self.asserv.setDist(0.2)
            self.asserv.setOdoXYTheta(0,1-self.robot.dimensions["back"], -pi/2)
            self.asserv.setPos(0, 0)
            self.state = SAVANCE1

        elif self.state == SAVANCE1 and e.proto == "asserv" and e.name == "done":
            # rotation -90
            self.asserv.setAngle(0)
            self.state = STOURNE1
            
        elif self.state == STOURNE1 and e.proto == "asserv" and e.name == "done":
            # on recule 2
            self.asserv.setVit(-.15)
            self.create_timer(5000, "recalage_x")
            #self.state = SRECULE2
            self.state = SWAIT2
            
        #elif self.state == SRECULE2 and e.proto == "asserv" and e.name == "backBumperState":
        #    # on attend (recalage)
        #    self.create_timer(2, "recalage2")
        #    self.state = SWAIT2
            
        elif self.state == SWAIT2 and e.proto == "internal" and e.name == "timeout" and e.args["timername"] == "recalage_x":
            # stop
            self.asserv.free()
            self.state = SSTOP2
            
        elif self.state == SSTOP2 and e.proto == "asserv" and e.name == "done":
            # Set odo, avance
            self.asserv.setOdoXTheta(-1.5+self.robot.dimensions["back"],0)
            self.robot.pos = Vertex(-1.5+self.robot.dimensions["back"], 0)
            self.logger.info("J'ai fini, bordel je fais quoi ?")
            self.state = -1
            self.internal.positionned()
            #self.asserv.setDist(0.05)
            #self.state = SAVANCE2

        #elif self.state == SAVANCE2 and e.proto == "asserv" and e.name == "done":
        #    self.logger.info("J'ai fini, bordel je fais quoi ?")
