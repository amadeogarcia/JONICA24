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
        if color == (0,255,0):
            objeto = 1
        if color == (0,0,255):
            objeto = 3
        
    if len(approxPoly) >= 11:
        if color == (0,255,0):
            objeto = 2
        if color == (0,0,255):
            objeto = 4

    # Verifico que el objeto se haya detectado correctamente
    """
    Es horrible no poder intercambiar entre chars y bytes indistintamente
    pero Python no me deja. Basicamente necesito que objeto este entre
    '1' y '4' pero sin ser de tipo char.
    """
    #if 0x31 <= objeto <= 0x34:  objeto = 0
    
    return objeto


def dibujar(mask, color):
    contornos, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in contornos:
        area = cv2.contourArea(c)
        if area > 20000:
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
            
            objetostr = str(objeto)
            objetostr +="\n"
            mensaje=objetostr.encode(encoding='UTF-8',errors='strict')
            
            lectura=seri.readline()
            trigger=lectura.decode('UTF-8').strip()
            if trigger=="leer":
	            seri.write(mensaje)
	            print(mensaje)
            
            #lectura=seri.readline()
            #trigger=lectura.decode('UTF-8').strip()
            #if(trigger=="leer"):
            
            #seri.write(mensaje)
			#
			
			            
            
            #, "   y en string:  ",objetostr)
            
            # A partir de aca es codigo de compatibilidad para dibujar y escribir en el stream de video
            # TODO: Borrar en la final release
            #obj = objeto - 0x30
            
            if objeto == 1:   
                color_name = "verde"  
                shape_name = "CUBO"
            
            if objeto == 2:   
                color_name = "verde"  
                shape_name = "esfera"
            
            if objeto == 3:   
                color_name = "rojo"  
                shape_name = "CUBO"
            
            if objeto == 4:   
                color_name = "roja"  
                shape_name = "esfera"
            
            if objeto < 1 or objeto >4:
                color_name = "NADA"  
                shape_name = "nada"
            
            cv2.drawContours(frameobjeto, [nuevoContorno], 0, color, 3)
            cv2.putText(frameobjeto, color_name, (x+10,y), font, 0.75, color, 1, cv2.LINE_AA)
            cv2.putText(frameobjeto, shape_name, (x+10,y-20), font, 0.75, color, 1, cv2.LINE_AA)
            
cap = cv2.VideoCapture(0)

verdeBajo = np.array([40,100,20],np.uint8)
verdeAlto = np.array([80,255,255],np.uint8)

redBajo1 = np.array([0,180,50],np.uint8)
redAlto1 = np.array([15,255,255],np.uint8)

redBajo2 = np.array([170,180,50],np.uint8)
redAlto2 = np.array([179,255,255],np.uint8)

font = cv2.FONT_HERSHEY_SIMPLEX
while True:

  ret,frame = cap.read()
  x1,y1=500,200
  x2,y2=1800,900
  zonadeteccion=frame.copy()
  frameobjeto= zonadeteccion[y1:y2,x1:x2]   # hago mas chica el area de deteccion, en realidad el area que cubre la camara es mayor
	

  if ret == True:
    frameHSV = cv2.cvtColor(frameobjeto,cv2.COLOR_BGR2HSV)
    maskVerde = cv2.inRange(frameHSV,verdeBajo,verdeAlto)
    maskRed1 = cv2.inRange(frameHSV,redBajo1,redAlto1)
    maskRed2 = cv2.inRange(frameHSV,redBajo2,redAlto2)
    maskRed = cv2.add(maskRed1,maskRed2)
    dibujar(maskVerde,(0,255,0))
    dibujar(maskRed,(0,0,255))
    cv2.imshow('camara',frameobjeto)

    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
