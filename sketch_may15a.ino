#include <Servo.h>
int pos=0;
int i=0;
Servo rampa;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  rampa.attach(9);

}

void loop() {
  // put your main code here, to run repeatedly:

//  delay(1000);
  if(Serial.available()){
    String dato = Serial.readStringUntil('\n');
    if (dato=="cuborojo")
        rampa.write(30);
    if (dato=="cuboverde")
        rampa.write(60);
    if (dato=="esferarojo")
        rampa.write(90);
    if (dato=="esferaverde")
        rampa.write(120);
    }
}
