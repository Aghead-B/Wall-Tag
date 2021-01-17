#this file requests, keeps track of and organzizes all system information.
from Hardware import Hardware
import threading
import json
import time
import db

#this is the actual game that is played with its rules.
class Game(object):

    hardwareObject = None
    info = None
    gameLives = 0
    gamePoints = 0
    targetHit = False
    waitingForHit = False
    gameFinished = False
    playerName = ""
    startTime = 0
    
    DEFAULT_LIVES = 3
    DEFAULT_POINTS = 0
    HIT_REWARD = 50
    NO_HIT_PENALTY = 70
    MAXIMUM_PLAYTIME = 5
    
    def __init__(self):
        self.hardwareObject = Hardware()
        
        infoCollectorThread = threading.Thread(target=self.infoCollector, args=[])
        infoCollectorThread.start()
        waitForHitThread = threading.Thread(target=self.waitForHit, args=[])
        waitForHitThread.start()

    # requests and expands on the dictionary formed in hardware() from hardware.py.
    def infoCollector(self):
        while True:
            info = self.hardwareObject.getInfo()
            info.update({
                'lives': self.gameLives,
                'points': self.gamePoints,
                'targetHit': self.targetHit,
                'waitingForHit': self.waitingForHit,
                'gameFinished': self.gameFinished,
                'playerName': self.playerName,
                'timePlayed': time.time() - self.startTime
            })
            self.info = info

    # returns the "new and updated" dictionary.
    def getInfo(self):
        return self.info
        
    def enableGun(self):
        self.hardwareObject.setGun(True)
    def disableGun(self):
        self.hardwareObject.setGun(False)
        
    def startHit(self):
        self.waitingForHit = True
        self.gameFinished = False
        
    def reset(self):
        self.gameLives = self.DEFAULT_LIVES
        self.gamePoints = self.DEFAULT_POINTS
        self.startTime = time.time()

    # compares the status of targets as a list and acts accordingly by the result of that list. (2.5 sec)
    def waitForHit(self):
        while True:
            if self.waitingForHit:
                targetIndex = self.hardwareObject.getRandomTargetIndex()
                targets = self.info["targetStatus"].copy()
                targets[targetIndex] = 1
                self.hardwareObject.setTargets(targets)
                beginTargetStatus = self.info["targetStatus"].copy()
                hitStartTime = time.time()
                while self.waitingForHit:
                    currentTargetStatus = self.info["targetStatus"]
                    if beginTargetStatus != currentTargetStatus and currentTargetStatus[targetIndex] == 1:
                        self.targetHit = True
                        self.waitingForHit = False
                        self.reward()
                        break
                    elif time.time() - hitStartTime >= 2.5:
                        self.targetHit = False
                        self.waitingForHit = False
                        self.penalty()
                        break
                        
    def reward(self):
        self.gamePoints += self.HIT_REWARD
        self.checkGameFinished()
        
    def penalty(self):
        if self.gamePoints - self.NO_HIT_PENALTY < 0:
            self.gamePoints = 0
        else:
            self.gamePoints -= self.NO_HIT_PENALTY
        
        self.gameLives -= 1
        self.checkGameFinished()
        self.hardwareObject.buzz(.2)

    #checks if the conditions for the game to finish have been met and stores the results.
    def checkGameFinished(self):
        if self.gameLives == 0:
            self.gameFinished = True
        if self.startTime - time.time() > self.MAXIMUM_PLAYTIME:
            self.gameFinished = True
            
        if self.gameFinished:
            
            timeEnded = time.time()
            time.sleep(1)
            info = self.info.copy()
            info["timePlayed"] = timeEnded - self.startTime
            db.putGameRecord(info)
            self.hardwareObject.buzz(.2)
            time.sleep(.1)
            self.hardwareObject.buzz(.2)
    
    def getHardwareStatus(self):
        return self.hardwareObject.getHardwareStatus()
        
    def setPlayerName(self, name):
        self.playerName = name
        
    def clearTargets(self):
        targets = self.info["targetStatus"]
        for i in range(len(targets)):
            targets[i] = 0
        self.hardwareObject.setTargets(targets)
        self.targetHit = False