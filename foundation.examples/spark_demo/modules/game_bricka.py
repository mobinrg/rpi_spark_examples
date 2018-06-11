# -*- coding: utf-8 -*-
# RPiSpark Testting Game Bricka
#
# Author: Kunpeng Zhang
# 2018.4.19
#
# See LICENSE for details.


import random
import os.path
from time import sleep
from PIL import Image
from PIL import ImageFont
import pygame
from pygame.locals import *

from JMRPiFoundations.Skeleton.RPiSparkModule import RPiSparkModule
from JMRPiFoundations.Utiles.AvgCalculators import MovingAvgCalculator
from JMRPiFoundations.Utiles.OSInfo import OSInfo

from modules.spark_module_helper import drawText
from modules.spark_module_helper import drawMultiLineText

def getCPUCount():
    myOS = OSInfo()
    cpu_info = myOS.getCPUInfo()
    return cpu_info["processor"]

####################################
# Bricka
#
SCREEN_SIZE   = 128,64

# Object dimensions
BRICK_MARGINS_Y = 11
BRICK_MARGINS_X = 8
BRICK_ROWS = 6
BRICK_COLS = 8
BRICK_WIDTH   = 12
BRICK_HEIGHT  = 1
PADDLE_WIDTH  = 24
PADDLE_HEIGHT = 3
BALL_DIAMETER = 4
BALL_RADIUS   = BALL_DIAMETER / 2
BALL_VEL = 3 if getCPUCount() == 1 else 2

MAX_PADDLE_X = SCREEN_SIZE[0] - PADDLE_WIDTH
MAX_BALL_X   = SCREEN_SIZE[0] - BALL_DIAMETER
MAX_BALL_Y   = SCREEN_SIZE[1] - BALL_DIAMETER

# Paddle Y coordinate
PADDLE_Y = SCREEN_SIZE[1] - PADDLE_HEIGHT - 2

# Color constants
BLACK = 1
WHITE = 1
BLUE  = 1
BRICK_COLOR = 1

# State constants
STATE_BALL_IN_PADDLE = 0
STATE_PLAYING = 1
STATE_WON = 2
STATE_GAME_OVER = 3

# http://soundimage.org/fantasywonder/
MUSIC_BG_FILE = "Fantasy_Game_Background_Looping.mp3"
class MusicNote():

    def getNoteFile(self, note):
        return os.path.abspath(os.path.join('music/notes/', note + ".wav"))

    def getBgFile(self, filename):
        return os.path.abspath( os.path.join('music/bg/', filename) )

    def getRandomNoteConfig(self):
        fadeout = random.randint(0, 10) % 5 == 0
        return {
            "volume":( random.randint(0, 10) * 0.1, random.randint(0, 10) * 0.1 ),
            "fadeout": random.randint(0, 8000) if fadeout == True else None,
        }

    def playNote(self, note, volume, fadeout):
        filename = self.getNoteFile(note)
        track1= pygame.mixer.Sound(filename)
        channel = track1.play()
        if channel is not None:
            rVol, lVol =  volume
            channel.set_volume(rVol, lVol)

            if fadeout!=None and fadeout>0:
                channel.fadeout(fadeout)

        return channel

    def playBgMusic(self, bgFilename ):
        pygame.mixer.music.load( bgFilename )
        pygame.mixer.music.play(-1)

class TestGameBricka(RPiSparkModule):
    myScreen = None
    myAudio = None
    myAttitude = None
    lastAccelMA_X = None

    myMusicNote = None
    myMusicChannel = None

    def _keyButtonDown(self, channel):
        if channel == self._RPiSparkConfig.BUTTON_ACT_A:
            if self.state == STATE_BALL_IN_PADDLE:
                self.ball_vel = [ BALL_VEL, -BALL_VEL ]
                self.state = STATE_PLAYING
                return

        if self.state == STATE_GAME_OVER or self.state == STATE_WON:
            self.init_game()
            return

