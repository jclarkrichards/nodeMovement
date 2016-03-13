import pygame
from pygame.locals import *
from vectors import Vector2D
from constants import *
UP = 1
DOWN = -1
LEFT = 2
RIGHT = -2
STOP = 0
DIRECTIONS = {UP:Vector2D(0,-1), DOWN:Vector2D(0,1),
              LEFT:Vector2D(-1,0), RIGHT:Vector2D(1,0), STOP:Vector2D()}

class FourWayAbstract(object):
    def __init__(self, nodes, nodeVal, entity):
        '''node is the starting node.  All other nodes are connected
        entity is the entity that travels from node to node'''
        self.nodes = nodes
        self.node = nodeVal
        self.target = nodeVal
        self.entity = entity
        self.direction = 0
        self.setValidDirections()

    def update(self, dt):
        pass

    def setValidNodeVals(self, nodeVal):
        '''Set the valid node values that the entity is allowed to move'''
        self.validValues = self.nodes[nodeVal].neighbors.values()
        for val in self.nodes[nodeVal].hidden:
            if val in self.validValues:
                self.validValues.remove(val)
        
    def setValidDirections(self):
        '''Set the valid directions that the entity is allowed to move'''
        self.validDirections = self.nodes[self.node].neighbors.keys()
        for nodeVal in self.nodes[self.node].hidden:
            for direction in self.nodes[self.node].neighbors.keys():
                if self.nodes[self.node].neighbors[direction] == nodeVal:
                    try:
                        self.validDirections.remove(direction)
                    except ValueError:
                        pass
    
    def setEntityDirection(self, direction):
        '''Set valid directions when in between nodes'''
        self.entity.direction = direction
        self.setTarget(direction)
        self.validDirections = [direction, direction*-1]
        
    def lengthFromNode(self, vector):
        vec = vector - self.nodes[self.node].position
        return vec.magnitudeSquared()

    def overshotTarget(self):
        '''Check if entity has overshot target node'''
        nodeToTarget = self.lengthFromNode(self.nodes[self.target].position)
        nodeToSelf = self.lengthFromNode(self.entity.position)
        return nodeToSelf > nodeToTarget

    def moveTowardsTarget(self, dt):
        '''Move entity towards the target'''
        ds = self.entity.speed*dt
        self.entity.position += DIRECTIONS[self.entity.direction]*ds

    def setTarget(self, direction):
        '''Set a new target based on the direction'''
        self.target = self.nodes[self.node].neighbors[direction]
        
    def reverseDirection(self):
        '''Swap the node and target'''
        temp = self.target
        self.target = self.node
        self.node = temp
        self.entity.direction *= -1

    #def removeOppositeDirection(self):
    #    self.setValidDirections()
        #self.validDirections = self.node.neighbors.keys()
    #    if self.entity.direction*-1 in self.validDirections:
    #        if len(self.validDirections) > 1:
    #            self.validDirections.remove(self.entity.direction*-1)

    #def portal(self):
    #    if self.nodes[self.node].portal:
    #        self.node = self.nodes[self.node].portal
    #        self.entity.position = self.nodes[self.node].position
    #        self.setValidDirections()
            #self.validDirections = self.nodes[self.node].neighbors.keys()
            
    def keyContinuous(self, key):
        '''Listen for directional key presses'''
        if key[K_UP]:
            self.direction = 1
        elif key[K_DOWN]:
            self.direction = -1
        elif key[K_RIGHT]:
            self.direction = -2
        elif key[K_LEFT]:
            self.direction = 2
        else:
            self.direction = 0
    
    def keyDiscrete(self, key):
        if key == K_LEFT:
            self.direction = LEFT
        elif key == K_RIGHT:
            self.direction = RIGHT
        elif key == K_UP:
            self.direction = UP
        elif key == K_DOWN:
            self.direction = DOWN


