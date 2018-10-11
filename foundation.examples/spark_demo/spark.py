# -*- coding: utf-8 -*-
# 
# RPi-Spark Demo
# 
# Author: Kunpeng Zhang
# 2018.4.09
# 2018.6.07
#
# See LICENSE for details.

import sys

from JMRPiFoundations.Skeleton.RPiSparkProvider import initSpark
from JMRPiFoundations.Devices.rpi_spark_z_1_0_0 import RPiSparkConfig as mySparkConfig
from modules.test_menu_list import TestMenuList

def main(argv):
    mySpark = initSpark()
    myModuleList = TestMenuList( mySparkConfig, mySpark )
    myModuleList.run()

if __name__ == "__main__":
   main(sys.argv[1:])
