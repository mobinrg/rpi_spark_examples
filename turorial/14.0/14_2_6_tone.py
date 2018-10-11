from time import sleep
import RPi.GPIO as GPIO

from JMRPiSpark.Drives.Audio.RPiTone import RPiTonePlayer
from JMRPiSpark.Drives.Audio.RPiTone import TONE_MID, TONE_BASS, TONE_A

##
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

    def _sndTone3Tigers(self):
        delay_2 = 0.075
        delay1 = 0.15
        delay2 = 0.3
        muteDelay1 = 0.05
        muteDelay2 = 0.1
        myMidTONE = TONE_MID[TONE_A]
        myBassTONE = TONE_BASS[TONE_A]

        tone3Tigers = [
            {"freq": myMidTONE[1], "reps": 1, "delay": delay1, "muteDelay": muteDelay1},
            {"freq": myMidTONE[2], "reps": 1, "delay": delay1, "muteDelay": muteDelay1},
            {"freq": myMidTONE[3], "reps": 1, "delay": delay1, "muteDelay": muteDelay1},
            {"freq": myMidTONE[1], "reps": 1, "delay": delay1, "muteDelay": muteDelay1},

            {"freq": myMidTONE[1], "reps": 1, "delay": delay1, "muteDelay": muteDelay1},
            {"freq": myMidTONE[2], "reps": 1, "delay": delay1, "muteDelay": muteDelay1},
            {"freq": myMidTONE[3], "reps": 1, "delay": delay1, "muteDelay": muteDelay1},
            {"freq": myMidTONE[1], "reps": 1, "delay": delay1, "muteDelay": muteDelay1},

            {"freq": myMidTONE[3], "reps": 1, "delay": delay1, "muteDelay": muteDelay1},
            {"freq": myMidTONE[4], "reps": 1, "delay": delay1, "muteDelay": muteDelay1},
            {"freq": myMidTONE[5], "reps": 1, "delay": delay2, "muteDelay": muteDelay1},

            {"freq": myMidTONE[3], "reps": 1, "delay": delay1, "muteDelay": muteDelay1},
            {"freq": myMidTONE[4], "reps": 1, "delay": delay1, "muteDelay": muteDelay1},
            {"freq": myMidTONE[5], "reps": 1, "delay": delay2, "muteDelay": muteDelay1},

            ################################

            {"freq": myMidTONE[5], "reps": 1, "delay": delay_2, "muteDelay": muteDelay1},
            {"freq": myMidTONE[6], "reps": 1, "delay": delay_2, "muteDelay": muteDelay1},
            {"freq": myMidTONE[5], "reps": 1, "delay": delay_2, "muteDelay": muteDelay1},
            {"freq": myMidTONE[4], "reps": 1, "delay": delay_2, "muteDelay": muteDelay1},
            {"freq": myMidTONE[3], "reps": 1, "delay": delay1, "muteDelay": muteDelay1},
            {"freq": myMidTONE[1], "reps": 1, "delay": delay1, "muteDelay": muteDelay1},

            {"freq": myMidTONE[5], "reps": 1, "delay": delay_2, "muteDelay": muteDelay1},
            {"freq": myMidTONE[6], "reps": 1, "delay": delay_2, "muteDelay": muteDelay1},
            {"freq": myMidTONE[5], "reps": 1, "delay": delay_2, "muteDelay": muteDelay1},
            {"freq": myMidTONE[4], "reps": 1, "delay": delay_2, "muteDelay": muteDelay1},
            {"freq": myMidTONE[3], "reps": 1, "delay": delay1, "muteDelay": muteDelay1},
            {"freq": myMidTONE[1], "reps": 1, "delay": delay1, "muteDelay": muteDelay1},

            {"freq": myMidTONE[1], "reps": 1, "delay": delay1, "muteDelay": muteDelay1},
            {"freq": myBassTONE[5], "reps": 1, "delay": delay1, "muteDelay": muteDelay1},
            {"freq": myMidTONE[1], "reps": 1, "delay": delay2, "muteDelay": muteDelay1},

            {"freq": myMidTONE[1], "reps": 1, "delay": delay1, "muteDelay": muteDelay1},
            {"freq": myBassTONE[5], "reps": 1, "delay": delay1, "muteDelay": muteDelay1},
            {"freq": myMidTONE[1], "reps": 1, "delay": delay2, "muteDelay": muteDelay1},
        ]

        self._myTone.playToneList(tone3Tigers)
        self._myTone.stopTone()

    def run(self):
        self._sndTone3Tigers()
        GPIO.cleanup()

if __name__ == "__main__":
    demo().run()
    print("Tone player demo is end.")

