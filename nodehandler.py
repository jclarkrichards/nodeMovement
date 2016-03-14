from node import NodeGroup
from nodemovement import FourWayMovement

class MapNode(object):
    def __init__(self):
        self.mapName = ''
        self.nodes = None
        self.neighbors = {}
        self.ID = 0
        self.playerStart = 0
        

class NodeHandler(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.area = None
        
    def loadMapData(self):
        pass
        

class Area1(MapNode):
    def __init__(self):
        MapNode.__init__(self)
        self.mapName = 'maze_test.txt'
        self.playerStart = 2
        
        
