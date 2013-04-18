#-*- coding: utf-8 -*-

from dispatcher import Dispatcher
from comm.comm import Comm

class IA:

    def __init__(self, name, **kargs):

        module = __import__("robots."+name) # import robots.<name>
        self.robot = getattr(getattr(module, name), name.capitalize()+"Robot")() # create <Name>Robot
        self.comm = Comm(self.robot)
        self.dispatcher = Dispatcher(self.robot, self.comm)
        self.dispatcher.start()
