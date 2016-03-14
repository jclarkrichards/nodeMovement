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

            if self.keyDirection:# if a key is being pressed
                if self.isValidDirection(self.keyDirection):
                    if self.keyDirection != self.entity.direction:
                        self.changeDirection()
                    else:#is in the same direction
                        self.setTarget(self.entity.direction)
                else: #key direction not in valid directions
                    self.checkCurrentDirection()
            else: #key not being pressed
                self.restOnNode()
               
        else: #has not overshot target
            if self.isResting():
                if self.isValidDirection(self.keyDirection):
                    self.setEntityDirection(self.keyDirection)
            else:
                if self.keyDirection == self.entity.direction*-1:
                    self.reverseDirection()
                    
    def checkCurrentDirection(self):
        '''Check if entity is able to continue in current direction'''
        if self.isValidDirection(self.entity.direction):
            self.setTarget(self.entity.direction)
        else:
            self.restOnNode()

    def restOnNode(self):
        '''Set the entity on top of a node and rest'''
        self.placeOnNode(self.node)
        self.entity.direction = STOP
        
    def isResting(self):
        '''Return True if entity is at rest'''
        return self.entity.direction == STOP
        
    def isValidDirection(self, direction):
        '''Return True if direction is a valid direction'''
        return direction in self.validDirections
        
    def changeDirection(self):
        '''Change entities direction'''
        self.placeOnNode(self.node)
        self.setEntityDirection(self.keyDirection)
        
    def placeOnNode(self, node):
        '''Place the entity on top of a node'''
        self.entity.position = self.nodes[node].position
        
    def keyDiscrete(self, key):
        pass
