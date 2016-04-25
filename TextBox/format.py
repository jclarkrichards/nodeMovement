"""Left justify text"""

class LeftJust(object):
    def __init__(self, phrase=''):
        self.phrase = phrase
        self.words = phrase.split()
        self.line = 0
        self.col = 0
        self.numChars = 0
        self.index = 0
        self.offsetX = 0 #0 for 1st word in phrase, 1 otherwise
        self.offsetY = 0 #1 for 1st word in line, 0 otherwise
        self.charlist = []
    
    def setFormat(self):
        for iword, word in enumerate(self.words):
            pass
    '''
    
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
    '''
