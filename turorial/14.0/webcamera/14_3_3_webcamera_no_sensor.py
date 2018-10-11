from JMRPiFoundations.Skeleton.RPiSparkModule import RPiSparkModule
from os import curdir, sep, path
import sys

from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from SensorDataPool import SensorDataPool 

SENSOR_DATA_POOL = SensorDataPool( interval = 4, imagePath = "./", enableBMP=False )

PORT_NUMBER = 8080
FILENAME_INDEX_HTML = "index.html"

class WebRequestHandler(BaseHTTPRequestHandler):

    def sendData(self):
        outputPage = None
        if self.path=="/":
            self.path= FILENAME_INDEX_HTML
            template = open( curdir + sep + self.path ).read()
            outputData = SENSOR_DATA_POOL.sensorData
            outputPage = template.format( outputData["image"] )

        try:
            print(FILENAME_INDEX_HTML)
            print(curdir + self.path, "index.html")
            print("load file: ",self.path)
            
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            
            if outputPage != None:
                self.wfile.write(outputPage)
            else:
                # Send the html message
                f = open( curdir + sep + self.path )
                self.wfile.write(f.read())
                f.close()

        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)

    def do_GET(self):
        """
            Handler for the GET requests
        """
        self.sendData()
        return

class WebCamera(RPiSparkModule):
    WebServer = None
    
    def onKeyButtonUp(self, channel):
        if channel == self.RPiSparkConfig.BUTTON_ACT_A:
            self.stopWebCamera()
            sys.exit()

    def stopWebCamera(self):
        print('\nShutting down the WebCamera server')
        self.releaseKeyButtons()
        SENSOR_DATA_POOL.stop()
        self.WebServer.socket.close()

    def setup(self):
        # setup all key buttons to INT mode, same time query work fine
        self.initKeyButtons("INT")

    def run(self):
        SENSOR_DATA_POOL.start()

        # Drawing the ball on the screen
        self.RPiSpark.Screen.clear()
        tip = "RPi-Spark WebCapture\nPORT: {}\nQuit: Ctrl + C  or\n      Button A".format(PORT_NUMBER)
        self.RPiSpark.Screen.write(tip, xy=(4,4), spacing=2)
        self.RPiSpark.Screen.refresh()

        try:
            #Create a web server and define the handler to manage the
            #incoming request
            self.WebServer = HTTPServer(('', PORT_NUMBER), WebRequestHandler)
            print('Started WebCamera httpserver on port: ', PORT_NUMBER)
            print('------------------------------------------------------------')
            print('Quit: Ctrl + C  or  Button A')

            #Wait forever for incoming htto requests
            self.WebServer.serve_forever()

        except KeyboardInterrupt:
            self.stopWebCamera()