
import cv2 

img=cv2.imread("D:\\#PICS\\Facebook\\FB_IMG_1615818063813.jpg")


cropped_Image=img[0:250,250:400]   #for cropping image


cv2.imshow("Cropped Image",cropped_Image)
cv2.waitKey(0)
