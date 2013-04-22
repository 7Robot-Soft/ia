# -*-coding:UTF-8 -*

from missions.mission import Mission
from events.internal import InternalEvent

class TestMission(Mission):
    """
    Events reçus : 
            - InternalEvent("goForward") pour savoir dans quelle sens on roule
            - Sensor()
            
    Events envoyés :
            - Internal("sensor") envoie la valeur max de tous les capteurs situés du côté où on avance
    """

    def __init__(self):
        super().__init__(__name__)
        # Liste des dernières valeurs des capteurs.
        # Dico car on connait pas à l'avance les id
        self.sensors        = {}
        self.sensorMaxValue =  0   # Valeur max de tous les capteurs
        # FIXME: si on avance il faut que ça soit la valeur max des capteurs à l'avant (et pas le max de tous les capteurs), si on recule ...
        self.goForward      = True # on avance ou on recule, pb d'inspiration

    
    def process_event(self, e):
        if   e.proto == "internal" and e.name == "goForward":
            self.goForward = True
        elif e.proto == "internal" and e.name == "goBackward":
            self.goForward = False
        elif e.proto == "sensor"   and e.name == "value":
            self.sensors[e.args["id"]] = e.args["value"]
            if e.args["value"] > self.sensorMaxValue:
                self.sensorMaxValue = e.args["value"]
                self.send_event(InternalEvent("Sensor", value=self.sensorMaxValue))
            
