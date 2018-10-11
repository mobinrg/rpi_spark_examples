from JMRPiFoundations.Skeleton.RPiSparkModule import RPiSparkModule
from Ball import Ball

class BallBox(RPiSparkModule):
    ball = None

    def setup(self):
        self.ball = Ball(64, 32, 5)

    def run(self):
        self.RPiSpark.Screen.Canvas.ellipse( self.ball.getXY(), 1, 1 )
        self.RPiSpark.Screen.refresh()