import pygame
from vectors import Vector2D
from entity import Entity
from image_set import SpriteHandler
from constants import *

class Player(Entity):
    def __init__(self):
        Entity.__init__(self)
        self.direction = 0
        self.previousDirection = 0
        self.facingDirection = 0
        self.speed = 60
        self.velocity = Vector2D()
        self.overrideKeys = False
        self.npc = False
        spriteHandler = SpriteHandler('PNG/joseph_basic.bmp')
        self.images = spriteHandler.grabSet((0,0,16,16), cols=4)
        self.image = self.images[0]
        
        
    def update(self, dt):
        if self.facingDirection == UP:
            self.image = self.images[0]
        elif self.facingDirection == DOWN:
            self.image = self.images[1]
        elif self.facingDirection == LEFT:
            self.image = self.images[2]
        elif self.facingDirection == RIGHT:
            self.image = self.images[3]
            
    
 


