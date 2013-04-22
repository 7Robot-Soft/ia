#-*- coding: utf-8 -*-

from dispatcher import Dispatcher
from comm.comm import Comm
from logging import getLogger

class IA:

    def __init__(self, name, **kargs):

        self.logger = getLogger("ia")

        module = __import__("robots."+name) # import robots.<name>
        self.robot = getattr(getattr(module, name), name.capitalize()+"Robot")() # create <Name>Robot
        self.comm = Comm(self.robot)
        self.dispatcher = Dispatcher(self.robot, self.comm)
        self.dispatcher.start()
        self.logger.info("IA started !")
        
        from events.internal import InternalEvent
        event = InternalEvent("start")
        self.dispatcher.add_event(event)
