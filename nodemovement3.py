import pygame
from pygame.locals import *
from vectors import Vector2D
from nodemovement import *

class FourWayContinuous(FourWayAbstract):
    def __init__(self, nodes, nodeVal, entity):
        '''node is the starting node.  All other nodes are connected
        entity is the entity that travels from node to node'''
        FourWayAbstract.__init__(self, nodes, nodeVal, entity)
        if self.entity.direction in self.validDirections:
            self.setEntityDirection(self.entity.direction)

    def update(self, dt):
        self.moveTowardsTarget(dt)
        
        if self.overshotTarget():
            self.node = self.target
            #self.portal()
            self.setValidDirections()

            if self.direction:# if a key is being pressed
                #if pressed direction is in the valid directions
                if self.isValidDirection(self.direction):
                    if self.direction != self.entity.direction:
                        self.changeDirection()
                    else:#is in the same direction
                        self.setTarget(self.entity.direction)
                else: #key direction not in valid directions
                    self.checkCurrentDirection()
            else: #key not being pressed
                self.restOnNode()
               
        else: #has not overshot target
            if self.entity.direction == STOP:
                if self.isValidDirection(self.direction):
                    self.setEntityDirection(self.direction)
            else:
                if self.direction == self.entity.direction*-1:
                    self.reverseDirection()
                    
    def checkCurrentDirection(self):
        '''Check if entity is able to continue in current direction'''
        if self.isValidDirection(self.entity.direction):
            self.setTarget(self.entity.direction)
        else:
            self.restOnNode()

    def restOnNode(self):
        self.entity.position = self.nodes[self.node].position
        self.entity.direction = STOP
        
    def isValidDirection(self, direction):
        return direction in self.validDirections
        
    def changeDirection(self):
        self.entity.position = self.nodes[self.node].position
        self.setEntityDirection(self.direction)
        
    def keyDiscrete(self, key):
        pass
