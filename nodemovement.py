import pygame
from pygame.locals import *
from vectors import Vector2D

UP, DOWN, LEFT, RIGHT, STOP = (1, -1, 2, -2, 0)
DIRECTIONS = {UP:Vector2D(0,-1), DOWN:Vector2D(0,1),
              LEFT:Vector2D(-1,0), RIGHT:Vector2D(1,0), STOP:Vector2D()}

class FourWayMovement(object):
    def __init__(self, entity, version=1):
        '''nodes is the dictionary of all nodes.  
        nodeVal is the value of the starting node.
        entity is the Entity that moves around the nodes.
        version is the type of movement required. (1, 2, or 3)'''
        self.nodes = {}
        self.node = 0
        self.target = 0
        self.entity = entity
        self.version = version
        self.keyDirection = STOP
        self.targetOvershot = False
        self.areaPos = Vector2D() #for testing the nodes on area idea
        self.minDistance = 0
        
    def setMinDistance(self, tilesize):
        '''Minimum distance between nodes'''
        self.minDistance = tilesize
        
    def test(self):
        self.setValidDirections()
        if self.version == 3:
            if self.isValidDirection(self.entity.direction):
                self.setEntityDirection(self.entity.direction)
                
    def loadNewNodes(self, nodes, startNode):
        '''Load a new set of nodes to use'''
        self.nodes = nodes
        self.node = startNode
        self.target = startNode
        self.keyDirection = self.entity.direction #STOP
        self.placeOnNode(self.node)

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
        #print self.node
        if self.overshotTarget():
            self.targetOvershot = True
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
                self.restOnNode(self.node)
               
        else: #has not overshot target
            self.targetOvershot = False
            if self.isResting():
                if self.isValidDirection(self.keyDirection):
                    self.setEntityDirection(self.keyDirection)
            else:
                if self.keyDirection == self.entity.direction*-1:
                    self.reverseDirection()
          
    #def setValidNodeVals(self, nodeVal):
    #    '''Set the valid node values that the entity is allowed to move'''
    #    self.validValues = self.nodes[nodeVal].neighbors.values()
    #    for val in self.nodes[nodeVal].hidden:
    #        if val in self.validValues:
    #            self.validValues.remove(val)
        
    def setValidDirections(self):
        '''Set the valid directions that the entity is allowed to move'''
        self.validDirections = self.nodes[self.node].neighbors.keys()
        self.removeHiddenNodes()
        
    def removeHiddenNodes(self):
        '''If a node is defined as hidden, then remove from valid directions'''
        for nodeVal in self.nodes[self.node].hidden:
            for direction in self.nodes[self.node].neighbors.keys():
                if self.nodes[self.node].neighbors[direction] == nodeVal:
                    try:
                        self.validDirections.remove(direction)
                    except ValueError:
                        pass
                      
    def getNeighborValue(self, node, direction):
        '''Return the value of a neighbor in a direction'''
        return self.nodes[node].neighbors[direction]
    
    def setEntityDirection(self, direction):
        '''Set valid directions when in between nodes'''
        self.entity.direction = direction
        self.setTarget(direction)
        self.validDirections = [direction, direction*-1]
        
    def lengthFromNode(self, vector):
        vec = vector - self.nodes[self.node].position
        return vec.magnitudeSquared()

    def currentNode(self):
        return self.nodes[self.node]

    def currentTarget(self):
        return self.nodes[self.target]
    
    def overshotTarget(self):
        '''Check if entity has overshot target node'''
        nodeToTarget = self.lengthFromNode(self.nodes[self.target].position)
        nodeToSelf = self.lengthFromNode(self.entity.position-self.areaPos)
        return nodeToSelf > nodeToTarget

    def moveTowardsTarget(self, dt):
        '''Move entity towards the target'''
        direction = DIRECTIONS[self.entity.direction]
        self.entity.velocity = direction * self.entity.speed
        #ds = self.entity.velocity*dt
        #ds.vecRound(1)
        #self.entity.position += ds
        self.entity.position += self.entity.velocity*dt

    def setTarget(self, direction):
        '''Set a new target based on the direction'''
        self.target = self.nodes[self.node].neighbors[direction]
        
    def reverseDirection(self):
        '''Swap the node and target'''
        temp = self.target
        self.target = self.node
        self.node = temp
        self.entity.direction *= -1

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
        self.placeOnNode(node)
        self.entity.previousDirection = self.entity.direction
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
        
    def placeOnNode(self, nodeVal):
        '''Place the entity on top of a node'''
        p = self.nodes[nodeVal].position + self.areaPos
        #self.entity.position = p
        if self.minDistance > 0:
            ds = p.diffToNearest(self.minDistance)
        else:
            ds = Vector2D()
        #self.entity.position += ds
        self.areaPos += ds
        self.entity.position = self.nodes[nodeVal].position + self.areaPos
        #dx = round(p.x/64.0)*64.0 - p.x
        #dy = round(p.y/64.0)*64.0 - p.y
        #self.position.x += dx
        #self.position.y += dy
        #self.areaPos.y += dx
        #self.areaPos.y += dy
        #self.entity.position = p.roundToNearest(64.0)
        #self.entity.position = self.nodes[nodeVal].position + self.areaPos
        
    def setKeyDirection(self, key):
        '''Set the direction of the key being pressed'''
        if key[K_UP]:
            self.keyDirection = UP
        elif key[K_DOWN]:
            self.keyDirection = DOWN
        elif key[K_RIGHT]:
            self.keyDirection = RIGHT
        elif key[K_LEFT]:
            self.keyDirection = LEFT
        else:
            self.keyDirection = None
    '''        
    def keyContinuous(self, key):
        if key[K_UP]:
            self.keyDirection = UP
        elif key[K_DOWN]:
            self.keyDirection = DOWN
        elif key[K_RIGHT]:
            self.keyDirection = RIGHT
        elif key[K_LEFT]:
            self.keyDirection = LEFT
        else:
            self.keyDirection = None
        
    def keyDiscrete(self, key):
        if key == K_LEFT:
            self.keyDirection = LEFT
        elif key == K_RIGHT:
            self.keyDirection = RIGHT
        elif key == K_UP:
            self.keyDirection = UP
        elif key == K_DOWN:
            self.keyDirection = DOWN
    '''


