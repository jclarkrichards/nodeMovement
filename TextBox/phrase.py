import pygame
from base import Text
from vectors import Vector2D
from entity import Character
from phraseFX import *
import numpy as np

class PhraseHandler(object):
    def __init__(self, phrase):
        self.phrase = phrase
        self.phraseList = []
        self.phraseArray = []
        self.readOut = None
        
    def update(self, dt):
        if self.readOut:
            self.readOut.update(dt, self.phraseList)
        
    def updatePhrase(self, phrase):
        '''Set a new phrase to use'''
        pass

    def mapPhrase(self, lookup):
        '''Get all of the character images to construct the phrase'''
        for letter in self.phrase:
            try:
                self.phraseList.append(Character(lookup[letter]))
            except KeyError:
                pass
            
    def setPosition(self, position):
        '''Set the position relative to the first letter on one line'''
        for i, letter in enumerate(self.phraseList):
            letter.setPosition(position, i, 0)
            #letter.setPosition((position[0]+letter.size[0]*i, position[1]))
            
    def setScale(self, scale):
        '''Make the letters bigger or smaller'''
        for letter in self.phraseList:
            newSize = (letter.size[0]*scale, letter.size[1]*scale)
            letter.image = pygame.transform.scale(letter.image, newSize)
            letter.setSize()

    def readoutCharacters(self, speed):
        '''Reads out the characters one at a time'''
        self.readOut = ReadOut(speed)
        for letter in self.phraseList:
            letter.alive = False

    def continueReadout(self):
        if self.readOut:
            speed = self.readOut.speed
            self.readoutCharacters(speed)

    def finishedReadout(self):
        if self.phraseList[-1].alive:
            return True
        return False

    def increaseSpeed(self):
        if self.readOut:
            self.readOut.increaseSpeed()

    def resetSpeed(self):
        if self.readOut:
            self.readOut.resetSpeed()
            
    def render(self, screen):
        '''Print the phrase onto the screen'''
        for letter in self.phraseList:
            letter.render(screen)
            
            
    """        
     #All of the methods below may be in the Phrase class        
    def useUpperCase(self):
        '''Use only uppercase letters'''
        self.phrase = self.phrase.upper()

    def setPhrase(self, phrase):
        '''Set the phrase to print to screen'''
        self.phrase = phrase

    def updatePhrase(self, newphrase):
        '''Update the phrase with a new phrase'''
        self.phrase = str(newphrase)
        self.parsePhrase()
        self.interpret()

    def interpret(self):
        '''Interpret a string into their corresponding character images.
        Determine the x,y position of each character.'''
        self.charlist = []
        maxrows = int(self.area.y / (self.charsize[1]+self.linespace))
        if maxrows < 1:
            maxrows = 1
        w, h = self.charsize
        row = 0
        while row < maxrows:
            try:
                thisphrase = self.phraselist[0]
            except IndexError:
                row = maxrows
            else:
                for j in range(len(thisphrase)):
                    pos = (j*w+self.position.x+self.textoffset,
                           row*(self.linespace+h)+self.position.y)
                    try:
                        image = self.textdict[thisphrase[j]]
                    except:
                        self.spaces.append((pos[0]-self.position.x) / w)
                    else:
                        self.charlist.append(AbstractEntity((w,h),image=image,
                                                            startpos=pos))
                self.phraselist.remove(thisphrase)
            row += 1

    def parsePhrase(self):
        '''Split the phrase into multiple lines if it exceeds MAXWIDTH.'''
        dx,dy = self.charsize
        width, height = self.area.toTuple()
        wordlist = self.phrase.split(' ')
        while len(wordlist) > 0:
            n = 0
            templist = []
            nextline = False
            while not nextline and len(wordlist) > 0:
                word = wordlist[0]
                n += len(word)*dx
                if n > width:
                    nextline = True
                else:
                    templist.append(word)
                    wordlist.remove(word)
                    n += self.wordspace
            self.phraselist.append(" ".join(templist))

    def fromTextFile(self, filename, thisline):
        '''Get a phrase from a text file.  Assume that each phrase
        is on a different line in the file'''
        indx = 0
        with open(filename, "r") as f:
            for line in f:
                if indx == thisline:
                    self.phrase = line
                    self.phrase.strip('\n')
                    break
                indx += 1
    """
