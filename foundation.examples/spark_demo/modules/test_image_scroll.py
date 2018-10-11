# RPiSpark Testting Menu List
# 
# Author: Kunpeng Zhang
# 2018.4.10
#
# See LICENSE for details.


import random
from PIL import Image
from time import sleep
import RPi.GPIO as GPIO
import os.path

from JMRPiFoundations.Skeleton.RPiSparkModule import RPiSparkModule
from JMRPiFoundations.Utiles.DataFilters import Sample3AxisMAFilter

images = [
    "pix001.jpg",
    "pix010.jpg",
    "pix011.jpg"
]

VIEW_MOVE_LEFT  = 0
VIEW_MOVE_RIGHT = 1
VIEW_MOVE_UP    = 2
VIEW_MOVE_DOWN  = 3

class TestImageScroll(RPiSparkModule):
    myScreen = None
    myKeyboard = None
    myAttitude = None
    mySampleFilterA = None
    actionStatus = 0
    moveCount = 0

    def _shakeDeviceCallback(self, channel ):
        self.showImage()
        self.actionStatus = 1

    ##
    # Init shake check INT
    def initShakeINT(self):
        MPU_INT_PIN = self.RPiSparkConfig.ATTITUDE_INT
        GPIO.setup( MPU_INT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP )
        GPIO.add_event_detect( MPU_INT_PIN, GPIO.RISING, callback=self._shakeDeviceCallback, bouncetime=1 )
        
    def cleanup(self):
        #release key buttons
        self.releaseKeyButtons()

        #close attitude sensor
        GPIO.remove_event_detect( self.RPiSparkConfig.ATTITUDE_INT )
        self.myAttitude.disableInt()
        self.myAttitude.sleep()
        
        #reset screen
        self.myScreen._initBuffer( "1", None )
        self.myScreen.refresh()

    def moveView( self, direction, offset = 5 ):
        screen = self.myScreen
        sW, sH = screen.getBufferSize()
        #LEFT
        if direction == VIEW_MOVE_LEFT:
            if screen.View.x - offset < 0:
                screen.View.x = 0
            else:
                screen.View.moveOffset( -1 * offset, 0 )
            self.actionStatus = 1
            return

        #RIGHT
        if direction == VIEW_MOVE_RIGHT:
            if screen.View.x + screen.View.width + offset > sW:
                screen.View.x = sW - screen.View.width
            else:
                screen.View.moveOffset( offset, 0 )
            self.actionStatus = 1
            return
        
        if direction == VIEW_MOVE_UP:
            if screen.View.y - offset < 0:
                screen.View.y = 0
            else:
                screen.View.moveOffset( 0, -1 * offset )
            self.actionStatus = 1
            return
    
        if direction == VIEW_MOVE_DOWN:
            if screen.View.y + screen.View.height + offset > sH:
                screen.View.y = sH - screen.View.height
            else:
                screen.View.moveOffset( 0, offset )
            self.actionStatus = 1
            return
        pass

    def loadImage(self):
        img_path = os.path.abspath(os.path.join('images/pix', random.choice(images)))
        return Image.open(img_path)
    
    def showImage(self):
        self.myScreen.redefineBuffer( self.loadImage() )
        self.myScreen.refresh()

    def setup(self):
        random.seed()
        self.myScreen = self.RPiSpark.Screen
        self.myKeyboard = self.RPiSpark.Keyboard
        self.myAttitude = self.RPiSpark.Attitude
        self.mySampleFilterA = Sample3AxisMAFilter(10)

    #Test Image Scroll
    def run(self):
        print("Shake device to change image. Press button A and Joy Up to exit testting ...")
        self.initKeyButtons("QUERY")

        self.myAttitude.openWith( accel = True, gyro = False, temp = False, cycle = False )
        self.myAttitude.setMotionInt()
        self.initShakeINT()

        self.showImage()
#         print("Display Size ( W, H) :", myScreen.getDisplaySize())
#         print("Buffer Size ( W, H) :", myScreen.getBufferSize())
#         print("Press button A to exit, button B or shake device to change image ...")

        accelVal = {"x":0, "y":0, "z":0}
        while self.actionStatus != 2:

            if self.moveCount % 5 == 1:
                accelVal = self.myAttitude.getAccelData()
                maAccel = self.mySampleFilterA.addSampleValue(accelVal["x"], accelVal["y"], accelVal["z"])
                if maAccel == None: continue
#                 print(maAccel)
                direH = (VIEW_MOVE_RIGHT if maAccel["x"]>0 else VIEW_MOVE_LEFT)
                direV = (VIEW_MOVE_UP if maAccel["y"]>0 else VIEW_MOVE_DOWN)
                self.moveView( direH, int(abs(maAccel["x"] * 1.5)) )
                self.moveView( direV, int(abs(maAccel["y"] * 1.5)) )

            if self.actionStatus == 1:
                self.actionStatus = 0
                self.myScreen.refresh()

            self.moveCount += 1

            #################################
            # Button status read
            #
            if self.readExitButtonStatus(): break

        #
        self.cleanup()
        
        print("Image Scroll testting done.")
