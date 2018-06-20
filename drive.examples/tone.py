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
from JMRPiSpark.Drives.Audio.RPiTone import TONE_MID, TONE_BASS, TONE_A

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
            self._myTone.playTone( freq=t, reps=2, delay=0.1, muteDelay=0.03 )

        tones = [ 20, 46, 69, 105, 160, 244, 371, 565, 859, 1300, 1980, 3020, 4600, 7000, 10600, 20000 ]
        for t in tones:
            self._myTone.playTone( freq=t, reps=1, delay=0.1, muteDelay=0.03 )

        self._myTone.stopTone()

    def _sndTone3Tigers(self):
        delay_2 = 0.075
        delay1 = 0.15
        delay2 = 0.3
        muteDelay1 = 0.05
        muteDelay2 = 0.1
        myTONE = TONE_MID[TONE_A]
        myTONE2 = TONE_BASS[TONE_A]

        tone3Tigers = [
            {"freq": myTONE[1], "reps": 1, "delay": delay1, "muteDelay": muteDelay1},
            {"freq": myTONE[2], "reps": 1, "delay": delay1, "muteDelay": muteDelay1},
            {"freq": myTONE[3], "reps": 1, "delay": delay1, "muteDelay": muteDelay1},
            {"freq": myTONE[1], "reps": 1, "delay": delay1, "muteDelay": muteDelay1},
            
            {"freq": myTONE[1], "reps": 1, "delay": delay1, "muteDelay": muteDelay1},
            {"freq": myTONE[2], "reps": 1, "delay": delay1, "muteDelay": muteDelay1},
            {"freq": myTONE[3], "reps": 1, "delay": delay1, "muteDelay": muteDelay1},
            {"freq": myTONE[1], "reps": 1, "delay": delay1, "muteDelay": muteDelay1},
            
            {"freq": myTONE[3], "reps": 1, "delay": delay1, "muteDelay": muteDelay1},
            {"freq": myTONE[4], "reps": 1, "delay": delay1, "muteDelay": muteDelay1},
            {"freq": myTONE[5], "reps": 1, "delay": delay2, "muteDelay": muteDelay1},
            
            {"freq": myTONE[3], "reps": 1, "delay": delay1, "muteDelay": muteDelay1},
            {"freq": myTONE[4], "reps": 1, "delay": delay1, "muteDelay": muteDelay1},
            {"freq": myTONE[5], "reps": 1, "delay": delay2, "muteDelay": muteDelay1},
            
            ################################
            
            {"freq": myTONE[5], "reps": 1, "delay": delay_2, "muteDelay": muteDelay1},
            {"freq": myTONE[6], "reps": 1, "delay": delay_2, "muteDelay": muteDelay1},
            {"freq": myTONE[5], "reps": 1, "delay": delay_2, "muteDelay": muteDelay1},
            {"freq": myTONE[4], "reps": 1, "delay": delay_2, "muteDelay": muteDelay1},
            {"freq": myTONE[3], "reps": 1, "delay": delay1, "muteDelay": muteDelay1},
            {"freq": myTONE[1], "reps": 1, "delay": delay1, "muteDelay": muteDelay1},
            
            {"freq": myTONE[5], "reps": 1, "delay": delay_2, "muteDelay": muteDelay1},
            {"freq": myTONE[6], "reps": 1, "delay": delay_2, "muteDelay": muteDelay1},
            {"freq": myTONE[5], "reps": 1, "delay": delay_2, "muteDelay": muteDelay1},
            {"freq": myTONE[4], "reps": 1, "delay": delay_2, "muteDelay": muteDelay1},
            {"freq": myTONE[3], "reps": 1, "delay": delay1, "muteDelay": muteDelay1},
            {"freq": myTONE[1], "reps": 1, "delay": delay1, "muteDelay": muteDelay1},
            
            {"freq": myTONE[1], "reps": 1, "delay": delay1, "muteDelay": muteDelay1},
            {"freq": myTONE2[5], "reps": 1, "delay": delay1, "muteDelay": muteDelay1},
            {"freq": myTONE[1], "reps": 1, "delay": delay2, "muteDelay": muteDelay1},

            {"freq": myTONE[1], "reps": 1, "delay": delay1, "muteDelay": muteDelay1},
            {"freq": myTONE2[5], "reps": 1, "delay": delay1, "muteDelay": muteDelay1},
            {"freq": myTONE[1], "reps": 1, "delay": delay2, "muteDelay": muteDelay1},
        ]
        
        self._myTone.playToneList(tone3Tigers)
        self._myTone.stopTone()

    def run(self):
        self._sndTone()
        self._sndTone3Tigers()
        GPIO.cleanup()

if __name__ == "__main__":
    demo().run()
    print("Tone player demo is end.")