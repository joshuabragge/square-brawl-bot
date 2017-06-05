from threading import *
import time
from game_functions.controller import button_mappings as bm

global guntwotimer
global gunonetimer
global onegunready
global twogunready

#gunonetimer = 0
#guntwotimer = 0

class Tread(object):

        def __init__(self):
            self.gunonetimer = 0
            self.guntwotimer = 0
            self.oneguncooling = False
            self.twoguncooling = False

        def __oneguncounter__(self, timer=4):
            # global gunonetimer
            # global onegunready
            while timer > -1:
                self.oneguncooling = True
                self.gunonetimer = timer
                time.sleep(1)
                timer = timer - 1
            self.oneguncooling = False

        def __twoguncounter__(self, timer=4):
            # global guntwotimer
            # global twogunready
            while timer > -1:
                self.twoguncooling = True
                self.guntwotimer = timer
                time.sleep(1)
                timer = timer - 1
            self.twoguncooling = False

        def guncounterone(self):
            onegun = Thread(target=self.__oneguncounter__, args=[bm.shotgun])
            onegun.start()

        def guncountertwo(self):
            twogun = Thread(target=self.__twoguncounter__, args=[bm.sniper])
            twogun.start()
