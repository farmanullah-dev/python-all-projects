import cv2 
import numpy as np 

img=cv2.imread("D:\\#PICS\\Facebook\\FB_IMG_1615818063813.jpg")

print(img.shape) #First we find the real shape of image 

Image_Resize=cv2.resize(img,(300,300)) #then we resize with our choice 


cv2.imshow("Original image",img) #first see the original image

cv2.imshow("Resize Image",Image_Resize) # and then the resize image 

cv2.waitKey(0)