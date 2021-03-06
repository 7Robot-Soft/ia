# -*-coding:UTF-8 -*
from threading import Thread
import os
from tools.class_manager import class_loader
from missions.mission import Mission
from queue import Queue
from logging import getLogger

class Dispatcher(Thread):

    def __init__(self, robot, comm):
        Thread.__init__(self)
        self.logger = getLogger("dispatcher")
        self.robot = robot
        self.queue = Queue()
        self.comm = comm
        self.comm.set_callback(self.add_event)
        self.comm.set_dispatcher(self)
        self.comm.init()
        self.logger.info("Loading missions…")
        self._load_all_missions('common')
        self._load_all_missions(robot.name)
        self.logger.info("All missions loaded !")

    def _load_all_missions(self, prefix):
        path = os.path.join(os.getcwd(), "missions", prefix)
        missions = set(class_loader(path))
        self.missions = []
        for mission in missions:
            if mission.__name__ != "Mission" and issubclass(mission, Mission):
                m = mission()
                m.robot = self.robot # proposition, on passe le robot en argument du constructeur
                m.dispatcher = self  # même proposition
                m.post_init()
                for channel in self.comm.channels:
                    setattr(m, channel, self.comm.channels[channel])
                self.missions += [m]
                self.logger.info("%s loaded" %mission.__name__)

    def add_event(self, event):
        self.queue.put(event, True, None)

    def symmetrical(self, sym):
        for channel in self.comm.channels:
            channel._symmetrical = sym

    def run(self):
        while True:
            event = self.queue.get(True, None)
            if self.robot.inverted:
                self.invert(event)
            self.logger.info("Dispatch event %s(%s)" %(event.proto, event.name))
            if event.dests == []:
                for mission in self.missions:
                    mission.process_event(event)
            else:
                for mission in event.dests:
                    mission.process_event(event)

