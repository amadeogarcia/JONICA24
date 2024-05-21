"""
Comando Linux para determinar el nombre de dispositivo serial:
dmesg | grep -v disconnect | grep -Eo "tty(ACM|USB)." | tail -1

Devuelve                  
ttyUSB0

Instalar biblioteca pyserial:
pip install pyserial
"""

# Defino las macros para forma y color
OBJ_INVALIDO = b'0'
CUBO_VERDE   = b'1'
ESFERA_VERDE = b'2'
CUBO_ROJO    = b'3'
ESFERA_ROJA  = b'4'

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
    objeto = OBJ_INVALIDO

    if len(approxPoly) <= 9 :
        if color == (0,255,0):
            objeto = CUBO_VERDE
        elif color == (0,0,255):
            objeto = CUBO_ROJO

    if len(approxPoly) >= 11:
        if color == (0,255,0):
            objeto = ESFERA_VERDE
        elif color == (0,0,255):
            objeto = ESFERA_ROJA
    # Verifico que el objeto se haya detectado correctamente
    if not (objeto == CUBO_VERDE or
            objeto == CUBO_ROJO  or
            objeto == ESFERA_VERDE or
            objeto == ESFERA_ROJA):
        objeto = OBJ_INVALIDO
    
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
            if objeto != OBJ_INVALIDO:
                if objeto == CUBO_VERDE or objeto == CUBO_ROJO:
                    shape_name = "CUBO"
                else:
                    shape_name = "ESFERA"
                
                if objeto == CUBO_VERDE or objeto == ESFERA_VERDE:
                    color_name = "VERDE"
                else:
                    color_name = "ROJO"

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