import ctypes
import struct
import time
from game_functions.game_navigation import game_locations as locations

CONST_DLL_VJOY = locations.CONST_DLL_VJOY

'''
modified from: https://gist.github.com/varlen/c47e807e647cc56a6faf9d548d2c00f3

----vJoy Settings-----
Axis: X and Y
POVs: Continuous / 0
Effects: Disabled
Number of Buttons: 8
----------------------

-----x360 Controller Settings-------
Settings <--> auto
Button Mappings:
0 = None
1 = X
2 = A
4 = B
16 = LS
32 = RS
64 = LT
128 = LR
------------------------------------

-----------vJoy Axis--------

wAxisY
wAxisX

(0,0) = top left
(16000,16000) = centered
(32000, 32000) = bottom right

------------------------
'''


class vJoy(object):
    def __init__(self, reference=1):
        self.handle = None
        self.dll = ctypes.CDLL(CONST_DLL_VJOY)
        self.reference = reference
        self.acquired = False

    def open(self):
        if self.dll.AcquireVJD(self.reference):
            self.acquired = True
            return True
        return False

    def close(self):
        if self.dll.RelinquishVJD(self.reference):
            self.acquired = False
            return True
        return False

    def generateJoystickPosition(self, wThrottle=0, wRudder=0, wAileron=0,
                                 wAxisX=16000, wAxisY=16000, wAxisZ=0,
                                 wAxisXRot=0, wAxisYRot=0, wAxisZRot=0,
                                 wSlider=0, wDial=0, wWheel=0,
                                 wAxisVX=0, wAxisVY=0, wAxisVZ=0,
                                 wAxisVBRX=0, wAxisVBRY=0, wAxisVBRZ=0,
                                 lButtons=0, bHats=0, bHatsEx1=0,
                                 bHatsEx2=0, bHatsEx3=0):
        """
        typedef struct _JOYSTICK_POSITION
        {
            BYTE    bDevice; // Index of device. 1-based
            LONG    wThrottle;
            LONG    wRudder;
            LONG    wAileron;
            LONG    wAxisX;
            LONG    wAxisY;
            LONG    wAxisZ;
            LONG    wAxisXRot;
            LONG    wAxisYRot;
            LONG    wAxisZRot;
            LONG    wSlider;
            LONG    wDial;
            LONG    wWheel;
            LONG    wAxisVX;
            LONG    wAxisVY;
            LONG    wAxisVZ;
            LONG    wAxisVBRX;
            LONG    wAxisVBRY;
            LONG    wAxisVBRZ;
            LONG    lButtons;
            // 32 buttons: 0x00000001 means button1 is pressed, 0x80000000 -> button32 is pressed
            DWORD   bHats;
            // Lower 4 bits: HAT switch or 16-bit of continuous HAT switch
                        DWORD   bHatsEx1;   // 16-bit of continuous HAT switch
                        DWORD   bHatsEx2;   // 16-bit of continuous HAT switch
                        DWORD   bHatsEx3;   // 16-bit of continuous HAT switch
        } JOYSTICK_POSITION, *PJOYSTICK_POSITION;
        """
        joyPosFormat = "BlllllllllllllllllllIIII"
        pos = struct.pack(joyPosFormat, self.reference, wThrottle, wRudder,
                          wAileron, wAxisX, wAxisY, wAxisZ,
                          wAxisXRot, wAxisYRot,
                          wAxisZRot, wSlider,
                          wDial, wWheel, wAxisVX, wAxisVY,
                          wAxisVZ, wAxisVBRX, wAxisVBRY, wAxisVBRZ,
                          lButtons, bHats, bHatsEx1, bHatsEx2, bHatsEx3)
        return pos

    def update(self, joystickPosition):
        if self.dll.UpdateVJD(self.reference, joystickPosition):
            return True
        return False

    def sendButtons(self, bState):
        joyPosition = self.generateJoystickPosition(lButtons=bState)
        return self.update(joyPosition)

    def setButton(self, index, state):
        if self.dll.SetBtn(state, self.reference, index):
            return True
        return False

    def sendJoystick(self, x, y, button):
        joystickvalue = self.generateJoystickPosition(wAxisX=x,
                                                      wAxisY=y,
                                                      lButtons=button)
        return self.update(joystickvalue)

    def aim(self, x=16000, y=16000, button=0,  defaultbutton=0, delay=0.05):
        self.sendJoystick(x=x, y=y, button=button)
        time.sleep(delay)
        self.sendJoystick(x=16000, y=16000, button=defaultbutton)

    def mselect(self, direction=None, button=0, delay=0.1):
        if direction is None:
            self.sendJoystick(x=16000, y=16000, button=button)
            time.sleep(delay)
            self.sendJoystick(x=16000, y=16000, button=0)
        elif direction == 'up':
            self.sendJoystick(x=16000, y=0, button=button)
            time.sleep(delay)
            self.sendJoystick(x=16000, y=16000, button=0)
        elif direction == 'down':
            self.sendJoystick(x=16000, y=32000, button=button)
            time.sleep(delay)
            self.sendJoystick(x=16000, y=16000, button=0)
        elif direction == 'left':
            self.sendJoystick(x=0, y=16000, button=button)
            time.sleep(delay)
            self.sendJoystick(x=16000, y=16000, button=0)
        else:
            self.sendJoystick(x=32000, y=16000, button=button)
            time.sleep(delay)
            self.sendJoystick(x=16000, y=16000, button=0)
