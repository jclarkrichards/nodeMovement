import pygame
from entity import Entity
from world import World
from areas import *

clock = pygame.time.Clock()

world = World()
world.setup(4, 3, 64)
player = Entity()
#player.setMoverMinDistance(world.tileSize)
world.addPlayer(player)

area = AreaTest(64, 64)
#area.divideIntoSubAreas(*world.screenSize)
area2 = AreaTest2(64, 64)
#area2.divideIntoSubAreas(*world.screenSize)
area3 = AreaTest3(64, 64)
world.addArea(area)
world.addArea(area2)
world.addArea(area3)
#for val in area.subAreas.keys():
#    print area.subAreas[val].entityOffset
#world.loadNewArea(area)

world.loadStartArea(area, 1)

while True:
    world.handleEvents()
    dt = clock.tick(30) / 1000.0
    world.update(dt)
    world.render()
    pygame.display.update()
