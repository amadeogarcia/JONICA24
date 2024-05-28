import cv2
import numpy as np

# Defino un diccionario con los posibles posicionamientos de la rampa
# TODO: Revisar segun si el servo va de 0 a 180 o de -90 a 90
posRampa = {
    'Default':      0,
    'Cubo Verde':   30,
    'Cubo Rojo':    60,
    'Esfera Verde': 90,
    'Esfera Roja':  120
}


# Funcion para codificar el objeto detectado
def objCode(approxPoly, color):
    obj = 'Default'

    if len(approxPoly) <= 7 :
        if color == (0,255,0):
            obj = 'Cubo Verde'
        if color == (0,0,255):
            obj = 'Cubo Rojo'
        
    if len(approxPoly) >= 10:
        if color == (0,255,0):
            obj = 'Esfera Verde'
        if color == (0,0,255):
            obj = 'Esfera Roja'
    
    return obj


# Defino las variables necesarias para el stream de video
cap = cv2.VideoCapture(0)

verdeBajo = np.array([40,80,20],np.uint8)
verdeAlto = np.array([80,255,255],np.uint8)

redBajo1 = np.array([0,170,60],np.uint8)
redAlto1 = np.array([15,255,255],np.uint8)

redBajo2 = np.array([170,170,60],np.uint8)
redAlto2 = np.array([179,255,255],np.uint8)

font = cv2.FONT_HERSHEY_SIMPLEX

# Funcion para dibujar el contorno del objeto, mostrando forma y color
def drawObj(mask, color):
    # Detecto todos los contornos en la imagen
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for c in contours:
        # Filtro los contornos detectados segun su area
        area = cv2.contourArea(c)
        if area > 70000:
            # Busco el centro del contorno
            M = cv2.moments(c)
            if (M["m00"]==0): M["m00"] = 1
            x = int(M["m10"]/M["m00"])
            y = int(M['m01']/M['m00'])
            
            # Creo el contorno
            newContour = cv2.convexHull(c)
                        
            # Calculo un poligono aproximado para detectar la forma
            epsilon = 0.01*cv2.arcLength(newContour,True)
            approx = cv2.approxPolyDP(newContour,epsilon,True)

            # Codifico el objeto
            obj = objCode(approx, color)

            # Dibujo el contorno y muestro el codigo
            cv2.drawContours(objFrame, [newContour], 0, color, 3)
            cv2.putText(objFrame, obj, (x+10,y), font, 0.75, color, 1, cv2.LINE_AA)

            # Devuelvo la codificacion del objeto detectado
            return obj

# Funcion para leer un frame y reducir la zona de deteccion
def readFrame():
    # Leo el siguiente frame
    ret,frame = cap.read()
    
    # Hago mas chica el area de deteccion, en realidad el area que cubre la camara es mayor
    x1,y1 = 500,200
    x2,y2 = 1800,900
    detectZone = frame.copy()
    objFrame = detectZone[y1:y2, x1:x2]   

    return ret, objFrame

# Funcion para analizar el frame leido
def parseFrame(frame):
    frameHSV = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    maskVerde = cv2.inRange(frameHSV,verdeBajo,verdeAlto)
    maskRed1 = cv2.inRange(frameHSV,redBajo1,redAlto1)
    maskRed2 = cv2.inRange(frameHSV,redBajo2,redAlto2)
    maskRed = cv2.add(maskRed1,maskRed2)

    obj1 = drawObj(maskVerde,(0,255,0))
    obj2 = drawObj(maskRed,(0,0,255))

    cv2.imshow('camara', frame)

    # TODO: REVISAR ESTO CON MALVA
    return obj1


# Funcion para cerrar todo
def exitFunc():
    cap.release()
    cv2.destroyAllWindows()