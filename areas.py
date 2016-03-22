from node import NodeGroup
from nodemovement import FourWayMovement

class Area1(object):
    def __init__(self, width, height):
        self.ID = 1
        mapName = 'maze_junk.txt'
        self.playerStart = 2
        nodes = NodeGroup(width, height)
        nodes.createNodeList(mapName)
        self.nodes = nodes.nodeDict
        self.neighbors = {}
        self.entityList = []


class Area2(object):
    def __init__(self, width, height):
        self.ID = 2
        mapName = 'maze_junk2.txt'
        self.playerStart = 5
        nodes = NodeGroup(width, height)
        nodes.createNodeList(mapName)
        self.nodes = nodes.nodeDict
        self.neighbors = {}
        self.entityList = []


class AreaTest(object):
    def __init__(self, width, height):
        self.ID = 2
        mapName = 'area_test.txt'
        self.playerStart = 1
        nodes = NodeGroup(width, height)
        nodes.createNodeList(mapName)
        self.nodes = nodes.nodeDict
        self.neighbors = {}
        self.entityList = []

        



        
        
