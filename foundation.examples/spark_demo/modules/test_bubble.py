# RPiSpark Testting Menu List
# 
# Author: Kunpeng Zhang
# 2018.4.10
#
# See LICENSE for details.


BUBBLE_R_MIN = 0.3
BUBBLE_R_MAX = 1.5
BUBBLE_OFFSET = BUBBLE_R_MAX * 1.5
BUBBLE_AMOUNT = 30

class Bubble():
    r = BUBBLE_R_MIN
    x = 0
    y = 0
    vx = 0
    vy = 0
    def __init__(self, scrWidth = 32, scrHeight = 32):
        if random.randint(0,30) % 3 == 0:
            self.r = random.random()
        self.x = random.randint(0,scrWidth)
        self.y = random.randint(0,scrHeight)

    def getPos(self):
        return self.x, self.y

import random
import pygame
from PIL import Image
from time import sleep
from JMRPiFoundations.skeleton.JMRPiSparkModule import SparkModuleBase
from JMRPiFoundations.utiles.JMSampleFilters import JMSample3AxisMAFilter

class TestBubble(SparkModuleBase):
    myScreen = None
    myAttitude = None
    myKeyboard = None
    mySampleFilter = None

    def setup(self):
        random.seed()
        self.myScreen = self._RPiSpark.Screen
        self.myKeyboard = self._RPiSpark.Keyboard
        self.myAttitude = self._RPiSpark.Attitude

        # Open attitude with all sensor ( accel, gyro, temp )
        # self.myAttitude.open()

        # Open attitude only accel sensor
        self.myAttitude.openWith( accel = True, gyro = False, temp = False, cycle = False )

        self.mySampleFilter = JMSample3AxisMAFilter(15)

        #change display buffer color mode to mono
        self.myScreen.changeBufferColorMode("1")
        self.myScreen.Display.on()
        self.myScreen.Display.setContrast( 0xA0 )
        self.myScreen.clearCanvas()
        self.clock = pygame.time.Clock()

    #Run Bubble
    def run(self):
        print("Press button A and Joy Up to exit testting ...")
        self._initKeyButtons("QUERY")

        bubbleList = []
        sW, sH = self.myScreen.getDisplaySize()
        for i in range( 0, BUBBLE_AMOUNT ):
            bubbleList.append( Bubble( sW, sH ) )

        while True:
            #################################
            # Button status read
            #
            if self._readExitButtonStatus(): break
            self.clock.tick(26)

            rawAccel = self.myAttitude.getAccelData( raw = False )
            maAccel = self.mySampleFilter.addSampleValue( rawAccel["x"], rawAccel["y"], rawAccel["z"] )
            if maAccel == None: continue

            offsetX = round( maAccel["x"], 1 )
            offsetY = round( maAccel["y"], 1 )
            offsetZ = round( maAccel["z"], 1 )

            self.myScreen.clearCanvas()
            for bubble in bubbleList:
                bubble.vx = offsetX * random.random() * -1
                bubble.vy = offsetY * random.random() # * 0.5
                bubble.x += bubble.vx
                bubble.y += bubble.vy

                if bubble.y > sH:
                    bubble.r = random.uniform (BUBBLE_R_MIN, BUBBLE_R_MAX)
                    bubble.y = -BUBBLE_OFFSET - bubble.r
                elif bubble.y < 0:
                    bubble.r = random.uniform(BUBBLE_R_MIN, BUBBLE_R_MAX)
                    bubble.y = sH + BUBBLE_OFFSET + bubble.r
                elif bubble.x > sW:
                    bubble.r = random.uniform(BUBBLE_R_MIN, BUBBLE_R_MAX)
                    bubble.x = -BUBBLE_OFFSET - bubble.r
                elif bubble.x < 0:
                    bubble.r = random.uniform(BUBBLE_R_MIN, BUBBLE_R_MAX)
                    bubble.x = sW + BUBBLE_OFFSET + bubble.r

                x,y = bubble.getPos()
                self.myScreen.Canvas.ellipse((x-bubble.r, y-bubble.r, x+bubble.r, y+bubble.r), fill=1 )

            self.myScreen.refresh()

        self._releaseKeyButtons()  #reset keyboard int
        print("Bubble testting done.")
