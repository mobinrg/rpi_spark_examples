class Ball:
    limitX = None
    limitY = None
    defX = None
    defY = None
    radius = None
    lastX = None
    lastY = None

    def __init__(self, x, y, r, limitRange = (127, 63) ):
        self.defX = x
        self.defY = y
        self.radius = r

        self.limitX = limitRange[0] - self.radius
        self.limitY = limitRange[1] - self.radius

        self.lastX = x
        self.lastY = y

    def reset(self):
        """
        Move ball to center of screen
        """
        self.lastX = self.defX
        self.lastY = self.defY

    def move(self, offsetX, offsetY):
        """
        Move ball coordinate
        return Boolean, if '0' means the ball not collide side of screen
        return integer, 0x1: top, 0x2: bottom, 0x4: left, 0x8: right
        """
        self.lastX += offsetX
        self.lastY += offsetY

        collideX = 0x0
        if self.lastX < self.radius: 
            self.lastX = self.radius
            collideX = collideX | 0x1

        if self.lastX > self.limitX:
            self.lastX = self.limitX
            collideX = collideX | 0x2

        collideY = 0x0
        if self.lastY < self.radius: 
            self.lastY = self.radius
            collideY = collideY | 0x4

        if self.lastY > self.limitY:
            self.lastY = self.limitY
            collideY = collideY | 0x8

        return collideX | collideY

    def getXY(self):
        """
        return coordinate of ball
        """
        return ( ( self.lastX - self.radius, self.lastY - self.radius ), ( self.lastX + self.radius, self.lastY + self.radius ) )