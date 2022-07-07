from pygame.sprite import Sprite 
from pygame import Surface
from pygame import Rect

class RobotGUI(Sprite):
    """
    This class receives an instance of the Robot agent, and creates a Sprite for it 
    """ 
    def __init__(self, body, width=20, length=20): 
        self.body = body

        self.x = self.body.robX 
        self.y = self.body.robY

        self.width = width
        self.length = length

        self.surface = Surface((self.width, self.length))
        self.surface.fill((0, 100, 200))  
        self.rect = self.surface.get_rect(center=(self.x, self.y))


    def updateLoc(self): 
        self.x = self.body.robX
        self.y = self.body.robY
        self.rect = self.surface.get_rect(center=(self.x, self.y))


    def __str__(self):
        return self.body.percepts().__str__()