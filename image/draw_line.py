import cv2 
import numpy as np

img=np.zeros((538,538,3),np.uint8)

# draw line on image 
# first name then start point of line,endpoint of line ,clour and then thickness 
# its take 5 parameter
#        (name,starting point ,end point ,BGR ,and thickness)
cv2.line(img,(0,0),(300,300),(140,110,0),4)
#same as like line draw rectangle 
cv2.rectangle(img,(110,150),(360,350),(140,110,0),-4) #if i put (-)then they will show me fill rectangle



cv2.imshow("image",img)

cv2.waitKey(0)