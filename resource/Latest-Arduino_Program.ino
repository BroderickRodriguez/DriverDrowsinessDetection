#include <SoftwareSerial.h>
#define BUZZER 9
#define M1 3 //Pin for motor 1
#define M2 5 //Pin for motor 2

//Delay used for each alarm
#define sdDelay 250 
#define nfDelay 270
#define dDelay 270

//Speed used for each alarm
#define sdSpeed 190
#define dSpeed 255
#define nfSpeed 127

//Tone used for each alarm
#define sdTone 0
#define dTone 500
#define nfTone 0


SoftwareSerial BT(0, 1); //Library for accessing bluetooth pins

void noAlarm(); // No Alarm
void sdAlarm(); // Slightly Drowsy
void dAlarm(); // Drowsy 
void nfAlarm(); // No Face detected

char state = '0';

void setup() 
{
  BT.begin(9600);
  
  pinMode(BUZZER, OUTPUT);
  pinMode(M1, OUTPUT);
  pinMode(M2, OUTPUT);
    
}


void loop() // run over and over
{

  if(BT.available()){
    state = BT.read();

    //For log purposes
    BT.write(state);
    
    if(state == '1'){
      sdAlarm();
    } else if (state == '2'){
      dAlarm();
    } else if (state == '3'){
      nfAlarm(); 
    }
    else {
      noAlarm();
    }
  }
  else {
    noAlarm();
  }

}

void noAlarm(){
  noTone(BUZZER);
  analogWrite(3, 0);
  analogWrite(5, 0);
}
void sdAlarm(){
  BT.write("\nStop Listening\n");
  BT.end();
  
  noTone(BUZZER);
  for(int i=0; i<3; i++){
    analogWrite(M1, sdSpeed);
    analogWrite(M2, sdSpeed);
    delay(sdDelay);
    analogWrite(M1, 0);
    analogWrite(M2, 0);
    delay(500);
  }
  
  BT.begin(9600);
  BT.write("\nStart Listening\n");
}
void dAlarm(){
  BT.write("\nStop Listening\n");
  BT.end();
  
  for(int i=0; i<3; i++){
    tone(BUZZER, 500);
    analogWrite(M1, dSpeed);
    analogWrite(M2, dSpeed);
    delay(dDelay);
    analogWrite(M1, 0);
    analogWrite(M2, 0);
    noTone(BUZZER);
    delay(500);
  }
  
  BT.begin(9600);
  BT.write("\nStart Listening\n");
}
void nfAlarm(){
  BT.write("\nStop Listening\n");
  BT.end();
  noTone(BUZZER);
  for(int i=0; i<2; i++){
    for(int j=0; j<2; j++){
      analogWrite(M1, nfSpeed);
      analogWrite(M2, nfSpeed);
      delay(nfDelay);
      analogWrite(M1, 0);
      analogWrite(M2, 0);
      delay(nfDelay);
    }
    delay(500);
  }
  BT.begin(9600);
  BT.write("\nStart Listening\n");
}
