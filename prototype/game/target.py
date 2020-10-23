# Code om uit te lezen uit het target of die wel of niet geraakt is
# Hij is nog zeer basic, want we hebben op dit moment maar 1 target
# 
# Geschreven door Evelien


# We maken gebruik van PySerial voor het uitlezen van de serial console van het target
import serial
ser = serial.Serial('/dev/serial/by-id/usb-1a86_USB2.0-Serial-if00-port0', 9600, timeout=1)
# De serial port is te vinden door 'ls /dev/serial/by-id/' uit te voeren, dan zie je welke serial devices er aangesloten zijn.
# Gebruik by-id omdat die niet verandert.
lastState = False
while ser:
    try:
        line = ser.readline();
        decoded = line.decode('utf-8')
        currentState = (decoded.strip() == '1')
        if lastState != currentState and currentState:
            if currentState == True:
                print("geraakt!")
                # Hier is het target geraakt
            else:
                # Hier is het target niet meer geraakt
                print(":(")
            lastState = currentState
    except:
        print("Something went wrong")
        # De ontvanger is niet meer te bereiken! Graag nog goede afhandeling dmv foutmelding weergeven ofzo
        break;