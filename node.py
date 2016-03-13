import pygame
from vectors import Vector2D
from numpy import loadtxt
from constants import *
import numpy

class Node(object):
    def __init__(self, pos):
        self.position = Vector2D(pos)
        self.neighbors = {}
        self.COLOR = WHITE
        self.portal = None
        self.hidden = []
        
class NodeGroup(object):
    def __init__(self):
        self.nodeDict = {}
        self.layout = None

    def createNodeList(self, filename):
        '''Create a dictionary of nodes'''
        dt = numpy.dtype((str, 2))
        self.layout = loadtxt(filename, dtype=dt)
        rows, cols = self.layout.shape

        for row in range(rows):
            for col in range(cols):
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
                self.nodeDict[nodeNum] = Node((col*TILEWIDTH, row*TILEHEIGHT))
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
        self.nodeDict[nodeVal1].neighbors[direction] = self.nodeDict[nodeVal2]

    def addNeighborTwoWay(self, nodeVal, neighborVal):
        self.addNeighborOneWay(nodeVal, neighborVal)
        self.addNeighborOneWay(neighborVal, nodeVal)

    def removeNeighborOneWay(self, nodeVal1, nodeVal2):
        '''Remove a neighbor from a node'''
        node = self.nodeDict[nodeVal1]
        node2 = self.nodeDict[nodeVal2]
        for key in node.neighbors.keys():
            if node.neighbors[key] == node2:
                junk = node.neighbors.pop(key)
                break

    def removeNeighborTwoWay(self, nodeVal, neighborVal):
        self.removeNeighborOneWay(nodeVal, neighborVal)
        self.removeNeighborOneWay(neighborVal, nodeVal)
        
    def addNode(self, pos, key=None):
        if key:
            self.nodeDict[key] = Node(pos)
        else:
            num = max(self.nodeDict.keys())
            num += 1
            self.nodeDict[num] = Node(pos)

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
            for nextnode in node.neighbors.values():
                pos2 = nextnode.position.toTuple()
                pygame.draw.line(screen, WHITE, pos1, pos2, 2)
        for node in self.nodeDict.values():
            pos1 = node.position.toTuple()
            pygame.draw.circle(screen, node.COLOR, pos1, 10)
