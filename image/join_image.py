import cv2
import numpy as np 

img=cv2.imread("D:\\#PICS\\Facebook\\FB_IMG_1615818063813.jpg")

imagee=np.hstack((img,img))
image_ver=np.vstack((img,img))

cv2.imshow("Image joint",imagee)
cv2.imshow("Vertical stack",image_ver)

cv2.waitKey(0)