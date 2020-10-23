#######################
## Serial connection ##
#######################

# We maken gebruik van PySerial voor het uitlezen van de serial console van het target
import serial
import sys

serTarget = serial.Serial('/dev/serial/by-id/usb-1a86_USB2.0-Serial-if00-port0', 9600, timeout=1)
serGun = serial.Serial('/dev/serial/by-id/usb-Arduino_LLC_Arduino_Leonardo-if00', 9600, timeout=1)

if not serTarget or not serGun:
    print("De gun/targets zijn niet aangesloten!")
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

###############
## Main loop ##
###############

gameRunning = True

while gameRunning:
    try:
        targetIsHit = getTargetStatus()
        targetDistance = getGunDistance()
        if targetIsHit:
            print(targetIsHit)
            print(targetDistance)
    except KeyboardInterrupt:
        print("Bye")
        sys.exit()
