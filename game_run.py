import pygame
from pygame.locals import *
from player import Player
from entity import Entity
from world import World
from areas import *
from TextBox.textboxes import TextBox

class Game(object):
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.world = World()
        self.world.setup(4, 3, 64)
        self.player = Player()
        self.world.addPlayer(self.player)
        area = AreaTest(64, 64)
        area2 = AreaTest2(64, 64)
        area3 = AreaTest3(64, 64)
        npc = Entity()
        npc.dialog = "Hello, I am an NPC"

        npc2 = Entity()
        npc2.dialog = "Hello, I am another NPC"
        area.addEntity(npc, 10)
        area2.addEntity(npc2, 4)
        print npc.node, npc.target
        self.world.addArea(area)
        self.world.addArea(area2)
        self.world.addArea(area3)
        self.world.loadStartArea(area)
        self.keyPressed = None

        self.box = TextBox(2, 25)
        self.box.setFont('deluxefont8px.png', 'text_map.txt', (8,8))
        self.box.setPosition(self.world.screenSize, lower=True)

    def controls(self):
        self.keyPressed = pygame.key.get_pressed()
        self.player.setKeyedDirection(self.keyPressed)
        if self.keyPressed[K_SPACE]:
            self.box.increaseSpeed()

        #print self.player.facingDirection, self.player.direction
        for event in pygame.event.get():
            if event.type == QUIT:
                self.quitGame()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE: #Action key
                    self.displayDialogBox()
            elif event.type == KEYUP:
                if event.key == K_SPACE:
                    self.box.resetSpeed()

    def displayDialogBox(self):
        d = self.player.facingDirection
        if not self.player.direction:
            #return node that the player is facing towards
            node = self.world.area.nodes.getNeighborNode(self.player.node, d)
            if node:
                #print node.ID, node.occupied, node.occupant
                if node.occupied and node.occupant:
                    self.box.readoutCharacters(node.occupant.dialog, 15)
                    #print node.occupant.dialog

    def readObjectText(self):
        pass
    
    def pause(self):
        pass
    
    def quitGame(self):
        '''Quit the game'''
        exit()
        
    def gameLoop(self):
        while True:
            dt = self.clock.tick(30) / 1000.0
            self.controls()
            if not self.box.active:
                self.world.update(dt)
            self.box.update(dt)
            self.world.render()
            self.box.render(self.world.screen)
            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.gameLoop()
