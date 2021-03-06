"""
The RobotTopLayer invokes changes inthe RobotMiddleLayer
"""

from .environments import AgentEnvironment


class RobotTopLayer(AgentEnvironment): 
    def __init__(self, middle: AgentEnvironment, timeout=5): 
        """
        Declares the variables of the Robot Top Layer
        """

        self.middle = middle   # the middle layer; the top layer invokes changes in this layer
        self.timeout = timeout # timeout after n=timeout moves
        self.locations = []
    
    def do(self, plan: dict = None) -> bool: 
        """
        .do will tell the self.middle the next location to visit
        plan is a dictionary of locations to visit {'visit': (x1, y1), (x2, y2), ... ]}
        """

        if plan:
            loc = plan['visit']
            arrived = self.middle.do({'go_to': loc, 'timeout': self.timeout}) # change percepts in middle layer
            
            if arrived: # if the robot has arrived
                return True
            else: 
                return False



