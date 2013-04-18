import sys
sys.path.append("../atp/")
from channel import Channel
import socket
from events.event import Event

class Comm:

    def __init__(self, robot, callback = None):

        self.robot = robot
        self._callback = callback

        self.channels = dict()
        self.streams = dict()

        host = "localhost"

        for device in self.robot.devices:
            sock = socket.socket()
            port = self.robot.devices[device]
            sock.connect((host, port))
            file = sock.makefile(mode="rw")
            stream = file.buffer
            channel = Channel(stream, lambda name, args: self.callback(device, name, args), proto = device)
            self.channels[device] = channel
            self.streams[device] = (sock, file, stream)

    def callback(self, proto, name, args):
        if self._callback == None:
            print("[%s.%s]" %(proto, name))
            for arg in args:
                print("\t%s:" %arg, args[arg])
        else:
            event = Event(proto, name, args)
            self._callback(event)

    def set_callback(self, callback):
        self._callback = callback
