#-*- coding: utf-8 -*-

import socket
from comm.comm import Comm

class Socket(Comm):

    def __init__(self, mail, host, port):
        super().__init__(mail)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))

    def stop(self):
        self.socket.shutdown(socket.SHUT_WR)
        self.socket.close()
        super().stop()
