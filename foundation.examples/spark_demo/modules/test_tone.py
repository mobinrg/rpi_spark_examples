# -*- coding: utf-8 -*-
# RPiSpark Tone Testting
# 
# Author: Kunpeng Zhang
# 2018.5.30
#
# See LICENSE for details.


import random
import os.path
from PIL import Image
from PIL import ImageFont
from time import sleep

from JMRPiFoundations.Skeleton.RPiSparkModule import RPiSparkModule
from JMRPiSpark.Drives.Audio.RPiTone import RPiTonePlayer

###################################
# Font 
#
FONT_NAME = "AHandMadeFont.ttf"
FONT_SIZE = 28

class TestTone(RPiSparkModule):
    myScreen = None
    
    def drawToneMode(self, y, toneMode):
        font = ImageFont.truetype(FONT_NAME, FONT_SIZE)
        fw, fh = font.getsize(toneMode)
        self.myScreen.Canvas.rectangle( (0, y, 128, y + fh + 5), fill= 0, outline= 0)
        self.myScreen.Canvas.text( ((128-fw)/2, y), toneMode, font=font, fill= 1)

    def _sndTone(self):
        myTone = RPiTonePlayer( self._RPiSparkConfig.SPEAKER )
        tones = [ 20, 46, 69, 105, 160, 244, 371, 565, 859, 1300, 1980 ]
        for t in tones:
            myTone.playTone( t, 1, 0.2, 0 )
#             print(t)
        myTone.stopTone()

    def setup(self):
        random.seed()
        self.myScreen = self._RPiSpark.Screen

    #Test display
    def run(self):
        self.myScreen.clearCanvas()
        self.drawToneMode(10, "Tone")
        self.myScreen.refresh()

        self._sndTone()
        print("Tone testting done.")
