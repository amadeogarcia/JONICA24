#ifndef utilities_h_
#define utilities_h_

#include <Arduino.h>
#include <Servo.h>

// Defino las macros para forma y color
#define CUBO_VERDE 0x11
#define CUBO_ROJO 0x12
#define ESFERA_VERDE 0x21
#define ESFERA_ROJA 0x22

// Lee el buffer serie y devuelve el codigo del objeto detectado
int getObject();
// Mueve el servo de la rampa inclinada
int moveRamp(int, Servo&);
// Mueve el servo de la ruleta
int moveWheel(int, Servo&);

#endif