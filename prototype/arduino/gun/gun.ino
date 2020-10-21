/*
 * IRremote: IRsendNecStandardDemo
 *
 *  Demonstrates sending NEC IR codes in standard format with 16 bit Address  8bit Data
 *
 *  Created on: 15.09.2020
 *  Copyright (C) 2020  Armin Joachimsmeyer
 *  armin.joachimsmeyer@gmail.com
 *
 *  This file is part of Arduino-RobotCar https://github.com/z3t0/Arduino-IRremote.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program.  If not, see <http://www.gnu.org/licenses/gpl.html>.
 */
// Deze sketch is gebaseerd op de democode van IRRemote, om een juist commando te versturen via IR.
// Hierin is het lezen van de afstand en het aanzetten van de laser diode geintegreerd.

#include <IRremote.h>
IRsend IrSender;

const int buttonPin = 6;     // the number of the pushbutton pin
// IR led is on D5
const int laserPin = 8;
int buttonState = 0;         // variable for reading the pushbutton status

// Deze zijn voor de afstandssensor
const int trigPin = 9;
const int echoPin = 10;

long duration;
int distance;

void setup() {
    pinMode(buttonPin, INPUT);
    pinMode(laserPin, OUTPUT);
    pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
    pinMode(echoPin, INPUT); // Sets the echoPin as an Input
    pinMode(LED_BUILTIN, OUTPUT);
    Serial.begin(9600);
}

uint16_t sAddress = 0xa90;
uint8_t sCommand = 0x34;
uint8_t sRepeats = 0;

void loop() {
    printDistance();
    buttonState = digitalRead(buttonPin);
    if (buttonState == HIGH) {
        digitalWrite(laserPin, HIGH);
        shootIR();
    } else {
        delay(50);
        digitalWrite(laserPin, LOW);
    }
}

void shootIR() {
    IrSender.sendNECStandard(sAddress, sCommand, sRepeats);
}

void printDistance() {
    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);
    // Sets the trigPin on HIGH state for 10 micro seconds
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);
    // Reads the echoPin, returns the sound wave travel time in microseconds
    duration = pulseIn(echoPin, HIGH);
    // Calculating the distance
    distance= duration*0.034/2;
    // Prints the distance on the Serial Monitor
    Serial.println(distance);
}
