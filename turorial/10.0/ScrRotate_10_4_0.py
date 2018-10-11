# -*- coding: utf-8 -*-
# RPi-Spark Base Demo
#    #04 Spark Hello World ( simple mode, uses 'rspk' lanuch it )
#    $> rspk 4_spark_hello_world --spark=HelloWorld
#
# Author: Kunpeng Zhang
# 2018.7.04
#
# See LICENSE for details.

from JMRPiFoundations.Skeleton.RPiSparkModule import RPiSparkModule
from JMRPiFoundations.Utiles.DataFilters import LowFilter3Axis
from PIL import ImageFont
from time import sleep

from math import atan, acos, sqrt

class HelloWorld(RPiSparkModule):

    def _calcTiltAngle(self, accel):
        pi = 3.1415926

        aX = atan( accel["x"] / sqrt( pow(accel["y"], 2) + pow(accel["z"], 2) ) )
        aY = atan( accel["y"] / sqrt( pow(accel["x"], 2) + pow(accel["z"], 2) ) )
        aZ = atan( sqrt( pow(accel["x"], 2) + pow(accel["y"], 2) ) / accel["z"] )

        aXY = atan(accel["x"] / accel["y"])
        aXYZ = acos(accel["z"] / sqrt(pow(accel["x"], 2) + pow(accel["y"], 2) + pow(accel["z"], 2) ))

        return {
            "aX": aX * 180 / pi,
            "aY": aY * 180 / pi,
            "aZ": aZ * 180 / pi,

            "aXY": aXY * 180 / pi,
            "aXYZ": aXYZ * 180 / pi,
        }
    
    def _getScreenDirection(self, accel):
#         if ( accel["z"] > -1 and accel["z"] < 1 ):
#             return 0

        if  ((accel["x"] > 0 and accel["x"] <= 5) and
            (accel["y"] > 5 and accel["y"] <= 10)):
            return 0

        if  ((accel["x"] >= -10 and accel["x"] <= -5 ) and
            (accel["y"] >= -5 and accel["y"] < 5)):
            return 90
        
        if  ((accel["x"] > -5 and accel["x"] <= 5 ) and
            (accel["y"] >= -10 and accel["y"] <= -5 )):
            return 180
        
        if  ((accel["x"] > 5 and accel["x"] <= 10 ) and
            (accel["y"] > -5 and accel["y"] <= 5 )):
            return 270

        return 0

    def _scrPortrait(self):
        self.RPiSpark.Screen.Canvas.rectangle( (0, 0, 127, 63), 0, 1 )
        self.RPiSpark.Screen.Canvas.rectangle( (2, 2, 125, 61), 0, 1 )

        # Show "Hello World !" on screen of RPi-Spark
        self.RPiSpark.Screen.Canvas.text( (24, 16), "Hello World !", 1, font=self.DEF_FONT )
        # Show current temperature of RPi-Spark 
        self.RPiSpark.Screen.Canvas.text( (24, 36), "Temp: {:6.2f}".format(self.RPiSpark.Attitude.getTemp()), 1, font=self.DEF_FONT )
        # Draw a line
        self.RPiSpark.Screen.Canvas.line( (24, 32, 98, 32), 1, 2 )

    def _scrLandscape(self):
        # Show "Hello World !" on screen of RPi-Spark
        self.RPiSpark.Screen.Canvas.rectangle( (0, 0, 63, 127), 0, 1 )
        self.RPiSpark.Screen.Canvas.rectangle( (2, 2, 61, 125), 0, 1 )

        self.RPiSpark.Screen.Canvas.text( (8, 5), "Hello", 1, font=self.DEF_FONT )
        self.RPiSpark.Screen.Canvas.text( (8, 16), "World", 1, font=self.DEF_FONT )
        # Show current temperature of RPi-Spark
        self.RPiSpark.Screen.Canvas.text( (10, 36), "Temp: ", 1, font=self.DEF_FONT )
        self.RPiSpark.Screen.Canvas.text( (10, 48), "{:6.2f}".format(self.RPiSpark.Attitude.getTemp()), 1, font=self.DEF_FONT )
        # Draw a line
        self.RPiSpark.Screen.Canvas.line( (4, 32, 59, 32), 1, 2 )

    def setup(self):
        # Create a PIL.ImageFont object instance
        self.DEF_FONT = ImageFont.load_default()
        # Open thermometer
        self.RPiSpark.Attitude.openWith(temp=True, accel=True, gyro=False)
        self.initKeyButtons("QUERY")

    def run(self):

        accelLFP = LowFilter3Axis(15.0, 1.5)
        while True:
            # Check exit key status ( JOY_UP + SW_A )
            if self.readExitButtonStatus():
                break;

            # Get Accel data from attitude sensor
            accelData = self.RPiSpark.Attitude.getAccelData()
            nAccelData = accelLFP.addSampleValue(accelData["x"], accelData["y"], accelData["z"])
            if nAccelData == None: continue

            devTiltAngle = self._calcTiltAngle(nAccelData)
            formatStr = "ax: %(aX).1f \t ay: %(aY).1f \t az: %(aZ).1f \t|\t  aXY: %(aXY).1f \t  aXYZ: %(aXYZ).1f \t "
            print(formatStr % devTiltAngle)

            scrDir = self._getScreenDirection(nAccelData)
            self.RPiSpark.Screen.rotateDirection(scrDir)

            if scrDir in [0, 180]: self._scrPortrait()
            if scrDir in [90, 270]: self._scrLandscape()
            self.RPiSpark.Screen.refresh()