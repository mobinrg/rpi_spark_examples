
# eye
# pupil
# Upper eyelid
# Lower eyelid
# nose
# mouth
# Upper lip
# Lower lip
# eyebrow

from JMRPiSpark.Drives.Screen.SScreen import SSRect

class Organ:
    # Screen Canvas
    _cavas = None
    # SSRect class
    _ssrect = None
    _ssrect_last = None

    def __init__(self, cavas, x, y, width, height):
        self._cavas = cavas
        self._ssrect = SSRect(x, y, width, height)
        self._ssrect_last = SSRect(x, y, width, height)

    def rest(self):
        self._ssrect_last = SSRect( self._ssrect.x, self._ssrect.y, self._ssrect.height, self._ssrect.width )

    def draw(self):
        raise NotImplementedError

class Eye(Organ):
    closedEye = False
    def draw(self):
        self._cavas.ellipse( self._ssrect.rectToArray(), 1 if closedEye!=False else 0, 1 )

class Eyelid(Organ):
    openPercent = 1
    def draw(self):
        self._cavas.ellipse( self._ssrect.rectToArray(), 1 , 0 )

class Pupil(Organ):
    def draw(self):
        self._cavas.ellipse( self._ssrect.rectToArray(), 0 , 0 )

class Nose(Organ):
    pass

class Lip(Organ):
    pass

class Eyebrow(Organ):
    pass


class SmileFace:
    pass