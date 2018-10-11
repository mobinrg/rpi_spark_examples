from JMRPiFoundations.Skeleton.RPiSparkModule import RPiSparkModule
from time import sleep

class A(RPiSparkModule):

    def drawEllipse(self, screen):
        screen.clear()
        outline = 1
        for x in range(2, 64, 4):
            screen.Canvas.arc( (64 - x,32 - x, 64 + x, 32 + x), 0, 360, 1)
            screen.refresh()

        sleep(1)

        for x in reversed(range(2, 64, 4)):
            screen.Canvas.arc( (64 - x,32 - x, 64 + x, 32 + x), 0, 360, 0)
            screen.refresh()

    def setup(self):
        self.initKeyButtons("QUERY")

    def run(self):
        self.drawEllipse(self.RPiSpark.Screen)