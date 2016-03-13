import pygame
from pygame.locals import *
from pacman import PacMan
from constants import *
from modeswitcher import ModeSwitcher
from groups import GhostGroup
from levelnodes import Level1Nodes
from pellets import PelletGroup

pygame.init()
screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
background = pygame.surface.Surface(SCREENSIZE).convert()
background.fill(BLACK)
nodes = Level1Nodes()
pacman = PacMan(*nodes.setPacNode())
clock = pygame.time.Clock()
ghosts = GhostGroup()
gameMode = ModeSwitcher()
start = False

pellets = PelletGroup('pellet_map.txt')
pellets.setupPellets()

while True:
    dt = clock.tick(30) / 1000.0
    if start:
        gameMode.update(dt)

    key_pressed = pygame.key.get_pressed()
    pacman.mover.keyContinuous(key_pressed)

    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        elif event.type == KEYDOWN:
            pacman.mover.keyDiscrete(event.key)
            if event.key == K_h:
                start = True
    if start:
        pellets.update(pacman, gameMode)
        ghosts.checkModeChange(gameMode)
        pacman.update(dt)
        ghosts.setGoal(pacman)
        ghosts.update(dt)
        #pellets.checkCollision(pacman)
        
    screen.blit(background, (0,0))
    nodes.render(screen)
    pellets.render(screen)
    pacman.render(screen)
    ghosts.render(screen)
    pygame.display.update()
