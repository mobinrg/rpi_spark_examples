# -*- coding: utf-8 -*-
#
# RPi.Spark Tone Play Demo
#
# Author: Kunpeng Zhang
# 2018.6.6
#
# See LICENSE for details.

from time import sleep
import RPi.GPIO as GPIO

from JMRPiSpark.Drives.Audio.RPiTone import RPiTonePlayer
from JMRPiSpark.Drives.Audio.RPiTone import TONE_MID, TONE_A

########################################################################
# Audio PINs
# PWM - Audio
# GPIO12 - set mode ALT0
# GPIO13 - set mode ALT0
class CONFIG_AUDIO:
    AUDIO_L = 12
    AUDIO_R = 13
    SPEAKER = 12

class demo:
    _myTone = None

    def __init__(self):
        self._myTone = RPiTonePlayer( CONFIG_AUDIO.SPEAKER )

    def _sndTone(self):
        for t in TONE_MID[TONE_A]:
            self._myTone.playTone( t, 1, 0.2, 0 )
        
        tones = [ 20, 46, 69, 105, 160, 244, 371, 565, 859, 1300, 1980 ]
        for t in tones:
            self._myTone.playTone( t, 1, 0.2, 0 )

        self._myTone.stopTone()
        pass

    def run(self):
        self._sndTone()
        GPIO.cleanup()

if __name__ == "__main__":
    demo().run()
    print("Tone player demo is end.")