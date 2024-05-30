"""
Para usar la GPIO de la RPi hay que instalar el paquete y una libreria de python:
    sudo apt-get install python3-rpi.gpio
    sudo pip3 install gpiozero
"""

from util import *
from datetime import datetime, timedelta
from gpiozero import AngularServo

#"""
# Mock factory para debuggear en PC
from gpiozero import Device
from gpiozero.pins.mock import MockFactory, MockPWMPin
Device.pin_factory = MockFactory(pin_class=MockPWMPin)
#"""

# Variables para delays (en milisegundos)
DELAY_MS = 1000
delay = timedelta(milliseconds=DELAY_MS)
t = datetime.now()

# Inicializo los dos servos
rampa =  AngularServo("GPIO2", min_angle=0, max_angle=270 , min_pulse_width=0.0005, max_pulse_width=0.0025)
ruleta = AngularServo("GPIO3", min_angle=0, max_angle=270 , min_pulse_width=0.0005, max_pulse_width=0.0025)


# Declaro las posiciones de ambos servos
pos_rampa = posRampa.get('Default')
pos_ruleta = 0

# Defino un diccionario con los estados de la MEF
state = {
    'Blank':               -1,
    'Detectando objeto':    0,
    'Moviendo rampa':       1,
    'Moviendo ruleta':      2
}

# Declaro los estados de la MEF
estado_actual = state.get('Detectando objeto')
prox_estado   = state.get('Blank')

while True:
    prox_estado = state.get('Detectando objeto')
    if estado_actual == state.get('Detectando objeto'):
        if datetime.now() - t > delay:
            objeto = 'Default'
            
            # Leo el frame de la camara
            ret, frame = readFrame()
            if ret == True:
                objeto = parseFrame(frame)
                
                # Espero al caracter de escape (tecla ESC) para salir del bucle infinito
                key = cv2.waitKey(1) & 0xFF
                if key == 27:
                    break
            
            if objeto != 'Default':
                t = datetime.now()
                prox_estado = state.get('Moviendo rampa')
    
    if estado_actual == state.get('Moviendo rampa'):
        pos_rampa = posRampa.get(objeto)
        rampa.angle = pos_rampa

        # Espero a que el servo llegue
        if datetime.now() - t > 2*delay:
            t = datetime.now()
            prox_estado = state.get('Moviendo ruleta')

    if estado_actual == state.get('Moviendo ruleta'):
        # Invierto la posicion del servo
        #pos_ruleta *= -1
        #ruleta.value = pos_ruleta
        
        #pos_ruleta = posRuleta.get(objeto)
        if pos_ruleta == 0:
            pos_ruleta = 220
        elif pos_ruleta == 220:
            pos_ruleta = 0
        ruleta.angle = pos_ruleta

        if datetime.now() - t > 2*delay:
            t = datetime.now()
            prox_estado = state.get('Detectando objeto')
    
    if estado_actual != prox_estado:
        estado_actual = prox_estado
    #print(estado_actual)

exitFunc()