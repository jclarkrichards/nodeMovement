import pygame
from pygame.locals import *
from vectors import Vector2D
from constants import *
#from nodemovement import FourWayMovement

class Entity(object):
    def __init__(self):
        self.ID = 0
        self.position = Vector2D() 
        self.direction = 0
        self.keyDirection = 0
        self.facingDirection = 0
        self.previousDirection = 0
        self.speed = 60
        self.velocity = Vector2D()
        self.dialog =''
        self.node = 0  #int value
        self.target = 0  #int value
        #self.overshotTarget = False
        self.targetOvershot = False
        self.overrideKeys = False
        
    def update(self, dt):
        pass
    
    def move(self, dt, key_pressed=None):
        '''Move entity around the nodes'''
        pass
    
    def performAction(self):
        '''Executes when action key is pressed'''
        pass

    def setKeyedDirection(self, key):
        '''key being pressed or simulated pressed'''
        if not self.overrideKeys:
            self.previousDirection = self.direction
            if key[K_UP]:
                self.keyDirection = UP
            elif key[K_DOWN]:
                self.keyDirection = DOWN
            elif key[K_RIGHT]:
                self.keyDirection = RIGHT
            elif key[K_LEFT]:
                self.keyDirection = LEFT
            else:
                self.keyDirection = None

    def render(self, screen):
        x, y = self.position.toTuple()
        pygame.draw.circle(screen, (200,200,0), (int(x), int(y)), 8)
