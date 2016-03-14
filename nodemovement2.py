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
            self.restOnNode(self.node)
            self.setValidDirections()
        else:
            if self.isValidDirection(self.keyDirection):
                if self.isResting():
                    self.setEntityDirection(self.keyDirection)
        self.keyDirection = STOP

        
    def keyContinuous(self, key_pressed):
        pass
    



    




    
