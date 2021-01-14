import threading
import time

import serial
import json
import sys
import random
import math
import os
import RPi.GPIO as gpio


class TargetDebounce(object):
    latest = []
    currentStatus = []
    differenceCounter = []

    def __init__(self, number):
        self.NUMBER_TARGETS = number
        for i in range(self.NUMBER_TARGETS):
            self.latest.append(0)
            self.currentStatus.append(0)
            self.differenceCounter.append(0)

    def update(self, list):
        self.setLatest(list)
        self.processLatest()
        self.updateStatus()

    def setLatest(self, list):
        for i in range(self.NUMBER_TARGETS):
            self.latest[i] = int(list[i])

    def processLatest(self):
        for i in range(self.NUMBER_TARGETS):
            latest = self.latest[i]
            current = self.currentStatus[i]
            if current != latest:
                self.differenceCounter[i] += 1

    def updateStatus(self):
        for i in range(self.NUMBER_TARGETS):
            difference = self.differenceCounter[i]
            current = self.currentStatus[i]
            if current == 0:
                if difference > 1:
                    self.resetCounter(i)
                    self.currentStatus[i] = 1
            elif current == 1:
                if difference > 10:
                    self.resetCounter(i)
                    self.currentStatus[i] = 0

    def resetCounter(self, i):
        self.differenceCounter[i] = 0

    def getStatus(self):
        return self.currentStatus


class Hardware(object):
    GUN_DISTANCE_SAMPLES = 3
    NUMBER_TARGETS = 6
    HALLEFFECT_PIN = 14
    BUZZER_PIN = 15

    error = False
    targetStatus = []
    gunDistance = 0
    isRunning = True
    hallEffectStatus = False

    serTarget = None
    serGun = None

    def __init__(self):
        gpio.setmode(gpio.BCM)
        gpio.setwarnings(False)
        
        for i in range(self.NUMBER_TARGETS):
            self.targetStatus.append(0)
        self._connectSerial()

        self.errorHandlingThread = threading.Thread(target=self.errorHandling)
        self.errorHandlingThread.start()

        self.readHallEffectThread = threading.Thread(target=self.readHallEffect)
        self.readHallEffectThread.start()

        if not self.error:
            self.readGunThread = threading.Thread(target=self.readGun)
            self.readGunThread.start()

            self.readTargetsThread = threading.Thread(target=self.readTargets)
            self.readTargetsThread.start()

    def readLine(self, serialObject, targets=False):
        if self.isRunning and not self.error:
            while True:
                try:
                    if targets:
                        line = serialObject.readline()
                        decoded = line.decode('ascii')
                        return decoded
                    else:
                        line = serialObject.readline()
                        decoded = line.decode('ascii')
                        decoded = decoded.strip()
                        decoded = decoded.replace('\n', '')
                        if decoded == '':
                            continue
                        return decoded

                except UnicodeDecodeError:  # Decoding foutjes negeren
                    continue
                except serial.SerialException:
                    self.error = True
                    return '0'
        else:
            return '0'

    def writeLine(self, serialObject, string):
        try:
            serialObject.write(string.encode())
        except serial.SerialException:
            self.error = True

    def _connectSerial(self):
        print("Hardware: trying to connect hardware")
        while True:
            try:
                serialDevices = os.listdir('/dev/serial/by-path/')
                if len(serialDevices) > 2:
                    self.error = True
                    print("Hardware: Can't determine targets or gun! Too many serial devices!")
                else:
                    for device in serialDevices:
                        try:
                            tempserial = serial.Serial('/dev/serial/by-path/' + device,
                                                           9600, timeout=1, xonxoff=False, rtscts=False, dsrdtr=False)
                            time.sleep(.5)
                            line = tempserial.readline()
                            line = line.decode('ascii')
                            if 'r' in line:
                                self.serTarget = tempserial
                                print("Hardware: connected targets")
                                if len(serialDevices) < 2:
                                    self.serGun = None
                            else:
                                self.serGun = tempserial
                                print("Hardware: connected gun")
                                if len(serialDevices) < 2:
                                    self.serTarget = None
                        except:
                            print("Hardware: could not connect to '/dev/serial/by-path/" + device)
                            self.error = True
                time.sleep(.5)
                if self.serTarget and self.serGun:
                    self.error = False
                    break
                else:
                    self.error = True
                    break

            except FileNotFoundError:
                self.serGun = None
                self.serTarget = None
                self.error = True
                break
       

    def errorHandling(self):
        while self.isRunning:
            time.sleep(.1)
            if self.error:
                print("Hardware: oh no an error!")
                self._connectSerial()

    def readTargets(self):
        """ Expects a message like 'r010000' over serial """
        debouncer = TargetDebounce(number=self.NUMBER_TARGETS)
        while self.isRunning:
            if not self.error:
                lines = []
                for i in range(5):
                    lines.append(self.readLine(self.serTarget, targets=True))
                for line in lines:
                    line = line.strip()
                    if len(line) == 7 and line[0] == 'r':
                        line = line[1:7]
                        list = [] 
                        list[:0] = line
                        debouncer.update(list)
                        self.targetStatus = debouncer.getStatus()

    def setTargets(self, list):
        if not self.error:
            string = 'w'
            for char in list:
                string += str(char)
            self.writeLine(self.serTarget, string + "\n")

    def readGun(self):
        while self.isRunning:
            if not self.error:
                distanceSum = 0
                i = 0
                while i < self.GUN_DISTANCE_SAMPLES:
                    distanceSum += int(self.readLine(self.serGun))
                    i += 1
                distance = distanceSum / self.GUN_DISTANCE_SAMPLES
                self.gunDistance = round(distance)

    def setGun(self, boolean):
        if not self.error:
            if boolean == True:
                self.writeLine(self.serGun, 'on')
            else:
                self.writeLine(self.serGun, 'off')

    def readHallEffect(self):
        gpio.setup(self.HALLEFFECT_PIN, gpio.IN)
        while True:
            if(gpio.input(self.HALLEFFECT_PIN) == False):
                self.hallEffectStatus = True
            else:
                self.hallEffectStatus = False
    
    def buzz(self, seconds):
        gpio.setup(self.BUZZER_PIN, gpio.OUT)
        gpio.output(self.BUZZER_PIN, False)
        gpio.output(self.BUZZER_PIN, True)
        time.sleep(seconds)
        gpio.output(self.BUZZER_PIN, False)
        
    def getRandomTargetIndex(self):
        return math.floor(random.random()*self.NUMBER_TARGETS)
        
    def getInfo(self):
        if len(self.targetStatus) != self.NUMBER_TARGETS:
            self.error = True
        return {'error': self.error, 'gunDistance': self.gunDistance, 'targetStatus': self.targetStatus, 'halleffect': self.hallEffectStatus}
        
    def getHardwareStatus(self):
        status = {'target': True, 'gun': True, 'halleffect': self.hallEffectStatus}
        if self.serTarget == None:
            status["target"] = False
        if self.serGun == None:
            status["gun"] = False
        return status


if __name__ == "__main__":
    hardwareObject = Hardware()
    hardwareObject.setGun(True)
    while True:
        try:
            print("Hardware: " + str(hardwareObject.getInfo()))
            time.sleep(.1)
        except:
            hardwareObject.isRunning = False
            break
