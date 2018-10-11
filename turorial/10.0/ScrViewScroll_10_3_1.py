import random
from PIL import Image
from time import sleep
import os.path

from JMRPiFoundations.Skeleton.RPiSparkModule import RPiSparkModule
from JMRPiFoundations.Utiles.DataFilters import Sample3AxisMAFilter

images = [
    "manhattan-336708_1280.jpg",
    "building.jpg",
    "low_poly.jpg"
]

ST_ACTION_NOTHING = 0
ST_ACTION_REFRESH = 1
ST_ACTION_EXIT = 10

VIEW_MOVE_LEFT  = 0
VIEW_MOVE_RIGHT = 1
VIEW_MOVE_UP    = 2
VIEW_MOVE_DOWN  = 3

class ScrViewScroll(RPiSparkModule):
    mySampleFilterA = None
    actionStatus = 0
    moveCount = 0
    dsp_contrast = 20

    def onDeviceShake(self, channel ):
        self._showImage()
        self.actionStatus = ST_ACTION_REFRESH

    def _cleanup(self):
        #release key buttons
        self.releaseKeyButtons()

        # close attitude sensor
        self.disableShakeDetect()
        self.RPiSpark.Attitude.sleep()

        #reset screen
        self.RPiSpark.Screen.changeBufferColorMode("1")
        self.RPiSpark.Screen.refresh()

    def _moveView( self, direction, offset = 5 ):
        screen = self.RPiSpark.Screen
        sW, sH = screen.getBufferSize()
        # LEFT
        if direction == VIEW_MOVE_LEFT:
            if screen.View.x - offset < 0:
                screen.View.x = 0
            else:
                screen.View.moveOffset( -1 * offset, 0 )
            self.actionStatus = ST_ACTION_REFRESH
            return

        # RIGHT
        if direction == VIEW_MOVE_RIGHT:
            if screen.View.x + screen.View.width + offset > sW:
                screen.View.x = sW - screen.View.width
            else:
                screen.View.moveOffset( offset, 0 )
            self.actionStatus = ST_ACTION_REFRESH
            return

        # UP
        if direction == VIEW_MOVE_UP:
            if screen.View.y - offset < 0:
                screen.View.y = 0
            else:
                screen.View.moveOffset( 0, -1 * offset )
            self.actionStatus = ST_ACTION_REFRESH
            return

        # DOWN
        if direction == VIEW_MOVE_DOWN:
            if screen.View.y + screen.View.height + offset > sH:
                screen.View.y = sH - screen.View.height
            else:
                screen.View.moveOffset( 0, offset )
            self.actionStatus = ST_ACTION_REFRESH
            return

    def _loadImage(self):
        img_path = os.path.abspath( os.path.join('images/', random.choice(images)) )
        return Image.open( img_path )
    
    def _showImage(self):
        self.RPiSpark.Screen.redefineBuffer( self._loadImage() )
        self.RPiSpark.Screen.refresh()

    def _adjustContrast(self, offset):
        self.dsp_contrast += offset
        if self.dsp_contrast > 255: self.dsp_contrast = 255
        if self.dsp_contrast < 20: self.dsp_contrast = 20
        self.RPiSpark.Screen.Display.setContrast(self.dsp_contrast)

    def setup(self):
        random.seed()
        self.mySampleFilterA = Sample3AxisMAFilter(10)
        self.initKeyButtons("QUERY")
        self.RPiSpark.Attitude.openWith( accel = True, gyro = False, temp = False, cycle = False )
        self.enableShakeDetect()

    def run(self):
        print("Shake device to change image. Press button A and Joy Up to exit testting ...")
        self._showImage()
        accelVal = {"x":0, "y":0, "z":0}
        while self.actionStatus != ST_ACTION_EXIT:

            #################################
            # Exit button status read
            if self.readExitButtonStatus(): break

            #################################
            # Adjust contrast
            if self.readKeyButton(self.RPiSparkConfig.BUTTON_JOY_UP):
                self._adjustContrast(20)

            if self.readKeyButton(self.RPiSparkConfig.BUTTON_JOY_DOWN):
                self._adjustContrast(-20)

            if self.moveCount % 5 == 1:
                accelVal = self.RPiSpark.Attitude.getAccelData()
                maAccel = self.mySampleFilterA.addSampleValue(accelVal["x"], accelVal["y"], accelVal["z"])
                if maAccel == None: continue

                direH = (VIEW_MOVE_RIGHT if maAccel["x"]>0 else VIEW_MOVE_LEFT)
                direV = (VIEW_MOVE_UP if maAccel["y"]>0 else VIEW_MOVE_DOWN)
                self._moveView( direH, int(abs(maAccel["x"] * 1.5)) )
                self._moveView( direV, int(abs(maAccel["y"] * 1.5)) )

            if self.actionStatus == ST_ACTION_REFRESH:
                self.RPiSpark.Screen.refresh()
                self.actionStatus = ST_ACTION_NOTHING

            self.moveCount += 1

        self._cleanup()
        print("Image Scroll testting done.")