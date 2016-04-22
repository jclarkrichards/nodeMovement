import pygame
from vectors import Vector2D
from entity import Entity

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
        
    def update(self, dt):
        pass
    
 


