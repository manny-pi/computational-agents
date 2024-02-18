#! /usr/local/bin/python3.8

"""
Run the environment.
"""

from controller.environment import Environment
import controller.agent as agent
from gui.sprite import GenericSprite, GenericSpriteGroup
from gui.envGUI import EnvironmentGUI
import pygame
from pygame.time import Clock
from pygame.colordict import THECOLORS

# Initialize modules
pygame.init()
update_queue, lock = agent.init()

# Instantiatet the AgentThread
agentThread = agent.AgentThread("AgentThread")
env_info = agentThread.get_env_info()

# Start the AgentThread
agentThread.start()

# Create the environment and startup its gui
WIDTH, LENGTH = env_info[0], env_info[1]
environment = Environment(width=WIDTH, length=LENGTH)
envGui = EnvironmentGUI(environment)
window = pygame.display.set_mode((WIDTH, LENGTH))
clock = Clock()

# List to hold all sprites
all_sprites = GenericSpriteGroup()
all_sprites_dict = dict()


def reducer(event):
    event_type = event.get("type")
    if event_type == "sprite-init" or event_type == "sprite-update":
        info = event.get("info")
        ID = info.get("ID")

        if event_type == "sprite-init":
            if ID in all_sprites_dict:
                raise Exception("Sprite already exists!")

            name = info.get("name")
            coordinates = info.get("coordinates")
            sprite = GenericSprite(ID, coordinates=coordinates)
            if name == "agent":
                sprite.set_color((0, 0, 255))

            all_sprites.add(sprite)
            all_sprites_dict[ID] = sprite
        elif event_type == "sprite-update":
            coordinates = info.get("coordinates")
            if ID in all_sprites_dict:
                sprite = all_sprites_dict.get(ID)
                sprite.set_coordinates(coordinates)
            else: 
                raise Exception(f"Sprite (sprite{ID}) not found.")


def render_all():
    """Renders the sprites without actually drawing them to the screen."""
    envGui.surface.fill(THECOLORS["aqua"])
    for sprite in all_sprites:
        envGui.surface.blit(sprite.get_surface(), sprite.get_rect())

    window.blit(envGui.surface, envGui.rect)


# Graphics Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    lock.acquire()
    try:
        reducer(update_queue.popleft())
    except IndexError:
        pass
    lock.release()

    render_all()
    pygame.display.flip()

    clock.tick(5)
