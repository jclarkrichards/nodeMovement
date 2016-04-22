import pygame
from vectors import Vector2D
from nodemovement import FourWayMovement

class World(object):
    def __init__(self):
        self.screenSize = (0, 0)
        self.tileSize = 1
        self.background = None
        self.screen = None
        self.dynamicOBJ = {}
        self.player = None
        self.areas = []
        self.area = None
        self.moveCalc = FourWayMovement(3)
        self.npcs = []
        
    def setup(self, x, y, tileSize=1):
        '''Set the width and height and size of each tile'''
        self.tileSize = float(tileSize)
        pygame.init()
        self.screen = self.setScreenSize(x*tileSize, y*tileSize)
        self.setBackground()
        
    def setScreenSize(self, width, height):
        self.screenSize = (width, height)
        return pygame.display.set_mode(self.screenSize, 0, 32)
        
    def setBackground(self):
        self.background = pygame.surface.Surface(self.screenSize).convert()
        self.background.fill((0,0,0))

    def addArea(self, area):
        self.areas.append(area)
        
    def addPlayer(self, entity):
        '''Set the player in the game'''
        self.player = entity
        
    def loadStartArea(self, area):
        '''An area is an object that defines the nodes and anything
        else that needs to be loaded into the world'''
        self.clearAll()
        self.area = area
        self.player.node = area.playerStart
        self.player.target = area.playerStart
        self.player.keyDirection = self.player.direction
        self.player.position = area.nodePosition(area.playerStart)
        self.centerEntities()
        for node, npc in self.area.entities.items():
            npc.position = area.nodePosition(node)
            self.npcs.append(npc)
       
    def loadTransferArea(self, nodeVal, areaVal):
        self.clearAll()
        self.area = self.areas[areaVal]
        self.area.reload()
        self.player.node = nodeVal
        self.player.target = nodeVal
        self.player.position = self.area.nodePosition(nodeVal)
        self.centerEntities()
        self.player.keyDirection = self.player.previousDirection
        self.player.overrideKeys = True
        for node, npc in self.area.entities.items():
            npc.position = area.nodePosition(node)
            self.npcs.append(npc)
        
    def centerEntities(self):
        '''Center the player and adjust the other entities'''
        x, y = self.screenSize
        centerVec = Vector2D(x/2, y/2)
        offset = centerVec - self.player.position
        self.area.position += offset
        self.player.position += offset
        
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
    
    def update(self, dt):
        self.scroll(dt)
        self.moveCalc.updatePosition(self.player, self.area, dt)
        node = self.area.nodes.table[self.player.node]
        target = self.area.nodes.table[self.player.target]
        self.loadArea(node, target)
        
    def loadArea(self, node, target):
        '''Loads a new area if conditions are right'''
        if self.player.targetOvershot:
            if node.transfer:
                if (self.player.previousDirection not in
                    target.neighbors):
                    self.loadTransferArea(*node.transfer)

    def scroll(self, dt):
        '''Scroll the screen'''
        self.area.position -= self.player.velocity*dt

    def clearDynamicObjects(self):
        self.dynamicOBJ = {}
        
    def clearNPCs(self):
        self.npcs = []
        
    def clearAll(self):
        '''Clear out all objects and nodes from the world'''
        self.clearDynamicObjects()
        self.clearNPCs()
    
    def render(self):
        self.screen.blit(self.background, (0,0))
        self.screen.blit(self.area.surface, self.area.position.toTuple())
        self.drawNodes(self.area.surface)
        self.player.render(self.screen)
        for npc in self.npcs:
            npc.render(self.area.surface)

    def drawNodes(self, surface):
        '''Really only used for testing purposes'''
        for node in self.area.nodes.table.values():
            pos1 = node.position.toTuple()
            for nextnodeVal in node.neighbors.values():
                pos2 = self.area.nodes.table[nextnodeVal].position.toTuple()
                pygame.draw.line(surface, (255,255,255), pos1, pos2, 2)
        for node in self.area.nodes.table.values():
            pos1 = node.position.toTuple()
            pos1 = (int(pos1[0]), int(pos1[1]))
            pygame.draw.circle(surface, (255,255,255), pos1, 6)
