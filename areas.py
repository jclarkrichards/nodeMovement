from node import NodeGroup
from nodemovement import FourWayMovement

class AreaSub(object):
    def __init__(self):
        self.startX, self.endX = (0, 0)
        self.startY, self.endY = (0, 0)
        self.neighbors = {}
        
    def setDimensions(self, row, col, width, height):
        self.startX = col*width
        self.endX = (col+1)*width
        self.startY = row*height
        self.endY = (row+1)*height
    
    
class AreaAbstract(object):
    def __init__(self, width, height):
        self.tileWidth, self.tileHeight = (width, height)
        self.width, self.height = (0, 0)
        self.ID = 0
        self.playerStart = 0
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
        
    def divideIntoSubAreas(self, screenWidth, screenHeight):
        '''Divide the area into multiple subareas'''
        rows = self.height / screenHeight
        cols = self.width / screenWidth
        numArea = 0
        for row in range(rows):
            for col in range(cols):
                self.subArea[numArea] = AreaSub()
                self.subArea[numArea].setDimensions(row, col, screenWidth, screenHeight)
                numArea += 1
    
    
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
        
     

        



        
        
