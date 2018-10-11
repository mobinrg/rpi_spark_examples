import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306 as SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

########################################################################
# Display PINs  SPI_0
# SSD1306 OLED 128x64
class CONFIG_DSP:
    DSP_RESET       = None
    DSP_DC          = 9  #use MISO for DC
    DSP_SPI_PORT    = 0
    DSP_SPI_DEVICE  = 0
    DSP_SPI_MAX_SPEED_HZ = 2000000  #up to 8500000

class demo:
    _myDSP = None
    _myDSP_IMG = None
    _myCanvas = None

    def __init__(self):
        #create display
        self._myDSP = SSD1306.SSD1306_128_64(
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
        self._myDSP.clear()
        self._myDSP.display()
        
        # create display buffer iamge.
        self._myDSP_IMG = Image.new( '1', (self._myDSP.width, self._myDSP.height) )
        # create drawing object to draw on image.
        self._myCanvas = ImageDraw.Draw(self._myDSP_IMG)

    def _saySomething(self, x, y, fontName, fontSize, msg ):
        try:
            font = ImageFont.truetype(fontName, fontSize)
        except:
            font = ImageFont.load_default()

        self._myCanvas.text((x, y), msg, font=font, fill=1)
        self._myDSP.image(self._myDSP_IMG)
        self._myDSP.display()

    def run(self):        
        self._saySomething( 8,4, "Roboto-Light.ttf", 26, "Hi")
        self._saySomething( 8,32, "Roboto-Light.ttf", 26, "RPi-Spark")

if __name__ == "__main__":
    print("Adafruit SSD1306 drive demo ...")
    demo().run()