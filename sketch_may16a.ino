#include <Servo.h>

//int pos=0;
//int i=0;
Servo rampa;
Servo ruleta;
int flag=0;
//int flaganterior=0;
int rul1=30, rul2=rul1+60;



String lectura(){
  //lectura de imagenes
  
  if(Serial.available()){
    String dato = Serial.readStringUntil('\n');
    return dato;
  }
}

//mover servo rampa inclinada:
int moverrampa(String clasificacion){
    int posiciondeseada=69;
    if (clasificacion=="cuborojo")
        posiciondeseada=30;
    if (clasificacion=="cuboverde")
        posiciondeseada=60;
    if (clasificacion=="esferarojo")
        posiciondeseada=90;
    if (clasificacion=="esferaverde")
        posiciondeseada=120;
    if(posiciondeseada!=69)
      rampa.write(posiciondeseada);
    return posiciondeseada;
    }
    

//mover servo ruleta:
void moverruleta(){
  if (ruleta.read()==rul1){
    ruleta.write(rul2);
    return;
  }
    
  if (ruleta.read()==rul2){
    ruleta.write(rul1);
    return;
  }

}

  


void setup() {
  
  // put your setup code here, to run once:
  Serial.begin(9600);
  rampa.attach(9);
  ruleta.attach(10);
  ruleta.write(rul1);
  rampa.write(30);
  
}


void loop() {
  // put your main code here, to run repeatedly:

  int posicionrampa=10, posicionruleta=10;
  String clasificacion="nada";
  
  if (flag==0){
    //Serial.println("leer");
    clasificacion=lectura();
    delay(1000);
    //Serial.println(" ");
    if (clasificacion == "cuboverde" || clasificacion == "esferarojo" || clasificacion == "esferaverde" || clasificacion == "cuborojo")
    //if (clasificacion != "nada")
      flag++;
  }


  if (flag==1){
    posicionrampa=moverrampa(clasificacion);
    delay(1000);
    flag++;
  }

  
  if (flag==2){
    if (rampa.read()==posicionrampa){
      flag++;
      delay(1000);
      }
  }

  if (flag==3){
    moverruleta();
    delay(1000);
    flag++;
  }

  if (flag==4){
    if (ruleta.read()==rul1 || ruleta.read()==rul2)
      delay(1000);
      flag=0;
  }

  Serial.print(clasificacion);
  Serial.print("      flag  ");
  Serial.print(flag);
  Serial.print("      ruleta  ");
  Serial.print(ruleta.read());
  Serial.print("           rampa  ");
  Serial.println(rampa.read());


//Serial.println("           rampa  ");
}
