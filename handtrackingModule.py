import cv2
import mediapipe as mp
import time

class handDetector():
    def __init__(self,mode=False,max_hands = 2,detection_con=0.5,track_con=0.5):
        self.mode = mode
        self.max_hands = max_hands
        self.detection_con = detection_con
        self.track_con = track_con
        self.lmList = []
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
                                        self.mode,
                                        self.max_hands,
                                        1,
                                        self.detection_con,
                                        self.track_con
                                        )
        self.mpDraw = mp.solutions.drawing_utils
    def findHands(self,img,draw=True):
        imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(self.results.multi_hand_landmarks)
        if self.results.multi_hand_landmarks :
            for handLms in self.results.multi_hand_landmarks :
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,self.mpHands.HAND_CONNECTIONS)
        return img
    def findPosition(self,img,handNo=0,draw=True):
        self.lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                # print(id,lm)
                h,w,c = img.shape
                cx,cy = int(lm.x*w) , int(lm.y*h)
                # print(id,cx,cy)
                self.lmList.append([id,cx,cy])
                if draw :
                    cv2.circle(img, (cx,cy),10,(255,0,0),cv2.FILLED)
        return self.lmList

def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img)
        if len(lmList) != 0 :
            print(lmList[4])

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        cv2.imshow("image", img)
        cv2.waitKey(1)


if __name__ == "__main__" :
    main()