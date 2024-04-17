import cv2
import mediapipe as mp
import  time
import HandTrackingModule as htm



pTime = 0
cTime = 0
cap = cv2.VideoCapture(0)
detector=htm.handDetector()
while True:
    success, img = cap.read()
    img=detector.findhands(img)
    lmList=detector.findposition(img,draw=True)
    #if len(lmList) !=0:
            #print(lmList[9])
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    #if draw==False thn below line donot run
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (150, 0, 200), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)

if __name__=="__main__":
    main()
