# -*- coding: utf-8 -*-
#
# RPiSpark Demo Menu List
# 
# Author: Kunpeng Zhang
# 2018.4.11
# 2018.6.7
#
# See LICENSE for details.


import random
import os.path
import RPi.GPIO as GPIO
from PIL import Image
from PIL import ImageFont
from time import sleep

#Submodules
from JMRPiFoundations.Skeleton.RPiSparkModule import RPiSparkModule

from modules.test_display import TestDisplay
from modules.test_buttons import TestButtons
from modules.test_bubble import TestBubble
from modules.test_attitude import TestAttitude
from modules.test_image_scroll import TestImageScroll
from modules.test_canvas import TestCanvas
from modules.dialog_screen import DialogScreen
from modules.dialog_screen import DialogConst
from modules.test_keycallback import TestKeyCallback
from modules.welcome_screen import TestWelcome
from modules.test_sim3d import TestSim3D
from modules.game_bricka import TestGameBricka
from modules.game_3d_starfield import Test3DStarfield
from modules.test_os_info import TestOSInfo
from modules.test_sound import TestSound
from modules.test_tone import TestTone

###################################
# Font 
#
FONT_NAME = "Roboto-Light.ttf"
FONT_SIZE = 12

###################################
# Action 
#
ACTION_NONE         = 0
ACTION_DRAW_MENU    = 1
ACTION_RUN_MODULE   = 2
ACTION_RETURN_MENU  = 3
ACTION_MENU_NEXT    = 4
ACTION_MENU_PREV    = 5
ACTION_EXIT         = 100

##########################################
# Menu Items
#
class MenuItems:
    MENU_ITEMS = [
            { "id": 100, "icon":"display.png", "title":"Display", "info":"" },
            { "id": 101,"icon":"button.png", "title":"Buttons", "info":""  },
            { "id": 102,"icon":"image.png", "title":"Image Scroll", "info":""  },
            { "id": 103,"icon":"canvas.png", "title":"Canvas Draw", "info":""  },
            { "id": 104,"icon":"sim3d.png", "title":"3D Sim", "info":"" },
            { "id": 106,"icon":"attitude.png", "title":"Attitude", "info":""  },
            { "id": 107,"icon":"sound_wave.png", "title":"Sound", "info":""  },
            { "id": 112,"icon":"sound_tone.png", "title":"Tone", "info":""  },
            { "id": 125,"icon":"os.png", "title":"OS Info", "info":""  },
            { "id": 105,"icon":"bubb.png", "title":"Bubble", "info":""  },
            { "id": 120,"icon":"bricka.png", "title":"Bricka", "info":""  },
            { "id": 121,"icon":"starfield.png", "title":"Starfield", "info":""  },
            { "id": 108,"icon":"about.png", "title":"About", "info":""  },
            { "id": 900,"icon":"exit.png", "title":"Exit", "info":""  }
        ]

    _menu_index = 0

    def __init__(self):
        self._menu_index = 0
    
    def previous(self):
        if self._menu_index > 0:
            self._menu_index -= 1
        return self.MENU_ITEMS[self._menu_index]

    def next(self):
        if self._menu_index < len(self.MENU_ITEMS)-1:
            self._menu_index += 1
        return self.MENU_ITEMS[self._menu_index]

    def curMenuItem(self):
        return self.MENU_ITEMS[self._menu_index]
    
    def curMenuItemIndex(self):
        return self._menu_index


