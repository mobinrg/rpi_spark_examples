from JMRPiFoundations.Skeleton.RPiSparkModule import RPiSparkModule
from time import sleep
import importlib

class Menu(RPiSparkModule):
    _runModule = None

    def drawMenuItem(self, x,y, menu_title, menu_desc):
        width = 16
        self.RPiSpark.Screen.Canvas.rectangle( (x, y, x + width, y + width), 0, 1 )
        self.RPiSpark.Screen.write(menu_title, xy=(x+6, y+3))
        self.RPiSpark.Screen.write(menu_desc, xy=(x + width + 8, y+3))

    def drawMenu(self):
        self.RPiSpark.Screen.clear()
        self.drawMenuItem(5, 10, "A", "One Wave")
        self.drawMenuItem(5, 32, "B", "Twin Waves")
        self.RPiSpark.Screen.refresh()

    def loadSpark(self, sparkName):
        try:
            SparkLib = importlib.import_module( sparkName, "package" )
        except Exception as err:
            print("ERR: {}\n".format(str(err)))
            return False
        
        try:
            SparkClass = getattr(SparkLib, sparkName)
            mySparkModule = SparkClass(self.RPiSparkConfig, self.RPiSpark)
            mySparkModule.run()
            return True
        except Exception as err:
            print("ERR: {}\n".format(str(err)))
            return False

    def onKeyButtonUp(self, channel):
        if self.RPiSparkConfig.BUTTON_ACT_A == channel: self._runModule = "A"
        if self.RPiSparkConfig.BUTTON_ACT_B == channel: self._runModule = "B"

    def setup(self):
        self.initKeyButtons("INT")

    def run(self):
        self.drawMenu()
        while True:
            #################################
            # Exit button status read
            #
            if self.readExitButtonStatus(): break

            #################################
            # Run Module
            #
            if self._runModule != None:
                if self.loadSpark( self._runModule ) == False:
                    print("Load {} module failed.".format(self._runModule))

                self._runModule = None
                self.drawMenu()

        self.releaseKeyButtons()
        self.RPiSpark.Screen.clear()
        self.RPiSpark.Screen.refresh()