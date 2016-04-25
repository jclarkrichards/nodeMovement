import pygame
from vectors import Vector2D
from phrase import PhraseHandler
from base import Text

class TextBox(object):
    def __init__(self, lines, charPerLine):
        self.charPerLine = charPerLine
        self.lines = lines
        self.position = Vector2D()
        self.width = 0
        self.height = 0
        self.phrase = None
        self.charsize = (0, 0)
        self.iphrase = 0
        self.textSurface = None
        self.active = False
        self.font = None
        
    def reset(self):
        self.phrase = None
        self.iphrase = 0
        self.textSurface = None
        self.active = False
        
    def update(self, dt):
        if self.phrase:
            self.phrase.update(dt)

    def setFont(self, image, txtfile, size):
        self.font = Text(image, txtfile, size)
        
    def createSurface(self):
        self.textSurface = pygame.surface.Surface((self.width, self.height))
        self.textSurface.fill((0,0,0))
        
    def setDimensions(self):
        '''dimensions based on characters width and height'''
        self.width = self.charPerLine*self.charsize[0]
        self.height = self.lines*self.charsize[1]
        self.createSurface()
        
    def setPositionManual(self, position):
        self.position = Vector2D(position)
        
    def setPosition(self, screenSize, lower=False, upper=False):
        if lower:
            x = (screenSize[0] - self.width) / 2.0
            y = screenSize[1] - (self.height + 8)
            self.position = Vecto2D(x, y)
        elif upper:
            pass
        
    def setPhrase(self, phrase, scale):
        '''The input phrase is a string. table is the dictionary'''
        #self.phraseStr = phrase
        #self.reset()
        self.phrase = PhraseHandler(phrase)
        self.phrase.mapPhrase(self.font.textDict) #self.phrase.phraseList
        self.charsize = self.phrase.phraseList[0].size
        self.setDimensions()
        self.scaleCharacters(scale)
        self.setCharPositions(phrase)
        
    def scaleCharacters(self, scale):
        '''Set dimensions of characters.  Changes dimensions of box'''
        self.phrase.setScale(scale)
        self.charsize = self.phrase.phraseList[0].size
        self.setDimensions()
        
    def setCharPositions(self, phrase):
        words = phrase.split()
        line = 0
        col = 0
        numChars = 0
        index = 0
        offsetX = 0 #0 for first word, 1 otherwise
        offsetY = 0 #1 for first word, 0 otherwise
        charlist = []
        
        for iword, word in enumerate(words):
            if numChars+len(word)+offsetX <= self.charPerLine:
                numChars += len(word)+offsetX
            else:
                numChars = len(word)
                line += 1
                offsetY = 1
                col = 0
                if line >= self.lines:
                    line = 0
                    self.phrase.phraseArray.append(charlist)
                    charlist = []

            for i in range(index+offsetY, len(word)+index+offsetX):
                self.phrase.phraseList[i].setPosition(self.position, col, line)
                charlist.append(self.phrase.phraseList[i])
                col += 1
            
            offsetX = 1
            offsetY = 0
            index = i+1
        self.phrase.phraseArray.append(charlist)
        self.phrase.phraseList = self.phrase.phraseArray[self.iphrase]

    def nextPhrase(self, supress=True):
        '''print out more phrases if queued up'''
        if supress:
            supress = not self.phrase.finishedReadout()
            
        if self.iphrase+1 < len(self.phrase.phraseArray):
            if not supress:
                self.textSurface.fill((200,0,20))
                self.iphrase += 1   
                self.phrase.phraseList = self.phrase.phraseArray[self.iphrase]
                self.phrase.continueReadout()
        else:
            if self.phrase.finishedReadout():
                self.reset()
            
    def readoutCharacters(self, phrase, speed, scale):
        '''Need to just call this once for each phraseset'''
        if not self.phrase and phrase:
            self.setPhrase(phrase, scale)
            
        if self.phrase:
            if self.active:
                self.nextPhrase()
            else:
                self.active = True
                self.phrase.readoutCharacters(speed)

    def increaseSpeed(self):
        if self.phrase:
            self.phrase.increaseSpeed()

    def resetSpeed(self):
        if self.phrase:
            self.phrase.resetSpeed()

    
    def render(self, screen):
        if self.active and self.phrase:
            screen.blit(self.textSurface, self.position.toTuple())
            self.phrase.render(self.textSurface)
