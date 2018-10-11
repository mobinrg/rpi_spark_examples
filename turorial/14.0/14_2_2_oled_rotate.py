import random
import os.path
from time import sleep
from PIL import Image
import spidev
from JMRPiSpark.Drives.Display.SSD1306 import SSD1306_128x64

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
    DSP_MIRROR_H    = False
    DSP_MIRROR_V    = False

class demo:
    _myDSP = None

    def __init__(self):
        #open spi bus
        spi = spidev.SpiDev()
        spi.open( CONFIG_DSP.DSP_SPI_PORT, CONFIG_DSP.DSP_SPI_DEVICE)
        spi.max_speed_hz = CONFIG_DSP.DSP_SPI_MAX_SPEED_HZ
        spi.cshigh = False
        spi.mode = 0
        #create display 
        self._myDSP = SSD1306_128x64 ( 
            spi,
            spiDC = CONFIG_DSP.DSP_DC,
            spiReset = CONFIG_DSP.DSP_RESET,
            mirrorH = CONFIG_DSP.DSP_MIRROR_H, 
            mirrorV = CONFIG_DSP.DSP_MIRROR_V
            )

        # initialize display
        self._myDSP.init()
        # display trun on
        self._myDSP.on()

    def _setImage(self):
        images = ["example_b.png", "example_w.png"]
        imageFile = os.path.abspath(os.path.join('images', random.choice(images)))
        self._myDSP.setImage( Image.open( imageFile ).convert('1') )
        self._myDSP.display()

    def run(self):
        random.seed()            
        
        # Show Image
        self._setImage()
        
        sleep(5)
        # display turn Off
        print("Display power off")
        self._myDSP.off()

if __name__ == "__main__":
    demo().run()
    print("SSD1306 Display demo is end.")