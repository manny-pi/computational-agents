"""
The RobotBody acts as an Environment that the layers above it can influence.

It receives commands from the Robot Middle Layer and acts them out in the 'physical' environment. 
"""

from environments import AgentEnvironment
from environments import Environment
from directions import Direction


class RobotBody(AgentEnvironment):
    """ 
    A simple digital agent that searches for objects in its environment
    """

    def __init__(self, env: Environment):
        """
        Declares the environment variables for the Robot Environment
        """

        self.__ID = hash(self)
        self.env = env

        # set the initial percepts of the Robot
        self.x = 50
        self.y = env.LENGTH - 30
        self.xDelta = self.yDelta = 10  # displacement along x and y axes
        self.robDir = Direction.NORTH  # the direction the Robot is facing
        self.pathBlocked = False  # if the path of the Robot is blocked

        # store the history of (x, y) positions of the Robot
        self.history = [(self.x, self.y)]

        # update queue to record changes to the robotbody
        self.__update_queue = None
        self.__update_queue_lock = None

    def percepts(self) -> dict:
        """
        Returns the state of the Robot in a dictionary
        """

        return {
            'x': self.x,
            'y': self.y,
            'robDir': self.robDir,
            'eyes': self.eyes(),
            'pathBlocked': self.pathBlocked
        }

    initial_percepts = percepts  # use percept function for initial percepts too

    def do(self, action) -> dict:
        """ 
        Performs an 'action' given by the Robot Middle Layer. This causes
        the object to change its 

        action is {'steer': directionf}
        direction is NORTH, EAST, SOUTH, or WEST
        """

        # set the Robot in the direction based on the action
        direction = action['steer']
        xNew = self.x
        yNew = self.y
        if direction == Direction.NORTH:
            yNew = self.y - self.yDelta
        elif direction == Direction.EAST:
            xNew = self.x + self.xDelta
        elif direction == Direction.SOUTH:
            yNew = self.y + self.yDelta
        elif direction == Direction.WEST:
            xNew = self.x - self.xDelta

        # execute if the Robot sees an object in its path
        if self.eyes():
            self.pathBlocked = True
        else:
            self.pathBlocked = False
            self.robDir = direction
            self.x = xNew
            self.y = yNew

            # Add the changes to the update queue
            self.__update_queue_lock.acquire()
            self.__update_queue.append({
                "type": "sprite-update",
                "info": {
                    "ID": self.__ID,
                    "coordinates": (self.x, self.y)
                }
            })
            self.__update_queue_lock.release()

        return self.percepts()

    def eyes(self) -> bool:
        """
        Returns True if there is an object in the direction that Robot is facing
        """

        # check if there's an object in the direction the Robot is facing
        goalX = self.x
        goalY = self.y
        if self.robDir == Direction.NORTH:
            goalY = self.y - self.yDelta
        elif self.robDir == Direction.EAST:
            goalX = self.x + self.xDelta
        elif self.robDir == Direction.SOUTH:
            goalY = self.y + self.yDelta
        elif self.robDir == Direction.WEST:
            goalX = self.x - self.xDelta

        # check if there's an object in the Robots path
        for obj, pos in self.env.objects.items():
            if pos == (goalX, goalY):
                self.pathBlocked = True

        return self.pathBlocked

    def register_update_queue(self, update_queue, lock):
        self.__update_queue = update_queue
        self.__update_queue_lock = lock

    def get_ID(self) -> int:
        return self.__ID
    
    def get_coordinates(self) -> "tuple[int, int]":
        return self.x, self.y