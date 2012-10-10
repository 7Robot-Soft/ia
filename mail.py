#-*- coding: utf-8 -*-

from comm.asserv import Asserv
from comm.captor import Captor

class Mail:

    def __init__(self):

        host = "localhost"
        asserv = Asserv(self, host, 1300)
        captor = Captor(self, host, 1301)
