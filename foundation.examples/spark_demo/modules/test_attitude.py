# RPiSpark Testting Menu List
# 
# Author: Kunpeng Zhang
# 2018.4.10
#
# See LICENSE for details.


from PIL import ImageFont
from time import sleep
import RPi.GPIO as GPIO
from JMRPiFoundations.Utiles.DataFilters import Sample3AxisMAFilter
from JMRPiFoundations.Skeleton.RPiSparkModule import RPiSparkModule

class TestAttitude(RPiSparkModule):
    myScreen = None
    myAttitude = None
    mySampleFilterA = None
    mySampleFilterG = None
    # Load default font.
    myFont = None
    shakeCount = 0
    
    def _shakeDeviceCallback(self, channel ):
        self.shakeCount += 1
    
    ##
    # Init shake check INT
    def initShakeINT(self):
        MPU_INT_PIN = self._RPiSparkConfig.ATTITUDE_INT
        GPIO.setup( MPU_INT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP )
        GPIO.add_event_detect( MPU_INT_PIN, GPIO.RISING, callback=self._shakeDeviceCallback, bouncetime=20 )

        #enable motion check int
        self.myAttitude.setMotionInt()
        
    def cleanup(self):
        GPIO.remove_event_detect( self._RPiSparkConfig.ATTITUDE_INT )
        self.myAttitude.disableInt()
        self.myAttitude.sleep()

    def displayData(self, x, y, data, title=""):
        draw = self.myScreen.Canvas
        fw, fh = self.myFont.getsize(title.upper())
        prec = 2

        draw.text((x,y), title.upper(), font=self.myFont, fill= 1 )
        if isinstance(data, float):
            draw.text((x,y+ fh), '{:.{prec}f}'.format(data, prec=prec), font=self.myFont, fill= 1)
            
        if isinstance(data, int):
            draw.text((x,y+ fh), '{}'.format(data), font=self.myFont, fill= 1)
        
        if isinstance(data, dict):
            draw.text((x,y+ fh), '{} : {:.{prec}f}'.format('x', data["x"], prec=prec), font=self.myFont, fill= 1) 
            draw.text((x,y+ fh * 2), '{} : {:.{prec}f}'.format('y', data["y"], prec=prec), font=self.myFont, fill= 1)
            draw.text((x,y+ fh * 3), '{} : {:.{prec}f}'.format('z', data["z"], prec=prec), font=self.myFont, fill= 1)

    def setup(self):
        self.myScreen = self._RPiSpark.Screen
        self.myAttitude = self._RPiSpark.Attitude

        self.mySampleFilterA = Sample3AxisMAFilter(15)
        self.mySampleFilterG = Sample3AxisMAFilter(15)

        #change display buffer color mode to mono
        self.myScreen.changeBufferColorMode("1")
        self.myScreen.Display.on()
        self.myScreen.Display.setContrast( 0xA0 )
        self.myScreen.clearCanvas()

        self.myFont = ImageFont.load_default()

    #Test display
    def run(self):
        print("Press button A and Joy Up to exit testting ...")
        self._initKeyButtons("QUERY")

        # Open attitude with all sensor ( accel, gyro, temp )
        self.myAttitude.setAccelRange(self.myAttitude.ACCEL_RANGE_2G)
        self.myAttitude.setGyroRange(self.myAttitude.GYRO_RANGE_250DEG)
        self.myAttitude.open()
        self.initShakeINT()

        while True:
            self.myScreen.clearCanvas()
            #################################
            # Read accel data
            aValue = self.myAttitude.getAccelData( raw = False )
            gValue = self.myAttitude.getGyroData()
            tValue = self.myAttitude.getTemp()

#             maAccel = self.mySampleFilterA.addSampleValue(aValue["x"], aValue["y"], aValue["z"])
#             maGyro = self.mySampleFilterA.addSampleValue(gValue["x"], gValue["y"], gValue["z"])
# 
#             if maAccel == None: continue
#             if maGyro == None: continue

            #print maAccel, aValue, "|", maGyro, gValue

            self.displayData(0,0, aValue, "Accel")
            self.displayData(64,0, gValue, "Gyro")
            self.displayData(0,44, tValue, "Temp")
            self.displayData(64,44, self.shakeCount, "Shake")

            self.myScreen.refresh()

            #################################
            # Button status read
            #
            if self._readExitButtonStatus(): break

        self.cleanup()
        print("Attitude testting done.")
