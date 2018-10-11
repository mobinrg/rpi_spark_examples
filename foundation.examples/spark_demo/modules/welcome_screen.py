# RPiSpark Testting Welcome Screen
# 
# Author: Kunpeng Zhang
# 2018.4.15
#
# See LICENSE for details.


import os.path
from PIL import Image
from time import sleep

from JMRPiFoundations.Skeleton.RPiSparkModule import RPiSparkModule

from modules.spark_module_helper import drawBtn
from modules.spark_module_helper import drawText
from modules.spark_module_helper import drawMultiLineText

###################################
# Font 
#
FONT_NAME = "AHandMadeFont.ttf"
FONT_SIZE = 28

FONT_NAME_MSG = "Roboto-Light.ttf"
FONT_SIZE_MSG = 11

class TestWelcome(RPiSparkModule):
    myScreen = None

#     def sndStart(self):
#         self.beepTone(5, 0.1)
#         self.beepTone(6, 0.1)
#         self.beepTone(2, 0.1)
#         self.beepTone(1, 0.1)
#         sleep(0.1)

    def setup(self):
        self.myScreen = self.RPiSpark.Screen

    #Test display
    def run(self):
        print("Welcome!\n")
        print("Press button any key continue ... \n")
        self.myScreen.clearCanvas()
        draw = self.myScreen.Canvas
        drawMultiLineText(draw, 0, 2, text= "Welcome", fontName = FONT_NAME, fontSize = FONT_SIZE)
        drawMultiLineText(draw, 0, 36, text= "Press any button\ncontinue ...", fontName = FONT_NAME_MSG, fontSize = FONT_SIZE_MSG)
        self.myScreen.refresh()
#         self.myScreen.Display.scrollWith(
#             hStart = 0, 
#             hEnd = 3, 
#             vOffset = 0,
#             vStart = 0,
#             vEnd = 64,
#             int = 0,
#             dire = "left"
#         )

        # Wait press button A or B
        self.initKeyButtons("QUERY")
#         self.sndStart()
        while True:
            if self.readAnyButtonStatus(): break
#             if self.readKeyButton(self.RPiSparkConfig.BUTTON_ACT_A):break
#             if self.readKeyButton(self.RPiSparkConfig.BUTTON_ACT_B):break

#         self.myScreen.Display.scrollOff()
