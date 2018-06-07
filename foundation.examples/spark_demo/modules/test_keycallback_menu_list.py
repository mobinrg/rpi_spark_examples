# RPiSpark Testting Menu List
# 
# Author: Kunpeng Zhang
# 2018.4.11
#
# See LICENSE for details.


import random
import os.path
from PIL import Image
from time import sleep

from JMRPiFoundations.skeleton.JMRPiSparkModule import SparkModuleBase
from modules.test_keycallback import TestKeyCallback

class TestKeyCallbackMenuList(SparkModuleBase):
    myKeyboard = None
    myScreen = None
    
    _actStatus = 0

    def _callbackKeyboard(self, channel):
#         print channel
        if channel == self._RPiSparkConfig.BUTTON_ACT_A:
            self._actStatus = 2
            return
 
        if channel == self._RPiSparkConfig.BUTTON_ACT_B:
            self._actStatus = 100
            return
 
        if channel == self._RPiSparkConfig.BUTTON_JOY_LEFT or channel == self._RPiSparkConfig.BUTTON_JOY_UP:
#             self.myMenuItems.previous()
            self._actStatus = 1
            return
 
        if channel == self._RPiSparkConfig.BUTTON_JOY_RIGHT or channel == self._RPiSparkConfig.BUTTON_JOY_DOWN:
#             self.myMenuItems.next()
            self._actStatus = 1
            return
 
    def _initKeyButtons(self):
        try:
            self.myKeyboard.configKeyButtons([
                {"id":self._RPiSparkConfig.BUTTON_ACT_A, "callback":self._callbackKeyboard},
                {"id":self._RPiSparkConfig.BUTTON_ACT_B, "callback":self._callbackKeyboard},
                {"id":self._RPiSparkConfig.BUTTON_JOY_UP, "callback":self._callbackKeyboard},
                {"id":self._RPiSparkConfig.BUTTON_JOY_DOWN, "callback":self._callbackKeyboard},
                {"id":self._RPiSparkConfig.BUTTON_JOY_LEFT, "callback":self._callbackKeyboard},
                {"id":self._RPiSparkConfig.BUTTON_JOY_RIGHT, "callback":self._callbackKeyboard},
                {"id":self._RPiSparkConfig.BUTTON_JOY_OK, "callback":self._callbackKeyboard}
            ])
        except:
            pass


    def setup(self):
        random.seed()
        self.myScreen = self._RPiSpark.Screen
        self.myKeyboard = self._RPiSpark.Keyboard

    #Test key callback
    def run(self):
        self._initKeyButtons()

        while True:
            # run submoudle
            if self._actStatus == 2:
                self._releaseKeyButtons()
                print("\nEnter Submodule ...")

                myTestModule = TestKeyCallback( self._RPiSparkConfig, self._RPiSpark )
                myTestModule.run()
                
                print("Return Menu List")
                self._initKeyboard()
                continue
        
