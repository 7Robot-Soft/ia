# -*-coding:UTF-8 -*

from missions.mission import Mission
from events.internal import InternalEvent


class TestMission(Mission):
    """
    Events reçus : 
        - InternalEvent("goForward") pour savoir dans quelle sens on roule
        - Sensor()
            
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
        self._sensorMaxValue =  -1   # Valeur max de tous les capteurs
        self._goForward      = True # on avance ou on recule, pb d'inspiration
        
    def post_init(self):
        # on peu pas le faire dans __init__(), on a pas encore l'attribut robot
        # Init valeur du sensor avant gauche à la valeur max
        self._sensors[self.robot.sensor_id_front_left]  = 10 
        self._sensors[self.robot.sensor_id_front_right] = 10 # init ...
        self._sensors[self.robot.sensor_id_back]        = 10 # init ...

    
    def process_event(self, e):
        if   e.proto == "internal" and e.name == "goForward":
            self._goForward = True
            self._sensorMaxValue = max(self._sensors[self.robot.sensor_id_front_left], self._sensors[self.robot.sensor_id_front_right])
        elif e.proto == "internal" and e.name == "goBackward":
            self.goForward = False
            self._sensorMaxValue = self._sensors[self.robot.sensor_id_back]
        elif e.proto == "sensor"   and e.name == "value":
            self._sensors[e.args["id"]] = e.args["value"]
            # On considère que les capteurs  placés du côté où on avanceS
            if self._goForward and (e.args["id"] == self.robot.sensor_id_front_left or e.args["id"] == self.robot.sensor_id_front_right) \
                or self._goForward and (e.args["id"] == self.robot.sensor_id_back):
                if e.args["value"] > self._sensorMaxValue:
                    self._sensorMaxValue = e.args["value"]
                    self.send_event(InternalEvent("Sensor", value=self._sensorMaxValue))
