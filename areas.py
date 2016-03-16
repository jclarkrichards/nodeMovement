from node import NodeGroup
from nodemovement import FourWayMovement

class Area1(object):
    def __init__(self, width, height):
        self.ID = 1
        self.mapName = 'map_junk.txt'
        self.playerStart = 2
        nodes = NodeGroup(width, height)
        nodes.createNodeList(self.area.mapName)
        self.nodes = nodes.nodeDict
        self.neighbors = {}
        
        
        
class World(object):
    def __init__(self):
        self.mapName = ''
        self.nodes = {}
        self.neighbors = {}
        self.ID = 0
        self.playerStart = 0
        self.movers = {}
        
        
class Area1(World):
    def __init__(self):
        World.__init__(self)
        self.ID = 1
        self.mapName = 'area2.txt'
        self.playerStart = 2
    
    def addPlayer(self, entity):
        entity.ID = 1 #for testing
        self.movers[entity.ID] = FourWayMovement(self.nodes, self.playerStart, entity, version=3)


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
        self.area.addPlayer(entity)
        
    def loadMapData(self):
        self.nodeCalculator.createNodeList(self.area.mapName)
        self.area.nodes = self.nodeCalculator.nodeDict
        
    def update(self, dt):
        for mover in self.area.movers.values():
            mover.update(dt)

    def render(self, screen):
        self.nodeCalculator.render(screen)
   


        
        
