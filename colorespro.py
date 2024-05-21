import cv2
import numpy as np

def dibujar(mask,color):
    contornos,_ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in contornos:
        area = cv2.contourArea(c)
        if area > 500:
            M = cv2.moments(c)
            if (M["m00"]==0): M["m00"]=1
            x = int(M["m10"]/M["m00"])
            y = int(M['m01']/M['m00'])
            nuevoContorno = cv2.convexHull(c)
            #cv2.circle(frame,(x,y),7,(0,255,0),-1)
            #cv2.putText(frame,'{},{}'.format(x,y),(x+10,y), font, 0.75,(0,255,0),1,cv2.LINE_AA)
            if color==(0,255,0):
                nombrecolor="verde"
            if color==(0,0,255):
                nombrecolor="rojo"
            cv2.putText(frame,nombrecolor,(x+10,y), font, 0.75,color,1,cv2.LINE_AA)
            cv2.drawContours(frame, [nuevoContorno], 0, color, 3)
            epsilon = 0.01*cv2.arcLength(nuevoContorno,True)
            approx = cv2.approxPolyDP(nuevoContorno,epsilon,True)
            if len(approx) <= 9:
                cv2.putText(frame,"cubo",(x+10,y-20), font, 0.75,color,1,cv2.LINE_AA)
            if len(approx) >= 11:
                cv2.putText(frame,"esfera",(x+10,y-20), font, 0.75,color,1,cv2.LINE_AA)
            #print(len(approx))    
            
    

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