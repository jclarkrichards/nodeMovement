"""Pass in a string of text and match the characters to the necessary images"""
from base import TextBase
from vectors import Vector2D
import pygame

class JDialog(TextBase):
    def __init__(self, position=(200,400), area=(350,30), phrase=''):
        TextBase.__init__(self, position, area, phrase=phrase)
        '''UPPERFRAMES and LOWERFRAMES are always from A to Z
        NUMBERFRAMES always go from 0 to 9'''
        self.readout_speed = 0.1
        self.total_time = 0
        self.displayed = False
        self.dispnum = 0
        self.dt = 0
        self.cursor = False

    def useCursor(self):
        self.cursor = True
        self.cursor_w, self.cursor_h = self.charsize
        self.cursor_w -= 2
        
    def readout(self, screen, time_passed):
        '''Read out the text to the screen at a given speed'''
        numchar = len(self.charlist)
        if self.dispnum == numchar:
            self.displayed = True
        self.dt += time_passed
        if time_passed > self.readout_speed:
            try:
                num = int(time_passed / self.readout_speed)
            except ZeroDivisionError:
                self.dispnum = numchar
            else:
                self.dispnum += num
                if self.dispnum > numchar:
                    self.dispnum = numchar
        elif self.dt >= self.readout_speed and not self.displayed:
            self.dispnum += 1
            self.dt = 0
        for i in range(self.dispnum):
            self.charlist[i].__render__(screen)

        if self.cursor:
            offset = 0
            if self.dispnum == numchar:
                self.dispnum -= 1
                offset = self.charsize[0]
            x, y = self.charlist[self.dispnum].position.toTuple()
            x += offset
            pygame.draw.rect(screen, (0,0,0), [x,y,self.cursor_w, 
                                               self.cursor_h])

class JLabel(TextBase):
    '''A simple text label to display a word or two of text'''
    def __init__(self, position=(0,0), area=(0,0), phrase=''):
        TextBase.__init__(self, position, area, phrase=phrase)
        
    def readout(self, screen, time_passed=0):
        numchar = len(self.charlist)
        for i in range(numchar):
            self.charlist[i].__render__(screen)


class JScroll(TextBase):
    '''Scrolls a phrase from right to left within a given area.'''
    def __init__(self, position=(0,0), area=(0,0), phrase=''):
        TextBase.__init__(self, position, area, phrase=phrase)
        self.repeat = False
        self.speed = 100
        self.textoffset = self.area.x

    def parsePhrase(self):
        '''The phrase is just one long string'''
        self.phraselist = [self.phrase]

    def updatePosition(self, time_passed):
        '''Change position so it moves from right to left'''
        for i, letter in enumerate(self.charlist):
            letter.position.x -= self.speed * time_passed
            if self.repeat:
                if self.charlist[-1].position.x <= self.position.x:
                    self.parsePhrase()
                    self.interpret()

    def setRepeat(self, repeat):
        '''Set to either True or False'''
        self.repeat = repeat

    def readout(self, screen, time_passed):
        '''Scrolls across the screen.'''
        numchar = len(self.charlist)
        self.updatePosition(time_passed)
        for letter in self.charlist:
            if (self.position.x <= letter.position.x <=
                self.position.x+self.area.x):
                letter.__render__(screen)


    
