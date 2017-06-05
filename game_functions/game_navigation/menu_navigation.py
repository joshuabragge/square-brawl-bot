import time
from pywinauto.application import Application
from game_functions.controller import button_mappings as bm
from game_functions.game_navigation import game_locations as locations


def launch_game(delay=5):
    x360 = Application().Start(cmd_line=locations.x360dir)
    time.sleep(delay)
    x360.Kill_()

    game = Application().Start(cmd_line=locations.gamedir)
    gwindow = game.Dialog
    gwindow.Wait('ready')
    button = gwindow[u'Play!']
    button.Click()


def start_game(vj_mselect, botsOn=False, mode='easy'):
    sleeping = 0.3
    if botsOn:
        # turn bot on
        time.sleep(sleeping)
        vj_mselect(direction='right', button=bm.none)
        time.sleep(sleeping)
        vj_mselect(direction='down', button=bm.none)
        time.sleep(sleeping)
        # vj_mselect 1 player
        vj_mselect(direction='left', button=bm.none)
        time.sleep(sleeping)
        vj_mselect(direction='up', button=bm.none)
        time.sleep(sleeping)
    vj_mselect(direction=None, button=bm.select)
    time.sleep(sleeping)
    # vj_mselect ffa
    vj_mselect(direction=None, button=bm.select)
    time.sleep(sleeping)
    vj_mselect(direction=None, button=bm.select)
    time.sleep(sleeping)
    # vj_mselect color (orange)
    if botsOn is False:
        time.sleep(5)
    vj_mselect(direction=None, button=bm.select)
    time.sleep(sleeping)
    # vj_mselect map
    vj_mselect(direction='right', button=bm.none)
    time.sleep(sleeping)
    vj_mselect(direction='down', button=bm.none)
    time.sleep(sleeping)
    vj_mselect(direction='down', button=bm.none)
    time.sleep(sleeping)
    vj_mselect(direction='down', button=bm.none)
    time.sleep(sleeping)
    vj_mselect(direction='down', button=bm.none)
    time.sleep(sleeping)
    time.sleep(sleeping)
    vj_mselect(direction=None, button=bm.select)
    time.sleep(sleeping)
    time.sleep(sleeping)
    vj_mselect(direction=None, button=bm.select)
    time.sleep(sleeping)
    time.sleep(sleeping)
    time.sleep(sleeping)
    # vj_mselect guns
    vj_mselect(direction='down', button=bm.none)
    time.sleep(sleeping)
    vj_mselect(direction='down', button=bm.none)
    time.sleep(sleeping)
    # vj_mselect shotgun
    vj_mselect(direction=None, button=bm.select)
    time.sleep(sleeping)
    # vj_mselect sniper
    vj_mselect(direction='down', button=bm.none)
    time.sleep(sleeping)
    vj_mselect(direction=None, button=bm.select)
