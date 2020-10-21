const int irPin = 6;
const int statusPin = 5;

int falseTime = 0;
int trueTime = 0;
int debounceTime = 50;
bool isTrue = true;
int buttonState = 1;

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
    buttonState = digitalRead(irPin);
    if (buttonState == HIGH) {
        // NO incoming signal (sensor outputs high)
        if (!isTrue) {
            trueTime++;
            if (trueTime > debounceTime) {
                isTrue = true;
                digitalWrite(statusPin, HIGH);
            }
        } else {
            falseTime = 0;  
        }
    } else {
        // Incoming signal (low pulses)
        isTrue = false;
        digitalWrite(statusPin, LOW);
        trueTime = 0;
    }
    delay(10);
    Serial.println(!isTrue);
}
