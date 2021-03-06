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
        self.robot      = None # initialized by dispatcher.py on mission loading
        self.dispatcher = None # initialized by dispatcher.py on mission loading

    def post_init(self):
        pass

    def _get_state(self):
        return self._state

    def _set_state(self, state):
        self.logger.info("[state] %s → %s" %(self._state, state))
        self._state = state

    state = property(_get_state, _set_state)

    def process_event(self, event):
        pass

    def create_timer(self, duration, timername=None):
        '''Cr un timer qui va envoyer un vnement Timer_end  la fin
        self.dispatch.add_event se termine immdiatement aprs l'ajout dans la queue
        donc le thread du Timer s'arrte aprs l'execution du add_event()
        donc il n'y a pas de problme d'execution concurrente entre le thread du timer
        et le dispatcher'''
        t = threading.Timer(duration/1000, self.dispatcher.add_event, \
                            [Event("internal", "timeout", {'timername':timername})])
        t.start()

    def create_event(self, proto, name, args = dict()):
        e = Event(proto, name, args)
        self.dispatcher.add_event(event)
    
    def send_event(self, event):
        self.dispatcher.add_event(event)
