import pygame
from pygame.locals import *
from node import NodeGroup
from entity import Entity
from nodehandler import NodeHandler

TILEWIDTH, TILEHEIGHT = (16, 16)
SCREENSIZE = (TILEWIDTH*25, TILEHEIGHT*25)
pygame.init()
screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
clock = pygame.time.Clock()
background = pygame.surface.Surface(SCREENSIZE).convert()
background.fill((0,0,0))

nodes = NodeHandler(TILEWIDTH, TILEHEIGHT)
jon = Entity()
nodes.setPlayer(jon)

while True:
    dt = clock.tick(30) / 1000.0
    key_pressed = pygame.key.get_pressed()
    nodes.area.movers[jon.ID].setKeyDirection(key_pressed)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
 
    nodes.update(dt)
    screen.blit(background, (0,0))
    nodes.render(screen)
    jon.render(screen)

    pygame.display.update()
