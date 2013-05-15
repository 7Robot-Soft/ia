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

SREPOS = 0
SPAUSING = 1
SPAUSED = 2
SRUN = 3
SDONE = 4

# Les états SPAUSED et SREPOS pourraient être mergés

class SpeedMission(Mission):
    '''
    Voir schéma papier, run2 non implémenté (changement de seuil après fin accélération)
    
    Lancer cette mission avec un internal event name="forward", args[dist"]
    
    A la fin de la mission, un internal event name="forwardDone" est dispatché
    '''

    def __init__(self):
        super().__init__(__name__)
        self.vit = 0 # distance à parcourir

    
    # Mission à copier/coller pour : setVit    
    #~ def speedToThreshold(self, speed):
        #~ '''Définit le seuil à setter sur les SICKS pour s'arrếter à temps'''
        #~ # Exemple de fonctionnement, valeurs à l'arrache
        #~ if speed > 0.7:
            #~ return 0
        #~ elif speed > 0.4:
            #~ return 4
        #~ elif speed > 0.2:
            #~ return 6
        #~ else:
            #~ return 10

    def voie_libre(self):
       # C'est plus simple de prendre la valeur précédente, sinon rajouter un état
       voielibre = self.missions["sensor"].sensorMinValue < 2
       return voielibre
        
    def process_event(self, e):
        if self.state == SREPOS:
            # lancement de cette mission
            # On récupère la pos init
            if e.proto == "internal" and e.name == "speed":
                # Init et on demande où on est
                self.vit = e.args["speed"]
                # On indique notre sens
                if self.vit > 0:
                    self.send_event(InternalEvent("goForward"))
                else:
                    self.send_event(InternalEvent("goBackward"))
                
                
                # on part que si la voie est libre et on lit notre position
            
                if self.voie_libre():
                    # On avance
                    self.state = SRUN
                    self.asserv.setVit(self.vit)
                else:
                    self.state = SPAUSED
                
                    
        elif self.state == SRUN:
            # Seuil dépassé
            if e.proto == "internal" and e.name == "sensor" and e.args["value"] >= 2:
                self.state = SPAUSING
                self.asserv.stop()
                
        elif self.state == SPAUSING:
            if e.proto == "asserv" and e.name == "done":
                self.state = SPAUSED
                self.asserv.getPos()
                
            elif e.proto == "internal" and e.name == "sensor" and e.args["value"] >= 2:
                # en faite plus besoin de d'arrêter, mais wait, on n'est pas encore arrêté
                # on reprend
                self.logger.debug("On repart from SPAUSING")
                # On repart (duplicate)
                self.asserv.setVit(self.vit)
                
        elif self.state == SPAUSED:
            if e.proto == "internal" and e.name == "sensor" and e.args["value"]  < 2:
                # Il n'y a plus personne, on repart
                self.state = SRUN
                self.logger.debug("On repart from SPAUSED")
                self.asserv.setVit(self.vit)
                
