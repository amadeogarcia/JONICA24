#include "utilities.hpp"

int getObject() {
  if( Serial.available() > 0 )
    return Serial.read();
}

int moveRamp(int object, Servo &rampa) {
    int pos;
    
    switch(object) {
      case CUBO_VERDE:
        pos = 30;
        break;
      case CUBO_ROJO:
        pos = 60;
        break;
      case ESFERA_VERDE:
        pos = 90;
        break;
      case ESFERA_ROJA:
        pos = 120;
        break;
      default:
        pos = 0;
    }
    
    if( pos )
      rampa.write(pos);
    
    return pos;
}

// TODO: cambiar implementacion segun la construccion de la ruleta
int moveWheel(int pos_actual, Servo &ruleta) {
  int next_pos = 0;
  switch(pos_actual) {
    case 30:
      next_pos = 90;
      break;
    case 90:
      next_pos = 30;
      break;
  }

  ruleta.write(next_pos);
  return next_pos;
}