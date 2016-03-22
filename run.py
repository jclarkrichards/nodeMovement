import pygame
from entity import Entity
from world import World
from areas import Area1, Area2, AreaTest

clock = pygame.time.Clock()

world = World()
world.setup(4, 3, 64)
player = Entity()
world.addPlayer(player)

area = AreaTest(64, 64)
world.loadNewArea(area)

while True:
    world.handleEvents()
    dt = clock.tick(30) / 1000.0
    world.update(dt)
    #nodes.render(screen)
    world.render()
    pygame.display.update()
