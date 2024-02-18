"""
A controller for the environment that the agent will be interacting in
"""

from environments import Environment

class Environment(Environment): 
    def __init__(self, width=200, length=200): 
        self.WIDTH = width 
        self.LENGTH = length 
        self.objects = {} # a dictionary of named locations for objects 

    def info(self):
        return self.WIDTH, self.LENGTH