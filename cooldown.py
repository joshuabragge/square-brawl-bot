from threading import *
import time
import buttonmap as bm

global guntwotimer
global gunonetimer
global onegunready
global twogunready

gunonetimer = 0
guntwotimer = 0
onegunready = True
twoguready = True

class Tread(object):

        def __init__(self):
            pass

        def __oneguncounter__(self, timer=4):
            global gunonetimer
            while timer >= 0:
                gunonetimer = timer
                time.sleep(1)
                timer = timer - 1
                print(timer)
            global onegunready
            onegunready = True

        def __twoguncounter__(self, timer=4):
            global guntwotimer
            while timer >= 0:
                guntwotimer = timer
                time.sleep(1)
                timer = timer - 1
                print(timer)
            global twogunready
            twoguready = True

        def guncounterone(self):
            onegun = Thread(target=self.__oneguncounter__, args=[bm.shotgun])
            onegun.start()

        def guncountertwo(self):
            twogun = Thread(target=self.__twoguncounter__, args=[bm.sniper])
            twogun.start()
