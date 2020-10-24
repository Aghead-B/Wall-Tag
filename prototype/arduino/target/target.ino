const int irPin = 6;
const int statusPin = 5;
const int minimumPulsesRequired = 2;

int falseTime = 0;
int trueTime = 0;
int debounceTime = 50;
bool notHit = true;
int sensorState = 1;
int pulses = 0;

void setup() {
    // put your setup code here, to run once:
    pinMode(irPin, INPUT);
    pinMode(statusPin, OUTPUT);
    digitalWrite(statusPin, HIGH);
    Serial.begin(9600);
  #if defined(__AVR_ATmega32U4__) || defined(SERIAL_USB) || defined(SERIAL_PORT_USBVIRTUAL)
    delay(2000); // To be able to connect Serial monitor after reset and before first printout
  #endif
}

void loop() {
    // put your main code here, to run repeatedly:
    sensorState = digitalRead(irPin);
    if (sensorState == HIGH) {
        // NO incoming signal (sensor outputs high)
        if (!notHit) {
            trueTime++;
            delay(5);
            if (trueTime > debounceTime) {
                notHit = true;
                //Serial.println(!sensorState);
            }
        } else {
            falseTime = 0;  
        }
    } else {
        // Incoming signal (low pulses)
        if (notHit == false || pulses >= minimumPulsesRequired && notHit == true) {
            notHit = false;
            trueTime = 0;
            pulses = 0;
        }
        pulses++;
    }
    if (notHit) {
        digitalWrite(statusPin, HIGH);
    } else {
        digitalWrite(statusPin, LOW);
    }
    
    Serial.println(!notHit);
    delay(10);
}
