import cv2
import time
import os
import handtrackingModule as htm
wCam, hCam = 640, 640

cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)

folderPath = "FingerImages"
myList = os.listdir(folderPath)
print(myList)
overlayList = []

for imPath in myList:
    image = cv2.imread(f"{folderPath}/{imPath}")
    overlayList.append(image)
print(len(overlayList))
pTime = 0
detector = htm.handDetector(detection_con=0.75)
tipIds = [4,8,12,16,20]
while True:
    success ,img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img,draw=0)
    # print(lmList)
    numId = [6,7,8,9]
    NUM = 0
    if len(lmList) !=0 :
        fingers = []
        if lmList[tipIds[0]][1] > lmList[tipIds[0]-2][1] :
            fingers.append(1)
        else :
            fingers.append(0)

        for id in range(1,5):

            if lmList[tipIds[id]][2] <lmList[tipIds[id]-2][2] :
                fingers.append(1)
                # print("index finger open")
            else :
                fingers.append(0)

        NUM = fingers.count(1)
    
    img[0:200,0:200] = overlayList[NUM]
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img,f"FPS:{int(fps)}",(400,70),cv2.FONT_HERSHEY_PLAIN,2,(0,0,255),3)
    cv2.imshow("image",img)
    cv2.waitKey(1)
