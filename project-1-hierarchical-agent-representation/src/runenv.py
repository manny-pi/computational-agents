"""
Run the environment
"""

from controller.robotBody import RobotBody
from controller.robotMiddle import RobotMiddleLayer
from controller.robotTop import RobotTopLayer
from controller.environment import Environment

from gui.envGUI import EnvironmentGUI
from gui.robotGUI import RobotGUI

import pygame
from pygame.time import Clock
from pygame import Surface 

from random import randint 
from math import sqrt, pow


class Point:
    def __init__(self, x, y): 
        self.x = x
        self.y = y 


# create the environment and startup its gui 
WIDTH = LENGTH = 800
environment = Environment(width=WIDTH, length=LENGTH)
envGui = EnvironmentGUI(environment)

# create the robot and startup its gui 
body = RobotBody(environment)
middle = RobotMiddleLayer(body)
top = RobotTopLayer(middle, timeout=30)
robGui = RobotGUI(body)

def euclideanDistance(p1, p2): 
    """Calculates the euclidian distance between given points (x_1, y_1) and (x_2, y_2).
    
    Args:
        p1 (Point): first point
        p2 (Point): second point
    
    Returns:
        float: the euclidian distance between the two points 
    """
    return sqrt(pow(p2.x - p1.x, 2) + pow(p2.y - p1.y, 2))

def getNearestLocation(locations): 
    """
    Scans a list of points, and returns the one nearest to the robot.
    """
    minDist = pow(WIDTH * LENGTH, 2)
    nearestLocation = None
    for location in locations:
        dist = euclideanDistance(Point(body.robX, body.robY), Point(location[0], location[1]))
        if dist < minDist: 
            nearestLocation = location
            minDist = dist

    return nearestLocation

def generateLocations(n): 
    """
    Returns a list of random locations in the environment [(x_1, y_1), ..., (x_n, y_n)]
    """
    locations = {}
    for i in range(n): 
        # Calculate random (x, y) coordinates
        x = randint(10, WIDTH - 100)
        x -= (x % 10) if x > 10 else x + (10 - x)
        y = randint(50, LENGTH - 100)
        y -= (y % 10) if y > 10 else y + (10 - y)
        loc = (x, y)

        # Create the surface where the location marker is drawn to
        surface = {}
        surf = Surface((10, 10))
        surf.fill((255, 0, 0))
        surface[surf] = surf.get_rect(center=loc) 
        locations[loc] = surface

    return locations


locations = generateLocations(50)  # (x, y) coordinates that the robot should visit
nextLocation = getNearestLocation(locations) 

window = pygame.display.set_mode((environment.WIDTH, environment.LENGTH), display=0)
running = True
clock = Clock()

searchStarted = False
stepsToGoal = 0
while running: 
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            running = False

    if not searchStarted: 
        searchStarted = True
        top.do({'visit': locations})

    arrived = top.do({'visit': nextLocation})
    if arrived: 
        try: 
            del locations[nextLocation]                     # delete the marker of the visited location
            nextLocation = getNearestLocation(locations)    # get the next location

        except IndexError: 
            print("Ran out locations")
            locations = generateLocations(50)
            locMarkers = genMarkers((10, 10), locations)
          
            nextLocation = locations.pop() 

        print(f"Arrived @ {nextLocation} -> {'yes' if arrived else 'timed-out'} | Steps Taken: {stepsToGoal}")

        stepsToGoal = 0
        arrived = False
    else: 
      stepsToGoal += 1 

    robGui.updateLoc()
    envGui.refresh() 

    envGui.surface.blit(robGui.surface, robGui.rect)
    window.blit(envGui.surface, envGui.rect)
    for key in locations: 
        location = locations[key]
        for surf, rect in location.items(): 
            window.blit(surf, rect)
    
    pygame.display.flip()

    clock.tick(10)
