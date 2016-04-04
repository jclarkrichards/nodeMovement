import pygame
from pygame.locals import *
from vectors import Vector2D

class World(object):
    def __init__(self):
        self.screenSize = (0, 0)
        self.tileSize = 1
        self.background = None
        self.screen = None
        self.nodes = {}
        self.activeNodes = {}
        self.ID = 0
        self.mapNeighbors = {}
        self.keyPressed = 0
        self.dynamicOBJ = {}
        self.player = None
        self.areaOffset = Vector2D()
        self.xScroll = True
        self.yScroll = True
        self.areas = []
        
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

    def addArea(self, area):
        self.areas.append(area)
        
    def addPlayer(self, entity):
        '''Set the player in the game'''
        self.player = entity
        
    def addNodes(self, nodes):
        self.nodes = nodes
    
    def removeNodes(self):
        self.nodes = {}
        
    def loadStartArea(self, area, subArea=0):
        '''An area is an object that defines the nodes and anything
        else that needs to be loaded into the world'''
        self.clearAll()
        self.addNodes(area.nodes)
        self.player.loadNewNodes(self.nodes, area.playerStart)
        #self.offsetEntities(area, subArea)
        self.centerEntities()
        
    def loadTransferArea(self, nodeVal, subAreaVal, areaVal):
        self.clearAll()
        self.areas[areaVal].reload()
        self.addNodes(self.areas[areaVal].nodes)
        self.player.loadNewNodes(self.nodes, nodeVal)
        #self.offsetEntities(self.areas[areaVal], subAreaVal)
        self.centerEntities()
        self.player.mover.keyDirection = self.player.previousDirection
        self.player.overrideKeys = True

    def offsetEntities(self, area, subArea):
        self.areaOffset = area.subAreas[subArea].entityOffset
        #print self.areaOffset
        for i in self.nodes.keys():
            #node = self.nodes[i]
            self.nodes[i].position -= self.areaOffset
        self.areaOffset *= -1
        #self.centerEntities()

    def centerEntities(self):
        '''Center the player and adjust the other entities'''
        x, y = self.screenSize
        centerVec = Vector2D(x/2, y/2)
        offset = centerVec - self.player.position
        #print centerVec, self.player.position, offset
        for i in self.nodes.keys():
            self.nodes[i].position += offset
        self.player.position += offset
        #print self.player.position
        
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
        #print self.player.position
        self.player.move(dt, self.keyPressed)
        self.scroll(dt)
        test = self.player.mover.nodes[self.player.mover.node].transfer
        if self.player.mover.targetOvershot:
            if test:
                if (self.player.previousDirection not in
                    self.player.mover.nodes[self.player.mover.target].neighbors):
                    self.loadTransferArea(*test)
                    #print "after loading"
                    #print self.player.position
                  
            #print self.player.mover.nodes[self.player.mover.target].neighbors
            #print self.player.previousDirection
            #print "Transfer!"
            print ""
            #self.loadTransferArea(*test)

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
            
        if self.areaOffset.y < 0:
            self.yScroll = False
            self.adjustYAxis()
        else:
            self.yScroll = True
            self.areaOffset.y += self.player.velocity.y*dt
        '''
    def scroll(self, dt):
        '''Scroll the screen'''
        for node in self.nodes.values():
            node.position -= self.player.velocity*dt
        self.player.position -= self.player.velocity*dt
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
            pos1 = (int(pos1[0]), int(pos1[1]))
            pygame.draw.circle(self.screen, (255,255,255), pos1, 6)
