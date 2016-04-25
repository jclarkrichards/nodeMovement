import numpy as np

class ReadOut(object):
    def __init__(self, speed):
        self.timer = 0
        self.counter = 0
        self.speed = speed
        self.prevSpeed = speed
        self.phraseIndex = 0
        self.numCharacters = 1 #num characters to print at once
        self.setSpeed(speed)

    def update(self, dt, phrase):
        if self.phraseIndex < len(phrase):
            self.counter += dt
            if self.counter >= self.timer:
                for i in range(self.numCharacters):
                    phrase[self.phraseIndex].alive = True
                    self.phraseIndex += 1
                    if self.phraseIndex >= len(phrase):
                        break
                self.counter = 0

    def setSpeed(self, speed):
        '''How fast to read out the characters'''
        self.speed = speed
        if speed > 0:
            self.timer = 1.0/speed
        self.numCharacters = int(np.ceil(.03*speed))
        #.03 is 1/framesPerSec

    def increaseSpeed(self):
        '''Increase speed by 50%'''
        if self.speed == self.prevSpeed:
            self.setSpeed(self.prevSpeed*3.5)

    def resetSpeed(self):
        if self.speed != self.prevSpeed:
            self.setSpeed(self.prevSpeed)
