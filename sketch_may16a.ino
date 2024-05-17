#include <Servo.h>
//int pos=0;
//int i=0;
Servo rampa;
Servo ruleta;
int flag=0;
//int flaganterior=0;




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
  if (ruleta.read()==40){
    ruleta.write(130);
    return;
  }
    
  if (ruleta.read()==130){
    ruleta.write(40);
    return;
  }

}

  


void setup() {
  
  // put your setup code here, to run once:
  Serial.begin(9600);
  rampa.attach(9);
  ruleta.attach(10);
  ruleta.write(40);
  rampa.write(30);
  
}


void loop() {
  // put your main code here, to run repeatedly:

  int posicionrampa=10, posicionruleta=10;
  String clasificacion="narnia";
  
  if (flag==0){
    clasificacion=lectura();
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
      }
  }

  if (flag==3){
    moverruleta();
    flag++;
  }

  if (flag==4){
    if (ruleta.read()==40 || ruleta.read()==130)
      flag=0;
  }

  Serial.println(clasificacion);
  Serial.print("      flag  ");
  Serial.print(flag);
  Serial.print("      ruleta  ");
  Serial.print(ruleta.read());
  Serial.print("           rampa  ");
  Serial.println(rampa.read());


//Serial.println("           rampa  ");
}
