# Walltag prototype game
#
# Gemaakt door Team UnderGod, een team bestaande uit:
#   Aghead Bilal, Damian Bitel, Evelien Dekkers, Hamza Ben Ali en Tim van Echtelt.
#
# Aghead en Damian hebben een begin gemaakt met deze code, wat is uitgewerkt en omgezet naar een class door Evelien.


import serial
import sys
import time
import timeit
import threading
import random
import mysql.connector

database = mysql.connector.connect(
    host="oege.ie.hva.nl",
    user="biteld",
    password="ZcPnyn7ZhG$z0V",
    database="zbiteld",
)


class Game(object):
    """
    De Game-class draait in principe op threads, omdat het enige tijd kost
    om gegevens van de Arduino's (gun en targets) te verkrijgen.
    (En zo worden eventuele vertragingen geen probleem voor de andere taken...)

    --- Threads --
    De class draait op dit moment 4 threads:

    updateTargetStatusThread:
        Bepalen of het doelwit geraakt is of niet

    updateGunDistanceThread:
        Gemeten afstand van gun uitlezen

    updatesThread:
        Tot nu toe houdt deze alleen de tijd bij

    gameThread:
        Hier draait de daadwerkelijke code van het spel


    Hieronder staan constanten en variabelen, die kunnen naar wens aangepast worden.

    """

    # Constants
    DEBUG = False
    GUN_DISTANCE_SAMPLES = 3
    TARGET_HIT_TIMEOUT = 2  # Seconden om te wachten op een schot
    COUNTDOWN_TIME = 3  # Seconden om af te tellen

    # Variables
    playerPoints = 0
    playerLives = 3
    updateRate = 10  # Keren per seconde

    # Initializers
    playerName = ''
    isRunning = True
    elapsedTime = 0
    gunDistance = 0
    targetStatus = False
    lastLine = ''

    def __init__(self, testMode = False):
        """
        De class begint altijd met het controleren van de verbindingen, zijn die er niet dan stopt de applicatie.
        """
        self.testMode = testMode

        if not self.testMode:
            try:
                self.serTarget = serial.Serial('/dev/serial/by-id/usb-1a86_USB2.0-Serial-if00-port0', 9600, timeout=1)
                self.serTargetStatus = "De targets zijn aangesloten!"
            except:
                self.serTargetStatus = "De targets zijn niet aangesloten!"
                sys.exit()

            try:
                self.serGun = serial.Serial('/dev/serial/by-id/usb-Arduino_LLC_Arduino_Leonardo-if00', 9600, timeout=1)
                self.serGunStatus = "De gun is  aangesloten!"
            except:
                self.serGunStatus = "De gun is niet aangesloten!"
                sys.exit()
        else:
            self.serTarget = TestObject('target')
            self.serGun = TestObject('gun')

        if self.DEBUG: self.lastLine = "DEBUG: Game ready"

    def readLine(self, serialObject):
        while True:
            try:
                line = serialObject.readline()
                decoded = line.decode('utf-8')
                decoded = decoded.strip()
                decoded = decoded.replace('\n', '')
                if decoded == '':
                    continue
                return decoded

            except UnicodeDecodeError:  # Decoding foutjes negeren
                continue
            except serial.SerialException:
                self.lastLine = 'Verbinding met gun of targets verloren!'
                self.isRunning = False
                self.quit()

    def updateTargetStatus(self):
        while self.isRunning:
            line = self.readLine(self.serTarget)
            currentState = (int(line) == 1)
            self.targetStatus = currentState

    def updateGunDistance(self):
        # De afstand wordt meerdere malen ingelezen en daarvan wordt het gemiddelde genomen.
        # Nog beter zouden de uitschieters hieruit gehaald worden.
        while self.isRunning:
            distanceSum = 0
            i = 0
            while i < self.GUN_DISTANCE_SAMPLES:
                distanceSum += int(self.readLine(self.serGun))
                i += 1
            distance = distanceSum / self.GUN_DISTANCE_SAMPLES
            self.gunDistance = round(distance)

    def updates(self):
        while self.isRunning:
            # Targets en gun zijn aparte threads omdat die tijd kosten

            # Tijd bijhouden
            self.currentTime = time.time()
            self.elapsedTime = self.currentTime - self.startTime

    def initThreads(self):
        # Alle threads worden hierin gestart, dit wordt aangeroepen vanuit start()
        self.updateGunDistaceThread = threading.Thread(target=self.updateGunDistance)
        self.updateGunDistaceThread.start()

        self.updateTargetStatusThread = threading.Thread(target=self.updateTargetStatus)
        self.updateTargetStatusThread.start()

        self.updatesThread = threading.Thread(target=self.updates)
        self.updatesThread.start()

        self.gameThread = threading.Thread(target=self.gameLoop)
        self.gameThread.start()

    # start() wordt aangeroepen om het gehele spel te starten.
    # Hierin worden ook de threads gestart, waaronder de game loop
    def start(self):
        # Om naam vragen en instructies geven aan begin van het hele spel
        time.sleep(1)
        self.lastLine = self.playerName + " get ready!"
        time.sleep(2)
        self.lastLine = "Je hebt " + str(self.playerLives) + " levens en " + str(
            self.TARGET_HIT_TIMEOUT) + " seconden om een doelwit te raken."
        time.sleep(3)

        self.startTime = time.time()
        self.initThreads()

    def quit(self):
        self.isRunning = False
        sys.exit()

    def countdown(self, seconds):
        for s in range(seconds):
            self.lastLine = str(seconds - s) + "..."
            time.sleep(1)


    # De daadwerkelijke game code!
    def gameLoop(self):
        roundTime = self.startTime
        endTime = 0
        waitingForHit = False # Initializer

        while self.isRunning:
            time.sleep(1 / self.updateRate)

            if self.DEBUG:
               self.lastLine = "DEBUG: " + str(int(self.elapsedTime)) + "s : " + str(self.gunDistance) + "cm, target hit = " + str(self.targetStatus)

            # En hier moet alle game code

            if (self.isRunning):
                # Sla de tijd op als je game start
                roundTime = time.time()
                if not waitingForHit:  # Game start hier
                    self.countdown(self.COUNTDOWN_TIME)
                    self.lastLine = "Schiet!"
                    startTime = self.currentTime
                    waitingForHit = True
                else:
                    # Dit is allemaal wanneer er gewacht wordt op een schot

                    if self.targetStatus:
                        # Doelwit geraakt
                        self.playerPoints += 1
                        waitingForHit = False
                        self.lastLine = "Goedzo! Je hebt nu " + str(self.playerPoints) + " punt(en)!"
                        time.sleep(2)

                    elif (self.currentTime - startTime) >= self.TARGET_HIT_TIMEOUT:
                        # Timeout (te lang gewacht met schieten)
                        self.playerLives -= 1
                        if self.playerLives == 0:
                            self.lastLine = "Je hebt geen levens meer! Game over!"
                        else:
                            self.lastLine = "Te laat met schieten! Je hebt nu maar " + str(self.playerLives) + " leven(s)."
                        waitingForHit = False
                        time.sleep(2)

                if self.playerLives == 0:
                    # sla de tijd op als je game afgelopen is
                    endTime = time.time()
                    timePlayed = float(endTime - startTime)
                    # hier wordt verbinding gemaakt met de database
                    cursor = database.cursor()
                    # gevegens worden naar de database gestuurd
                    sql = "INSERT INTO `Game` " \
                          "(`nickname`, `score`, `lives`, `date`, `time_played`) " \
                          "VALUES (%s, %s, %s, NOW(),%s);"
                    cursor.execute(sql, (self.playerName, self.playerPoints, self.playerLives, timePlayed))
                    database.commit()
                    self.quit()



class TestObject(object):
    def __init__(self, type):
        self.type = type
        self.i = 0
        self.targetline = '0'

    def readline(self):
        time.sleep(.5)
        line = '0'
        if self.type == 'gun':
            line = str(random.randrange(100, 250)) # afstand van gun
        elif self.type == 'target':
            if self.i % 10 == 0:
                if self.targetline == '0':
                    self.targetline = '1'
                else:
                    self.targetline = '0'
            line = self.targetline
        self.i += 1
        return line.encode()
