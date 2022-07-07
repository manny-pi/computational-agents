from pygame import Surface 
from controller.environment import Environment


class EnvironmentGUI: 
    def __init__(self, env: Environment): 
        self.WIDTH = env.WIDTH 
        self.LENGTH = env.LENGTH

        self.surface = Surface((self.WIDTH, self.LENGTH))
        self.surface.fill((60, 200, 100))  
        self.rect = self.surface.get_rect(bottomleft=(0, self.LENGTH))

    def refresh(self): 
        self.surface.fill((150, 200, 100))
