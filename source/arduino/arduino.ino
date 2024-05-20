#include <Servo.h>
#include "utilities.hpp"

#define DETECTAR_OBJETO 0
#define MOVER_RAMPA 1
#define MOVER_RULETA 2
#define MIN_DELAY 100     // En milisegundos

// Declaracion de variables
Servo rampa, ruleta;
int estado_actual = DETECTAR_OBJETO,
    proximo_estado = -1;
int objeto = 0;                         // Codigo del objeto detectado
unsigned long t = 0;                    // Variable para delays
int pos_rampa = 30, pos_ruleta = 30;      // Variables de posicionamiento

void setup() {
  
  // Abro el puerto serie
  Serial.begin(9600);
  
  // Configuro el servo de la rampa al pin 9
  // Muevo la rampa a su posicion inicial de 30 grados
  rampa.attach(9);
  rampa.write(pos_rampa);

  // Configuro el servo de la rampa al pin 10
  // Muevo la rampa a su posicion inicial
  ruleta.attach(10);
  ruleta.write(pos_ruleta);
    
}


void loop() {
  
  switch(estado_actual) {
    case DETECTAR_OBJETO:
      if( millis() - t > 5*MIN_DELAY ) {
        objeto = getObject();
        if( objeto ) {
          t = millis();
          proximo_estado = MOVER_RAMPA;
        }
      }
      break;
    
    case MOVER_RAMPA:
      if( millis() - t > 2*MIN_DELAY ) {
        if( rampa.read() != pos_rampa )
          pos_rampa = moveRamp(objeto, rampa);
        else {
          t = millis();
          proximo_estado = MOVER_RULETA;
        }
      }
      break;

    case MOVER_RULETA:
      if( millis() - t > 5*MIN_DELAY ) {
        if( rampa.read() != pos_ruleta )
          pos_ruleta = moveWheel(pos_ruleta, ruleta);
        else {
          t = millis();
          proximo_estado = DETECTAR_OBJETO;
        }
      }
      break;      

    default:
      proximo_estado = DETECTAR_OBJETO;
      break;
  }

  if( estado_actual != proximo_estado )
    estado_actual = proximo_estado;

/*
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
    pos_rampa=moverrampa(clasificacion);
    delay(1000);
    flag++;
  }

  
  if (flag==2){
    if (rampa.read()==pos_rampa){
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
    if (ruleta.read()==pos_ruleta_1 || ruleta.read()==pos_ruleta_2)
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
*/

}
