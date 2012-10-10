#-*- coding: utf-8 -*-

from comm.socket import Socket
from comm.atp import decode, encode

class Robot(Socket):

    def __init__(self, mail, host, port):
        super().__init__(mail, host, port)

    def run(self):
        self.socket.send(b'\x81\x05\x80')
        file = self.socket.makefile(buffering=1, errors='replace')
        decode(file.buffer, self.receive)

    def send(self, id, args):
        encode(buffer, id, args)

    def receive(self, id, args):
        print("[%d]" %id)
        for i in args:
            print("\t", i)
