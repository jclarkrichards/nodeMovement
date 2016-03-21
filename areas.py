from node import NodeGroup
from nodemovement import FourWayMovement

NORTH, SOUTH, EAST, WEST = 1, 2, 3, 4

class AreaSub(object):
    def __init__(self):
        self.startX, self.endX = (0, 0)
        self.startY, self.endY = (0, 0)
        self.neighbors = {NORTH:None, SOUTH:None, EAST:None, WEST:None}
        self.nodes = {}
        self.active = False
        
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
        
    def deactivateAll(self):
        '''Make all areas inactive'''
        for area in self.subAreas.values():
            area.active = False
            
    def activate(self, area):
        '''Make an area active and surrounding areas'''
        self.deactivateAll()
        area.active = True
        for val in area.neighbors.values():
            if val:
                self.subAreas.active = True
        
    def divideIntoSubAreas(self, screenWidth, screenHeight):
        '''Divide the area into multiple subareas'''
        rows = self.height / screenHeight
        cols = self.width / screenWidth
        numArea = 0
        for row in range(rows):
            for col in range(cols):
                self.subAreas[numArea] = AreaSub()
                self.subAreas[numArea].setDimensions(row, col, screenWidth, screenHeight)
                self.distributeNodes(self.subAreas[numArea])
                numArea += 1
        self.setNeighbors(rows, cols)
        
    def distributeNodes(self, area):
        '''Distribute the nodes into the subAreas'''
        for nodeVal in self.nodes.keys():
            nodePos = self.nodes[nodeVal].position
            if (nodePos.x >= area.startX and
                nodePos.x < area.endX and
                nodePos.y >= area.startY and
                nodePos.y < area.endY):
                area.nodes[nodeVal] = self.nodes[nodeVal]
        for nodeVal in area.nodes.values():
            junk = self.nodes.pop(nodeVal)
                
    def setNeighbors(self, rows, cols):
        '''Set the neighbors for each subArea'''
        for areaVal in self.subAreas.keys():
            area = self.subAreas[areaVal]
            if areaVal - cols >= 0:
                area.neighbors[NORTH] = areaVal-cols
            if areaVal + cols < rows*cols:
                area.neighbors[SOUTH] = areaVal+cols
            if areaVal - 1 >= 0 and
               (areaVal-1)/cols == areaVal/cols:
                area.neighbors[WEST] = areaVal - 1
            if areaVal + 1 < rows*cols:
                if (areaVal+1)/cols == areaVal/cols:
                    area.neighbors[EAST] = areaVal + 1
    
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
        
     

        



        
        
