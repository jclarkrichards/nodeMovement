import pygame
from pygame.locals import *
from vectors import Vector2D
from nodemovement import *

class FourWayDiscrete(FourWayAbstract):
    def __init__(self, node, entity):
        '''node is the starting node.  All other nodes are connected
        entity is the entity that travels from node to node'''
        FourWayAbstract.__init__(self, node, entity)
        
    def update(self, dt):
        self.moveTowardsTarget(dt)
        if self.overshotTarget():
            self.node = self.target
            self.entity.position = self.node.position
            self.validDirections = self.node.directions
            self.entity.direction = STOP
        else:
            if self.direction in self.validDirections:
                if self.entity.direction == STOP:
                    self.entity.direction = self.direction
                    self.setTarget(self.direction)
                    self.validDirections = [self.direction]
        self.direction = STOP

    def keyContinuous(self, key_pressed):
        pass
    



    




    
