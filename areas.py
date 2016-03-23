from node import NodeGroup
from nodemovement import FourWayMovement
from vectors import Vector2D

class SubArea(object):
    def __init__(self):
        self.startX, self.endX = (0,0)
        self.startY, self.endY = (0,0)
        self.nodes = {}
        self.active = False
        self.neighbors = {}
        self.entityOffset = Vector2D()
        self.start = Vector2D()
        self.end = Vector2D()
        
    def setDimensions(self, row, col, width, height):
        self.start = Vector2D(col, col+1) * width
        self.end = Vector2D(row, row+1) * height
        #self.startX = col*width
        #self.endX = (col+1)*width
        #self.startY = row*height
        #self.endY = (row+1)*height

        
class AreaAbstract(object):
    def __init__(self, width, height):
        self.tileWidth, self.tileHeight = width, height
        self.width, self.height = (0, 0)
        self.ID = 0
        self.playerStart = 1
        self.areaStart = 0
        self.nodes = {}
        self.neighbors = {}
        self.entityList = []
        self.subAreas = {}

    def load(self, mapName):
        nodes = NodeGroup(self.tileWidth, self.tileHeight)
        nodes.createNodeList(mapName)
        self.nodes = nodes.nodeDict
        self.width = nodes.cols * self.tileWidth
        self.height = nodes.rows * self.tileHeight
        #print self.width, self.height

    def divideIntoSubAreas(self, screenW, screenH):
        '''Divide the area into multiple subAreas the size of the screen'''
        rows = self.height / screenH
        cols = self.width / screenW
        numArea = 0
        #print rows, cols
        for row in range(rows):
            for col in range(cols):
                self.subAreas[numArea] = SubArea()
                self.subAreas[numArea].setDimensions(row, col,
                                                     screenW, screenH)
                self.subAreas[numArea].entityOffset = Vector2D(col*screenW,
                                                               row*screenH)
                self.distributeNodes(self.subAreas[numArea])
                numArea += 1
                
    def distributeNodes(self, area):
        '''Distribute the nodes into the subAreas'''
        for nodeVal in self.nodes.keys():
            nodePos = self.nodes[nodeVal].position
            if (nodePos.x >= area.start.x and
                nodePos.x < area.end.x and
                nodePos.y >= area.start.y and
                nodePos.y < area.end.y):
                area.nodes[nodeVal] = self.nodes[nodeVal]

        #works, but need to figure out rest before activating this
        #for nodeVal in area.nodes.keys():
        #    junk = self.nodes.pop(nodeVal)

            
            
class Area1(AreaAbstract):
    def __init__(self, width, height):
        AreaAbstract.__init__(self, width, height)
        self.ID = 1
        self.load('maze_junk.txt')
        self.playerStart = 2


class Area2(AreaAbstract):
    def __init__(self, width, height):
        AreaAbstract.__init__(self, width, height)
        self.ID = 2
        self.load('maze_junk2.txt')
        self.playerStart = 5


class AreaTest(AreaAbstract):
    def __init__(self, width, height):
        AreaAbstract.__init__(self, width, height)
        self.ID = 2
        self.load('area_test.txt')
        self.playerStart = 1



        



        
        
