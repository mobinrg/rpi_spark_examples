# -*- coding: utf-8 -*-
#
# RPi.Spark MPU6050 Demo
#
# Author: Kunpeng Zhang
# 2018.6.6
#
# See LICENSE for details.

from time import sleep
import RPi.GPIO as GPIO

from JMRPiSpark.Drives.Attitude.MPU6050 import MPU6050
from JMRPiSpark.Drives.Attitude.MPU6050 import DEF_MPU6050_ADDRESS

MPU_INT_PIN = 25

class demo:
    _count = 0
    _shakeCount = 0
    _myAttitude = None

    def __init__(self):
        self._myAttitude = MPU6050( DEF_MPU6050_ADDRESS )

    def _shakeDeviceCallback(self, channel):
        self._shakeCount += 1
        print("\n--- SHAKED DEVICE: {} ---\n".format(self._shakeCount))

    def run(self):
        GPIO.setmode(GPIO.BCM)
        
        # Open attitude with all sensor ( accel, gyro, temp )
        self._myAttitude.setAccelRange( MPU6050.ACCEL_RANGE_2G )
        self._myAttitude.setGyroRange( MPU6050.GYRO_RANGE_250DEG )
        self._myAttitude.open()
        # self._myAttitude.openWith( accel = True, gyro = True, temp = True, cycle = False )
        
        # Init shake check INT -- GPIO 25 ( BCM )
        GPIO.setup( MPU_INT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP )
        GPIO.add_event_detect( MPU_INT_PIN, GPIO.RISING, callback=self._shakeDeviceCallback, bouncetime=20 )
        # enable motion check int
        self._myAttitude.setMotionInt()

        # Demo will run 2 min, you can shake device at during
        while True:
            if self._count > 120: break
            print( self._myAttitude.getAllData ( ) )
            sleep(1)
            self._count += 1

        # Clear up gpio resource
        GPIO.remove_event_detect( MPU_INT_PIN )
        self._myAttitude.disableInt() # Disable MPU6050 motion interrupt
        self._myAttitude.sleep()    # close MPU6050
        GPIO.cleanup()


if __name__ == "__main__":
    demo().run()
    print("MPU6050 demo is end.")