# -*- coding: utf-8 -*-
# RPi Spark Base Demo
#    #04 Spark Hello World ( simple mode, uses 'rspk' lanuch it )
#
# Author: Kunpeng Zhang
# 2018.7.04
#
# See LICENSE for details.

from JMRPiFoundations.Skeleton.RPiSparkModule import RPiSparkModule
from PIL import ImageFont

class HelloWorld(RPiSparkModule):
    def setup(self):
        # Create a PIL.ImageFont object instance
        self.DEF_FONT = ImageFont.load_default()
        # Open thermometer 
        self.RPiSpark.Attitude.openWith(temp=True, accel=False, gyro=False)

    def run(self):
        # Show "Hello World !" on screen of RPi Spark
        self.RPiSpark.Screen.Canvas.text( (24, 16), "Hello World !", 1, font=self.DEF_FONT )
        # Show current temperature of RPi Spark 
        self.RPiSpark.Screen.Canvas.text( (24, 36), "Temp: {:6.2f}".format(self.RPiSpark.Attitude.getTemp()), 1, font=self.DEF_FONT )
        # Draw a line
        self.RPiSpark.Screen.Canvas.line( (24, 32, 98, 32), 1, 2 )
        self.RPiSpark.Screen.refresh()