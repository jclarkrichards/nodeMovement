import pygame
from pygame.locals import *
from node import NodeGroup
from entity import Entity
from nodehandler import NodeHandler
from world import World

world = World()
world.setup(25, 25, 16)

clock = pygame.time.Clock()
nodes = NodeHandler(TILEWIDTH, TILEHEIGHT)
player = Entity()
#nodes.setPlayer(player)
world.addDynamicObject(player, setAsPlayer=True)

while True:
    world.handleEvents()
    dt = clock.tick(30) / 1000.0
    #key_pressed = pygame.key.get_pressed()
    #player.move(dt, key_pressed)
    world.update(dt)
    #nodes.update(dt)
    #nodes.render(screen)
    world.render()
    pygame.display.update()
