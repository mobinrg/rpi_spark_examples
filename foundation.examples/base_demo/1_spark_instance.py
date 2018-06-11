# -*- coding: utf-8 -*-
# RPi Spark Base Demo
#    #01 Create Spark Instance
#
# Author: Kunpeng Zhang
# 2018.6.07
#
# See LICENSE for details.

import sys

from JMRPiFoundations.Skeleton.RPiSparkProvider import initSpark
 
def main(argv):
    mySpark = initSpark()
    print(mySpark)
    print(dir(mySpark))
    print(mySpark.version())
 
if __name__ == "__main__":
   main(sys.argv[1:])
