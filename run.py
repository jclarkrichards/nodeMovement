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

area.divideIntoSubAreas(*world.screenSize)

for val in area.subAreas.keys():
    print area.subAreas[val].entityOffset
#world.loadNewArea(area)

world.loadNewArea(area, 0)

while True:
    world.handleEvents()
    dt = clock.tick(30) / 1000.0
    world.update(dt)
    #nodes.render(screen)
    world.render()
    pygame.display.update()
