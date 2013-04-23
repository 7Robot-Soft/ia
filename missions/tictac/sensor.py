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
            
    Préconditions :
        - la classe Robot utilisée déclare les attributs sensor_id_front/back_left/right
    """

    def __init__(self):
        super().__init__(__name__)
        # Liste des dernières valeurs des capteurs.
        # Dico car on connait pas à l'avance les id
        self.sensors        = {}
        self.sensorMaxValue =  -1   # Valeur max de tous les capteurs
        # FIXME: si on avance il faut que ça soit la valeur max des capteurs à l'avant (et pas le max de tous les capteurs), si on recule ...
        self.goForward      = True # on avance ou on recule, pb d'inspiration
        
    def post_init(self):
        # on peu pas le faire dans __init__(), on a pas encore setté l'attribut robot
        self.sensors[self.robot.sensor_id_front_left]  = 10 # init valeur du sensor avant gauche à la valeur max
        self.sensors[self.robot.sensor_id_front_right] = 10 # init ...
        self.sensors[self.robot.sensor_id_back]        = 10 # init ...

    
    def process_event(self, e):
        if   e.proto == "internal" and e.name == "goForward":
            self.goForward = True
            self.sensorMaxValue = max(self.sensors[self.robot.sensor_id_front_left], self.sensors[self.robot.sensor_id_front_right])
        elif e.proto == "internal" and e.name == "goBackward":
            self.goForward = False
            self.sensorMaxValue = self.sensors[self.robot.sensor_id_back]
        elif e.proto == "sensor"   and e.name == "value":
            self.sensors[e.args["id"]] = e.args["value"]
            # On considère que les capteurs  placés du côté où on avanceS
            if self.goForward and (e.args["id"] == self.robot.sensor_id_front_left or e.args["id"] == self.robot.sensor_id_front_right) \
                or self.goForward and (e.args["id"] == self.robot.sensor_id_back):
                if e.args["value"] > self.sensorMaxValue or self.sensorMaxValue == -1:
                    self.sensorMaxValue = e.args["value"]
                    self.send_event(InternalEvent("Sensor", value=self.sensorMaxValue))
