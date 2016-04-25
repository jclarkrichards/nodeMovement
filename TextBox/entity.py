import pygame
from vectors import Vector2D

class Character(object):
    def __init__(self, surfaceObj):
        self.image = surfaceObj
        self.position = Vector2D()
        self.size = self.image.get_size()
        self.alive = True
        
    def update(self, dt):
        pass
    
    def setPositionManual(self, position):
        '''position can be a tuple or a list in (x,y) format'''
        self.position = Vector2D(tuple(position))
        
    def setPosition(self, position, col, row):
        #print self.size
        self.position = Vector2D(self.size[0]*col, self.size[1]*row)
        #self.position = position + Vector2D(self.size[0]*col, self.size[1]*row)

    def setSize(self):
        self.size = self.image.get_size()
        
    def render(self, screen):
        if self.alive:
            screen.blit(self.image, self.position.toTuple())
    
