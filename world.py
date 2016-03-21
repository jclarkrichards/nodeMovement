import pygame
from pygame.locals import *

class World(object):
    def __init__(self):
        self.screenSize = (0, 0)
        self.tileSize = 1
        self.background = None
        self.screen = None
        self.nodes = {}
        self.ID = 0
        self.mapNeighbors = {}
        self.keyPressed = 0
        self.dynamicOBJ = {}
        self.player = None
        
    def setup(self, x, y, tileSize=1):
        '''Set the width and height and size of each tile'''
        self.tileSize = tileSize
        pygame.init()
        self.screen = self.setScreenSize(x*tileSize, y*tileSize)
        self.setBackground()
        
    def setScreenSize(self, width, height):
        self.screenSize = (width, height)
        return pygame.display.set_mode(self.screenSize, 0, 32)
        
    def setBackground(self):
        self.background = pygame.surface.Surface(self.screenSize).convert()
        self.background.fill((0,0,0))
        
    def addPlayer(self, entity):
        '''Set the player in the game'''
        self.player = entity
        
    def addNodes(self, nodes):
        self.nodes = nodes
    
    def removeNodes(self):
        self.nodes = {}
        
    def loadNewArea(self, area):
        '''An area is an object that defines the nodes and anything
        else that needs to be loaded into the world'''
        self.clearAll()
        #self.addNodes(area.nodes)
        self.addNodes(area.subAreas[self.areaStart].nodes)
        self.player.loadNewNodes(self.nodes, area.playerStart)
        for entity in area.entityList:
            self.addDynamicObject(entity)
        
    def __addObject__(self, database, obj):
        if obj.ID in database.keys():
            return
        if len(database) == 0:
            obj.setID(0)
            database[0] = obj
            return
        newID = max(database.keys()) + 1
        obj.setID(newID)
        database[newID] = obj
    
    def addDynamicObject(self, obj):
        self.__addObject__(self.dynamicOBJ, obj)
    
    def handleEvents(self):
        '''Checks for key presses, mouse clicks, etc...'''
        self.keyPressed = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
    
    def update(self, dt):
        self.player.move(dt, self.keyPressed)
    
    def clearDynamicObjects(self):
        self.dynamicOBJ = {}
        
    def clearAll(self):
        '''Clear out all objects and nodes from the world'''
        self.removeNodes()
        self.clearDynamicObjects()
    
    def render(self):
        self.screen.blit(self.background, (0,0))
        self.drawNodes()
        self.player.render(self.screen)
        for item in self.dynamicOBJ.values():
            item.render(self.screen)

    def drawNodes(self):
        '''Really only used for testing purposes'''
        for node in self.nodes.values():
            pos1 = node.position.toTuple()
            for nextnodeVal in node.neighbors.values():
                pos2 = self.nodes[nextnodeVal].position.toTuple()
                pygame.draw.line(self.screen, (255,255,255), pos1, pos2, 2)
        for node in self.nodes.values():
            pos1 = node.position.toTuple()
            pygame.draw.circle(self.screen, (255,255,255), pos1, 6)
