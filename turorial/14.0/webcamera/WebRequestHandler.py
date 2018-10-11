from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer

PORT_NUMBER = 8080
FILENAME_INDEX_HTML = "index.html"

class WebRequestHandler(BaseHTTPRequestHandler):

    def sendData(self):
        outputPage = None
        if self.path=="/":
            self.path= FILENAME_INDEX_HTML
            template = open( curdir + sep + self.path ).read()
            outputData = SENSOR_DATA_POOL.sensorData
            outputPage = template.format(
                outputData["image"],
                outputData["date"],
                outputData["temp"], 
                outputData["baro"], 
                outputData["alt"])

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