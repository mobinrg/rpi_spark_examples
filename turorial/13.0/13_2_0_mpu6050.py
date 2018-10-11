import RPi.GPIO as GPIO
from JMRPiSpark.Drives.Attitude.MPU6050 import MPU6050
from JMRPiSpark.Drives.Attitude.MPU6050 import DEF_MPU6050_ADDRESS

GPIO.setmode(GPIO.BCM)
myAttitude = MPU6050( DEF_MPU6050_ADDRESS )
myAttitude.setAccelRange( MPU6050.ACCEL_RANGE_2G )
myAttitude.setGyroRange( MPU6050.GYRO_RANGE_250DEG )
myAttitude.open()
print( myAttitude.getAllData ( ) )
myAttitude.sleep()    # close MPU6050
