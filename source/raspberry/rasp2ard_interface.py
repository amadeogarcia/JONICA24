"""
Comando Linux para determinar el nombre de dispositivo serial:
dmesg | grep -v disconnect | grep -Eo "tty(ACM|USB)." | tail -1

Devuelve                  
ttyUSB0

Instalar biblioteca pyserial:
pip install pyserial
"""

# Defino las macros para forma y color
CUBO = 0x30         # '0'
ESFERA = 0x31       # '1'
VERDE = 0x01        #  1
ROJO = 0x03         #  3

"""
Segun los valores ASCII elegidos, las combinaciones quedan como sigue:
* CUBO VERDE = '1'
* ESF. VERDE = '2'
* CUBO ROJO  = '3'
* ESF. ROJA  = '4'
"""

# Importo las bibliotecas necesarias
import serial
import cv2
import numpy as np

# Abro el puerto serie
seri = serial.Serial('/dev/ttyUSB0',9600)
seri.flushInput()

# Funcion para detectar el objeto
def codigoObjeto(approxPoly, color):
    # Inicializo el byte a transmitir
    objeto = 0

    if len(approxPoly) <= 9 :
        objeto += CUBO
    if len(approxPoly) >= 11:
        objeto += ESFERA
    
    if color == (0,255,0):
        objeto += VERDE
    if color == (0,0,255):
        objeto += ROJO

    # Verifico que el objeto se haya detectado correctamente
    """
    Es horrible no poder intercambiar entre chars y bytes indistintamente
    pero Python no me deja. Basicamente necesito que objeto este entre
    '1' y '4' pero sin ser de tipo char.
    """
    if 0x31 <= objeto <= 0x34:  objeto = 0
    
    return objeto


def dibujar(mask, color):
    contornos, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in contornos:
        area = cv2.contourArea(c)
        if area > 500:
            M = cv2.moments(c)
            if (M["m00"]==0): M["m00"] = 1
            x = int(M["m10"]/M["m00"])
            y = int(M['m01']/M['m00'])
            nuevoContorno = cv2.convexHull(c)
            
            #cv2.circle(frame,(x,y),7,(0,255,0),-1)
            #cv2.putText(frame,'{},{}'.format(x,y),(x+10,y), font, 0.75,(0,255,0),1,cv2.LINE_AA)
            #cv2.putText(frame,nombrecolor,(x+10,y), font, 0.75,color,1,cv2.LINE_AA)
            #cv2.drawContours(frame, [nuevoContorno], 0, color, 3)
            
            # Calculo un poligono aproximado para detectar la forma
            epsilon = 0.01*cv2.arcLength(nuevoContorno,True)
            approx = cv2.approxPolyDP(nuevoContorno,epsilon,True)

            # Envio el codigo del objeto seleccionado al Arduino
            objeto = codigoObjeto(approx, color)
            seri.write(objeto)

            # A partir de aca es codigo de compatibilidad para dibujar y escribir en el stream de video
            # TODO: Borrar en la final release
            obj = objeto - 0x30
            if obj:
                if obj > 2:   color_name = "ROJO"
                else:         color_name = "VERDE"
                if obj % 2:   shape_name = "ESFERA"
                else:         shape_name = "ESFERA"
                cv2.drawContours(frame, [nuevoContorno], 0, color, 3)
                cv2.putText(frame, color_name, (x+10,y), font, 0.75, color, 1, cv2.LINE_AA)
                cv2.putText(frame, shape_name, (x+10,y-20), font, 0.75, color, 1, cv2.LINE_AA)
            
cap = cv2.VideoCapture(0)

verdeBajo = np.array([40,50,10],np.uint8)
verdeAlto = np.array([80,255,255],np.uint8)

redBajo1 = np.array([0,100,20],np.uint8)
redAlto1 = np.array([15,255,255],np.uint8)

redBajo2 = np.array([170,100,20],np.uint8)
redAlto2 = np.array([179,255,255],np.uint8)

font = cv2.FONT_HERSHEY_SIMPLEX
while True:

  ret,frame = cap.read()

  if ret == True:
    frameHSV = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    maskVerde = cv2.inRange(frameHSV,verdeBajo,verdeAlto)
    maskRed1 = cv2.inRange(frameHSV,redBajo1,redAlto1)
    maskRed2 = cv2.inRange(frameHSV,redBajo2,redAlto2)
    maskRed = cv2.add(maskRed1,maskRed2)
    dibujar(maskVerde,(0,255,0))
    dibujar(maskRed,(0,0,255))
    cv2.imshow('frame',frame)

    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()