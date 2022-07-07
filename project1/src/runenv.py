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
from random import randint 


# create the environment and startup its gui 
WIDTH = LENGTH = 400
environment = Environment(width=WIDTH, length=LENGTH)
envGui = EnvironmentGUI(environment)

# create the robot and startup its gui 
body = RobotBody(environment)
middle = RobotMiddleLayer(body)
top = RobotTopLayer(middle, timeout=30)
robGui = RobotGUI(body)

def genLoc(n): 
    """
    Returns a list of random locations in the environment
    """
    locations = []
    for i in range(n): 
      x = randint(0, WIDTH - 50)
      x -= (x % 10) if x > 10 else x + (10 - x)
      
      y = randint(50, LENGTH - 50)
      y -= (y % 10) if y > 10 else y + (10 - y)
      locations.append((x, y))
    
    return locations

from pygame import Surface 
def genMarkers(size, locations: list) -> list: 
    """
    Generate markers centered at each of the locations provided in list

    Returns a {Surface: Rect} dicitionary
    """
    
    surfaces = {} 
    for loc in locations: 
        surf = Surface(size)
        surf.fill((randint(0, 255), randint(0, 255), randint(0, 255)))
        surfaces[surf] = loc 
    return surfaces 

# locations Robot should visit 
locations = genLoc(50)
locMarkers = genMarkers((10, 10), locations) 
nextLocation = locations.pop() 

window = pygame.display.set_mode((environment.WIDTH, environment.LENGTH), display=0)
running = True
clock = Clock()

stepsToGoal = 0
while running: 
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            running = False

    arrived = top.do({'visit': nextLocation})
    if arrived: 
        try: 
            nextLocation = locations.pop()
            locMarkers.popitem()
        except IndexError: 
            print("Ran out locations")
            locations = genLoc(50)
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
    for marker in locMarkers: 
        window.blit(marker, marker.get_rect(center=locMarkers[marker]))
    
    pygame.display.flip()

    clock.tick(10)
