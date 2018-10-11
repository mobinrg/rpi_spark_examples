from JMRPiFoundations.Skeleton.RPiSparkModule import RPiSparkModule
from PIL import Image
from time import sleep
import os.path

ANIMATION_IMG_FILE = "flower_small.jpg"
class ScrViewAnimation(RPiSparkModule):
    def _loadImage(self, filename):
        img_path = os.path.abspath(os.path.join('images/', filename))
        return Image.open(img_path)

    def setup(self):
        self.RPiSpark.Screen.redefineBuffer( self._loadImage( ANIMATION_IMG_FILE ) )
    
    def run(self):        
        for row in range(0, 8):
            for col in range(0,4):
                self.RPiSpark.Screen.View.moveTo(col * 128, row * 72 )
                self.RPiSpark.Screen.refresh()
                sleep(0.02)

        sleep(2)

        for row in range(7, -1, -1):
            for col in range(3, -1, -1):
                self.RPiSpark.Screen.View.moveTo(col * 128, row * 72 )
                self.RPiSpark.Screen.refresh()
                sleep(0.05)