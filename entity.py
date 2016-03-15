import pygame
from vectors import Vector2D

class Entity(object):
    def __init__(self):
        self.ID = 0
        self.position = Vector2D() 
        self.direction = 0
        self.speed = 60
        
    def update(self, dt):
        pass

    def render(self, screen):
        x, y = self.position.toTuple()
        pygame.draw.circle(screen, (200,200,0), (int(x), int(y)), 8)
