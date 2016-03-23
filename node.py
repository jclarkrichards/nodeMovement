import pygame
from vectors import Vector2D
from numpy import loadtxt
import numpy
"testing"
UP = 1
DOWN = -1
LEFT = 2
RIGHT = -2
STOP = 0
DIRECTIONS = {UP:Vector2D(0,-1), DOWN:Vector2D(0,1),
              LEFT:Vector2D(-1,0), RIGHT:Vector2D(1,0), STOP:Vector2D()}

class Node(object):
    def __init__(self, pos):
        self.position = Vector2D(pos)
        self.neighbors = {}
        self.hidden = []
        self.COLOR = (255,255,255)
        self.portal = None

class NodeGroup(object):
    def __init__(self, tileW, tileH):
        self.nodeDict = {}
        self.layout = None
        self.tileW = tileW
        self.tileH = tileH
        self.rows, self.cols = (0, 0)

    def createNodeList(self, filename):
        '''Create a dictionary of nodes'''
        self.nodeDict = {}
        dt = numpy.dtype((str, 2))
        self.layout = loadtxt(filename, dtype=dt)
        self.rows, self.cols = self.layout.shape

        for row in range(self.rows):
            for col in range(self.cols):
                self.createNodeFromLayout(row, col)
                if self.isPositiveDigit(row, col):
                    self.walkRight(row, col)
                    self.walkDown(row, col)
                    self.walkLeft(row, col)
                    self.walkUp(row, col)

        #numpy.savetxt('maze_nodes2.txt', self.layout, fmt='%s')
        
    def isOutOfBounds(self, row, col):
        '''Check if requested row and column values are out of bounds'''
        if row >= 0 and col >= 0:
            try:
                val = self.layout[row][col]
            except IndexError:
                return True
            else:
                return False
        return True

    def createNodeFromLayout(self, row, col):
        '''Create Node object and add to dictionary'''
        if self.layout[row][col] == '+':
            try:
                nodeNum = max(self.nodeDict.keys())
            except ValueError:
                nodeNum = 0
            finally:
                nodeNum += 1
                self.nodeDict[nodeNum] = Node((col*self.tileW, row*self.tileH))
                self.layout[row][col] = str(nodeNum)

    def isPositiveDigit(self, row, col):
        '''Check if layout value is a positive digit'''
        if str(self.layout[row][col]).isdigit():
            if int(self.layout[row][col]) > 0:
                return True
        return False

    def isValidPath(self, row, col, pathVal):
        '''Check if layout value is same as pathVal'''
        if not self.isOutOfBounds(row, col):
            if self.layout[row][col] == pathVal:
                return True
        return False

    def linkNodes(self, row1, col1, row2, col2):
        '''Link Node2 to Node1 as a neighbor'''
        if self.isPositiveDigit(row2, col2):
            nodeVal1 = int(self.layout[row1][col1])
            nodeVal2 = int(self.layout[row2][col2])
            self.addNeighborOneWay(nodeVal1, nodeVal2)
            
    def addNeighborOneWay(self, nodeVal1, nodeVal2):
        '''Set the node at nodeVal2 as a neighbor of node at nodeVal1'''
        tempVec = self.nodeDict[nodeVal2].position - \
                  self.nodeDict[nodeVal1].position
        tempVec = tempVec.normalize()
        for key in DIRECTIONS.keys():
            if DIRECTIONS[key] == tempVec:
                direction = key
                break
        self.nodeDict[nodeVal1].neighbors[direction] = nodeVal2

    def addNeighborTwoWay(self, nodeVal, neighborVal):
        self.addNeighborOneWay(nodeVal, neighborVal)
        self.addNeighborOneWay(neighborVal, nodeVal)

    def removeNeighborOneWay(self, nodeVal1, nodeVal2):
        '''Remove nodeVal2 from a nodeVal1 as a neighbor'''
        for key in self.nodeDict[nodeVal1].neighbors.keys():
            if self.nodeDict[nodeVal1].neighbors[key] == nodeVal2:
                junk = self.nodeDict[nodeVal1].neighbors.pop(key)
                break

    def removeNeighborTwoWay(self, nodeVal, neighborVal):
        self.removeNeighborOneWay(nodeVal, neighborVal)
        self.removeNeighborOneWay(neighborVal, nodeVal)
        
    def addNode(self, pos, key=None):
        '''Manually add a node to the nodeDict'''
        if key:
            self.nodeDict[key] = Node(pos)
        else:
            num = max(self.nodeDict.keys())
            num += 1
            self.nodeDict[num] = Node(pos)

    def addHiddenNode(self, nodeVal1, nodeVal2):
        '''Add nodeVal2 as a hidden node to nodeVal1'''
        self.nodeDict[nodeVal1].hidden.append(nodeVal2)
        
    def clearAndAddHidden(self, nodeVal1, nodeVal2):
        '''Clear the hidden nodes and add a new hidden node'''
        self.nodeDict[nodeVal1].hidden = []
        self.addHiddenNode(nodeVal1, nodeVal2)
        
    def clearHiddenNodes(self, nodeVal):
        '''Clear the hidden nodes'''
        self.nodeDict[nodeVal].hidden = []
        
    def walkRight(self, row, col):
        '''Try and find nodes to the right'''
        dx = 1
        while self.isValidPath(row, col+dx, '-'):
            dx += 1
        if not self.isOutOfBounds(row, col+dx):
            self.createNodeFromLayout(row, col+dx)
            self.linkNodes(row, col, row, col+dx)

    def walkLeft(self, row, col):
        '''Try and find nodes to the left'''
        dx = 1
        while self.isValidPath(row, col-dx, '-'):
            dx += 1
        if not self.isOutOfBounds(row, col-dx):
            self.createNodeFromLayout(row, col-dx)
            self.linkNodes(row, col, row, col-dx)

    def walkDown(self, row, col):
        '''Try and find nodes down'''
        dy = 1
        while self.isValidPath(row+dy, col, '|'):
            dy += 1
        if not self.isOutOfBounds(row+dy, col):
            self.createNodeFromLayout(row+dy, col)
            self.linkNodes(row, col, row+dy, col)

    def walkUp(self, row, col):
        '''Try and find nodes up'''
        dy = 1
        while self.isValidPath(row-dy, col, '|'):
            dy += 1
        if not self.isOutOfBounds(row-dy, col):
            self.createNodeFromLayout(row-dy, col)
            self.linkNodes(row, col, row-dy, col)

    def render(self, screen):
        for node in self.nodeDict.values():
            pos1 = node.position.toTuple()
            for nextnodeVal in node.neighbors.values():
                pos2 = self.nodeDict[nextnodeVal].position.toTuple()
                pygame.draw.line(screen, (255,255,255), pos1, pos2, 2)
        for node in self.nodeDict.values():
            pos1 = node.position.toTuple()
            pygame.draw.circle(screen, node.COLOR, pos1, 5)

