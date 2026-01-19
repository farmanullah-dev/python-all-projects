import cv2

#first import video  video capture is a function 
vid=cv2.VideoCapture("C:/Users\Hp\Downloads/Video/#best rabab ---# music #subscribe.mp4")
    
    #if the video play show sucess 
while True:
    sucess, img=vid.read()
          # for showing the video in screen 
    cv2.imshow("Video",img)
      # waite until the user will press q means quite
    if cv2.waitKey(10)& 0xFF==ord('q'):
      break