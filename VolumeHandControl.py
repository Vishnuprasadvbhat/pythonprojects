import cv2
import time

import nltk
import numpy as np
import HandTrackingModule as htm
import  math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


#applying width and height of the camera as per standard resolution
###############################parameters
wCam,hCam =640,480
##############################

#calling camera
cap=cv2.VideoCapture(0)
#using it here as per propid width is 3 and height is 4
cap.set(3,wCam)
cap.set(4,hCam)
ptime=0
cTime=0


detector=htm.handDetector(detectionCon=0.7)
#My sincere thanks to Mr.Andres for creating Python Core Audio Windows Library
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volRange=volume.GetVolumeRange() #(-96.0, 0.0, 0.125) this is the range we have our volume play

minVol=volRange[0]
maxVol=volRange[1]#now we can use this than using paraameters of getVolumeRANGE
vol=0


while True:
    success,img =cap.read()

    img=detector.findhands(img)
    lmList=detector.findposition(img,draw=False)
    #lmList.append(id,x1,y1,x2,y2)
    if len(lmList)!=0:
        #print(lmList[4],lmList[8])

        x1,y1=lmList[4][1],lmList[4][2] #retriving their pixel for positions
        x2,y2=lmList[8][1],lmList[8][2]
        cx, cy = (x1+x2)//2,(y1+y2)//2 #finding center point landmark 4 and 8
        #if id==4 & id==8:
        cv2.circle(img,(x1,y1),7,(255,0,255),cv2.FILLED)
        cv2.circle(img,(x2,y2), 7, (255, 0, 255), cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255,0,255),3)#draws line between landmark 4 and 8
        cv2.circle(img,(cx,cy), 7, (255, 0, 255), cv2.FILLED)#it creates a circle in the center of line joining lm 4&8
        length=math.hypot(x2-x1,y2-y1)
        #print(length)

        #hand range 50-300
        #volume range -96 to 0
        #using numpy we convert the ranges
        volBar=400
        volPer=0
        vol=np.interp(length,[50,225],[minVol,maxVol])
        volBar=np.interp(length,[50,250],[400,150])
        volPer=np.interp(length,[50,250],[0,100])

        print(int(length),vol)
        volume.SetMasterVolumeLevel(vol, None)  # this turns our volume higher and lower

        if length<50:#if length b/w 4 and 8 is less than 50, centre circle of that line becomes green
            cv2.circle(img,(cx,cy), 7, (0, 255,0 ), cv2.FILLED)

        cv2.rectangle(img,(50,150),(85,400),(255,0,0),3)
        cv2.rectangle(img,(50,int(volBar)),(85,400),(255,0,0),cv2.FILLED)
        cv2.putText(img, f'{int(volPer)}%', (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0), 3)

    cTime=time.time()
    fps= 1 / (cTime-ptime)
    ptime=cTime

    cv2.putText(img,f'FPS: {int(fps)}',(40,50), cv2.FONT_HERSHEY_COMPLEX, 1,(255,0,0),3)
    cv2.imshow("Img",img)
    cv2.waitKey(1)

