import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw

from JMRPiSpark.Drives.Screen.SScreenSSD1306 import SScreenSSD1306

########################################################################
# Display PINs  SPI_0
# SSD1306 OLED 128x64
class CONFIG_DSP:
    DSP_RESET       = None
    DSP_DC          = 9  #use MISO for DC
    DSP_SPI_PORT    = 0
    DSP_SPI_DEVICE  = 0
    DSP_SPI_MAX_SPEED_HZ = 2000000  #up to 8500000

    #Screen color mode BW
    SCREEN_BUFFER_COLOR_MODE_BW = "1"
    #Screen direction [0, 90, 180, 270]
    SCREEN_ROTATING = 180

class demo:
    _myScreen = None
    _myDSP = None

    def __init__(self):
        #create display
        self._myDSP = Adafruit_SSD1306.SSD1306_128_64(
            rst = CONFIG_DSP.DSP_RESET, 
            dc = CONFIG_DSP.DSP_DC, 
            spi = SPI.SpiDev(
                    CONFIG_DSP.DSP_SPI_PORT, 
                    CONFIG_DSP.DSP_SPI_DEVICE, 
                    max_speed_hz=CONFIG_DSP.DSP_SPI_MAX_SPEED_HZ
                )
            )
        # initialize display
        self._myDSP.begin()

        #create screen
        self._myScreen = SScreenSSD1306(
            self._myDSP, 
            bufferSize=(128,64),
            bufferColorMode = CONFIG_DSP.SCREEN_BUFFER_COLOR_MODE_BW, 
            displayDirection = CONFIG_DSP.SCREEN_ROTATING
        )
        # clear up screen
        self._myScreen.clear()
        self._myScreen.refresh()

    def run(self):
        self._myScreen.write("Hi\nRPi-Spark", xy=(0,0), fontName="Roboto-Light.ttf", fontSize=26  )
        self._myScreen.refresh()

if __name__ == "__main__":
    print("Adafruit SSD1306 drive demo ...")
    demo().run()