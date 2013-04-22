# -*-coding:UTF-8 -*

import logging
import threading

from events.event import Event
from logging import getLogger

class Mission:
    def __init__(self, name):
        self._state = 0
        self._name = name
        self.logger = getLogger(name)

    def _get_state(self):
        return self._state

    def _set_state(self, state):
        self.logger.info("[state] %s → %s" %(self._state, state))
        self._state = state

    state = property(_get_state, _set_state)

    def process_event(self, event):
        pass

    def create_timer(self, duration, timername="Timer"):
        '''Cr un timer qui va envoyer un vnement Timer_end  la fin
        self.dispatch.add_event se termine immdiatement aprs l'ajout dans la queue
        donc le thread du Timer s'arrte aprs l'execution du add_event()
        donc il n'y a pas de problme d'execution concurrente entre le thread du timer
        et le dispatcher'''
        t = threading.Timer(duration/1000, self.dispatcher.add_event, \
                            [Event("internal", "timer", self, **{'timername':timername})])
        t.start()
