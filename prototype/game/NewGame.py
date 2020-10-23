#######################
## Serial connection ##
#######################

# We maken gebruik van PySerial voor het uitlezen van de serial console van het target
import serial
import sys
import time

serTarget = serial.Serial('/dev/serial/by-id/usb-1a86_USB2.0-Serial-if00-port0', 9600, timeout=1)
serGun = serial.Serial('/dev/serial/by-id/usb-Arduino_LLC_Arduino_Leonardo-if00', 9600, timeout=1)

if not serTarget:
    print("De targets zijn niet aangesloten!")
    sys.exit()
if not serGun:
    print( "De gun is niet aangesloten!" )
    sys.exit()


##########################
## Function definitions ##
##########################
def getTargetStatus():
    try:
        line = serTarget.readline();
        decoded = line.decode('utf-8')
        currentState = (decoded.strip() == '1')
        return currentState
    except:
        print("Something went wrong")
        sys.exit()
        # De ontvanger is niet meer te bereiken! Graag nog goede afhandeling dmv foutmelding weergeven ofzo

def getGunDistance():
    try:
        line = serGun.readline();
        decoded = line.decode('utf-8')
        distance = decoded.strip()
        return distance
    except:
        print("Something went wrong")
        sys.exit()
        # De ontvanger is niet meer te bereiken! Graag nog goede afhandeling dmv foutmelding weergeven ofzo

def livesModule():
    while lives != 0:
        timeElapsed = 0
        interval = 100
        if timeElapsed >= 2000:
            lives - 1
            timeElapsed = 0
        timeElapsed += interval
        time.sleep( interval / 1000 )
# De lifeModule chekt om de 2 seconden of er raak is geschoten en als dat niet zo is gaar er 1 leven er af

def playerModule():
    speler = input( "Voer hier uw nickname in: " )
    print( speler + " Get Ready !" )


###############
## Main loop ##
###############


gameRunning = True
points = 0
lifes = 3
while gameRunning:
    try:
        player = playerModule()
        targetIsHit = getTargetStatus()
        targetDistance = getGunDistance()
        lives = livesModule()
        if targetDistance >100:
            targetIsHit = False
            print("Je staat te dicht bij!!")
        if targetIsHit:
            points + 1
            print("Raak !!!")
            print(targetDistance)
        if lives == 0:
            print(player + "Game Over your points:")
            print( points )
            break;

    except KeyboardInterrupt:
        print("Bye")
        sys.exit()







