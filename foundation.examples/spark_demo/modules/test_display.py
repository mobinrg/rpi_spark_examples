# RPiSpark Testting Menu List
# 
# Author: Kunpeng Zhang
# 2018.4.11
#
# See LICENSE for details.


import random
import os.path
from PIL import Image
from time import sleep
from JMRPiFoundations.skeleton.JMRPiSparkModule import SparkModuleBase

class TestDisplay(SparkModuleBase):
    mySCREEN = None
    myDSP = None

    def _setWhiteNoise(self):
        for p in range(0, len(self.myDSP._buffer)):
            self.myDSP._buffer[p] = random.randint( 0x00, 0xFF )

    def _setImage(self):
        images = ["example_b.png", "example_w.png"]
        imageFile = os.path.abspath(os.path.join('images', random.choice(images)))
        self.myDSP.setImage( Image.open( imageFile ).convert('1') )
        self.myDSP.display()

    def setup(self):
        random.seed()
        self.myDSP = self._RPiSpark.Screen.Display
        self.mySCREEN = self._RPiSpark.Screen

    #Test display
    def run(self):
        # Blank Noise
        for b in range(0, 50):
            self._setWhiteNoise()
            self.myDSP.display()
            
        # Show Image
        self._setImage()

        # Change contrast 0 - 255
        for c in range( 0x00, 0xFF, 0x20 ):
            self.myDSP.setContrast(c)
            sleep(0.1)

        for c in range( 0xFF, 0x00, -0x20 ):
            self.myDSP.setContrast(c)
            sleep(0.1)

#         # Scroll Left
#         self.myDSP.scrollWith(
#             hStart = 0, 
#             hEnd = 7, 
#             vOffset = 0,
#             vStart = 0,
#             vEnd = 64,
#             int = 0,
#             dire = "left" 
#         )
#         sleep(5)
#         # Scroll Right
#         self.myDSP.scrollWith(
#             hStart = 0, 
#             hEnd = 7, 
#             vOffset = 0,
#             vStart = 0,
#             vEnd = 64,
#             int = 0,
#             dire = "right" 
#         )
#         sleep(5)
#         # Scroll Up
#         self.myDSP.scrollWith(
#             hStart = 0, 
#             hEnd = 0, 
#             vOffset = 4,
#             vStart = 0,
#             vEnd = 64,
#             int = 0,
#             dire = "left" 
#         )
#         sleep(5)
#         # Scroll Down
#         self.myDSP.scrollWith(
#             hStart = 0, 
#             hEnd = 0, 
#             vOffset = -4,
#             vStart = 0,
#             vEnd = 64,
#             int = 0,
#             dire = "left" 
#         )
#         sleep(5)
# 
#         self.myDSP.scrollOff()

        # Blink Display
        sleep(1)
        for b in range(0, 5):
            self.myDSP.off()
            sleep(0.1)
            self.myDSP.on()
            sleep(0.2)

        self.myDSP.off()
        print("Display testting done.")
