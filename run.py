import pygame
from pygame.locals import *
from entity import Entity
from world import World
from areas import Area1

world = World()
world.setup(25, 25, 16)

clock = pygame.time.Clock()
nodes = NodeHandler(TILEWIDTH, TILEHEIGHT)
player = Entity()
world.addPlayer(player)

area = Area1(16, 16)
world.loadNewArea(area)

while True:
    world.handleEvents()
    dt = clock.tick(30) / 1000.0
    #key_pressed = pygame.key.get_pressed()
    #player.move(dt, key_pressed)
    world.update(dt)
    #nodes.render(screen)
    world.render()
    pygame.display.update()
