# RPiSpark 3D starfield
# 
# Author: Kunpeng Zhang
# 2018.5.04
#
#
#  3D Starfield Simulation
#  Developed by Leonel Machava <leonelmachava@gmail.com>
# 
#  http://codeNtronix.com
#  http://twitter.com/codentronix
#
#
# See LICENSE for details.


import pygame, math
from random import randrange
from random import randint
import os.path
from PIL import Image

from JMRPiFoundations.Skeleton.RPiSparkModule import RPiSparkModule
from JMRPiFoundations.Utiles.DataFilters import Sample3AxisMAFilter

STAR_NUM    = 120
STAR_DEPTH  = 96

class Test3DStarfield(RPiSparkModule):
    _star_num = 0
    _star_depth = 0
    _speed = 0
    _stars = None
    _clock = None

    myScreen    = None
    myAttitude  = None
    
    def onKeyButtonDown(self, channel):
        if channel == self.RPiSparkConfig.BUTTON_ACT_A:
#             self._draw_mode = DRAW_MODE_LINE if self._draw_mode != DRAW_MODE_LINE else DRAW_MODE_LINE_BALL 
            return

        if channel == self.RPiSparkConfig.BUTTON_JOY_UP:
            self._speed += 1 if self._speed + 1 < 9 else 0
            return
        
        if channel == self.RPiSparkConfig.BUTTON_JOY_DOWN:
            self._speed -= 1 if self._speed - 1 > 0 else 0
            return

    def initStars(self):
        self._stars = []
        for i in range(self._star_num):
            # A star is represented as a list with this format: [X,Y,Z]
            star = [randrange(-25,25), randrange(-25,25), randrange(1, self._star_depth)]
            self._stars.append(star)

    def drawStars(self, originX, originY, newDepth = None ):
        sW, sH = self.myScreen.getDisplaySize()
        for star in self._stars:
            star[2] -= self._speed

            if star[2] <= 0:
                star[0] = randrange(-25,25)
                star[1] = randrange(-25,25)
                star[2] = self._star_depth

            k = 128.0 / star[2]
            x = int(star[0] * k + originX)
            y = int(star[1] * k + originY)

            if 0 <= x < sW and 0 <= y < sH:
                size = (1 - float(star[2]) / self._star_depth) * 5
                if self._speed < 7:
                    self.myScreen.Canvas.ellipse((x,y,x+size,y+size), 1, 1)
                else:
                    k = 128 / ( star[2] + self._speed * randint(1,3) )
                    x0 = int(star[0] * k + originX)
                    y0 = int(star[1] * k + originY)
                    self.myScreen.Canvas.line((x0,y0, x,y), randint(0,1), randint(1,2))

    def setup(self):
        self.myScreen = self.RPiSpark.Screen
        self.myAttitude = self.RPiSpark.Attitude
        self.myAttitude.openWith( accel = True, gyro = False, temp = False, cycle = False )

        pygame.init()

        self._clock = pygame.time.Clock()
        self._star_num = STAR_NUM
        self._star_depth = STAR_DEPTH
        self._speed = 3
        self.initStars()

    #run
    def run(self):
        print("----------------------------------------------------------------")
        print("Starfield ...")
        print("Change Speed: Joy Up and Down    Exit: Joy Up and button A")
        self.initKeyButtons("INT")

        ScreenW, ScreenH = self.myScreen.Display.width, self.myScreen.Display.height
        originX = ScreenW / 2
        originY = ScreenH / 2
        myAccelFilter = Sample3AxisMAFilter(15)

        self.myScreen.clear()
        while True:
            accelV = self.myAttitude.getAccelData( raw = False )
            lastAccelMA = myAccelFilter.addSampleValue(accelV["x"], accelV["y"], accelV["z"])
            if lastAccelMA == None: continue

            angleX = math.atan2(lastAccelMA["x"], lastAccelMA["z"]) * (180/3.14);
            angleY = math.atan2(lastAccelMA["y"], lastAccelMA["z"]) * (180/3.14);

            self._clock.tick(32)
            #################################
            # Button status read
            #
            if self.readExitButtonStatus(): break

            #################################
            # Draw stars
            #
            offsetX = -round( angleX / 180, 2 )
            offsetY = round( angleY / 180, 2 )
            oX = originX + offsetX * originX
            oY = originY + offsetY * originY

            self.myScreen.clear()
            self.drawStars(oX, oY, None)
            self.myScreen.refresh()

        self.myAttitude.sleep()
        self.releaseKeyButtons()  #reset keyboard int
