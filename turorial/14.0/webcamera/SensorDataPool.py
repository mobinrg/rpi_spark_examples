import time
import threading

from picamera import PiCamera
from picamera import Color

FILENAME_CAPTURE_IMG = "foo.jpg"

class SensorDataPool:
    _interval = None
    _imagePath = None
    _timer = None
    _bmp085 = None
    _camera = None

    count = 0
    sensorData = None

    def __init__(self, interval = 2, imagePath = "./", enableBMP=True):
        self.sensorData = {}

        self._interval = interval
        self._imagePath = imagePath + FILENAME_CAPTURE_IMG
        
        if enableBMP: self._initBMPSensor()
        
        self._camera = PiCamera()
        self._camera.rotation = 90
        self._camera.preview_fullscreen=False
        # camera.preview_window=(0, 0, 800, 1066)
        self._camera.resolution = (640, 480)
        self._camera.annotate_text_size = 12
        self._camera.annotate_foreground = Color('white')
        #self._camera.annotate_background = Color('white')
        self._camera.start_preview()
        
    def _initBMPSensor(self):
        import Adafruit_BMP.BMP085 as BMP085 # Imports the BMP library
        self._bmp085 = BMP085.BMP085()

    def _callbackTimer(self):
        self.count = self.count + 1
        self._readSensorData()
        self._timer = threading.Timer(self._interval, self._callbackTimer)
        self._timer.start()

    def _captureImage(self):
        if self._bmp085!=None: 
            annotateText = u"{} | Temp: {:.1f} *C | Baro: {:.0f} hPa | Alt: {:.2f} m".format(
                self.sensorData["date"],
                self.sensorData["temp"],
                self.sensorData["baro"] / 100, 
                self.sensorData["alt"])
        else:
            annotateText = u"{}".format(self.sensorData["date"])

        self._camera.annotate_text = annotateText
        # Camera warm-up time
        self._camera.capture(self._imagePath)

    def _readSensorData(self):
        self.sensorData["date"] = time.strftime("%Y-%m-%d %a %H:%M:%S")
        if self._bmp085!=None:
            self.sensorData["temp"] = self._bmp085.read_temperature()
            self.sensorData["baro"] = self._bmp085.read_pressure()
            self.sensorData["alt"] = self._bmp085.read_altitude()

        self._captureImage();
        self.sensorData["image"] = self._imagePath
        #print(self.sensorData)
    
    def start(self):
        self._timer = threading.Timer( 1, self._callbackTimer )
        self._timer.start()

    def stop(self):
        self._timer.cancel()