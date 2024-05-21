#include <Servo.h>
#include "utilities.hpp"

#define DETECTAR_OBJETO 0
#define MOVER_RAMPA 1
#define MOVER_RULETA 2
#define DELAY 250                           // En milisegundos

// Declaracion de variables
Servo rampa, ruleta;
int estado_actual = DETECTAR_OBJETO,
    proximo_estado = -1;
bool ruleta_movida = false;                 // Bandera para saber si ya movi la ruleta

char objeto = 0;                            // Codigo del objeto detectado
unsigned long t = 0;                        // Variable para delays
int pos_rampa = 30, pos_ruleta = 30;        // Variables de posicionamiento


unsigned long t_debug = 0;

void setup() {
  // Abro el puerto serie
  Serial.begin(9600);
  Serial.println("Inicializando...");
  
  // Configuro el servo de la rampa al pin 9
  // Muevo la rampa a su posicion inicial de 30 grados
  rampa.attach(9);
  rampa.write(pos_rampa);

  // Configuro el servo de la rampa al pin 10
  // Muevo la rampa a su posicion inicial
  ruleta.attach(10);
  ruleta.write(pos_ruleta);

  t_debug = millis();
}


void loop() {

  if( millis() - t_debug > DELAY ) {
    Serial.print(objeto);
    Serial.print("      rampa  ");
    Serial.print(pos_rampa);
    Serial.print("      ruleta  ");
    Serial.println(pos_ruleta);
    t_debug = millis();
  }

  switch(estado_actual) {
    case DETECTAR_OBJETO:
      if( millis() - t > DELAY ) {
        objeto = getObject();

        if( checkObject(objeto) ) {
          t = millis();
          proximo_estado = MOVER_RAMPA;
          Serial.println("Moviendo rampa...");
        }
      }
      break;
    
    case MOVER_RAMPA:
      pos_rampa = getRampPos(objeto);
      rampa.write(pos_rampa);
      
      if( millis() - t > 2*DELAY ) {
        if( rampa.read() == pos_rampa || (pos_rampa == pos_rampa) ) {
          t = millis();
          proximo_estado = MOVER_RULETA;
          Serial.println("Moviendo ruleta...");
        }
      }
      
      break;

    case MOVER_RULETA:
      if( !ruleta_movida ) {
        pos_ruleta = getWheelPos(pos_ruleta);
        ruleta_movida = true;
      }
      ruleta.write(pos_ruleta);
      
      if( millis() - t > 2*DELAY ) {
        if( rampa.read() == pos_ruleta || (pos_ruleta == pos_ruleta) ) {
          t = millis();
          ruleta_movida = false;
          proximo_estado = DETECTAR_OBJETO;
          Serial.println("Detectando objeto...");
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
