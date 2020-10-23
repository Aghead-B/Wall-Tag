# Code om de afstand uit de arduino van de gun uit te lezen
# Afstand is in cm (centimeters)
# 
# Geschreven door Evelien


# We maken gebruik van PySerial voor het uitlezen van de serial console van het target
import serial
ser = serial.Serial('/dev/serial/by-id/usb-Arduino_LLC_Arduino_Leonardo-if00', 9600, timeout=1)
# De serial port is te vinden door 'ls /dev/serial/by-id/' uit te voeren, dan zie je welke serial devices er aangesloten zijn.
# Gebruik by-id omdat die niet verandert.

averageAmount = 5 # Aantal getallen om te gebruiken voor de uiteindelijke afstand
errorDistance = 1000 # Afstand waarbij we zeker weten dat de sensor bedekt is of niet goed werkt

def getAverageNumber(numbers):
    total = int(0)
    for x in numbers:
        total = int(total + int(x))
    return int(total / len(numbers))
    
i = 0
numbers = []
while ser:
    try:
        line = ser.readline();
        decoded = line.decode('utf-8')
        distance = decoded.strip()
        if distance: # Wanneer er iets te lezen is
            numbers.append(distance)
            i += 1
            if i % averageAmount == 0:
                average = getAverageNumber(numbers)
                if average > errorDistance:
                    print("Something went wrong (sensor covered or non functioning?)")
                else:
                    print(average)
                numbers = []
    except:
        print("Something went wrong")
        # De gun is niet meer te bereiken! Graag nog goede afhandeling dmv foutmelding weergeven ofzo
        break;