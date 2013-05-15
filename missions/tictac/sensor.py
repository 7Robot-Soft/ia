# -*-coding:UTF-8 -*

from missions.mission import Mission
from events.internal import InternalEvent

# TODO : gérer la carte IR

class SensorMission(Mission):
    """
    Events reçus : 
        - InternalEvent("goForward") pour savoir dans quelle sens on roule
        - Asserv.SICKValue : valeurs (près) 0 1 2 3 4 5 6 6 7 8 9(loin) (oui, j'ai changé la convention initiale définie fin Mars)
            
    Events envoyés :
        - Internal("sensor") envoie la valeur max de tous les capteurs situés 
        du côté où on avance
            
    Préconditions :
        - la classe Robot utilisée déclare les attributs 
        sensor_id_front/back_left/right
    """

    def __init__(self):
        super().__init__(__name__)
        # Liste des dernières valeurs des capteurs.
        # Dico car on connait pas à l'avance les id
        self._sensors        = {}
        self._tsops          = {}
        self.sensorMaxValue  =  0   # Valeur max de tous les capteurs
        self._goForward      = True # on avance ou on recule, pb d'inspiration
        self.threshold       = 0
        self.range           = "over"
        
    def post_init(self):
        # on peu pas le faire dans __init__(), on a pas encore l'attribut robot
        # Init valeur du sensor avant gauche à la valeur max
        self._sensors[self.robot.sensor_id_front_left]  = [10,10,10,10,10] 
        self._sensors[self.robot.sensor_id_front_right] = [10,10,10,10,10] # init ...
        self._sensors[self.robot.sensor_id_back]        = [0,0,0,0,0] # init ...
        for i in range(16):
            self._tsops[i] = 0

    
    def process_event(self, e):
        # Changement du seuil (OBSOLETE)
        if e.proto == "internal" and e.name == "setThreshold":
            self.threshold = e.args["threshold"]
            # Mise à jour du range
            if self.sensorMaxValue < self.threshold:
                self.range = "over"
            else:
                self.range = "under"
                
        # On nous préviens que l'on avance
        elif   e.proto == "internal" and e.name == "goForward":
            self._goForward = True
            self.logger.debug("Go forward !!")
            # ou min() selon convention
            #~ self.sensorMaxValue = max(0.2*sum(self._sensors[self.robot.sensor_id_front_left]), 0.2*sum(self._sensors[self.robot.sensor_id_front_right]))
            self.sensorMaxValue = 10
        
        # On nous prévient qu'on recule
        elif e.proto == "internal" and e.name == "goBackward":
            self.logger.debug("Go backward !!")
            self._goForward = False
            self.sensorMaxValue = 10
            #~ self.sensorMaxValue = self._sensors[self.robot.sensor_id_back]
      
        # Event capteur
        #~ elif e.proto == "asserv"   and e.name == "SICKValue":
            #~ self._sensors[e.args["id"]].insert(0,e.args["value"])
            #~ self._sensors[e.args["id"]].pop()
            # On considère que les capteurs  placés du côté où on avanceS
            #~ if self._goForward and (e.args["id"] == self.robot.sensor_id_front_left or e.args["id"] == self.robot.sensor_id_front_right) \
                #~ or not self._goForward and (e.args["id"] == self.robot.sensor_id_back):
                    #~ 
                #~ # REFACTORER
                #~ if self._goForward:
                    #~ sensorMaxValue = max(0.2*sum(self._sensors[self.robot.sensor_id_front_left]), 0.2*sum(self._sensors[self.robot.sensor_id_front_right]))
                #~ else:
                    #~ sensorMaxValue = 0.2*sum(self._sensors[self.robot.sensor_id_back])
                    #~ 
                #~ print ("SICK", sensorMaxValue)
                #~ if sensorMaxValue != self.sensorMaxValue:
                    #~ self.logger.debug("New max value (sick) %d" % sensorMaxValue)
                    #~ self.sensorMaxValue = sensorMaxValue
                    #~ self.send_event(InternalEvent("sensor", value=self.sensorMaxValue))
                    #~ 
                    #~ # Détection de changement de seuils
                    #~ if self.sensorMaxValue > self.threshold and self.range == "under":
                        #~ self.range = "over"
                        #~ self.send_event(InternalEvent("sensorRange", range=self.range))
                    #~ elif self.sensorMaxValue < self.threshold and self.range == "over":
                        #~ self.range = "under"
                        #~ self.send_event(InternalEvent("sensorRange", range=self.range))
                        
        elif e.proto == "turret" and e.name == "pos":
            #self.logger.info("turret (%d) %d" % (e.args["angle"], e.args["distance"]) )
            
            if e.args["distance"] > 5:
                # faut s'arrêter si le danger vient dans notre sens de parcours
                if 10 <= e.args["angle"] and e.args["angle"] <= 14 and self._goForward:
                    # on avance, danger devant
                    val = 5
                elif 2 <= e.args["angle"] and e.args["angle"] <= 6 and (not self._goForward):
                    # on recule, danger sur l'arrière
                    val = 5
                else:
                    # le danger est à droite ou gauche
                    val = 0
            else:
                # pas de danger
                val = 0
            self.send_event(InternalEvent("sensor", value=val))
            self.logger.info("Value %d" % val)
            #~ if (10 <= e.args["angle"] and e.args["angle"] <= 14 and self._goForward)  or  (2 <= e.args["angle"] and e.args["angle"] <= 6 and not self._goForward):
                #~ self._tsops[e.args["angle"]] = e.args["distance"]
                #~ if self._goForward:
                    #~ sensorMaxValue = max(self._tsops[10], self._tsops[11], self._tsops[12], self._tsops[13], self._tsops[14])
                #~ else:
                    #~ sensorMaxValue = max(self._tsops[2], self._tsops[3], self._tsops[4], self._tsops[5], self._tsops[6])
                #~ 
                #~ self.logger.info("New max value (turret) %d" % sensorMaxValue)
                #~ self.sensorMaxValue = sensorMaxValue
                #~ self.send_event(InternalEvent("sensor", value=self.sensorMaxValue))
                    
                
            
            
