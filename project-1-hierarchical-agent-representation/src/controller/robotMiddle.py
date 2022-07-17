"""
The RobotMiddleLayer invokes changes in the RobotBody 
"""

from .environments import AgentEnvironment
from .directions import Direction


class RobotMiddleLayer(AgentEnvironment): 
    def __init__(self, env: AgentEnvironment): 
        self.env = env 
        self.percepts = env.initial_percepts() # get the initial percepts of the RobotBodyLayer

    def initial_percepts(self): 
        """
        Does nothing / The middle layer doesn't have any initial percepts, but 
        has to be implemented because this class is a subclass of agents.Environment
        """

        return {}
    
    def do(self, action: dict) -> dict: 
        """
        action is a {'go_to': target_pos, 'timeout': timeout}
        target_pos is (x, y) pair 
        timeout is the number of steps to try 

        returns {'arrived': True} when arrived is True 
            or {'arrived' False} if the Robot timed out 
        """ 

        if 'timeout' in action: # Execut e if the Robot can timeout 
            remaining = action['timeout']
        else: 
            remaining = -1  # Execute if the Robot never times out
        target_pos = action['go_to'] 
        arrived = self.close_enough(target_pos)
        while not arrived and remaining != 0: 
            self.percepts = self.env.do({'steer': self.steer(target_pos)})
            remaining -= 1
            arrived = self.close_enough(target_pos)

            if not arrived: 
                return # so the gui can update after every move 

        return {'arrived': arrived}
        
    def steer(self, target_pos: tuple) -> Direction: 
        """ 
        Determines how to steer, depending on the location of the object the 
        Robot is searching for 

        Returns 'NORTH', 'EAST', 'SOUTH', or 'WEST'
        """ 

        if self.percepts['eyes']: # execute if there's something in the Robots path
            if self.percepts['robDir'] == Direction.NORTH: 
                return Direction.EAST 
            elif self.percepts['robDir'] == Direction.EAST: 
                return Direction.SOUTH 
            elif self.percepts['robDir'] == Direction.SOUTH: 
                return Direction.WEST 
            elif self.percepts['robDir'] == Direction.WEST: 
                return Direction.NORTH 
        
        else: 
            goalX, goalY = target_pos 
            robX, robY = self.percepts['robX'], self.percepts['robY']

            # turn the Robot in the direction of target_pos
            if goalX > robX: 
                return Direction.EAST
            elif goalX < robX: 
                return Direction.WEST
            elif goalY > robY: 
                return Direction.SOUTH 
            elif goalY < robY: 
                return Direction.NORTH

    def close_enough(self, target_pos) -> bool:
        """
        Returns True if the object in front of the Robot is the desired object
        """

        goalX, goalY = target_pos
        percepts = self.env.percepts()
        robX, robY = percepts['robX'], percepts['robY']

        if abs(robX - goalX) == 0 and abs(robY - goalY) == 0: 
            return True

        return False
