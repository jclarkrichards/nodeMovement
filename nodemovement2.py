import pygame
from pygame.locals import *
from vectors import Vector2D
from nodemovement import *

STOP = 0

class FourWayDiscrete(FourWayAbstract):
    def __init__(self, nodes, nodeVal, entity):
        '''node is the starting node.  All other nodes are connected
        entity is the entity that travels from node to node'''
        FourWayAbstract.__init__(self, nodes, nodeVal, entity)
        
    def update(self, dt):
        self.moveTowardsTarget(dt)
        if self.overshotTarget():
            self.node = self.target
            self.entity.position = self.nodes[self.node].position
            self.validDirections = self.nodes[self.node].neighbors
            self.entity.direction = STOP
        else:
            if self.keyDirection in self.validDirections:
                if self.entity.direction == STOP:
                    self.entity.direction = self.keyDirection
                    self.setTarget(self.keyDirection)
                    self.validDirections = [self.keyDirection]
        self.keyDirection = STOP

        
    def keyContinuous(self, key_pressed):
        pass
    



    




    
