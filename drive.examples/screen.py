# -*- coding: utf-8 -*-
#
# JMRPi.Spark Screen Demo
#
# Author: Kunpeng Zhang
# 2018.6.6
#
# See LICENSE for details.

import random
import os.path
import spidev
from PIL import Image
from PIL import ImageFont
from time import sleep
from math import sin
from JMRPiDrives.display.JMRPiDisplay_SSD1306 import SSD1306_128x64
from JMRPiDrives.screen.JMRPiScreen_SSD1306 import SScreenSSD1306

###################################
# Font 
#
FONT_NAME = "AHandMadeFont.ttf"
FONT_SIZE = 22

# DEF_FONT = ImageFont.load_default()
DEF_FONT = ImageFont.truetype(FONT_NAME, FONT_SIZE)

########################################################################
# Display PINs  SPI_0
# SSD1306 OLED 128x64
#
class CONFIG_DSP:
    DSP_RESET       = None
    DSP_DC          = 9  #use MISO for DC
    DSP_SPI_PORT    = 0
    DSP_SPI_DEVICE  = 0
    DSP_SPI_MAX_SPEED_HZ = 2000000  #up to 8500000

    #Display mirror
    DSP_MIRROR_H    = True
    DSP_MIRROR_V    = True
    
    # Screen rotating, can be choose in [ 0, 90, 180, 270 ]
    SCREEN_ROTATING = 0
    # Screen buffer color mode, can be choose in [ "1", "RGB" ]
    SCREEN_BUFFER_COLOR_MODE_RGB = "RGB"
    SCREEN_BUFFER_COLOR_MODE_BW = "1"

class demo:
    _myScreen = None

    def __init__(self):
        #open spi bus
        spi = spidev.SpiDev()
        spi.open( CONFIG_DSP.DSP_SPI_PORT, CONFIG_DSP.DSP_SPI_DEVICE)
        spi.max_speed_hz = CONFIG_DSP.DSP_SPI_MAX_SPEED_HZ
        spi.cshigh = False
        spi.mode = 0
        #create display 
        SSD1306 = SSD1306_128x64 ( 
            spi,  
            spiDC = CONFIG_DSP.DSP_DC,
            spiReset = CONFIG_DSP.DSP_RESET,
            mirrorH = CONFIG_DSP.DSP_MIRROR_H, 
            mirrorV = CONFIG_DSP.DSP_MIRROR_V
            )

        SSD1306.init()
        SSD1306.on()
        
        self._myScreen = SScreenSSD1306( 
                SSD1306, 
                bufferColorMode = CONFIG_DSP.SCREEN_BUFFER_COLOR_MODE_BW, 
                displayDirection = CONFIG_DSP.SCREEN_ROTATING
            )

    def _setWhiteNoise(self):
        for p in range(0, len(self._myScreen.Display._buffer)):
            self._myScreen.Display._buffer[p] = random.randint( 0x00, 0xFF )

    def _setImage(self):
        images = ["example_b.png", "example_w.png"]
        imageFile = os.path.abspath(os.path.join('images', random.choice(images)))
        
        self._myScreen.redefineBuffer( Image.open(imageFile) )
        self._myScreen.refresh()

    def _drawSineWave(self, screen):
        screen.clear()
        screen.Canvas.line( (0,0, 0, 64 ), 1, 1)
        screen.Canvas.line( (0,32, 128, 32 ), 1, 1)
        screen.refresh()

        for x in range(0, 128, 1):
            xt = x / 3.14159
            y = sin( xt * 0.4 ) * 24
            screen.Canvas.point( (x, y + 32), 1)
            screen.refresh()
            
        for x in range(0, 128, 1):
            xt = x / 3.14159
            y = sin( xt * 0.4 ) * 24
            y2 = sin( xt * 0.4 + 4 ) * 24
            screen.Canvas.point( (x, y + 32), 0)
            screen.Canvas.point( (x, y2 + 32), 1)
            screen.refresh()
            
    def _drawText(self, screen, fillColor):
            sW, sH = screen.getDisplaySize()
            # Write two lines of text.
            tX = random.randint(0, (sW-50))
            tY = random.randint(0, (sH-20))
            if random.randint(0, 1) == 1:
                screen.Canvas.text((tX, tY),  "Hello World!",  font=DEF_FONT, fill=fillColor)
            else:
                screen.Canvas.text((tX, tY), "Welcome!", font=DEF_FONT, fill=fillColor)

    def run(self):
        random.seed()
        
        # Draw a sin curve
        print("Draw a sin curve")
        self._drawSineWave(self._myScreen)
        sleep(0.2)
        self._myScreen.clear()
        
        # Draw a text
        print("Draw a sin curve")
        self._drawText( self._myScreen, 1 )
        self._myScreen.refresh()
        sleep(2)
        
        # Blink Display
        print("Blink display testing ... ")
        sleep(1)
        for b in range(0, 5):
            self._myScreen.Display.off()
            sleep(0.1)
            self._myScreen.Display.on()
            sleep(0.2)
            
        # Reload image show to display
        print("Reload image to display ... ")
        self._setImage()
        sleep(2)

        print("Blank Noise testing ... ")
        # Blank Noise
        for b in range(0, 50):
            self._setWhiteNoise()
            self._myScreen.Display.display()

        # Show Image
        self._setImage()

        print("Adjust contrast testing ... ")
        # Change contrast 0 - 255
        for c in range( 0x00, 0xFF, 0x20 ):
            self._myScreen.Display.setContrast(c)
            sleep(0.1)

        for c in range( 0xFF, 0x00, -0x20 ):
            self._myScreen.Display.setContrast(c)
            sleep(0.1)

        sleep(2)
        print("Display power off")
        self._myScreen.clear()
        self._myScreen.Display.off()

if __name__ == "__main__":
    demo().run()
    print("Screen with SSD1306 demo is end.")