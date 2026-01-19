
# video break into images 

import cv2

#first we import a video in our files
video=cv2.VideoCapture("C:\\Users\Hp\Downloads\\Video\Mouj New Pashto Rabab EDM Remix Music -New Year 2024- -VOA Deeva- -New Pashto Songs- - Dostaan -_2.mp4")
ret,img=video.read()# read the video

count=0

while True:
    if ret==True:
        # imgN%d they give name to frames in files like N1,N2 ,N3 like this 
        cv2.imwrite("C:\\Frames\\imgN%d.jpg"%count,img)
        video.set(cv2.CAP_PROP_POS_MSEC,(count**50))

        ret,img=video.read()
        cv2.imshow("res",img)

        count+=1

        if cv2.waitKey(0) & 0xFF==ord("q"):
            break
        cv2.destroyAllWindows()

        video.release
        cv2.destroyAllWindows()

