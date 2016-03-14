import pygame
from pygame.locals import *
from node import NodeGroup
from entity import Entity

TILEWIDTH, TILEHEIGHT = (16, 16)
SCREENSIZE = (TILEWIDTH*30, TILEHEIGHT*30)
pygame.init()
screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
background = pygame.surface.Surface(SCREENSIZE).convert()
background.fill((0,0,0))

nodes = NodeGroup(TILEWIDTH, TILEHEIGHT)
nodes.createNodeList('maze_test.txt')

clock = pygame.time.Clock()

jon = Entity(nodes.nodeDict)

while True:
    dt = clock.tick(30) / 1000.0
    key_pressed = pygame.key.get_pressed()
    jon.move.keyContinuous(key_pressed)
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        if event.type == KEYDOWN:
            pass
            #jon.move.keyDiscrete(event.key)
            
    jon.update(dt)

    screen.blit(background, (0,0))
    nodes.render(screen)
    jon.render(screen)

    pygame.display.update()
