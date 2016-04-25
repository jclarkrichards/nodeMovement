"""Any class that uses text needs to inherit from this class"""
import pygame
from image_set import SpriteHandler
from vectors import Vector2D
import numpy as np
import os

class Text(object):
    def __init__(self, sheet, txtfile, charsize):
        base = 'TextBox/'
        self.sheet = base+sheet
        self.txtfile = base+txtfile
        self.charsize = charsize
        self.imageChars = []
        self.textChars = []
        self.textDict = {}
        self.loadSheet()
    
    def getRowNums(self):
        rowNums = []
        self.textChars = []
        print os.getcwd()
        with open(self.txtfile) as f:
            for line in f:
                thisline = list(np.array(line.split(), dtype=str))
                self.textChars += thisline
                rowNums.append(len(thisline))
        return rowNums
        
    def loadSheet(self):
        '''Load the character sheet'''
        rowNums = self.getRowNums()
        sheet = SpriteHandler(self.sheet)
        w, h = self.charsize
        self.imageChars = sheet.grabAll(w, h, rowNums)
        self.mapCharacters()
        
    def mapCharacters(self):
        '''Map the image characters to the text characters'''
        self.textDict = {}
        if len(self.textChars) != len(self.imageChars):
            return "textChars and imageChars do not match!"
        for i, char in enumerate(self.textChars):
            self.textDict[char] = self.imageChars[i]
        self.addSpaceCharacter()
        
    def addSpaceCharacter(self):
        '''Add a space character to the dictionary'''
        frame = pygame.Surface(self.charsize).convert()
        frame.fill((255,0,255))
        frame.set_colorkey((255,0,255))
        self.textDict[' '] = frame #pygame.Surface(self.charsize).convert()
        
   



