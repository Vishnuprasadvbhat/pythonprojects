import cv2
import mediapipe as mp
import  time

#creating our videoobject using our pc cam
cap= cv2.VideoCapture(0)

#creating object from class Hands
#mandate lineofcode
mpHands =mp.solutions.hands

#object created,check the hands  parameter for Hand Landmarks
hands=mpHands.Hands()#we dont add as it has default parameter

#using mpDraw to draw the points
mpDraw=mp.solutions.drawing_utils

#for calutaing fps we we define previous time and current time
pTime=0
cTime=0


#this code will give us frame
while True:
    success,img =cap.read()
 #sending rgb img to hands by converting our img to rgb becoause hands class only uses RGB images
    imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
#calling object hands with its method proceess which wil process the frames for us and output we wil be stored in result
    results=hands.process(imgRGB)
    #print(results.multi_hand_landmarks)#it gives mediapipe -python based solution for given above code
    # After printing when you show hand to webcam it outputs some cordinates else none


    if results.multi_hand_landmarks:
#when we shows hands it can  be multiple hands observed by the cam,
# so to make know each hands is observe and its values we write this loop
        for handLms in results.multi_hand_landmarks:
            for id,lm in enumerate(handLms.landmark):#lm will return landmark from handLms.landmark
        # id will return exact index number relating to our finger
                #print(id,lm)
        # in the print statement we get id as 1 to 20 and axis x,y,z(landmarks)using to find location for lm on the hand
        # location must be in pixel but its in decimals as they are return ratio of the img,we need to mulitiply it with
        # width and height to get pixel value
                h,w,c=img.shape #this gives structural definations of img :height,width c for channel
                cx,cy=int(lm.x*w),int(lm.y*h)# this will give us positions of the centre in int
                #print(cx,cy) this will print all positions without specifying id's (lms) so
                print(id,cx,cy)
        #this code will create a circle in id location '0' with certain parameter defining its presence
        #img: createcircle in img window,use positions, 25: radius (255): color
                if id==4:
                    cv2.circle(img,(cx,cy),15,(255,0,255),cv2.FILLED)



            mpDraw.draw_landmarks(img, handLms,mpHands.HAND_CONNECTIONS)
    # we get infomartion of landmark(x and y coordinates) and id number(checking the list of their index number )
    # hand_connections will gives connectedlines btw the dots , we get all 21 handmarkings from this

#here we call time function for calculating fps
    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime

#this code is for displaying fps on the screen with various parameters

    cv2.putText(img,str(int(fps)),(10,70), cv2.FONT_HERSHEY_PLAIN,3,(255,0,255), 3)
    # img : as we put in on our webcam window
    # str: we want it in str as it is time so converting using str,its in int type
    # 10,70 for giving position in the window
    # appplying font for fps i.e hershey_plain
    # thn we write scale as 3, for colorcode as (255,0,255) for purple and 3 for thickness of the fps

#Running a webcam
    cv2.imshow("Image",img)
    cv2.waitKey(1)