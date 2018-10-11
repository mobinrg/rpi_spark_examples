import pygame
from pygame.locals import *
import os.path

MUSIC_FILE_BG = "Fantasy_Game_Background_Looping.mp3" # http://soundimage.org/fantasywonder/
MUSIC_FILE_COLLODE = "din4.ogg"

class MusicNote():
    track = None
    trackCh = None

    def __init__(self):
        pygame.init()
        pygame.mixer.init()

    def getMusicFile(self, filename):
        return os.path.abspath( os.path.join('music/', filename) )

    def playNote(self, vol = 0.2, fadeout = 500, note = MUSIC_FILE_COLLODE ):
        if self.trackCh == None:
            self.track = pygame.mixer.Sound(self.getMusicFile(note))
            self.trackCh = self.track.play()
        else:
            self.trackCh.stop()

        self.track.play()
        self.trackCh.set_volume( vol, vol)
        if fadeout!=None and fadeout>0:
            self.trackCh.fadeout(fadeout)

    def playBgMusic(self, bgFilename = MUSIC_FILE_BG ):
        pygame.mixer.music.load( self.getMusicFile(bgFilename) )
        pygame.mixer.music.play(-1)

    def stop(self):
        pygame.mixer.music.stop()
        if self.track != None:
            self.track.stop()