import pygame
from vectors import Vector2D
from nodemovement import FourWayMovement

class Entity(object):
    def __init__(self, nodes, nodeVal):
        self.ID = 0
        self.position = Vector2D() 
        self.direction = 0
        self.speed = 60
        self.mover = FourWayMovement(nodes, nodeVal, self, version=3)
        
    def setID(self, ID):
        self.ID = ID
        
    def update(self, dt):
        pass
    
    def move(self, dt, key_pressed=None):
        '''Move entity around the nodes'''
        if key_pressed:
            self.mover.setKeyDirection(key_pressed)
        self.mover.update(dt)

    def render(self, screen):
        x, y = self.position.toTuple()
        pygame.draw.circle(screen, (200,200,0), (int(x), int(y)), 8)
