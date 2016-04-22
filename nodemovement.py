import pygame
from pygame.locals import *
from vectors import Vector2D
from constants import *

class FourWayMovement(object):
    def __init__(self, version):
        '''nodes is the dictionary of all nodes.  
        nodeVal is the value of the starting node.
        entity is the Entity that moves around the nodes.
        version is the type of movement required. (1, 2, or 3)'''
        self.entity = None #entity
        self.area = None
        self.nodes = {}
        self.node = 0
        self.target = 0
        self.areaPos = Vector2D()
        self.version = version
        self.keyDirection = STOP
        self.validDirections = []
        
    def updatePosition(self, entity, area, dt):
        '''The only method that should be called from the outside'''
        self.entity = entity
        self.area = area
        self.onStart()
        self.update(dt)
        self.onExit()

    def onStart(self):
        '''These variables are shorter and easier to read'''
        self.nodes = self.area.nodes.table
        self.node = self.entity.node
        self.target = self.entity.target
        self.areaPos = self.area.position
        self.keyDirection = self.entity.keyDirection
        self.targetOvershot = self.entity.targetOvershot
        if self.entity.overrideKeys:
            print self.keyDirection, self.entity.previousDirection
            self.keyDirection = self.entity.previousDirection
            self.entity.overrideKeys = False
            
    def onExit(self):
        '''Update the modified values of entity and area'''
        self.entity.node = self.node
        self.entity.target = self.target
        self.area.nodes.table = self.nodes
        self.entity.keyDirection = self.keyDirection
        self.entity.targetOvershot = self.targetOvershot
        
    def update(self, dt):
        if self.version == 1:
            self.__updateVersion1__(dt)
        elif self.version == 2:
            self.__updateVersion2__(dt)
        elif self.version == 3:
            self.__updateVersion3__(dt)
        
    def __updateVersion1__(self, dt):
        '''Entity jumps from node to node.  
        No visual movement.'''
        pass
    
    def __updateVersion2__(self, dt):
        '''Entity visually moves from node to node, 
        but stops on each node'''
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
    
    def __updateVersion3__(self, dt):
        '''Entity visually moves from node to node, 
        but does not stop on each node'''
        self.moveTowardsTarget(dt)
        if self.overshotTarget():
            self.targetOvershot = True
            self.node = self.target
            self.setValidDirections()

            if self.keyDirection:# if a key is being pressed
                if self.isValidDirection(self.keyDirection):
                    if self.keyDirection != self.entity.direction:
                        self.changeDirection()
                    else:#is in the same direction
                        self.setTarget(self.entity.direction)
                else: #key direction not in valid directions
                    self.restOnNode(self.node)
            else: #key not being pressed
                self.restOnNode(self.node)
               
        else: #has not overshot target
            self.targetOvershot = False
            if self.isResting():
                self.setValidDirections()
                if self.isValidDirection(self.keyDirection):
                    self.setEntityDirection(self.keyDirection)
                else:
                    if self.keyDirection:
                        self.entity.facingDirection = self.keyDirection
            else:
                if self.keyDirection == self.entity.direction*-1:
                    self.reverseDirection()
          
    def setValidDirections(self):
        '''Set the valid directions that the entity is allowed to move'''
        self.validDirections = self.nodes[self.node].neighbors.keys()
        self.removeHiddenNodes()
        self.removeOccupiedNodes()
        
    def removeHiddenNodes(self):
        '''If a node is defined as hidden, then remove from valid directions'''
        for nodeVal in self.nodes[self.entity.node].hidden:
            for direction in self.nodes[self.entity.node].neighbors.keys():
                if self.nodes[self.entity.node].neighbors[direction] == nodeVal:
                    self.removeDirection(direction)

    def removeOccupiedNodes(self):
        '''If a node is occupied with another object, remove it'''
        for direction in self.nodes[self.node].neighbors.keys():
            node = self.area.nodes.getNeighborNode(self.node, direction)
            if node.occupied:
                self.removeDirection(direction)

    def removeDirection(self, direction):
        try:
            self.validDirections.remove(direction)
        except ValueError:
            pass
    
    def setEntityDirection(self, direction):
        '''Set valid directions when in between nodes'''
        self.entity.direction = direction
        self.entity.facingDirection = direction
        self.setTarget(direction)
        self.validDirections = [direction, direction*-1]
        #print direction
        
    def lengthFromNode(self, vector):
        vec = vector - self.nodes[self.node].position
        return vec.magnitudeSquared()
    
    def overshotTarget(self):
        '''Check if entity has overshot target node'''
        nodeToTarget = self.lengthFromNode(self.nodes[self.target].position)
        nodeToSelf = self.lengthFromNode(self.entity.position-self.areaPos)
        return nodeToSelf > nodeToTarget and self.node != self.target

    def moveTowardsTarget(self, dt):
        '''Move entity towards the target'''
        self.updateEntityVelocity()

    def updateEntityVelocity(self):
        direction = DIRECTIONS[self.entity.direction]
        self.entity.velocity = direction * self.entity.speed

    def setTarget(self, direction):
        '''Set a new target based on the direction'''
        self.target = self.nodes[self.node].neighbors[direction]
        
    def reverseDirection(self):
        '''Swap the node and target'''
        temp = self.target
        self.target = self.node
        self.node = temp
        self.entity.direction *= -1
        self.entity.facingDirection *= -1

    def removeOppositeDirection(self):
        '''Remove opposite direction only if there are other 
        directions to choose from'''
        self.setValidDirections()
        if self.isValidDirection(self.entity.direction*-1):
            if len(self.validDirections) > 1:
                self.validDirections.remove(self.entity.direction*-1)

    def portal(self):
        if self.nodes[self.node].portal:
            self.node = self.nodes[self.node].portal
            self.placeOnNode(self.node)
            self.setValidDirections()
            
    def checkCurrentDirection(self):
        '''Check if entity is able to continue in current direction'''
        if self.isValidDirection(self.entity.direction):
            self.setTarget(self.entity.direction)
        else:
            self.restOnNode(self.node)

    def restOnNode(self, node):
        '''Set the entity on top of a node and rest'''
        if not self.entity.npc:
            self.entity.position = self.area.nodePosition(node)
        self.entity.previousDirection = self.entity.direction
        self.entity.direction = STOP
        self.updateEntityVelocity()
        
    def isResting(self):
        '''Return True if entity is at rest'''
        return self.entity.direction == STOP
        
    def isValidDirection(self, direction):
        '''Return True if direction is a valid direction'''
        return direction in self.validDirections
        
    def changeDirection(self):
        '''Change entities direction'''
        self.restOnNode(self.node)
        self.setEntityDirection(self.keyDirection)
        


