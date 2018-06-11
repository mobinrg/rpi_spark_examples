# RPiSpark Testting Menu List
# 
# Author: Kunpeng Zhang
# 2018.4.12
#
# See LICENSE for details.

import os.path
from time import sleep
from PIL import ImageFont
from JMRPiFoundations.Skeleton.RPiSparkModule import RPiSparkModule
from modules.spark_module_helper import drawBtn
from modules.spark_module_helper import drawText
from modules.spark_module_helper import drawMultiLineText

class DialogConst:
    DIALOG_BUTTON_UNKNOW    = 0
    DIALOG_BUTTON_DONE      = 1
    DIALOG_BUTTON_YES       = 1
    DIALOG_BUTTON_NO        = 2

class DialogScreen(RPiSparkModule):
    myScreen = None
    fontName = None
    fontSize = 12

    def drawButtons(self, x, y, aTitle="", bTitle="", aState=0, bState=0):
        draw = self._RPiSpark.Screen.Canvas
        drawBtn(draw, x=x, y=y, outline=255, fill=aState, dire="a")
        drawText(draw, x=x+22, y=y, title = aTitle)
    
        bX = x+72
        drawBtn(draw, x=bX, y=y, outline=255, fill=bState, dire="b")
        drawText(draw, x=bX+22, y=y,title = bTitle)

    def showYesNo(self, message = ""):
        self.myScreen.clearCanvas()
        draw = self._RPiSpark.Screen.Canvas
        drawMultiLineText(draw, 0,0, text=message, fontName=self.fontName, fontSize = self.fontSize )
        self.drawButtons(10, 50, aTitle = "YES", bTitle = "NO")
        self.myScreen.refresh()

        self._initKeyButtons("QUERY")
        result = DialogConst.DIALOG_BUTTON_UNKNOW
        sleep(0.5)
        while True:
            if self._readKeyButton(self._RPiSparkConfig.BUTTON_ACT_A):
                result = DialogConst.DIALOG_BUTTON_YES
                break

            if self._readKeyButton(self._RPiSparkConfig.BUTTON_ACT_B):
                result = DialogConst.DIALOG_BUTTON_NO
                break
        return result
    
    def showMessage(self, message = "", waitKey = None):
        self.myScreen.clearCanvas()
        draw = self._RPiSpark.Screen.Canvas
        drawMultiLineText(draw, 0,0, text=message, fontName=self.fontName, fontSize = self.fontSize )
        self.myScreen.refresh()

        self._initKeyButtons("QUERY")
        if waitKey != None:
            sleep(0.5)
            while True:
                if self._readAnyButtonStatus(): break
#                 if self._readKeyButton(self._RPiSparkConfig.BUTTON_ACT_A):break
#                 if self._readKeyButton(self._RPiSparkConfig.BUTTON_ACT_B):break        

    def setup(self):
        self.myScreen = self._RPiSpark.Screen

#     #Show dialog
#     def run(self):
#         self.showYESNO("Are you sure\nto exit?")
#         sleep(3)
#         pass
