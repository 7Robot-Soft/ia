from threading import Thread
import os
from tools.class_manager import class_loader
import missions
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
        self._load_all_missions(robot.name)

    def _load_all_missions(self, prefix):
        path = os.path.join(os.getcwd(), "missions", prefix)
        missions = set(class_loader(path))
        self.missions = []
        for mission in missions:
            if mission.__name__ != "mission":
                self.logger.info("Load: %s" %mission.__name__)
                m = mission()
                m.robot = self.robot
                for channel in self.comm.channels:
                    setattr(m, channel, self.comm.channels[channel])
                self.missions += [m]

    def add_event(self, event):
        self.queue.put(event, True, None)

    def run(self):
        while True:
            event = self.queue.get(True, None)
            for mission in self.missions:
                mission.process_event(event)

