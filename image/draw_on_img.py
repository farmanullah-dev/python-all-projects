import cv2
import numpy as np

# first we make a image zeros means black image and then we make 3 color channel 
img=np.zeros((512,512,3),np.uint8)

 #[:] means apply color in whole image 
img[:]=255,0,0  # 255 is the number of blue 
 # if i want to not apply in all then we give value to [:] in this 
 #like this [height: weight, 100,300] like this 
cv2.imshow("Image",img)

cv2.waitKey(0)