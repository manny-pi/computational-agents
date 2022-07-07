"""
Here we test the Robot to see if everything is working correctly
"""

from environments import AgentEnvironment, Environment
from robotBody import RobotBody
from robotMiddle import RobotMiddleLayer
from robotTop import RobotTopLayer

def testRobot(): 
    environment = environment.Environment()

    body = RobotBody(environment)
    middle = RobotMiddleLayer(body)
    top = RobotTopLayer(middle, timeout=30)

    top.do({'visit': [(180, 40), (0, 0), (20, 20), (40, 180)]})

testRobot() 