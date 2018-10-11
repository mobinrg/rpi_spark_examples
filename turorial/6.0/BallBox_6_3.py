from JMRPiFoundations.Skeleton.RPiSparkModule import RPiSparkModule
from Ball import Ball

class BallBox(RPiSparkModule):
    ball = None
    velocity = None

    def setup(self):
        self.velocity = 3
        self.ball = Ball(64, 32, 5)
        # setup all key buttons to query mode
        self.initKeyButtons("QUERY")

    def run(self):

        while True:

            # Check exit key status ( JOY_UP + SW_A )
            if self.readExitButtonStatus():
                break;

            # Move the ball up
            if self.readKeyButton(self.RPiSparkConfig.BUTTON_JOY_UP):
                self.ball.move(0, -self.velocity)

            # Move the ball down
            if self.readKeyButton(self.RPiSparkConfig.BUTTON_JOY_DOWN):
                self.ball.move(0, self.velocity)

            # Move the ball left
            if self.readKeyButton(self.RPiSparkConfig.BUTTON_JOY_LEFT):
                self.ball.move(-self.velocity, 0)

            # Move the ball right
            if self.readKeyButton(self.RPiSparkConfig.BUTTON_JOY_RIGHT):
                self.ball.move(self.velocity, 0)

            # Move the ball to center of screen
            if self.readKeyButton(self.RPiSparkConfig.BUTTON_JOY_OK):
                self.ball.reset()

            # Drawing the ball on the screen
            self.RPiSpark.Screen.clear()
            self.RPiSpark.Screen.Canvas.ellipse( self.ball.getXY(), 1, 1 )
            self.RPiSpark.Screen.refresh()

        print("BallBox is done.")