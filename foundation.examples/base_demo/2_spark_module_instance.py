# -*- coding: utf-8 -*-
# RPi Spark Base Demo
#    #02 Create Spark Module Instance
#
# Author: Kunpeng Zhang
# 2018.6.07
#
# See LICENSE for details.

import sys

from JMRPiFoundations.Skeleton.RPiSparkProvider import initSpark
from JMRPiFoundations.Skeleton.RPiSparkModule import RPiSparkModule
from JMRPiFoundations.Devices.rpi_spark_z_1_0_0 import RPiSparkConfig as mySparkConfig

class DemoModule(RPiSparkModule):
    def setup(self):
        print("\nCall module's setup() ...\n")
        print("You can inherit and implement your setup code in the setup() function.")
        pass
    
    def run(self):
        print("\nCall module's run() ...\n")
        print("You can inherit and implement your application code in the run() function.")
        print("This is a simple demo...\n")
        pass

def main(argv):
    mySpark = initSpark()
    myModule = DemoModule(mySparkConfig, mySpark)
    myModule.run()

if __name__ == "__main__":
   main(sys.argv[1:])
