# -*- coding: utf-8 -*-
# RPi Spark Base Demo
#    #03 Spark Hello World ( full mode -- single app and module )
#
# Author: Kunpeng Zhang
# 2018.6.25
#
# See LICENSE for details.

import sys
from PIL import ImageFont
from JMRPiFoundations.Skeleton.RPiSparkProvider import initSpark
from JMRPiFoundations.Devices.rpi_spark_z_1_0_0 import RPiSparkConfig as mySparkConfig
from JMRPiFoundations.Skeleton.RPiSparkModule import RPiSparkModule

class HelloWorldModule(RPiSparkModule):
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

def main(argv):
    mySpark = initSpark()
    myModule = HelloWorldModule(mySparkConfig, mySpark)
    myModule.run()

if __name__ == "__main__":
   main(sys.argv[1:])