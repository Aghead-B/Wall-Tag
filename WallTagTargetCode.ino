/*

const int irPinnen[] = {6,0,0,0,0,0};

const int statusPinnen[] = {5,0,0,0,0,0};

*/


const int irPinnen[] = {41,40,39,38,37,36};

const int statusPinnen[] = {18,19,20,21,28,29};

const int aantalSensoren = 6;
char ledcontrol[aantalSensoren];
int latestChar;
int geraaktePin[aantalSensoren];

void setup() {
    // put your setup code here, to run once:
    for (int i=0; i<aantalSensoren; i++) {
      pinMode(irPinnen[i], INPUT);
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
      geraaktePin[i] = digitalRead(irPinnen[i]);
      Serial.print(geraaktePin[i]);
    }
    Serial.write("\n");
          
}

void serialFlush(){
  while(Serial.available() > 0) {
    char t = Serial.read();
  }
}   
