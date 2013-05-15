from channel import Channel
import socket
import sys
from events.event import Event
from logging import getLogger
from settings import ATP_HOST
from comm.internal import InternalChannel

class Comm:

    def __init__(self, robot, **kwargs):

        self.logger = getLogger("comm.comm")

        self.robot = robot
        self._callback = None

        self.host = ATP_HOST

        for arg in kwargs:
            if arg == "host":
                self.host = kwargs[arg]

    def init(self):


        self.channels = dict()
        self.streams = dict()


        for device in self.robot.devices:
            sock = socket.socket()
            port = self.robot.devices[device]
            try:
                sock.connect((self.host, port))
            except:
                print("Failed to connect on %s:%d" % (self.host, port))
                sys.exit(-1)
            file = sock.makefile(mode="rw")
            stream = file.buffer
            channel = Channel(stream, lambda name, args, device = device: self.callback(device, name, args), proto = device, transmitter = self.robot.transmitter)
            self.channels[device] = channel
            self.streams[device] = (sock, file, stream)


        internal = InternalChannel(self.dispatcher)
        self.channels["internal"] = internal

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

    def set_dispatcher(self, dispatcher):
        self.dispatcher = dispatcher
