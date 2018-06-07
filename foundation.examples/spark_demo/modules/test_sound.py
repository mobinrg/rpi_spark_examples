# RPiSpark Testting Menu List
# 
# Author: Kunpeng Zhang
# 2018.4.12
#
# See LICENSE for details.


import random
import os.path
import pygame
from pygame.locals import *
from PIL import Image
from PIL import ImageFont
from time import sleep
from JMRPiFoundations.skeleton.JMRPiSparkModule import SparkModuleBase
from modules.spark_module_helper import drawBtn
from modules.spark_module_helper import drawText

###################################
# Font 
#
FONT_NAME = "AHandMadeFont.ttf"
FONT_SIZE = 28

###################################
# Sound Resources 
#
SOUND_SUNNY = {
    "title":"Sunny farm",
    "bg": "bird.ogg", 
    "something": [
        "cat.ogg",
        "sheep.ogg",
        "woodpecker.ogg",
        "chick.ogg",
        "hens.ogg",
        "cock02.ogg",
        "dogs.ogg"
        ]
    }

SOUND_RAIN = {
    "title":"Rain",
    "bg": "rain_far.ogg", 
    "something": ["thunder.ogg"]
    }

SOUND_CITY = {
    "title":"City",
    "bg": "city_sound.ogg", 
    "something": [
        "bike_move.ogg",
        "bike_whistle.ogg",
        "moto_engine2.ogg",
        "traffic_jam.ogg",
        "bike_whistle_2.ogg",
        "car_engine.ogg"
        ]
    }

SOUND_ENV = [SOUND_SUNNY, SOUND_RAIN, SOUND_CITY]
SOUND_MODE_SUNNY = 0
SOUND_MODE_RAIN = 1
SOUND_MODE_CITY = 2

ACTION_NONE = 0
ACTION_EXIT = 100
ACTION_SWITCH_SOUND_MODE = 1

class TestSound(SparkModuleBase):
    myScreen = None
    myKeyboard = None
    myAudio = None
    mySoundMode = 0
    _actStatus = 0
    
    def _keyButtonDown(self, channel):
        if channel == self._RPiSparkConfig.BUTTON_ACT_A:
            self._actStatus = ACTION_SWITCH_SOUND_MODE
            return
 
        if channel == self._RPiSparkConfig.BUTTON_ACT_B:
            self._actStatus = ACTION_EXIT
            return

    def getSoundFilePath(self, filename):
        return os.path.abspath(os.path.join('music/', filename))

    def playBgMusic(self, bgFilename, curFadeout = 1000 ):
        if curFadeout>0:
            pygame.mixer.music.fadeout(curFadeout)
        track = pygame.mixer.music.load(bgFilename)
        pygame.mixer.music.play()

    def _soundStop(self, channel):
        print("Sound playing done.", channel)

    def playSomething(self, filename, volume, fadeout):
        track1= pygame.mixer.Sound(filename)
        channel = track1.play()
        if channel is not None:
            rvol, lvol =  volume
            channel.set_volume(rvol, lvol)
    
        if fadeout!=None and fadeout>0:
            channel.fadeout(fadeout)

        return channel

    def getRandomSomethingConfig(self, soundMode):
        fileIndex = random.randint(0, len(SOUND_ENV[soundMode]["something"])-1 )
        fadeout = random.randint(0, 10) % 5 == 0
        return {
                "volume":( random.randint(0, 10) * 0.1, random.randint(0, 10) * 0.1 ),
                "fadeout": random.randint(0, 8000) if fadeout == True else None,
                "filename": SOUND_ENV[soundMode]["something"][ fileIndex ]
                }

    def changeSoundMode(self, newSoundMode, channel ):
        channel.stop()
        self.playBgMusic( self.getSoundFilePath(SOUND_ENV[newSoundMode]["bg"]) )

    def drawButtons(self, x, y, aTitle="", bTitle="", aState=0, bState=0):
        draw = self.myScreen.Canvas
        drawBtn(draw, x=x, y=y, outline=255, fill=aState, dire="a")
        drawText(draw, x=x+22, y=y, title="MODE")
    
        bX = x+72
        drawBtn(draw, x=bX, y=y, outline=255, fill=bState, dire="b")
        drawText(draw, x=bX+22, y=y,title="EXIT")
    
    def drawSoundMode(self, y, soundMode):
        font = ImageFont.truetype(FONT_NAME, FONT_SIZE)
        modeTitle = SOUND_ENV[soundMode]["title"]
        fw, fh = font.getsize(modeTitle)
        self.myScreen.Canvas.rectangle( (0, y, 128, y + fh + 5), fill= 0, outline= 0)
        self.myScreen.Canvas.text( ((128-fw)/2, y), modeTitle, font=font, fill= 1)

    def setup(self):
        pygame.mixer.init()
        random.seed()
        self.myScreen = self._RPiSpark.Screen
        self.myKeyboard = self._RPiSpark.Keyboard
        self.myAudio = self._RPiSpark.Audio
        self.mySoundMode = random.randint(0, len(SOUND_ENV)-1)

    #Test Sound
    def run(self):
        self._initKeyButtons("INT")
        self.myAudio.on()
        somethingConfig = self.getRandomSomethingConfig(self.mySoundMode)
        myChannel = self.playSomething( self.getSoundFilePath(somethingConfig["filename"]), 
                                       somethingConfig["volume"], 
                                       somethingConfig["fadeout"])
        self.myScreen.clearCanvas()
        self.drawButtons( x=10, y=48, aTitle="Mode", bTitle="Exit" )
        self.drawSoundMode( y=2, soundMode = self.mySoundMode )
        self.myScreen.refresh()

        self.playBgMusic( self.getSoundFilePath(SOUND_ENV[self.mySoundMode]["bg"]) )

        while True:
            if self._actStatus == ACTION_NONE:
                if pygame.mixer.music.get_busy() != True:
                    pygame.mixer.music.rewind()
                    pygame.mixer.music.play()
        
                if myChannel.get_busy() != True:
                    if random.randint(0, 100) % 25 == 0 :
                        somethingConfig = self.getRandomSomethingConfig(self.mySoundMode)
                        myChannel = self.playSomething( self.getSoundFilePath(somethingConfig["filename"]), 
                                                   somethingConfig["volume"], 
                                                   somethingConfig["fadeout"])
                        
                continue

            # Switch sound mode
            if self._actStatus == ACTION_SWITCH_SOUND_MODE:
                self._actStatus = ACTION_NONE
                self.mySoundMode = self.mySoundMode + 1 if self.mySoundMode<len(SOUND_ENV)-1 else 0
                self.drawSoundMode( y=2, soundMode = self.mySoundMode) 
                self.changeSoundMode(self.mySoundMode, myChannel)
                self.myScreen.refresh()
                continue

            # Exit
            if self._actStatus == ACTION_EXIT: 
                break

        myChannel.stop()
        pygame.mixer.music.stop()
        self._releaseKeyButtons()  #reset keyboard int
        self.myAudio.off()
        print("Sound playback example done.")
