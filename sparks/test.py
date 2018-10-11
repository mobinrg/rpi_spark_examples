#import sys
from JMRPiFoundations.Skeleton.RPiSparkProvider import initSpark
from JMRPiFoundations.Devices.rpi_spark_z_1_0_0 import RPiSparkConfig as mySparkConfig
from JMRPiSparks.Menu.RPiSparkMenu import RPiMenu

mySpark = initSpark()

myMenu = RPiMenu(mySparkConfig, mySpark)
myMenu.run()
