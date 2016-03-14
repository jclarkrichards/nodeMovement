from node import NodeGroup
from nodemovement import FourWayMovement

class MapNode(object):
    def __init__(self):
        self.mapName = ''
        self.nodes = {}
        self.neighbors = {}
        self.ID = 0
        self.playerStart = 0
        self.movers = {}
        
        
class Area1(MapNode):
    def __init__(self):
        MapNode.__init__(self)
        self.ID = 1
        self.mapName = 'maze_test.txt'
        self.playerStart = 2
    
    def addEntity(self, entity):
        entity.ID = 1 #for testing
        self.movers[entity.ID] = FourWayMovement(self.nodes, 1, entity, level=3)


class NodeHandler(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        #self.nodes = {}
        self.areaID = 1
        self.areas = {1:Area1()}
        self.area = self.areas[self.areaID]
        self.nodeCalculator = NodeGroup(width, height)
        self.loadMapData()
        
    def setArea(self, ID):
        self.area = self.areas[ID]
        
    def setPlayer(self, entity):
        self.player = entity
        self.area.addEntity(entity)
        
    def loadMapData(self):
        self.nodeCalculator.createNodeList(self.area.mapName)
        self.area.nodes = self.nodeCalculator.nodeDict
        
    def update(self, dt):
        for mover in self.area.moveList.values():
            mover.update(dt)
    
   


        
        