#         if channel == self._RPiSparkConfig.BUTTON_JOY_UP:
#             self._viewer_fov += 8 if self._viewer_fov < 128 else 128
#             return
#
#         if channel == self._RPiSparkConfig.BUTTON_JOY_DOWN:
#             self._viewer_fov -= 8 if self._viewer_fov > 0 else 0
#             return

    def init_game(self):
        self.lives = 3
        self.score = 0
        self.state = STATE_BALL_IN_PADDLE

        self.paddle   = pygame.Rect( 0, PADDLE_Y, PADDLE_WIDTH, PADDLE_HEIGHT )
        self.ball     = pygame.Rect( 0, PADDLE_Y - BALL_DIAMETER, BALL_DIAMETER, BALL_DIAMETER )

        self.ball_vel = [ BALL_VEL, -BALL_VEL ]
        self.create_bricks()

    def create_bricks(self):
        y_ofs = BRICK_MARGINS_Y
        self.bricks = []
        for i in range( BRICK_ROWS ):
            x_ofs = BRICK_MARGINS_X
            for j in range( BRICK_COLS ):
                self.bricks.append( {"rect":pygame.Rect( x_ofs, y_ofs, BRICK_WIDTH, BRICK_HEIGHT ), "note":str(j)} )
                x_ofs += BRICK_WIDTH + 2
            y_ofs += BRICK_HEIGHT + 2

    def draw_bricks(self):
        for brick in self.bricks:
            brickXY = ( brick["rect"].left, brick["rect"].top, brick["rect"].right, brick["rect"].bottom)
            self.myScreen.Canvas.rectangle( brickXY, BRICK_COLOR, 1 )

    def check_input(self):
        accelV = self.myAttitude.getAccelData( raw = False )
        self.paddle.left -= accelV["x"] * 2

        if self.paddle.left <= 0:
            self.paddle.left = 0

        if self.paddle.left > MAX_PADDLE_X:
            self.paddle.left = MAX_PADDLE_X
        pass

    def move_ball(self):
        self.ball.left += self.ball_vel[0]
        self.ball.top  += self.ball_vel[1]

        if self.ball.left <= 0:
            self.ball.left = 0
            self.ball_vel[0] = -self.ball_vel[0]
        elif self.ball.left >= MAX_BALL_X:
            self.ball.left = MAX_BALL_X
            self.ball_vel[0] = -self.ball_vel[0]

        if self.ball.top < 0:
            self.ball.top = 0
            self.ball_vel[1] = -self.ball_vel[1]
        elif self.ball.top >= MAX_BALL_Y:
            self.ball.top = MAX_BALL_Y
            self.ball_vel[1] = -self.ball_vel[1]

    def handle_collisions(self):
        for brick in self.bricks:
            if self.ball.colliderect(brick["rect"]):
                self.score += 3
                self.ball_vel[1] = -self.ball_vel[1]
                self.bricks.remove(brick)

                #Play music note
                config = self.myMusicNote.getRandomNoteConfig()
                if self.myMusicChannel != None and self.myMusicChannel.get_busy() == True:
                    self.myMusicChannel.stop()
                self.myMusicChannel = self.myMusicNote.playNote( brick["note"], config["volume"], config["fadeout"] )

                break

        if len(self.bricks) == 0:
            self.state = STATE_WON

        if self.ball.colliderect(self.paddle):
            self.ball.top = PADDLE_Y - BALL_DIAMETER
            self.ball_vel[1] = -self.ball_vel[1]
        elif self.ball.top > self.paddle.top:
            self.lives -= 1
            if self.lives > 0:
                self.state = STATE_BALL_IN_PADDLE
            else:
                self.state = STATE_GAME_OVER

    def show_stats(self):
        if self.font:
            txt = " LIVES: " + str(self.lives) + " SCORE: " + str(self.score)
            self.myScreen.Canvas.text( (0, 0 ), txt.upper(),  font=self.font, fill= 1 )
            pass

    def show_message( self, message ):
        if self.font:
            fw, fh = self.myScreen.Canvas.multiline_textsize( message, self.font )
            x = (SCREEN_SIZE[0] - fw) / 2
            y = (SCREEN_SIZE[1] - fh) / 2

            self.myScreen.Canvas.rectangle( (x - 2, y, x + fw + 2, y + fh), 1, 1 )
            self.myScreen.Canvas.multiline_text(
                (x, y) ,
                message,
                font = self.font,
                align="center",
                fill=0)
            pass

    def setup(self):
        random.seed()
        self.myMusicNote = MusicNote()
        self.myScreen = self._RPiSpark.Screen
        self.myAudio = self._RPiSpark.Audio
        self.myAttitude = self._RPiSpark.Attitude
        self.myAttitude.openWith( accel = True, gyro = False, temp = False, cycle = False )

        pygame.init()
        self.font = ImageFont.load_default()
        self.clock = pygame.time.Clock()
        self.init_game()

    #Test display
    def run(self):
        self.myAudio.on()
        pygame.mixer.init()
        self.lastAccelMA_X = MovingAvgCalculator(15)
        self._initKeyButtons("INT")

        self.myMusicNote.playBgMusic( self.myMusicNote.getBgFile( MUSIC_BG_FILE ) )

        while 1:
            #################################
            # Button status read
            # Button A + Joy Up to quit game
            if self._readExitButtonStatus(): break

            self.clock.tick(36)
            self.myScreen.clear()
            if self.check_input() == False: continue

            self.draw_bricks()

            # Draw paddle
            paddleXY = (self.paddle.left, self.paddle.top, self.paddle.right, self.paddle.bottom)
            self.myScreen.Canvas.rectangle( paddleXY, BRICK_COLOR, 0 )

            # Draw ball
            ballXY = (self.ball.left, self.ball.top, self.ball.right, self.ball.bottom)
            self.myScreen.Canvas.ellipse( ballXY, BRICK_COLOR, 1 )

            self.show_stats()

            if self.state == STATE_PLAYING:
                self.move_ball()
                self.handle_collisions()
            elif self.state == STATE_BALL_IN_PADDLE:
                self.ball.left = self.paddle.left + self.paddle.width / 2
                self.ball.top  = self.paddle.top - self.ball.height
                self.show_message("Press button A to\nlaunch the ball")
            elif self.state == STATE_GAME_OVER:
                self.show_message("GAME OVER!\nPress Button A \nto play again")
            elif self.state == STATE_WON:
                self.show_message("YOU WON!\nPress Button A \nto play again")

            self.myScreen.refresh()

        self._releaseKeyButtons()  #reset keyboard int
        pygame.mixer.music.stop()
        self.myAudio.off()
