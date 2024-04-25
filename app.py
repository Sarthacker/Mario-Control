import cv2 as cv
import mediapipe as mp
import numpy as np
import time
import math
import HandTrackingModule as htm
import pyautogui as pg

ptime = 0
wcam, hcam = 640, 480
cap = cv.VideoCapture(0)
cap.set(3, wcam)
cap.set(4, hcam)
detector = htm.handDetector(detectionCon=0.7)

while True:
    success,img=cap.read()
    img=detector.findHands(img)
    lmlist=detector.findPosition(img,draw=False)
    
    # ctime=time.time()
    # fps=1/(ctime-ptime)
    # ptime=ctime

    # cv.putText(img, f'FPS: {int(fps)}', (20, 60), cv.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)

    # cv.imshow("Img", img)
    
    if(len(lmlist)!=0):
        # it moves right with index finger
        right1,right2=lmlist[8][1],lmlist[8][2]
        right11,right22=lmlist[5][1],lmlist[5][2]
        right_length=math.hypot(right11-right1,right22-right2)
        
        # it moves left with middle finger
        left1,left2=lmlist[12][1],lmlist[12][2]
        left11,left22=lmlist[9][1],lmlist[9][2]
        left_length=math.hypot(left11-left1,left22-left2)
        
        # # it jumps with little finger
        jump1,jump2=lmlist[20][1],lmlist[20][2]
        jump11,jump22=lmlist[17][1],lmlist[17][2]
        jump_length=math.hypot(jump11-jump1,jump22-jump2)
        
        # # it fires with thumb
        fire1,fire2=lmlist[4][1],lmlist[4][2]
        fire11,fire22=lmlist[1][1],lmlist[1][2]
        fire_length=math.hypot(fire11-fire1,fire22-fire2)
        
        # print(right_length,left_length,jump_length,fire_length)
        
        if(right_length>=115):
            pg.press('right')
        if(left_length>=110):
            pg.press('left')
        if(jump_length>=115):
            pg.press('z')
        if(fire_length>=145):
            pg.press('x')
            
    # cv.waitKey(0)