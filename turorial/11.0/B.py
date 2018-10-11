from JMRPiFoundations.Skeleton.RPiSparkModule import RPiSparkModule
from time import sleep

class B(RPiSparkModule):

    def drawTwinArc(self, screen):
        screen.clear()
        for x in range(2, 64, 4):
            screen.Canvas.arc( (64 - x, 0 - x, 64 + x, 0 + x), 0, 180, 1)
            screen.Canvas.arc( (64 - x, 64 - x, 64 + x, 64 + x), 180, 0, 1)
            screen.refresh()
        sleep(1)
        for x in reversed(range(2, 64, 4)):
            screen.Canvas.arc( (64 - x, 0 - x, 64 + x, 0 + x), 0, 180, 0)
            screen.Canvas.arc( (64 - x, 64 - x, 64 + x, 64 + x), 180, 0, 0)
            screen.refresh()

    def setup(self):
        self.initKeyButtons("QUERY")

    def run(self):
        self.drawTwinArc(self.RPiSpark.Screen)