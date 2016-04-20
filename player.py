import pygame
from vectors import Vector2D
from nodemovement import FourWayMovement
from entity import Entity

class Player(Entity):
    def __init__(self):
        Entity.__init__(self)
        self.direction = 0
        self.previousDirection = 0
        self.facingDirection = 0
        self.speed = 60
        self.mover = FourWayMovement(self, version=3)
        self.velocity = Vector2D()
        self.overrideKeys = False
        
    def update(self, dt):
        pass
    
    def loadNewNodes(self, nodes, startNode):
        '''Allow entity to move around the new node set'''
        self.mover.loadNewNodes(nodes, startNode)
        self.mover.test()
        
    def move(self, dt, key_pressed=None):
        '''Move entity around the nodes'''
        if key_pressed and not self.overrideKeys:
            self.mover.setKeyDirection(key_pressed)
        self.mover.update(dt)
        self.overrideKeys = False


