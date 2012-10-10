#-*- coding: utf-8 -*-

from threading import Thread, Event

class Comm(Thread):

    def __init__(self, mail):
        Thread.__init__(self)
        self.running = Event()
        self.mail = mail

    def run(self):
        pass

    def notify(self):
        pass

    def stop(self):
        self.running.set()
