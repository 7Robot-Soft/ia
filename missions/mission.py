# -*-coding:UTF-8 -*

import logging
import threading

from events.event import Event

class Mission:
    def __init__(self):
        self._state = 0

    @property
    def state(self):
        return self._state

    @state.setter
    def _set_state(self, state):
        print("[state] %s -> %s" %(self._state, state))
        self._state = state

    def process_event(self, event):
        pass

    def create_timer(self, duration, timername="Timer"):
        '''Cr un timer qui va envoyer un vnement Timer_end  la fin
        self.dispatch.add_event se termine immdiatement aprs l'ajout dans la queue
        donc le thread du Timer s'arrte aprs l'execution du add_event()
        donc il n'y a pas de problme d'execution concurrente entre le thread du timer
        et le dispatcher'''
        t = threading.Timer(duration/1000, self.dispatch.add_event, \
                            [Event("timer", "timeout", self, **{'timername':timername})])
        t.start()
