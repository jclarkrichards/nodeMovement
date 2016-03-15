import pygame
#from nodemovement import FourWayMovement
#from nodemovement2 import FourWayDiscrete
#from nodemovement3 import FourWayContinuous
from vectors import Vector2D

class Entity(object):
    def __init__(self):#, nodes, startNode):
        self.ID = 0
        self.position = Vector2D() #nodes[startNode].position
        self.direction = 0
        #self.move = FourWayMovement(nodes, startNode, self, version=3)
        self.speed = 100
        
    def update(self, dt):
        pass
        #self.move.update(dt)

    def render(self, screen):
        x, y = self.position.toTuple()
        pygame.draw.circle(screen, (200,200,0), (int(x), int(y)), 8)
