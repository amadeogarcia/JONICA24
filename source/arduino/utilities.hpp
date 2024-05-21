#ifndef utilities_h_
#define utilities_h_

#include <Arduino.h>
#include <Servo.h>

// Defino las macros para forma y color
#define CUBO_VERDE      1
#define ESFERA_VERDE    2
#define CUBO_ROJO       3
#define ESFERA_ROJA     4

// Lee el buffer serie y devuelve el codigo del objeto detectado
String getObject();
// Verifica que el objeto recibido sea correcto
bool checkObject(String);
// Obtiene la posición a la que se debe mover el servo de la rampa inclinada
int getRampPos(String);
// Obtiene la posición a la que se debe mover el servo de la ruleta
int getWheelPos(int);

#endif
