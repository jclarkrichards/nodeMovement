"""
grabSingle(clip, scale)
    clip is in (x, y, width, height) format
grabSet(start, scale, rows, cols)
    Assumes all frames are the same width and height and arranged in rows
    start is the starting frame in (x, y, width, height) format
grabAll(w, h, rowNums, scale)
    Assumes all frames are the same width and height and arranged in rows
    rowNums is a list of how many frames to grab in each row
"""
import pygame
 
class SpriteHandler(object):
    def __init__(self, filename):
        self.filename = filename
        self.sheet = None
        self.frame = None
        self.frameset = []
        self.load()
        
    def load(self):
        '''Load a sprite sheet for use'''
        self.sheet = pygame.image.load(self.filename).convert_alpha()
        
    def grabSingle(self, clip, scale=1):
        '''Grab a single frame from the sheet.
        clip=(x,y,width,height) of image to clip'''
        #self.sheet.set_clip(pygame.Rect(clip))
        #return self.sheet.subsurface(self.sheet.get_clip()) #can I scale this?
        frame = pygame.Surface(clip[2:]).convert()
        frame.set_colorkey((255,0,255))
        #print frame.get_colorkey()
        frame.blit(self.sheet, (0,0), clip)
        #if scale != 1:
        #    return pygame.transform.scale(frame, (clip[2]*scale, clip[3]*scale))
        return frame
    
    def grabSet(self, start, scale=1, rows=1, cols=1):
        '''Grab a set of images from FILENAME'''
        x, y, w, h = start
        frameset = []
        for row in range(rows):
            for col in range(cols):
                clip = (x+w*col, y+h*row, w, h)
                frameset.append(self.grabSingle(clip, scale=scale))
        return frameset
        
    def grabAll(self, w, h, rowNums, scale=1):
        '''Grab all of the frames from the spritesheet.'''
        rows = len(rowNums)
        frameset = []
        for row in range(rows):
            for col in range(rowNums[row]):
                clip = (w*col, h*row, w, h)
                frameset.append(self.grabSingle(clip, scale=scale))
        return frameset
