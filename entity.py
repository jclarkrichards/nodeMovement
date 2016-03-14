import pygame
from nodemovement2 import FourWayDiscrete
from nodemovement3 import FourWayContinuous
from vectors import Vector2D

class Entity(object):
    def __init__(self, nodes):
        startNode = 2
        self.position = nodes[startNode].position
        self.direction = 1
        self.move = FourWayContinuous(nodes, startNode, self)
        self.speed = 100
        
    def update(self, dt):
        self.move.update(dt)

    def render(self, screen):
        x, y = self.position.toTuple()
        pygame.draw.circle(screen, (200,200,0), (int(x), int(y)), 8)
