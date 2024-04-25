import cv2 as cv
import mediapipe as mp
import numpy as np
import time


class handDetector:
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.trackCon = trackCon
        self.detectionCon = detectionCon
        self.maxHands = maxHands
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, int(self.detectionCon), int(self.trackCon))
        self.mpdraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks) ----> this shows the position of the hands in the camera

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpdraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img
    
    def findPosition(self,img,handNo=0,draw=True):
        
        lmlist=[]
        
        if self.results.multi_hand_landmarks:
            myHand=self.results.multi_hand_landmarks[handNo]
            for id,lm in enumerate(myHand.landmark):
                h,w,c=img.shape
                cx,cy=int(lm.x*w),int(lm.y*h)
                # print(id,cx,cy)
                lmlist.append([id,cx,cy])
                # if draw:
                #     cv.circle(img,(cx,cy),15,(255,0,255),cv.FILLED)
                
        return lmlist


def main():
    ptime = 0
    ctime = 0
    wcam, hcam = 640, 480
    cap = cv.VideoCapture(0)
    cap.set(3, wcam)
    cap.set(4, hcam)
    detector = handDetector()
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmlist=detector.findPosition(img)
        
        if len(lmlist)!=0:  # -----> this is used here because if no hands are shown then the code will end since it will not be able to find any hand and hence the list will become empty
            print(lmlist[4])

        ctime=time.time()
        fps=1/(ctime-ptime)
        ptime=ctime

        cv.putText(img, f'FPS: {int(fps)}', (20, 60), cv.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)

        cv.imshow("Img", img)
        cv.waitKey(1)


if __name__ == "__main__":
    main()
