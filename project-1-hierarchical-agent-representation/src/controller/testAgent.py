"""
Here we test the Robot to see if everything is working correctly
"""

from environment import Environment
from robotBody import RobotBody
from robotMiddle import RobotMiddleLayer
from robotTop import RobotTopLayer


def testRobot():
    environment = Environment(100, 100)

    body = RobotBody(environment)
    middle = RobotMiddleLayer(body)
    top = RobotTopLayer(middle, timeout=30)

    top.do({'visit': [(180, 40), (0, 0), (20, 20), (40, 180)]})


testRobot()


"""
class AgentThread(Thread):
    def __init__(self, ...):
        super().__init__()
    
    def init(self):
        return env, event_queue
    
    def run(self):
        # logic for task completion
"""
