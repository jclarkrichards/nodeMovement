from node import NodeGroup
from vectors import Vector2D
import pygame

class AreaAbstract(object):
    def __init__(self, width, height):
        self.position = Vector2D()
        self.tileWidth, self.tileHeight = width, height
        self.width, self.height = (0, 0)
        self.size = (0, 0)
        self.ID = 0
        self.playerStart = 1
        self.areaStart = 0
        self.nodes = None
        self.neighbors = {}
        self.entityList = []
        self.surface = None
        self.entities = {}
        
    def load(self, mapName):
        self.nodes = NodeGroup(self.tileWidth, self.tileHeight)
        self.nodes.createNodeList(mapName)
        self.width = self.nodes.cols * self.tileWidth
        self.height = self.nodes.rows * self.tileHeight
        self.size = (self.width, self.height)
        self.surface = pygame.Surface(self.size)
        self.surface.fill((100,20,30))
        self.position = Vector2D()
        
    def nodePosition(self, nodeVal):
        '''Return the position of a node on area with correction'''
        test = self.nodes.table[nodeVal].position + self.position
        ds = test.diffToNearest(16)
        self.position += ds
        return self.nodes.table[nodeVal].position + self.position
        
    def addEntity(self, entity, node):
        '''Add an entity and the node it must start on'''
        self.entities[node] = entity
        
    def setNodeAsOccupied(self, nodeVal):
        self.nodes.setOccupied(nodeVal)
        
   
class AreaTest(AreaAbstract):
    def __init__(self, width, height):
        AreaAbstract.__init__(self, width, height)
        self.ID = 2
        self.load('area_test2.txt')
        self.playerStart = 5
        self.nodes.table[1].transfer = (27, 1)
        self.nodes.table[21].transfer = (1, 2)
        self.nodes.table[3].occupied = True #for testing occupancy
        
    def reload(self):
        self.load('area_test2.txt')
        self.nodes.table[1].transfer = (27, 1)
        self.nodes.table[21].transfer = (1, 2)
        
class AreaTest2(AreaAbstract):
    def __init__(self, width, height):
        AreaAbstract.__init__(self, width, height)
        self.ID = 3
        self.load('area_test3.txt')
        self.playerStart = 3
        self.nodes.table[27].transfer = (1, 0)

    def reload(self):
        self.load('area_test3.txt')
        self.nodes.table[27].transfer = (1, 0)


class AreaTest3(AreaAbstract):
    def __init__(self, width, height):
        AreaAbstract.__init__(self, width, height)
        self.ID = 3
        self.load('area_test4.txt')
        self.playerStart = 3
        self.nodes.table[1].transfer = (21, 0)

    def reload(self):
        self.load('area_test4.txt')
        self.nodes.table[1].transfer = (21, 0)




        
        
