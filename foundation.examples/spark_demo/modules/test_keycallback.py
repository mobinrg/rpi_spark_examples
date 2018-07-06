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
from JMRPiFoundations.Skeleton.RPiSparkModule import RPiSparkModule

class TestKeyCallback(RPiSparkModule):
    myKeyboard = None
    myScreen = None
    _actStatus = 0
    
    def _callback(self, channel):
        if channel == 23: self._actStatus = 100
        print(self.__module__, " -- " ,channel)

    def _initKeyButtons(self):
        try:
            self.myKeyboard.configKeyButtons([
                {"id":self.RPiSparkConfig.BUTTON_ACT_A, "callback":self._callback},
                {"id":self.RPiSparkConfig.BUTTON_ACT_B, "callback":self._callback},
                {"id":self.RPiSparkConfig.BUTTON_JOY_UP, "callback":self._callback},
                {"id":self.RPiSparkConfig.BUTTON_JOY_DOWN, "callback":self._callback},
                {"id":self.RPiSparkConfig.BUTTON_JOY_LEFT, "callback":self._callback},
                {"id":self.RPiSparkConfig.BUTTON_JOY_RIGHT, "callback":self._callback},
                {"id":self.RPiSparkConfig.BUTTON_JOY_OK, "callback":self._callback}
            ])
        except:
            pass
#         super(RPiSparkModule, self)._initKeyboard()
#         self.myKeyboard.setKeyButtonCallback(self.RPiSparkConfig.BUTTON_ACT_A, self._callback )
#         self.myKeyboard.setKeyButtonCallback(self.RPiSparkConfig.BUTTON_ACT_B, self._callback )
#         self.myKeyboard.setKeyButtonCallback(self.RPiSparkConfig.BUTTON_JOY_UP, self._callback )
#         self.myKeyboard.setKeyButtonCallback(self.RPiSparkConfig.BUTTON_JOY_DOWN, self._callback )
        return

    def setup(self):
        random.seed()
        self.myScreen = self.RPiSpark.Screen
        self.myKeyboard = self.RPiSpark.Keyboard

    #Test key callback
    def run(self):
        self._initKeyButtons()
        
        while True:
            if self._actStatus == 100:
                print("Exit",  self.__module__)
                break
            pass
        
        self._releaseKeyButtons()
        print ("RESET Key", self.__module__)
        
