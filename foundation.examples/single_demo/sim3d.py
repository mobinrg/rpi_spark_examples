# -*- coding: utf-8 -*-
# RPi Spark Single Demo
#
# Show mode: Button A 
# Field of vision: Joy Up and Down 
# Exit: Button A + Joy Up
#
# Author: Kunpeng Zhang
# 2018.6.07
#
# See LICENSE for details.

import sys

from JMRPiFoundations.Skeleton.RPiSparkProvider import initSpark
from JMRPiFoundations.Devices.rpi_spark_z_1_0_0 import RPiSparkConfig as mySparkConfig
from modules.sim3d import TestSim3D

def main(argv):
    mySpark = initSpark()
    mySingleApp = TestSim3D( mySparkConfig, mySpark )
    mySingleApp.run()

if __name__ == "__main__":
   main(sys.argv[1:])
