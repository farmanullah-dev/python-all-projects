import cv2

# using webcam 
# (0)is the default camera of system
cap=cv2.VideoCapture(0)
cap.set(3,460) #set width of frame
cap.set(4,480)# set height of frame
cap.set(10,100) # for brightnessq
while True:
    sucess,img=cap.read()

    cv2.imshow("web",img)

    if cv2.waitKey(1) & 0xFF== ord('q'):
     break 