import cv2
from cvzone.HandTrackingModule import HandDetector
import math
import numpy as np
import cvzone


wCam, hCam = 1280 ,720
#webcam
cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
# cap = cv2.VideoCapture(0)

cap.set(3,wCam)
cap.set(4,hCam)

# hand detector
detector = HandDetector(detectionCon=0.8,maxHands=1)
# find function
x = [80,85,90,100,110,120, 130,140,160,180,200,220,260,300]
y = [95,90,85,80,75,70, 65,60,55,50,45,40,35,30]

coff = np.polyfit(x,y,2)


#loop
while True :
  success , img = cap.read()
  # hands , img = detector.findHands(img)
  hands = detector.findHands(img,draw = False)
  if hands:
    lmList = hands[0]['lmList']
    x, y, w, h = hands[0]['bbox']
    # print(len(lmList))
    #chose two point to measure the distance(should be constant no matter the gesture changes)
    x1,y1,z1 = lmList[5]
    x2,y2,z2 = lmList[17]
    # cv2.putText(img,"5",(x1,y1),cv2.FONT_HERSHEY_PLAIN,2,(255,0,255),2)
    # cv2.putText(img,"17",(x2,y2),cv2.FONT_HERSHEY_PLAIN,2,(255,0,255),2)
    distance = math.sqrt((y2 - y1)**2 + (x2-x1)**2)
    distanceCM = coff[0]*(distance**2) + coff[1]*(distance) +coff[2]
    print(int(distance),distanceCM)
    cvzone.putTextRect(img,f"{int(distanceCM)} cm",(x+5,y-20),2,colorT=(0,255,0),colorR=(0,0,0))
    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,255),3)


  cv2.imshow("Image",img)
  cv2.waitKey(1)

