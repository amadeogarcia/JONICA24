import cv2
from PIL import Image

from util import get_limits


#yellow = [0, 255, 255]  # yellow in BGR colorspace
green = [0, 255, 0]  # green in BGR colorspace
red = [0, 0, 255]  # yellow in BGR colorspace

cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
while True:
    ret, frame = cap.read()

    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lowerLimit, upperLimit = get_limits(color=green)

    mask = cv2.inRange(hsvImage, lowerLimit, upperLimit)

    
    
    blurredmask = cv2.dilate(mask,cv2.getStructuringElement(cv2.MORPH_RECT,(5,5)),iterations = 3)
    blurredmask = cv2.erode(blurredmask,cv2.getStructuringElement(cv2.MORPH_RECT,(3,3)),iterations = 1)
    blurredmask = cv2.GaussianBlur(blurredmask, (9, 9), 3)

    cv2.imshow('mascaraverde', blurredmask)

    cann= cv2.Canny(blurredmask,1,1)
    cv2.imshow('mascaraverdecanny', cann)

    mask_ = Image.fromarray(mask)

    bbox = mask_.getbbox()

    if bbox is not None:
        x1, y1, x2, y2 = bbox
        frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)
        frame = cv2.putText(frame,'Verde', (x1+7, y1-12), 2 ,0.7, (0, 255, 0), 2)
    
    cnts,_ = cv2.findContours(cann, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)# OpenCV 4
    cv2.drawContours(frame, cnts, -1, (0,100,0), 2)

    for contorno in cnts:
        epsilon = 0.001*cv2.arcLength(contorno,True)
        periv=cv2.arcLength(contorno,True)
        areav=cv2.contourArea(contorno)
        if(areav!=0):
            relav=periv*periv/areav
            print("                         verde",relav)
        approx = cv2.approxPolyDP(contorno,epsilon,True)
        x,y,w,h = cv2.boundingRect(approx)
        #print("                         verde",len(approx))
        if (relav<15):
            cv2.putText(frame,'esfera', (x,y+55),1,1.5,(0,255,0),2)
        if (relav>15):
            cv2.putText(frame,'cubo', (x,y+55),1,1.5,(0,255,0),2)
    

# repito para rojo

    lowerLimit, upperLimit = get_limits(color=red)

    mask = cv2.inRange(hsvImage, lowerLimit, upperLimit)

    blurredmask = cv2.GaussianBlur(mask, (3, 3), 3)
    #blurredmask = cv2.erode(blurredmask,cv2.getStructuringElement(cv2.MORPH_RECT,(3,3)),iterations = 1)
    blurredmask = cv2.dilate(blurredmask,cv2.getStructuringElement(cv2.MORPH_RECT,(5,5)),iterations = 1)
    
    #cv2.imshow('mascararoja', blurredmask)
    

    mask_ = Image.fromarray(mask)

    canr= cv2.Canny(blurredmask,1,1)
    #cv2.imshow('mascararojacanny', canr)

    bbox = mask_.getbbox()

    if bbox is not None:
        x1, y1, x2, y2 = bbox
        frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 5)
        frame = cv2.putText(frame,'Rojo', (x1+7, y1-12), 2 ,0.7, (0, 0, 255), 2)
    
    cnts,_ = cv2.findContours(blurredmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)# OpenCV 4
    cv2.drawContours(frame, cnts, -1, (0,255,0), 2)

    for contorno in cnts:
        epsilon = 0.001*cv2.arcLength(contorno,True)
        perir=cv2.arcLength(contorno,True)
        arear=cv2.contourArea(contorno)
        if(arear!=0):
            relar=perir*perir/arear
            print("rojo ",relar)
        approx = cv2.approxPolyDP(contorno,epsilon,True)
        x,y,w,h = cv2.boundingRect(approx)
        print("rojo ",len(approx))
        if (relar<15):
            cv2.putText(frame,'esfera', (x,y-5),1,1.5,(0,255,0),2)
        if (relar>15):
            cv2.putText(frame,'cubo', (x,y+55),1,1.5,(0,255,0),2)
        
        

      
    cv2.imshow('camara', frame)

    #cv2.waitKey(0)

    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

cap.release()

cv2.destroyAllWindows()
