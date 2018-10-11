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
from time import sleep

class HelloWorld(RPiSparkModule):

    def _scrPortrait(self):
        self.RPiSpark.Screen.Canvas.rectangle( (0, 0, 127, 63), 0, 1 )
        self.RPiSpark.Screen.Canvas.rectangle( (2, 2, 125, 61), 0, 1 )        
        # Show "Hello World !" and current temperature of RPi-Spark on screen of RPi-Spark
        text = "Hello World !\nTemp: {:6.2f}".format(self.RPiSpark.Attitude.getTemp())
        self.RPiSpark.Screen.write(text, xy=(0,16), spacing=10, screenCenter=True)
        # Draw a line
        self.RPiSpark.Screen.Canvas.line( (24, 32, 98, 32), 1, 2 )

    def _scrLandscape(self):
        # Show "Hello World !" on screen of RPi-Spark
        self.RPiSpark.Screen.Canvas.rectangle( (0, 0, 63, 127), 0, 1 )
        self.RPiSpark.Screen.Canvas.rectangle( (2, 2, 61, 125), 0, 1 )
        # Show "Hello World !" and current temperature of RPi-Spark on screen of RPi-Spark
        text = "Hello\nWorld !\nTemp:\n{:6.2f}".format(self.RPiSpark.Attitude.getTemp())
        self.RPiSpark.Screen.write(text, xy=(0,16), spacing=10, screenCenter=True)        
        # Draw a line
        self.RPiSpark.Screen.Canvas.line( (4, 32, 63, 32), 1, 2 )

    def setup(self):
        # Open thermometer
        self.RPiSpark.Attitude.openWith(temp=True, accel=False, gyro=False)

    def run(self):
        self._scrPortrait()
        self.RPiSpark.Screen.refresh()
        sleep(4)

        self.RPiSpark.Screen.rotateDirection(90)
        self._scrLandscape()
        self.RPiSpark.Screen.refresh()
        sleep(4)

        self.RPiSpark.Screen.rotateDirection(180)
        self._scrPortrait()
        self.RPiSpark.Screen.refresh()
        sleep(4)

        self.RPiSpark.Screen.rotateDirection(270)
        self._scrLandscape()
        self.RPiSpark.Screen.refresh()