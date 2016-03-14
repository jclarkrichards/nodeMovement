import pygame
from pygame.locals import *
from node import NodeGroup
from entity import Entity

TILEWIDTH, TILEHEIGHT = (16, 16)
SCREENSIZE = (TILEWIDTH*30, TILEHEIGHT*30)
pygame.init()
screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
clock = pygame.time.Clock()
background = pygame.surface.Surface(SCREENSIZE).convert()
background.fill((0,0,0))

nodes = NodeGroup(TILEWIDTH, TILEHEIGHT)
nodes.createNodeList('maze_test.txt')
jon = Entity(nodes.nodeDict, 2)

while True:
    dt = clock.tick(30) / 1000.0
    key_pressed = pygame.key.get_pressed()
    jon.move.setKeyPressed(key_pressed)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
 
    jon.update(dt)

    screen.blit(background, (0,0))
    nodes.render(screen)
    jon.render(screen)

    pygame.display.update()
