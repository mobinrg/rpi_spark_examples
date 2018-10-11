from JMRPiFoundations.Skeleton.RPiSparkModule import RPiSparkModule
from PIL import ImageFont
from Ball import Ball

DEF_FONT = ImageFont.load_default()

class BallBox(RPiSparkModule):
    ball = None
    velocity = None

    def _drawVel(self):
        self.RPiSpark.Screen.Canvas.rectangle( (2, 2, 38, 16), 0, 0 )
        self.RPiSpark.Screen.write("VEL:{:1d}".format( self.velocity ), xy=(0,4))

    def _changeVel(self, offsetVel):
        """
        Change velocity of ball move
        offsetVel can be > 0 to increase velocity or < 0 to reduce velocity
        velocity is limited between 1 and 9, default: 3
        """
        self.velocity += offsetVel
        if self.velocity < 1:
            self.velocity = 1

        if self.velocity > 9:
            self.velocity = 9

    def _keyButtonUp(self, channel):
        # Press SW_A to reduce velocity
        if channel == self.RPiSparkConfig.BUTTON_ACT_A:
           self._changeVel(-1)
           return

        # Press SW_B to increase velocity
        if channel == self.RPiSparkConfig.BUTTON_ACT_B:
           self._changeVel(1)
           return

    def setup(self):
        self.velocity = 3
        self.ball = Ball(64, 32, 5)
        # setup all key buttons to INT mode, same time query work fine
        self.initKeyButtons("INT")

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
            self._drawVel()
            self.RPiSpark.Screen.Canvas.ellipse( self.ball.getXY(), 1, 1 )
            self.RPiSpark.Screen.refresh()

        print("BallBox is done.")