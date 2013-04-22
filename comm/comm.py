import sys
sys.path.append("../atp/")
from channel import Channel
import socket
from events.event import Event
from logging import getLogger
from settings import ATP_HOST

class Comm:

    def __init__(self, robot, **kwargs):

        self.logger = getLogger("comm.comm")

        self.robot = robot
        self._callback = None

        host = ATP_HOST

        for arg in kwargs:
            if arg == "callback":
                self._callback = kwargs[arg]
            elif arg == "host":
                host = kwargs[arg]

        self.channels = dict()
        self.streams = dict()


        for device in self.robot.devices:
            sock = socket.socket()
            port = self.robot.devices[device]
            sock.connect((host, port))
            file = sock.makefile(mode="rw")
            stream = file.buffer
            channel = Channel(stream, lambda name, args, device = device: self.callback(device, name, args), proto = device, transmitter = self.robot.transmitter)
            self.channels[device] = channel
            self.streams[device] = (sock, file, stream)

    def callback(self, proto, name, args):
        if self._callback == None:
            self.logger.info("[%s.%s]" %(proto, name))
            for arg in args:
                self.logger.info("\t%s:" %arg, args[arg])
        else:
            event = Event(proto, name, args)
            self._callback(event)

    def set_callback(self, callback):
        self._callback = callback
