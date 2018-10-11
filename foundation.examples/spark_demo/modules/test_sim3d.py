# RPiSpark Testting Simulation 3D
# 
# Author: Kunpeng Zhang
# 2018.4.16
#
# Adapted from:
# http://codentronix.com/2011/05/12/rotating-3d-cube-using-python-and-pygame/
#
#
# See LICENSE for details.


import sys
import math
import pygame
import random
from JMRPiFoundations.Skeleton.RPiSparkModule import RPiSparkModule
from JMRPiFoundations.Utiles.DataFilters import Sample3AxisMAFilter

class Point3D:
    x = 0; y = 0; z = 0
    
    def __init__(self, x = 0, y = 0, z = 0):
        self.x, self.y, self.z = float(x), float(y), float(z)

    def rotateX(self, angle):
        """ Rotates the point around the X axis by the given angle in degrees. """
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        y = self.y * cosa - self.z * sina
        z = self.y * sina + self.z * cosa
        return Point3D(self.x, y, z)
 
    def rotateY(self, angle):
        """ Rotates the point around the Y axis by the given angle in degrees. """
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        z = self.z * cosa - self.x * sina
        x = self.z * sina + self.x * cosa
        return Point3D(x, self.y, z)
 
    def rotateZ(self, angle):
        """ Rotates the point around the Z axis by the given angle in degrees. """
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        x = self.x * cosa - self.y * sina
        y = self.x * sina + self.y * cosa
        return Point3D(x, y, self.z)
 
    def project(self, scrWidth, scrHeight, fov, viewerDistance):
        """ Transforms this 3D point to 2D using a perspective projection. """
        factor = fov / (viewerDistance + self.z)
        x = self.x * factor + scrWidth / 2
        y = -self.y * factor + scrHeight / 2
        return Point3D(x, y, 1)

DRAW_MODE_LINE          = 0
DRAW_MODE_LINE_BALL     = 1

class TestSim3D(RPiSparkModule):
    myScreen = None
    myAttitude = None
    
    # DRAW_MODE_LINE | DRAW_MODE_LINE_BALL
    _draw_mode = DRAW_MODE_LINE
    # 32 ~ 128
    _viewer_fov = 96
    # 2 ~ 10
    _viewer_distance = 6
    
    def onKeyButtonDown(self, channel):
        if channel == self.RPiSparkConfig.BUTTON_ACT_A:
            self._draw_mode = DRAW_MODE_LINE if self._draw_mode != DRAW_MODE_LINE else DRAW_MODE_LINE_BALL 
            return

        if channel == self.RPiSparkConfig.BUTTON_JOY_UP:
            self._viewer_fov += 8 if self._viewer_fov + 8 < 128 else 0
            return
        
        if channel == self.RPiSparkConfig.BUTTON_JOY_DOWN:
            self._viewer_fov -= 8 if self._viewer_fov - 8 > 0 else 0
            return

    def _initSimulation(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.vertices = [
            Point3D(-1,1,-1),
            Point3D(1,1,-1),
            Point3D(1,-1,-1),
            Point3D(-1,-1,-1),
            Point3D(-1,1,1),
            Point3D(1,1,1),
            Point3D(1,-1,1),
            Point3D(-1,-1,1)
        ]

        # Define the vertices that compose each of the 6 faces. These numbers are
        # indices to the vertices list defined above.
        self.faces = [(0,1,2,3),(1,5,6,2),(5,4,7,6),(4,0,3,7),(0,4,5,1),(3,2,6,7)]
        self.angleX, self.angleY, self.angleZ = 0, 0, 0

    def setup(self):
        self.myScreen = self.RPiSpark.Screen
        self.myAttitude = self.RPiSpark.Attitude
        self.myAttitude.openWith( accel = True, gyro = False, temp = False, cycle = False )

        self._initSimulation()
        self._draw_mode = random.randint(DRAW_MODE_LINE, DRAW_MODE_LINE_BALL)

    #Run 3d Sim
    def run(self):
        print("-----------------------------------------------------")
        print("Show mode: button A | Field of vision: Joy Up and Down | Exit: button A + Joy Up")

        self.initKeyButtons("INT")
        #change display buffer color mode to RGB
        self.myScreen.changeBufferColorMode("RGB")

        ScreenW, ScreenH = self.myScreen.Display.width, self.myScreen.Display.height
        myAccelFilter = Sample3AxisMAFilter(15)
        while True:
            accelV = self.myAttitude.getAccelData( raw = False )
            lastAccelMA = myAccelFilter.addSampleValue(accelV["x"], accelV["y"], accelV["z"])
            if lastAccelMA == None: continue

            #################################
            # Button status read
            #
            if self.readExitButtonStatus(): break

            self.clock.tick(36)
            self.myScreen.clear()

            # Will hold transformed vertices.
            t = []
            for v in self.vertices:
                # Rotate the point around X axis, then around Y axis, and finally around Z axis.
                r = v.rotateX(self.angleX).rotateY(self.angleY).rotateZ(self.angleZ)
                # Transform the point from 3D to 2D
                p = r.project(ScreenW, ScreenH, self._viewer_fov, self._viewer_distance)
                # Put the point in the list of transformed vertices
                t.append(p)

            for f in self.faces:
                self.myScreen.Canvas.line( ((t[f[1]].x, t[f[1]].y), (t[f[2]].x, t[f[2]].y)), (90,90,90), 1 )
                self.myScreen.Canvas.line( ((t[f[3]].x, t[f[3]].y), (t[f[0]].x, t[f[0]].y)), (90,90,90), 1 )

                if self._draw_mode == DRAW_MODE_LINE:
                    self.myScreen.Canvas.line( ((t[f[0]].x, t[f[0]].y), (t[f[1]].x, t[f[1]].y)), (255,255,255), 3 )
                    self.myScreen.Canvas.line( ((t[f[2]].x, t[f[2]].y), (t[f[3]].x, t[f[3]].y)), (255,255,255), 3 )

                # Draw vertice balls
                if self._draw_mode == DRAW_MODE_LINE_BALL:
                    self.myScreen.Canvas.ellipse( (t[f[3]].x - 3, t[f[3]].y - 3, t[f[3]].x + 3, t[f[3]].y + 3), 0, (255,255,255) )
                    self.myScreen.Canvas.ellipse( (t[f[0]].x - 3, t[f[0]].y - 3, t[f[0]].x + 3, t[f[0]].y + 3), 0, (255,255,255) )

            self.angleX -= round(lastAccelMA["y"], 1) * 1.5
            self.angleY += round(lastAccelMA["x"], 1) * 1.5
            # self.angleZ += round(lastAccelMA["z"], 1) * 2
            self.myScreen.refresh()

        self.releaseKeyButtons()  #reset keyboard int
