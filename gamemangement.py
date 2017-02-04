import time
from pywinauto.application import Application
import buttonmap as bm
import locations


def launch_game(delay=5):
    x360 = Application().Start(cmd_line=locations.x360dir)
    time.sleep(delay)
    x360.Kill_()

    game = Application().Start(cmd_line=locations.gamedir)
    gwindow = game.Dialog
    gwindow.Wait('ready')
    button = gwindow[u'Play!']
    button.Click()
    #time.sleep(delay)

def start_game(vj_mselect, botsOn=False, mode='easy'):
    sleeping = 1
    if botsOn:
        #turn bot on#
        time.sleep(sleeping)
        vj_mselect(direction='right',button=bm.none)
        time.sleep(sleeping)
        vj_mselect(direction='down',button=bm.none)
        time.sleep(sleeping)
        #vj_mselect 1 player
        vj_mselect(direction='left',button=bm.none)
        time.sleep(sleeping)
        vj_mselect(direction='up',button=bm.none)
        time.sleep(sleeping)
    vj_mselect(direction=None,button=bm.select)
    time.sleep(sleeping)
    #vj_mselect ffa
    vj_mselect(direction=None,button=bm.select)
    time.sleep(sleeping)
    #vj_mselect color (orange)
    vj_mselect(direction=None,button=bm.select)
    time.sleep(0.5)
    if botsOn == False:
        time.sleep(5)
    vj_mselect(direction=None,button=bm.select)
    time.sleep(0.5)
    #vj_mselect map
    vj_mselect(direction=None,button=bm.select)
    time.sleep(0.5)
    #vj_mselect guns
    #vj_mselect revolver
    vj_mselect(direction=None,button=bm.select)
    time.sleep(0.5)
    #vj_mselect sniper
    vj_mselect(direction='down',button=bm.none)
    time.sleep(sleeping)
    vj_mselect(direction='down',button=bm.none)
    time.sleep(sleeping)
    vj_mselect(direction='down',button=bm.none)
    time.sleep(sleeping)
    vj_mselect(direction=None,button=bm.select)