##########################################
# Menu List Module
#
class TestMenuList(RPiSparkModule):
    myScreen = None
    myKeyboard = None
    myMenuItems = None

    _actStatus = ACTION_NONE
    
    def _sndFinish(self):
        self._beepTone(5, 0.05)

    ##########################################
    # Key Buttons Process
    #
    def _keyButtonUp(self, channel):
        if channel == self._RPiSparkConfig.BUTTON_ACT_A:
            self._actStatus = ACTION_NONE
            return

        if channel in (self._RPiSparkConfig.BUTTON_ACT_B, self._RPiSparkConfig.BUTTON_JOY_OK):
            self._actStatus = ACTION_RUN_MODULE
            return

        if channel == self._RPiSparkConfig.BUTTON_JOY_UP:
            self._actStatus = ACTION_MENU_PREV
            return

        if channel == self._RPiSparkConfig.BUTTON_JOY_DOWN:
            self._actStatus = ACTION_MENU_NEXT
            return

        self._actStatus = ACTION_NONE        

    ##########################################
    # Menu Item Draw
    #
    def getIconFilePath(self, filename):
        return os.path.abspath(os.path.join('images/icon/', filename))
    
    def drawMenuItem(self, menuItem):
        iconW = 96; iconH = 54
        titleW = 128; titleH = 10
        
        icon = Image.open( self.getIconFilePath( menuItem["icon"] ))
        icon = icon.resize((iconW,iconH))

        if icon != None:
            self.myScreen._buffer.paste(icon, (16, 0, 112, 54))

        # Load default font.
#         font = ImageFont.load_default()
        font = ImageFont.truetype(FONT_NAME, FONT_SIZE)
        fw, fh = font.getsize( menuItem["title"].upper() )
        tX = 0; tY = 54
        self.myScreen.Canvas.text((tX + ((titleW-fw)/2), tY + (titleH-fh)/2),  menuItem["title"].upper(),  font=font, fill= 1 )

    ##########################################
    # Sub Module Run 
    #
    def runTestModule(self, moduleID):
        #Display
        if moduleID == 100:
            myTestModule = TestDisplay( self._RPiSparkConfig, self._RPiSpark )
            myTestModule.run()
            return ACTION_RETURN_MENU
        
        #Buttons
        if moduleID == 101:
            myTestModule = TestButtons( self._RPiSparkConfig, self._RPiSpark )
            myTestModule.run()
            return ACTION_RETURN_MENU
        
        #Image Scroll
        if moduleID == 102:
            myTestModule = TestImageScroll( self._RPiSparkConfig, self._RPiSpark )
            myTestModule.run()
            return ACTION_RETURN_MENU
            
        #Canvas Draw
        if moduleID == 103:
            myTestModule = TestCanvas( self._RPiSparkConfig, self._RPiSpark )
            myTestModule.run()
            return ACTION_RETURN_MENU

        #3D sim
        if moduleID == 104:
            myTestModule = TestSim3D( self._RPiSparkConfig, self._RPiSpark )
            myTestModule.run()
            return ACTION_RETURN_MENU

        #Bubble
        if moduleID == 105:
            myTestModule = TestBubble( self._RPiSparkConfig, self._RPiSpark )
            myTestModule.run()
            return ACTION_RETURN_MENU
        
        #Attutude
        if moduleID == 106:
            myTestModule = TestAttitude( self._RPiSparkConfig, self._RPiSpark )
            myTestModule.run()
            return ACTION_RETURN_MENU

        #Sound
        if moduleID == 107:
            myTestModule = TestSound( self._RPiSparkConfig, self._RPiSpark )
            myTestModule.run()
            return ACTION_RETURN_MENU
        
        #Tone
        if moduleID == 112:
            myTestModule = TestTone( self._RPiSparkConfig, self._RPiSpark )
            myTestModule.run()
            return ACTION_RETURN_MENU
        
        #OS Info
        if moduleID == 125:
            myTestModule = TestOSInfo( self._RPiSparkConfig, self._RPiSpark )
            myTestModule.run()
            return ACTION_RETURN_MENU

        #About
        if moduleID == 108:
            myDialog = DialogScreen( self._RPiSparkConfig, self._RPiSpark )
            myDialog.fontName = FONT_NAME
            myDialog.fontSize = FONT_SIZE
            myDialog.showMessage("RPi Spark\nwww.mobinrg.com\nv 1.0.0\n(c) 2018.4", waitKey=True)
            return ACTION_RETURN_MENU

        #Exit
        if moduleID == 900:
            myDialog = DialogScreen( self._RPiSparkConfig, self._RPiSpark )
            myDialog.fontName = FONT_NAME
            myDialog.fontSize = FONT_SIZE
            isExit = myDialog.showYesNo("Are you sure\nto exit?")
            if isExit == DialogConst.DIALOG_BUTTON_YES:
                myDialog.showMessage("\nTestting\nis done.\n")
                return ACTION_EXIT
            return ACTION_RETURN_MENU

        #Test Game Bricka
        if moduleID == 120:
            myTestModule = TestGameBricka( self._RPiSparkConfig, self._RPiSpark )
            myTestModule.run()
            return ACTION_RETURN_MENU
        
        #Test Game Bricka
        if moduleID == 121:
            myTestModule = Test3DStarfield( self._RPiSparkConfig, self._RPiSpark )
            myTestModule.run()
            return ACTION_RETURN_MENU
        
        pass

    def setup(self):
        self.myMenuItems = MenuItems()
        self._actStatus = 1

        self.myScreen = self._RPiSpark.Screen
        self.myKeyboard = self._RPiSpark.Keyboard

        #change display buffer color mode to mono
        self.myScreen.changeBufferColorMode("1")
