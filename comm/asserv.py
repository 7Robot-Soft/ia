#-*- coding: utf-8 -*-

from comm.robot import Robot

class Asserv(Robot):

    def __init__(self, mail, host, port):
        super().__init__(mail, host, port)

    def receive(self, id, args):
        pass
