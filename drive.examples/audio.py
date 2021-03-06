# -*- coding: utf-8 -*-
#
# RPi.Spark Audio Play Demo
#
# Author: Kunpeng Zhang
# 2018.6.6
#
# See LICENSE for details.

import random
import os.path
import pygame
from pygame.locals import *
from time import sleep
import RPi.GPIO as GPIO

from JMRPiSpark.Drives.Audio.RPiAudio import RPiAudioDevice

SOUND_MUSIC = [ "erhu.ogg", "piano.ogg" ]

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
    _count = 0
    _myAudio = None

    def __init__(self):
        self._myAudio = RPiAudioDevice( CONFIG_AUDIO.AUDIO_R, CONFIG_AUDIO.AUDIO_L )

    def _getSoundFilePath(self, filename):
        return os.path.abspath(os.path.join('music/', filename))

    def _playMusic(self, sndFile, volume = 1.0):
        track = pygame.mixer.music.load( sndFile )
        if track is not None:
            rvol, lvol =  volume
            track.set_volume(rvol, lvol)

        pygame.mixer.music.play()

    def run(self):
        pygame.mixer.init()
        random.seed()
        self._myAudio.on()

        fileIndex = random.randint(0, len( SOUND_MUSIC ) - 1)
        self._playMusic( self._getSoundFilePath( SOUND_MUSIC[fileIndex] ) )

        while True:
            if self._count > 15: break
            sleep(1)
            self._count += 1
            pass

        pygame.mixer.music.stop()
        self._myAudio.off()

if __name__ == "__main__":
    demo().run()
    print("Audio player demo is end.")