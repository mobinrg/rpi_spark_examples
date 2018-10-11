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
        return Boolean, if 'True' means the ball collide side of screen
        """
        self.lastX += offsetX
        self.lastY += offsetY

        collideX = False
        if self.lastX < self.radius: 
            self.lastX = self.radius
            collideX = True

        if self.lastX > self.limitX:
            self.lastX = self.limitX
            collideX = True

        collideY = False
        if self.lastY < self.radius: 
            self.lastY = self.radius
            collideY = True

        if self.lastY > self.limitY:
            self.lastY = self.limitY
            collideY = True

        return collideX or collideY

    def getXY(self):
        """
        return coordinate of ball
        """
        return ( ( self.lastX - self.radius, self.lastY - self.radius ), ( self.lastX + self.radius, self.lastY + self.radius ) )