#include "utilities.hpp"

String getObject() {
  if( Serial.available() > 0 ){
    //Serial.print("el objeto es    ");
    //Serial.println(Serial.read());
    Serial.println("leer");
    return Serial.readStringUntil('\n');
    }
  
  return "0";
}

bool checkObject(String object) {
  if( object.toInt() >= 1 && object.toInt() <= 4 )
    return true;

  return false;
}

int getRampPos(String object) {
    int pos;
    
    switch(object.toInt()) {
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
        
    return pos;
}

// TODO: cambiar implementacion segun la construccion de la ruleta
int getWheelPos(int pos_actual) {
  int next_pos = 0;
  switch(pos_actual) {
    case 30:
      next_pos = 90;
      break;
    case 90:
      next_pos = 30;
      break;
  }

  return next_pos;
}
