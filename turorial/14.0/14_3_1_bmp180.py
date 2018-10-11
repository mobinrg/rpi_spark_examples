from JMRPiFoundations.Skeleton.RPiSparkModule import RPiSparkModule
import Adafruit_BMP.BMP085 as BMP085 # Imports the BMP library

class BMP180(RPiSparkModule):
    BMPSensor = None
    
    def setup(self):
        # Create an 'object' containing the BMP180 data
        self.BMPSensor = BMP085.BMP085()

    def run(self):
        self.RPiSpark.Screen.write('BMP-180 sensor', xy=(0,4), screenCenter=True)
        dataTxt = "Temp: {0:0.2f} C\nBaro: {1:0.2f} Pa\n Alt: {2:0.2f} m".format(
            self.BMPSensor.read_temperature(),
            self.BMPSensor.read_pressure(),
            self.BMPSensor.read_altitude())

        self.RPiSpark.Screen.write(dataTxt, xy=(12,26), spacing=1)

        # Draw a 2 pixels width line
        self.RPiSpark.Screen.Canvas.line( (12, 20, 116, 20), 1, 3 )        
        self.RPiSpark.Screen.refresh()