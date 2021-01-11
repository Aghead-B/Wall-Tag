/*

const int irPinnen[] = {6,0,0,0,0,0};

const int statusPinnen[] = {5,0,0,0,0,0};

*/


const int irPinnen[] = {A5, A4, A3, A2, A1, A0};

const int statusPinnen[] = {3, 2, 0, 1, 8, 9};

const int aantalSensoren = 6;
char ledcontrol[aantalSensoren];
int latestChar;
int geraaktePin[aantalSensoren];

void setup() {
    // put your setup code here, to run once:
    for (int i=0; i<aantalSensoren; i++) {
      pinMode(irPinnen[i], INPUT);
      digitalWrite(irPinnen[i], HIGH); // Internal pullup
      pinMode(statusPinnen[i], OUTPUT);
      digitalWrite(statusPinnen[i], HIGH);
    }
    Serial.begin(9600);
  #if defined(__AVR_ATmega32U4__) || defined(SERIAL_USB) || defined(SERIAL_PORT_USBVIRTUAL)
    delay(2000); // To be able to connect Serial monitor after reset and before first printout
  #endif
}

void loop(){
    // Serial loop to store the incoming values in 6 characters of 0 & 1
    if (Serial.available() > 0){
      boolean continueToRead = false;
      for(int i=0; i<aantalSensoren; i){
         latestChar = Serial.read();
         if (!continueToRead && i ==0) {
           if (latestChar != 'w') {serialFlush();break;}
           if (latestChar == 'w') {continueToRead = true;}
         }
         if (continueToRead) {
           if (latestChar == '1' || latestChar == '0'){
             ledcontrol[i] = latestChar;
             i++;
           }
         }
      }
      if (continueToRead) {
       // If else statements that turn on the sensors and the status Led pins based on the input in (ledcontrol)     
        for(int i = 0; i<aantalSensoren; i++){
          int targetActive = ledcontrol[i];
          if (targetActive == '1') {
            digitalWrite(statusPinnen[i], LOW);
          } else{
            digitalWrite(statusPinnen[i], HIGH);
          }  
        }
      }
    }

    Serial.write("r");
    for(int i = 0; i<aantalSensoren; i++) {
      int pinRead = digitalRead(irPinnen[i]);
      // Hier moet de logica omgedraaid worden, omdat de sensor LOW is wanneer die geraakt wordt.
      if (pinRead == 0) {
        geraaktePin[i] = 1;
      } else {
        geraaktePin[i] = 0;
      }
      Serial.print(geraaktePin[i]);
    }
    Serial.write("\n");
          
}

void serialFlush(){
  while(Serial.available() > 0) {
    char t = Serial.read();
  }
}   
