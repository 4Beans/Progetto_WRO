#include <Servo.h>
#include <time.h>

Servo myservo;

//PIN
// motori
const int avanti=2;
const int vel=3;
const int indietro=4;
// ultrasuoni
const int echoSx=10;
const int echoDx=11;
const int trigger=12; // trigger in comune per entrambe
// comunicazione con raspberry
const int pinDx90=5;
const int pinSx90=8;
const int reset=7;
const int pinSx=6;
const int pinDx=13;
const int comStop=10;

//VARIABILI
unsigned long previousMillis=0;
unsigned long currentMillis=0;
int stato=0;
int velocita=130;

void setup() {
  myservo.attach(9);
  pinMode(indietro,OUTPUT);
  pinMode(vel,OUTPUT);
  pinMode(avanti,OUTPUT);
  pinMode(trigger,OUTPUT);
  pinMode(echoSx,INPUT);
  pinMode(echoDx,INPUT);
  pinMode(reset,INPUT);
  pinMode(pinSx90,INPUT);
  pinMode(pinDx90,INPUT);
  pinMode(pinSx,INPUT);
  pinMode(pinDx,INPUT);
  pinMode(comStop,INPUT);
  Serial.begin(9600);
  stop();
  raddrizza();
}

void loop() {
  if(digitalRead(reset)==HIGH)
    stato=1;
  
  //currentMillis = millis();

  switch(stato){
    case 0:
      stop();
      if(digitalRead(reset)==HIGH)
        stato=1;
      break;
    case 1:
      vai(velocita);
      if(digitalRead(comStop)==HIGH){
        stato=0;
        break;
      }
      if(digitalRead(pinDx90)==HIGH)
        destra90();
      if(digitalRead(pinSx90)==HIGH)
        sinistra90();
      if(digitalRead(pinDx)==HIGH)
        raddrizzaSinistra();
      if(digitalRead(pinSx)==HIGH)
        raddrizzaDestra();
      /*if (currentMillis - previousMillis >= 60) {
        previousMillis = currentMillis;
        checkMuro();
      }*/
      break;
  }
}

// funzioni movimento
void raddrizza(){
  myservo.write(86);
}
void destra(){
  myservo.write(40);
}
void destra90(){
  vai(160);
  delay(200);
  destra();
  delay(465);
  raddrizza();
  vai(velocita);
}
void raddrizzaDestra(){
  destra();
  delay(400);
  sinistra();
  vai(160);
  delay(400);
  raddrizza();
  vai(velocita);
}
void sinistra(){
  myservo.write(140);
}
void sinistra90(){
  vai(160);
  delay(200);
  sinistra();
  delay(500);
  raddrizza();
  vai(velocita);
}
void raddrizzaSinistra(){
  sinistra();
  delay(300);
  destra();
  vai(160);
  delay(500);
  raddrizza();
  vai(velocita);  
}
void vai(int velocita){
  analogWrite(vel,velocita);
  digitalWrite(avanti,HIGH);
  digitalWrite(indietro,LOW);
}
void frena(){
  analogWrite(vel,255);
  digitalWrite(avanti,LOW);
  digitalWrite(indietro,HIGH);
}
void stop(){
  analogWrite(vel,0);
  digitalWrite(avanti,LOW);
  digitalWrite(indietro,LOW);
}

//funzioni ultrasuoni
int distance(int echo){
  digitalWrite(trigger, LOW); 
  delayMicroseconds(2);
  // Sets the trigPin on HIGH state for 10 micro seconds
  digitalWrite(trigger, HIGH); 
  delayMicroseconds(10);
  digitalWrite(trigger, LOW);
  int duration = pulseIn(echo, HIGH); // Reads the echoPin, returns the sound wave travel time in microseconds
  int distance= duration*0.034/2;
  return distance;
}
