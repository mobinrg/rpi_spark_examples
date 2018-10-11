#!/usr/bin/python
# -*- coding: utf-8 -*-
# RPi-Spark Base Demo
#    #03 Spark Hello World ( full mode -- single app and module )
#
# Author: Kunpeng Zhang
# 2018.6.25
# 2018.9.25
#
# See LICENSE for details.

import sys
from JMRPiFoundations.Skeleton.RPiSparkProvider import initSpark
from JMRPiFoundations.Devices.rpi_spark_z_1_0_0 import RPiSparkConfig as mySparkConfig
from JMRPiFoundations.Skeleton.RPiSparkModule import RPiSparkModule

class HelloWorldModule(RPiSparkModule):
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

def main(argv):
    mySpark = initSpark()
    myModule = HelloWorldModule(mySparkConfig, mySpark)
    myModule.run()

if __name__ == "__main__":
   main(sys.argv[1:])