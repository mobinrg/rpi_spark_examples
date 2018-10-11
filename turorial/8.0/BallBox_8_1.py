from JMRPiFoundations.Skeleton.RPiSparkModule import RPiSparkModule
from Ball import Ball
from JMRPiSpark.Drives.Audio.RPiTone import RPiTonePlayer

class BallBox(RPiSparkModule):
    ball = None
    damping = None
    tonePlayer = None

    def _drawVel(self):
        self.RPiSpark.Screen.Canvas.rectangle( (2, 2, 38, 16), 0, 0 )
        self.RPiSpark.Screen.write("DIS:{:1d}".format( self.damping ), xy=(0,4))

    def _changeDam(self, offsetVel):
        """
        Change damping of ball move
        offsetVel can be > 0 to increase damping or < 0 to reduce damping
        damping is limited between 0 and 9, default: 3
        """
        self.damping += offsetVel
        if self.damping < 0:
            self.damping = 0

        if self.damping > 9:
            self.damping = 9

    def onKeyButtonUp(self, channel):
        # Press SW_A to reduce damping
        if channel == self.RPiSparkConfig.BUTTON_ACT_A:
           self._changeDam(-1)
           return

        # Press SW_B to increase damping
        if channel == self.RPiSparkConfig.BUTTON_ACT_B:
           self._changeDam(1)
           return

    def setup(self):
        self.damping = 3
        self.ball = Ball(64, 32, 5)
        # setup all key buttons to INT mode, same time query work fine
        self.initKeyButtons("INT")
        # Open accel
        self.RPiSpark.Attitude.openWith(temp=True, accel=True, gyro=False)
        self.tonePlayer = RPiTonePlayer(self.RPiSparkConfig.SPEAKER, 10 )

    def run(self):

        vX = 0
        vY = 0
        fv = -3
        collideXY = 0
        lastCollideXY = 0

        while True:
            # Check exit key status ( JOY_UP + SW_A )
            if self.readExitButtonStatus():
                break;

            # Get Accel data from attitude sensor
            accelData = self.RPiSpark.Attitude.getAccelData()

            vX += accelData["x"]
            vY += accelData["y"]

            collideXY = self.ball.move( -vX, vY )
            
            if collideXY > 0:
                if collideXY in [1,2,5,6,9,10]:
                    vX += fv if vX > 0 else -fv
                    vX = -vX

                if collideXY in [4,8,5,6,9,10]:
                    vY += fv if vY > 0 else -fv
                    vY = -vY

                if collideXY in [1,2,4,8]:
                    if (lastCollideXY != collideXY) and (abs(vX) > 2 or abs(vY) > 2):
                        self.beepTone( note = 4 , delay=0.025, muteDelay=0.01, tonePlayer = self.tonePlayer)

            lastCollideXY = collideXY

            # Move the ball up
            if self.readKeyButton(self.RPiSparkConfig.BUTTON_JOY_UP):
                self.ball.move(0, -self.damping)

            # Move the ball down
            if self.readKeyButton(self.RPiSparkConfig.BUTTON_JOY_DOWN):
                self.ball.move(0, self.damping)

            # Move the ball left
            if self.readKeyButton(self.RPiSparkConfig.BUTTON_JOY_LEFT):
                self.ball.move(-self.damping, 0)

            # Move the ball right
            if self.readKeyButton(self.RPiSparkConfig.BUTTON_JOY_RIGHT):
                self.ball.move(self.damping, 0)

            # Move the ball to center of screen
            if self.readKeyButton(self.RPiSparkConfig.BUTTON_JOY_OK):
                self.ball.reset()
                # vX = 0
                # vY = 0

            # Drawing the ball on the screen
            self.RPiSpark.Screen.clear()
            self._drawVel()
            self.RPiSpark.Screen.Canvas.ellipse( self.ball.getXY(), 1, 1 )
            self.RPiSpark.Screen.refresh()

        self.releaseKeyButtons()
        print("BallBox is done.")