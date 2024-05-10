import cv2
from PIL import Image

from util import get_limits


yellow = [0, 255, 255]  # yellow in BGR colorspace
green = [0, 255, 0]  # green in BGR colorspace
red = [0, 0, 255]  # yellow in BGR colorspace

cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
while True:
    ret, frame = cap.read()

    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lowerLimit, upperLimit = get_limits(color=green)

    mask = cv2.inRange(hsvImage, lowerLimit, upperLimit)

    mask_ = Image.fromarray(mask)

    bbox = mask_.getbbox()

    if bbox is not None:
        x1, y1, x2, y2 = bbox
        frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)
        frame = cv2.putText(frame,'Verde', (x1+7, y1-12), 2 ,0.7, (0, 255, 0), 2)
        

# repito para rojo

    lowerLimit, upperLimit = get_limits(color=red)

    mask = cv2.inRange(hsvImage, lowerLimit, upperLimit)

    mask_ = Image.fromarray(mask)

    bbox = mask_.getbbox()

    if bbox is not None:
        x1, y1, x2, y2 = bbox
        frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 5)
        frame = cv2.putText(frame,'Rojo', (x1+7, y1-12), 2 ,0.7, (0, 0, 255), 2)


    cv2.imshow('camara', frame)

    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

cap.release()

cv2.destroyAllWindows()
