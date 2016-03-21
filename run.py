import pygame
from entity import Entity
from world import World
from areas import Area1, Area2

clock = pygame.time.Clock()

world = World()
world.setup(25, 25, 16)
player = Entity()
world.addPlayer(player)

area = Area2(16, 16)
world.loadNewArea(area)

while True:
    world.handleEvents()
    dt = clock.tick(30) / 1000.0
    world.update(dt)
    #nodes.render(screen)
    world.render()
    pygame.display.update()
