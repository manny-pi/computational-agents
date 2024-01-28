"""
The RobotBody acts as an Environment that the layers above it can influence 

It receives commands from the Robot Middle Layer and acts them out in the environment
"""

from .environments import AgentEnvironment
from .environments import Environment
from .directions import Direction
from enum import Enum


class RobotBody(AgentEnvironment): 
    """ 
    A simple 'simulated agent' that searches for objects in its environment
    """
    
    def __init__(self, env: Environment): 
        """
        Declares the environment variables for the Robot Environment
        """

        self.env = env

        # set the initial percepts of the Robot 
        self.robX = 50
        self.robY = env.LENGTH - 30
        self.robXDelta = self.robYDelta = 10 # displacement along x and y axes
        self.robDir = Direction.NORTH # the direction the Robot is facing
        self.pathBlocked = False # if the path of the Robot is blocked

        # store the history of (x, y) positions of the Robot
        self.history = [(self.robX, self.robY)]

    def percepts(self) -> dict: 
        """
        Returns the state of the Robot in a dictionary
        """
        
        return {
            'robX': self.robX, 
            'robY': self.robY, 
            'robDir': self.robDir, 
            'eyes': self.eyes(), 
            'pathBlocked': self.pathBlocked
        }
    
    initial_percepts = percepts # use percept function for initial percepts too

    def do(self, action) -> dict: 
        """ 
        Performs an 'action' given by the Robot Middle Layer

        action is {'steer': directionf}
        direction is NORTH, EAST, SOUTH, or WEST
        """

        # set the Robot in the direction based on the action
        direction = action['steer']
        robXNew = self.robX 
        robYNew = self.robY
        if direction == Direction.NORTH: 
            robYNew = self.robY - self.robYDelta
            self.robDir = Direction.NORTH 
        elif direction == Direction.EAST: 
            robXNew = self.robX + self.robXDelta 
            self.robDir = Direction.EAST
        elif direction == Direction.SOUTH: 
            robYNew = self.robY + self.robYDelta 
            self.robDir = Direction.SOUTH
        elif direction == Direction.WEST: 
            robXNew = self.robX - self.robXDelta
            self.robDir = Direction.WEST

        # execute if the Robot sees an object in its path 
        if self.eyes(): 
            self.pathBlocked = True
        else:
            self.pathBlocked = False
            self.robX = robXNew
            self.robY = robYNew 

        return self.percepts()
        
    def eyes(self) -> bool: 
        """
        Returns True if there is an object in the direction that Robot is facing
        """

        # check if there's an object in the direction the Robot is facing
        goalX = self.robX 
        goalY = self.robY
        if self.robDir == Direction.NORTH: 
            goalY = self.robY - self.robYDelta 
        elif self.robDir == Direction.EAST: 
            goalX = self.robX + self.robXDelta 
        elif self.robDir == Direction.SOUTH: 
            goalY = self.robY + self.robYDelta 
        elif self.robDir == Direction.WEST: 
            goalX = self.robX - self.robXDelta

        # check if there's an object in the Robots path
        for obj, pos in self.env.objects.items(): 
            if pos == (goalX, goalY): 
                self.pathBlocked = True

        return self.pathBlocked