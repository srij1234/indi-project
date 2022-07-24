from pyfirmata import Arduino,SERVO,util
from time import sleep

import cv2
import numpy as np

port= '/dev/ttyACM0'
pin=9
pin2=10
board=Arduino(port)


def rotateservo(pin,angle):
    board.digital[pin].write(angle)
    sleep(0.015)
rotateservo(pin,90)
cap = cv2.VideoCapture(0)
while True:
    _, image = cap.read()
    hsv_frame = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    low_green = np.array([25, 52, 72])
    high_green = np.array([102, 255, 255])
    green_mask = cv2.inRange(hsv_frame, low_green, high_green)
    frame = cv2.blur(image,(10,10))
    green = cv2.bitwise_and(frame, frame, mask=green_mask)
   
    gray=cv2.cvtColor(green,cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray,110, 255, cv2.THRESH_BINARY)
    
    contours, hierarchies = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
        if (cv2.contourArea(c)>500):
            h,w,channel=image.shape
            
            rect=cv2.minAreaRect(c)
          
            image = cv2.circle(image,(int(rect[0][0]),int(rect[0][1])) ,5, [0,0,255], 2)
            
            box = cv2.boxPoints(rect) 
            box = np.int0(box)
            cv2.drawContours(image,[box],0,(0,0,255),2)
           
            x=int(rect[0][0])
            y=int(rect[0][1])
            if x>252:
            	rotateservo(pin,1)
            else:
                rotateservo(pin,0)
            print(x)
        
    cv2.imshow("Framen", image)
  
    key = cv2.waitKey(1)
    if key == 27:
        break
