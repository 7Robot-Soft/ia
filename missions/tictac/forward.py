# -*- coding: utf-8 -*-
'''
Created on 5 mai 2012

Liste des tats :
    repos
    forwarding
    pausing
    waiting
    stopping
'''

from missions.mission import Mission
from events.internal import InternalEvent


from mathutils.types import Vertex
from math import cos, sin, pi, copysign

from time import sleep

SREPOS = 0
SPAUSING = 1
SPOS = 1.5
SPAUSED = 2
SPAUSED2 = 2.5
SPOS2 = 2.8
SRUN = 3
SDONE = 4

# Les états SPAUSED et SREPOS pourraient être mergés

class ForwardMission(Mission):
    '''
    Voir schéma papier, run2 non implémenté (changement de seuil après fin accélération)
    
    Lancer cette mission avec un internal event name="forward", args[dist"]
    
    A la fin de la mission, un internal event name="forwardDone" est dispatché
    '''

    def __init__(self):
        super().__init__(__name__)
        self._distance_parcourue = 0
        self._last_pos = Vertex(0,0)
        self.dist = 0 # distance à parcourir

    

    def voie_libre(self):
       # C'est plus simple de prendre la valeur précédente, sinon rajouter un état
       voielibre = self.missions["sensor"].sensorMaxValue <= 2
       return voielibre
        
    def process_event(self, e):
        if self.state == SREPOS:
            # lancement de cette mission
            # On récupère la pos init
            if e.proto == "internal" and e.name == "forward":
                # Init, on dit notre sens  et on demande où on est
                self.dist = e.args["dist"]
                if self.dist > 0:
                    self.send_event(InternalEvent("goForward"))
                else:
                    self.send_event(InternalEvent("goBackward"))
                self.asserv.getPos()
                self.state = SPOS
            # on part que si la voie est libre et on lit notre position
        if self.state == SPOS:
            if e.proto == "asserv" and e.name == "pos":
                self._last_pos = Vertex(e.args["x"], e.args["y"])
                if True:# self.voie_libre(): # FIXME
                    # On avance
                    self.state = SRUN
                    self.logger.info("On re avance")
                    self.asserv.dist(self.dist)
                else:
                    self.state = SPAUSED
                
                    
        elif self.state == SRUN:
            if e.proto == "asserv" and e.name == "done":
                self.state = SDONE
                self.send_event(InternalEvent("forwardDone"))
                self.state = SREPOS
                sleep(1)
            # Seuil dépassé
            if e.proto == "internal" and e.name == "sensor" and e.args["value"] > 2:
                self.state = SPAUSING
                self.asserv.pause()
                
        elif self.state == SPAUSING:
            if e.proto == "asserv" and e.name == "done":
                sleep(1)
                self.state = SPAUSED
                self.asserv.getPos()
                
            elif e.proto == "internal" and e.name == "sensor" and e.args["value"]  <= 2:
                # en faite plus besoin de d'arrêter, mais wait, on n'est pas encore arrêté
                # on reprend
                self.logger.debug("On repart from SPAUSING")
                self.asserv.getPos()
                self.state = SPOS2
        if self.state == SPOS2:
            if e.proto == "asserv" and e.name == "pos":
                # On repart (duplicate)
                current_pos = Vertex(e.args["x"], e.args["y"])
                print("iiiii")
                print(current_pos)
                print(self._last_pos)
                self._distance_parcourue += (current_pos-self._last_pos).norm()
                self._last_pos = current_pos
                self.logger.debug("PARCOURU")
                self.logger.debug(self._distance_parcourue)
                self.logger.debug("reste à parcourir")
                self.logger.debug(self.dist-self._distance_parcourue)
                self.asserv.dist(max(0,self.dist-self._distance_parcourue))
                self.state = SRUN
                
        elif self.state == SPAUSED:
            if e.proto == "internal" and e.name == "sensor" and e.args["value"]  <= 2:
                # Il n'y a plus personne
                self.state = SPAUSED2
                self.logger.debug("On repart from SPAUSED")
                self.asserv.getPos()
                # Calcul de la distance parcourue
        elif self.state == SPAUSED2:
            if e.proto == "asserv" and e.name == "pos":
                # On repart (duplicate)
                current_pos = Vertex(e.args["x"], e.args["y"])
                self.logger.info(e.args["x"])
                self.logger.info(e.args["y"])
                print("iiiii")
                print(current_pos)
                print(self._last_pos)
                self._distance_parcourue += (current_pos-self._last_pos).norm()
                self._last_pos = current_pos
                self.logger.debug("PARCOURU")
                self.logger.debug(self._distance_parcourue)
                self.logger.debug("reste à parcourir")
                self.logger.debug(self.dist-self._distance_parcourue)
                self.asserv.dist(max(0,self.dist-self._distance_parcourue))
                self.state = SRUN
                
