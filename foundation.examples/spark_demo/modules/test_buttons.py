# RPiSpark Testting Menu List
# 
# Author: Kunpeng Zhang
# 2018.4.10
#
# See LICENSE for details.


from PIL import ImageFont
from JMRPiFoundations.Skeleton.RPiSparkModule import RPiSparkModule
from modules.spark_module_helper import drawBtn

class TestButtons(RPiSparkModule):
    myScreen = None
    myKeyboard = None
    dispContrast = 128

    def _changeContrast(self, up=True):
        if up:
            self.dispContrast += 16 if self.dispContrast < 239 else 0
        else:
            self.dispContrast -= 16 if self.dispContrast > 16 else 0

        self.myScreen.Display.setContrast(self.dispContrast)

    def setup(self):
        self.myScreen = self.RPiSpark.Screen
        self.myKeyboard = self.RPiSpark.Keyboard

        #change display buffer color mode to mono
        self.myScreen.changeBufferColorMode("1")
        self.myScreen.Display.on()
        self.myScreen.Display.setContrast(self.dispContrast)
        self.myScreen.clearCanvas()

    #Test display
    def run(self):
        print("Press button A and Joy Up to exit testting ...")
        self._initKeyButtons("QUERY")
        while True:
            #################################
            # Draw button status
            #
            draw = self.RPiSpark.Screen.Canvas
            pressBtnA = 0 if self.myKeyboard.readKeyButton(self.RPiSparkConfig.BUTTON_ACT_A) else 255 
            drawBtn(draw, x=96, y=32, outline=255, fill=pressBtnA, dire="a" )

            pressBtnB = 0 if self.myKeyboard.readKeyButton(self.RPiSparkConfig.BUTTON_ACT_B) else 255
            drawBtn(draw, x=112, y=12, outline=255, fill=pressBtnB, dire="b")

            pressJoyL = 0 if self.myKeyboard.readKeyButton(self.RPiSparkConfig.BUTTON_JOY_LEFT) else 255
            drawBtn(draw, x=1, y=19, outline=255, fill=pressJoyL, dire="left")

            pressJoyU = 0 if self.myKeyboard.readKeyButton(self.RPiSparkConfig.BUTTON_JOY_UP) else 255
            drawBtn(draw, x=19, y=1, outline=255, fill=pressJoyU, dire="up")

            pressJoyR = 0 if self.myKeyboard.readKeyButton(self.RPiSparkConfig.BUTTON_JOY_RIGHT) else 255
            drawBtn(draw, x=37, y=19, outline=255, fill=pressJoyR, dire="right")

            pressJoyD = 0 if self.myKeyboard.readKeyButton(self.RPiSparkConfig.BUTTON_JOY_DOWN) else 255
            drawBtn(draw, x=19, y=37, outline=255, fill=pressJoyD, dire="down")

            pressJoyC = 0 if self.myKeyboard.readKeyButton(self.RPiSparkConfig.BUTTON_JOY_OK) else 255
            drawBtn(draw, x=19, y=19, outline=255, fill=pressJoyC, dire="center")

            self.myScreen.refresh()

            # Change Contrast
            if self.myKeyboard.readKeyButton(self.RPiSparkConfig.BUTTON_JOY_UP) == False:
                self._changeContrast(True)

            if self.myKeyboard.readKeyButton(self.RPiSparkConfig.BUTTON_JOY_DOWN) == False:
                self._changeContrast(False)

            # Press Button A and Joy UP to exit
            if self.myKeyboard.readKeyButton(self.RPiSparkConfig.BUTTON_ACT_A) == False and self.myKeyboard.readKeyButton(self.RPiSparkConfig.BUTTON_JOY_UP) == False:  
                break

        print("Button testting done.")
