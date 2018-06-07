# -*- coding: utf-8 -*-
# RPiSpark OS Info
#
# Author: Kunpeng Zhang
# 2018.5.31
#
# See LICENSE for details.


import os.path
import threading
from PIL import ImageFont
from PIL import Image
from time import sleep

from JMRPiFoundations.skeleton.JMRPiSparkModule import SparkModuleBase
from JMRPiFoundations.utiles.JMOSInfo import JMOSInfo

class TestOSInfo(SparkModuleBase):
    myScreen = None
    # Load default font.
    myFont = None
    myTime = None
    myOS = None
    
    _info_new = False
    _info_disk = None
    _info_mem = None
    _info_cpu = None
    _info_cpu_usage = None
    _info_ip = None

    def _callbackTimer(self):
        self._getOSInfo()

        self.myTime = threading.Timer(5.5, self._callbackTimer)
        self.myTime.start()

    def _getOSInfo(self):
        self._info_disk = self.myOS.getDiskUsage("/")
        self._info_mem = self.myOS.getMemUsage()
        self._info_cpu = self.myOS.getCPUInfo()
        self._info_cpu_usage = self.myOS.getCPUsage()
        self._info_ip = self.myOS.getIPAddr()
        self._info_new = True

    def displayData(self, x, y, data, title=""):
        draw = self.myScreen.Canvas
        fw, fh = self.myFont.getsize(title.upper())
        prec = 0

        draw.text((x,y), title.upper(), font=self.myFont, fill= 1 )
        if isinstance(data, str):
            draw.text((x + fw, y ), '{}'.format(data), font=self.myFont, fill= 1)
            return

        if isinstance(data, float):
            draw.text((x + fw, y), '{:.{prec}%}'.format(data, prec=prec), font=self.myFont, fill= 1)
            return
            
        if isinstance(data, int):
            draw.text((x + fw, y), '{}'.format(data), font=self.myFont, fill= 1)
            return
        
        if isinstance(data, dict):
            draw.text((x,y+ fh), '{} : {:.{prec}f}'.format('x', data["x"], prec=prec), font=self.myFont, fill= 1) 
            draw.text((x,y+ fh * 2), '{} : {:.{prec}f}'.format('y', data["y"], prec=prec), font=self.myFont, fill= 1)
            draw.text((x,y+ fh * 3), '{} : {:.{prec}f}'.format('z', data["z"], prec=prec), font=self.myFont, fill= 1)
            return

    def setup(self):
        self.myScreen = self._RPiSpark.Screen
        self.myFont = ImageFont.load_default()

    #Test OS Info
    def run(self):
        print("Press button A and Joy Up to exit testting ...")
        self._initKeyButtons("QUERY")

        self.myScreen.clearCanvas()
        self.displayData(20,28, "Loading ...", "")
        self.myScreen.refresh()

        self.myOS = JMOSInfo()
        self.myTime = threading.Timer(1, self._callbackTimer)
        self.myTime.start()

        while True:
            #################################
            # Button status read
            #
            if self._readExitButtonStatus(): break
            
            if self._info_new:
                self.myScreen.clearCanvas()
                self.displayData(0,0, self._info_cpu["hardware"] + "(" + str(self._info_cpu["processor"]) + ")", "CPU: ")
                self.displayData(102,0, self._info_cpu_usage, "")
                
                self.displayData(0,16, self.myOS.bytes2Human(self._info_disk["total"] * 1000), "HDD: ")
                self.displayData(56,16, self.myOS.bytes2Human(self._info_disk["used"] * 1000), "/ ")
                self.displayData(102,16, self._info_disk["usage"], "")
                
                self.displayData(0,32, self.myOS.bytes2Human(self._info_mem["total"] * 1000), "MEM: ")
                self.displayData(56,32, self.myOS.bytes2Human(self._info_mem["used"] * 1000), "/ ")
                self.displayData(102,32, self._info_mem["usage"], "")
        
                self.displayData(0,48, self._info_ip[0], " IP: ")
                self.myScreen.refresh()
                self._info_new = False

        self.myTime.cancel()
        print("OS information done.")
