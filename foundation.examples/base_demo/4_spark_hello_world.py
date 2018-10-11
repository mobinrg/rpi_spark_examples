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

class HelloWorld(RPiSparkModule):
    def setup(self):
        # Open thermometer 
        self.RPiSpark.Attitude.openWith(temp=True, accel=False, gyro=False)

    def run(self):
        # Show "Hello World !" and current temperature of RPi-Spark on screen of RPi-Spark
        text = "Hello World !\nTemp: {:6.2f}".format(self.RPiSpark.Attitude.getTemp())
        self.RPiSpark.Screen.write( text, xy=(0, 16), spacing=10, screenCenter=True )
        # Draw a line
        self.RPiSpark.Screen.Canvas.line( (24, 32, 98, 32), 1, 2 )
        self.RPiSpark.Screen.refresh()