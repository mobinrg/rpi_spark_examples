# -*- coding: utf-8 -*-
#
# RPi.Spark KeyButton Demo
#
# Author: Kunpeng Zhang
# 2018.6.6
#
# See LICENSE for details.

from time import sleep
import RPi.GPIO as GPIO

from JMRPiSpark.Drives.Key.RPiKeyButtons import RPiKeyButtons
from JMRPiSpark.Drives.Key.RPiKeyButtons import DEF_BOUNCE_TIME_SHORT_MON
from JMRPiSpark.Drives.Key.RPiKeyButtons import DEF_BOUNCE_TIME_NORMAL

########################################################################
# Key buttons include Joystick buttons and Action buttons, 
# use BCM mode, there are keyboard layout:
# 
#             [JOY UP]                                   
# [JOY LEFT]              [JOY RIGHT]             [ACT_A]         [ACT_B]
#             [JOY DOWN]                                 
#
class CONFIG_KEY:
    # Action Buttons    BCM_IO_NUM
    BUTTON_ACT_A        = 22
    BUTTON_ACT_B        = 23
 
    # Joy Buttons       BCM_IO_NUM
    BUTTON_JOY_LEFT     = 26
    BUTTON_JOY_RIGHT    = 27
    BUTTON_JOY_UP       = 5
    BUTTON_JOY_DOWN     = 6
    BUTTON_JOY_OK       = 24

class demo:
    _myKey = None

    def __init__(self):
        self._myKey = RPiKeyButtons()

    def _getKeyButtonName(self, keyBtn):
        if keyBtn == CONFIG_KEY.BUTTON_ACT_A: return "BUTTON_A"
        if keyBtn == CONFIG_KEY.BUTTON_ACT_B: return "BUTTON_B"
        
        if keyBtn == CONFIG_KEY.BUTTON_JOY_UP: return "JOY_UP"
        if keyBtn == CONFIG_KEY.BUTTON_JOY_DOWN: return "JOY_DOWN"
        if keyBtn == CONFIG_KEY.BUTTON_JOY_RIGHT: return "JOY_RIGHT"
        if keyBtn == CONFIG_KEY.BUTTON_JOY_LEFT: return "JOY_LEFT"
        if keyBtn == CONFIG_KEY.BUTTON_JOY_OK: return "JOY_CENTER"
        return "UNKNOW"

    def _keyButtonDown(self, channel):
        print("DOWN:\t{}".format(self._getKeyButtonName(channel)))
        pass

    def _keyButtonUp(self, channel):
        print("UP:\t{}\n".format(self._getKeyButtonName(channel)))
        pass

    def _callbackKeyButton(self, channel):
        """!
            Key button interrupt event callback function
            Inherit this method to implement your want
        """
        if self._myKey.readKeyButton(channel) == 0:
            self._keyButtonDown(channel)
            return

        if self._myKey.readKeyButton(channel) == 1:
            self._keyButtonUp(channel)
            return

    def _initKeyButtons(self, mode = "INT"):
        """!
            Init all key buttons interrupt events or query mode. 
            Inherit the _keyButtonDown and _keyButtonUp to implement your want
    
            @param mode: Can be { "INT" | "QUERY" }, default is "INT" 
        """
        if mode.upper() == "INT":
            try:
                self._myKey.configKeyButtons(
                    enableButtons = [
                        {"id":CONFIG_KEY.BUTTON_ACT_A, "callback":self._callbackKeyButton},
                        {"id":CONFIG_KEY.BUTTON_ACT_B, "callback":self._callbackKeyButton},
                        {"id":CONFIG_KEY.BUTTON_JOY_UP, "callback":self._callbackKeyButton},
                        {"id":CONFIG_KEY.BUTTON_JOY_DOWN, "callback":self._callbackKeyButton},
                        {"id":CONFIG_KEY.BUTTON_JOY_LEFT, "callback":self._callbackKeyButton},
                        {"id":CONFIG_KEY.BUTTON_JOY_RIGHT, "callback":self._callbackKeyButton},
                        {"id":CONFIG_KEY.BUTTON_JOY_OK, "callback":self._callbackKeyButton}
                    ],
                    bounceTime = DEF_BOUNCE_TIME_SHORT_MON )
            except:
                pass

        if mode.upper() == "QUERY":
            self._myKey.configKeyButtons([
                {"id":CONFIG_KEY.BUTTON_ACT_A, "callback":None},
                {"id":CONFIG_KEY.BUTTON_ACT_B, "callback":None},
                {"id":CONFIG_KEY.BUTTON_JOY_OK, "callback":None},
                {"id":CONFIG_KEY.BUTTON_JOY_UP, "callback":None},
                {"id":CONFIG_KEY.BUTTON_JOY_DOWN, "callback":None},
                {"id":CONFIG_KEY.BUTTON_JOY_LEFT, "callback":None},
                {"id":CONFIG_KEY.BUTTON_JOY_RIGHT, "callback":None}
            ])
     
    def _releaseKeyButtons(self):
        """!
            Release all key button events
        """
        self._myKey.removeKeyButtonEvent([
            CONFIG_KEY.BUTTON_ACT_A,
            CONFIG_KEY.BUTTON_ACT_B,
            CONFIG_KEY.BUTTON_JOY_UP,
            CONFIG_KEY.BUTTON_JOY_DOWN,
            CONFIG_KEY.BUTTON_JOY_LEFT,
            CONFIG_KEY.BUTTON_JOY_RIGHT,
            CONFIG_KEY.BUTTON_JOY_OK
        ])
 
    def _readKeyButton(self, keyBtn):
        """!
            Read key button status, return 0 / 1
        """
        if self._myKey.readKeyButton( keyBtn ) == 0:
            sleep(0.02)
            return 0 if self._myKey.readKeyButton( keyBtn ) else 1
        return 0
 
    def _readExitButtonStatus(self):
        """!
            Read Exit action ( button A and Joy UP press down same time )
        """
        pressA = self._readKeyButton(CONFIG_KEY.BUTTON_ACT_A)
        pressUp = self._readKeyButton(CONFIG_KEY.BUTTON_JOY_UP)
        return pressA and pressUp

    def run(self):
        print("\nPress any key button to test ...\n < JOY UP + Button A to Exit >\n\n")
        self._initKeyButtons("INT")

        while True:
            if self._readExitButtonStatus(): break
            pass

        self._releaseKeyButtons()
        GPIO.cleanup()

if __name__ == "__main__":
    demo().run()
    print("Key buttons demo is end.")