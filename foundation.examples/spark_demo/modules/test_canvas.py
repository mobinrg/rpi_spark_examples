# RPiSpark Screen Draw Test
# 
# Author: Kunpeng Zhang
# 2018.4.11
# 2018.5.02
#
# See LICENSE for details.


import random
from math import sin
from PIL import Image
from PIL import ImageFont
from time import sleep
from JMRPiFoundations.skeleton.JMRPiSparkModule import SparkModuleBase

DEF_FONT = ImageFont.load_default()

class TestCanvas(SparkModuleBase):
    myScreen = None

    def getColor(self, colorMode ):
        if "RGB" == colorMode:
            return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        if "1" == colorMode:
            return random.randint(0, 1)

    def drawText(self, screen, fillColor):
            sW, sH = screen.getDisplaySize()
            # Write two lines of text.
            tX = random.randint(0, (sW-10))
            tY = random.randint(0, (sH-10))
            if random.randint(0, 1) == 1:
                screen.Canvas.text((tX, tY),  "Hello World!",  font=DEF_FONT, fill=fillColor)
            else:
                screen.Canvas.text((tX, tY), "Welcome ", font=DEF_FONT, fill=fillColor)

    def drawShape(self, screen ):
        sW, sH = screen.getDisplaySize()
        shape = random.randint(0, 7)
    #     shape = 7
        xy = [
                random.randint(0, sW),
                random.randint(0, sH),
                random.randint(0, sW),
                random.randint(0, sH)
            ]
        width = random.randint(0, 10)
        fill = self.getColor( screen._buffer_color_mode )
        outline = self.getColor(  screen._buffer_color_mode  )
    
        #arc(xy, start, end, fill=None)
        if 0 == shape:
            screen.Canvas.arc(xy, random.randint(0, 180), random.randint(0, 180), fill)
            return
        
        #chord(xy, start, end, fill=None, outline=None)
        if 1 == shape:
            screen.Canvas.chord(xy, random.randint(0, 180), random.randint(0, 180), fill, outline)
            return
        
        #ellipse(xy, fill=None, outline=None)
        if 2 == shape:
            screen.Canvas.ellipse(xy, 0, outline)
            return
        
        #line(xy, fill=None, width=0)
        if 3 == shape:
            screen.Canvas.line(xy, fill, width)
            return
        
        #pieslice(xy, start, end, fill=None, outline=None)
        if 4 == shape:
            screen.Canvas.pieslice(xy, random.randint(0, 180), random.randint(0, 180), fill, outline)
            return
        #point(xy, fill=None)
        if 5 == shape:
            screen.Canvas.point(xy, fill)
            return
        #rectangle(xy, fill=None, outline=None)
        if 6 == shape:
            screen.Canvas.rectangle(xy, fill, outline)
            return
        
        #draw TEXT
        if 7 == shape: 
            self.drawText(screen, fill)
            return
        
    def drawEllipse(self, screen):
        outline = self.getColor(  screen._buffer_color_mode  )
        for x in range(2, 64, 4):
            screen.Canvas.arc( (64 - x,32 - x, 64 + x, 32 + x), 0, 360, 1)
            screen.refresh()
            #################################
            # Button status read
            #
            if self._readExitButtonStatus(): return True

        sleep(1)

        for x in reversed(range(2, 64, 4)):
            screen.Canvas.arc( (64 - x,32 - x, 64 + x, 32 + x), 0, 360, 0)
            screen.refresh()
            #################################
            # Button status read
            #
            if self._readExitButtonStatus(): return True
            
        return False

    def drawLine(self, screen):
        outline = self.getColor(  screen._buffer_color_mode  )
        for y in range(0, 64, 5):
            screen.Canvas.line( (0,0, 128, y ), 1, 1)
            screen.refresh()
            #################################
            # Button status read
            #
            if self._readExitButtonStatus(): return True

        for x in reversed(range(0, 128, 5)):
            screen.Canvas.line( (0,0, x, 64 ), 1, 1)
            screen.refresh()
            #################################
            # Button status read
            #
            if self._readExitButtonStatus(): return True

        for x in range(0, 128, 5):
            screen.Canvas.line( (0,0, x, 64 ), 0, 1)
            screen.refresh()
            #################################
            # Button status read
            #
            if self._readExitButtonStatus(): return True

        for y in reversed(range(0, 64, 5)):
            screen.Canvas.line( (0,0, 128, y ), 0, 1)
            screen.refresh()
            #################################
            # Button status read
            #
            if self._readExitButtonStatus(): return True
            
        return False
            
    def drawTwinArc(self, screen):
        for x in range(2, 64, 4):
            screen.Canvas.arc( (64 - x, 0 - x, 64 + x, 0 + x), 0, 180, 1)
            screen.Canvas.arc( (64 - x, 64 - x, 64 + x, 64 + x), 180, 0, 1)
            screen.refresh()
            #################################
            # Button status read
            #
            if self._readExitButtonStatus(): return True
        sleep(1)
        for x in reversed(range(2, 64, 4)):
            screen.Canvas.arc( (64 - x, 0 - x, 64 + x, 0 + x), 0, 180, 0)
            screen.Canvas.arc( (64 - x, 64 - x, 64 + x, 64 + x), 180, 0, 0)
            screen.refresh()
            #################################
            # Button status read
            #
            if self._readExitButtonStatus(): return True

        return False
            
    def drawSineWave(self, screen):
        screen.clear()
        screen.Canvas.line( (0,0, 0, 64 ), 1, 1)
        screen.Canvas.line( (0,32, 128, 32 ), 1, 1)
        screen.refresh()

        for x in range(0, 128, 1):
            xt = x / 3.14159
            y = sin( xt * 0.4 ) * 24
            screen.Canvas.point( (x, y + 32), 1)
            screen.refresh()
            #################################
            # Button status read
            #
            if self._readExitButtonStatus(): return True
            
        for x in range(0, 128, 1):
            xt = x / 3.14159
            y = sin( xt * 0.4 ) * 24
            y2 = sin( xt * 0.4 + 4 ) * 24
            screen.Canvas.point( (x, y + 32), 0)
            screen.Canvas.point( (x, y2 + 32), 1)
            screen.refresh()
            #################################
            # Button status read
            #
            if self._readExitButtonStatus(): return True
            
        return False

    def setup(self):
        random.seed()
        self.myScreen = self._RPiSpark.Screen
        self.myScreen.clearCanvas()
        self.myScreen.refresh()

    #Test canvas
    def run(self):
        print("Press button A and Joy Up to exit testting ...")
        self._initKeyButtons("QUERY")

        drawMode = 0
        while True:
            #################################
            # Button status read
            #
            if self._readExitButtonStatus(): break

            if drawMode == 0: 
                isBreak = self.drawEllipse(self.myScreen)
                if isBreak: break

            if drawMode == 1:
                isBreak = self.drawLine(self.myScreen)
                if isBreak: break

            if drawMode == 2:
                isBreak = self.drawTwinArc(self.myScreen)
                if isBreak: break

            if drawMode == 3:
                isBreak = self.drawSineWave(self.myScreen)
                sleep(0.2)
                self.myScreen.clear()
                if isBreak: break

            if drawMode>4 and drawMode < 100:
                self.drawShape(self.myScreen)
                self.myScreen.refresh()
            elif drawMode > 100:
                self.myScreen.clear()
                self.drawText( self.myScreen, self.getColor( self.myScreen._buffer_color_mode ) )
                self.myScreen.refresh()
                sleep(0.3)

            drawMode += 1 
            if drawMode > 120:
                drawMode = 0;
                self.myScreen.clear()