#         self.myScreen.Display.setContrast(self.dispContrast)        
        self.myScreen.clearCanvas()
        self.myScreen.refresh()
        self.myScreen.Display.on()

    #Test display
    def run(self):
        # First show welcome screen
        myTestModule = TestWelcome( self._RPiSparkConfig, self._RPiSpark )
        myTestModule.run()
        
        print("----------------------------------------------------------------")
        print("Select a module to test ...")
        print("Switch module: Joy Up and Down | Joy Left and Right    Run: button B")

        self._initKeyButtons()
        while True:                
            ####################################
            # Action impletment 
            #
            
            # Do nothing
            if self._actStatus == ACTION_NONE: continue

            #Exit
            if self._actStatus == ACTION_EXIT: break

            # Return menu item list
            if self._actStatus == ACTION_RETURN_MENU:
                print(" Return menu list ...")                
                #change display buffer color mode to mono
                self.myScreen.changeBufferColorMode("1")
                self.myScreen.Display.on()
                self.myScreen.Display.setContrast( 0xA0 )

                #Reconfig keyboard int
                self._initKeyButtons()
                self._actStatus = ACTION_DRAW_MENU
                continue
            
            # Run submoudle
            if self._actStatus == ACTION_RUN_MODULE:
                self._actStatus = ACTION_NONE
                self._releaseKeyButtons()  #reset keyboard int

                # do something for submodule ...
                menuItem = self.myMenuItems.curMenuItem()
                print(" Run [ {} ] module ...".format(menuItem["title"]) )
                nextAction = self.runTestModule( self.myMenuItems.curMenuItem()["id"] )
                if nextAction == ACTION_EXIT: break # exit testing
                self._actStatus = nextAction
#                 print("NEXT ACT: ", self._actStatus)
                continue

            # Previous Menu Item
            if self._actStatus == ACTION_MENU_PREV:
                self.myMenuItems.previous()
                self._actStatus = ACTION_DRAW_MENU
                self._beep()
                continue

            # Next Menu Item
            if self._actStatus == ACTION_MENU_NEXT:
                self.myMenuItems.next()
                self._actStatus = ACTION_DRAW_MENU
                self._beep()
                continue

            # Update menu item
            if self._actStatus == ACTION_DRAW_MENU:
                self.myScreen.clearCanvas()
                self.drawMenuItem( self.myMenuItems.curMenuItem() )
                self.myScreen.refresh()
                self._actStatus = ACTION_NONE
                continue

        self._releaseKeyButtons()
        self._sndFinish()
        GPIO.cleanup()
        print("\nTestting done.")
