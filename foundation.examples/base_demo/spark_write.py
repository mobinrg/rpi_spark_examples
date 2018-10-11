# -*- coding: utf-8 -*-
# RPi-Spark Base Demo
#    #03 Spark Hello World ( full mode -- single app and module )
#
# Author: Kunpeng Zhang
# 2018.6.25
#
# See LICENSE for details.

import sys
from JMRPiFoundations.Skeleton.RPiSparkProvider import initSpark
from JMRPiFoundations.Devices.rpi_spark_z_1_0_0 import RPiSparkConfig as mySparkConfig
from JMRPiFoundations.Skeleton.RPiSparkModule import RPiSparkModule

class HelloWorldModule(RPiSparkModule):
    def setup(self):
        # Create a PIL.ImageFont object instance
#         self.DEF_FONT = ImageFont.load_default()
        # Open thermometer 
        self.RPiSpark.Attitude.openWith(temp=True, accel=False, gyro=False)

    def run(self):
        self.RPiSpark.Screen.write("Hello World !")
        self.RPiSpark.Screen.write("Hello World !\nLeft Align", align="left", xy=(0,8), spacing=3,screenCenter=True)
#         self.RPiSpark.Screen.write("Hello World\nLeft Align", align="center", xy=(0,24), spacing=3)
        self.RPiSpark.Screen.write("Hello World !\nRight Align", align="right", xy=(0,42), screenCenter=True)
        self.RPiSpark.Screen.refresh()

def main(argv):
    mySpark = initSpark()
    myModule = HelloWorldModule(mySparkConfig, mySpark)
    myModule.run()

if __name__ == "__main__":
   main(sys.argv[1:])