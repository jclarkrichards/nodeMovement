import pygame
#from pygame.locals import *
from vectors import Vector2D
from nodemovement import FourWayMovement
#import numpy as np

class World(object):
    def __init__(self):
        self.screenSize = (0, 0)
        self.tileSize = 1
        self.background = None
        self.screen = None
        #self.nodes = {}
        #self.activeNodes = {}
        #self.ID = 0
        #self.mapNeighbors = {}
        self.dynamicOBJ = {}
        self.player = None
        #self.areaOffset = Vector2D()
        #self.xScroll = True
        #self.yScroll = True
        self.areas = []
        self.area = None
        #self.areaSurface = None
        #self.surfacePos = Vector2D()
        self.moveCalc = FourWayMovement(3)
        
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
        
    #def addNodes(self, nodes):
    #    self.nodes = nodes
    
    #def removeNodes(self):
    #    self.nodes = {}
        
    def loadStartArea(self, area):
        '''An area is an object that defines the nodes and anything
        else that needs to be loaded into the world'''
        self.clearAll()
        self.area = area
        self.player.node = area.playerStart
        self.player.target = area.playerStart
        self.player.keyDirection = self.player.direction
        self.player.position = area.nodes.nodePosition(area.playerStart)
        #self.addNodes(area.nodes)
        #self.player.loadNewNodes(self.nodes, area.playerStart)
        #self.areaSurface = pygame.Surface(area.size)
        #self.areaSurface.fill((100,20,30))
        self.centerEntities()
        
    def loadTransferArea(self, nodeVal, areaVal):
        self.clearAll()
        self.area = self.areas[areaVal]
        self.area.reload()
        self.player.node = nodeVal
        self.player.target = nodeVal
        self.player.position = area.nodes.nodePosition(area.playerStart)
        #self.addNodes(self.area.nodes)
        #self.player.loadNewNodes(self.nodes, nodeVal)
        #self.areaSurface = pygame.Surface(self.areas[areaVal].size)
        #self.areaSurface.fill((100,20,30))
        self.centerEntities()
        #self.player.mover.keyDirection = self.player.previousDirection
        self.player.keyDirection = self.player.previousDirection
        self.player.overrideKeys = True

    def centerEntities(self):
        '''Center the player and adjust the other entities'''
        x, y = self.screenSize
        centerVec = Vector2D(x/2, y/2)
        offset = centerVec - self.player.position
        #for i in self.nodes.keys():
        #    self.nodes[i].position += offset
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
    
    def update(self, dt):#, key):
        self.scroll(dt)
        self.moveCalc.updatePosition(self.player, self.area, dt)
        
        #self.player.mover.areaPos = self.surfacePos
        #self.player.move(dt, key)
        #self.surfacePos = self.player.mover.areaPos
        node = self.area.nodes.table[self.player.node]
        target = self.area.nodes.table[self.player.target]
        self.loadArea(self.player.node, self.player.target)

    def loadArea(self, node, target):
        '''Loads a new area if conditions are right'''
        if self.player.targetOvershot:
            if node.transfer:
                #print node.transfer
                if (self.player.previousDirection not in
                    target.neighbors):
                    self.loadTransferArea(*node.transfer)

                  
        '''
        if self.xScroll and self.yScroll:
            self.scroll(dt)
        elif self.xScroll and not self.yScroll:
            self.scrollXAxis(dt)
        elif self.yScroll and not self.xScroll:
            self.scrollYAxis(dt)
        #print self.player.mover.nodes[self.player.mover.node]
        #for node in self.nodes.values():
        #    node.position -= self.player.velocity*dt
        #self.player.position -= self.player.velocity*dt
        #self.areaOffset += self.player.velocity*dt
        if self.areaOffset.x < 0:
            self.xScroll = False
            self.adjustXAxis()
            print self.areaOffset.x
        else:
            self.xScroll = True
            self.areaOffset.x += self.player.velocity.x*dt
v            
        if self.areaOffset.y < 0:
            self.yScroll = False
            self.adjustYAxis()
        else:
            self.yScroll = True
            self.areaOffset.y += self.player.velocity.y*dt
        '''
    def scroll(self, dt):
        '''Scroll the screen'''
        self.area.position -= self.player.velocity*dt

        #for node in self.nodes.values():
        #    node.position -= self.player.velocity*dt
        #self.player.position -= self.player.velocity*dt
        #print self.player.position, self.surfacePos
    """    
    def scrollXAxis(self, dt):
        '''Scroll the screen'''
        for node in self.nodes.values():
            node.position.x -= self.player.velocity.x*dt
        self.player.position.x -= self.player.velocity.x*dt
        
    def scrollYAxis(self, dt):
        '''Scroll the screen'''
        for node in self.nodes.values():
            node.position.y -= self.player.velocity.y*dt
        self.player.position.y -= self.player.velocity.y*dt
      
    def adjustXAxis(self):
        '''Scroll the screen'''
        if self.areaOffset.x != 0.0:
            for node in self.nodes.values():
                node.position.x += self.areaOffset.x
            self.player.position.x += self.areaOffset.x
            self.areaOffset.x = 0.0
            
    def adjustYAxis(self):
        '''Scroll the screen'''
        if self.areaOffset.y != 0.0:
            for node in self.nodes.values():
                node.position.y += self.areaOffset.y
            self.player.position.y += self.areaOffset.y
            self.areaOffset.y = 0.0
    """        
    def clearDynamicObjects(self):
        self.dynamicOBJ = {}
        
    def clearAll(self):
        '''Clear out all objects and nodes from the world'''
        #self.removeNodes()
        self.clearDynamicObjects()
    
    def render(self):
        self.screen.blit(self.background, (0,0))
        self.screen.blit(self.area.surface, self.area.position.toTuple())
        self.drawNodes(self.area.surface)
        self.player.render(self.screen)
        #for item in self.dynamicOBJ.values():
        #    item.render(self.screen)

    def drawNodes(self, surface):
        '''Really only used for testing purposes'''
        for node in self.area.nodes.table.values():
            pos1 = node.position.toTuple()
            for nextnodeVal in node.neighbors.values():
                pos2 = self.area.nodes.table[nextnodeVal].position.toTuple()
                pygame.draw.line(surface, (255,255,255), pos1, pos2, 2)
                #pygame.draw.line(self.screen, (255,255,255), pos1, pos2, 2)
        for node in self.area.nodes.table.values():
            pos1 = node.position.toTuple()
            pos1 = (int(pos1[0]), int(pos1[1]))
            pygame.draw.circle(surface, (255,255,255), pos1, 6)
            #pygame.draw.circle(self.screen, (255,255,255), pos1, 6)
