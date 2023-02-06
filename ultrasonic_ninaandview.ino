#define trig1 PIN_PC3
#define echo1 PIN_PC2


long duration1;             
int distance1;             

void setup() {
pinMode(PIN_PC5, OUTPUT);
pinMode(PIN_PD3, OUTPUT);
pinMode(trig1, OUTPUT);    
pinMode(echo1, INPUT);   
}

void loop() {
digitalWrite(trig1, LOW); 
delayMicroseconds(2);
digitalWrite(trig1, HIGH); 
delayMicroseconds(10);
digitalWrite(trig1, LOW); 

duration1 = pulseIn(echo1, HIGH);

distance1 = (duration1*0.034)/2;

if(distance1<30){

  digitalWrite(PIN_PD3,HIGH);
  tone(PIN_PC5,5000);
  delay(60);
  tone(PIN_PC5,0);
  delay(60);
 
}

else{
  digitalWrite(PIN_PD3,LOW);
  noTone(PIN_PC5);
}

delay(50);
}
