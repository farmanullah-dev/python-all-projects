import cv2

img=cv2.imread("D:\\#PICS\\Facebook\\FB_IMG_1615818063813.jpg")

imgGray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)  # the image will show gray

#for blur image
imageBlur=cv2.GaussianBlur(imgGray,(7,7),0)  #now we will show the blur image 

cv2.imshow("Grayimage",imgGray) # first we make grayimage
cv2.imshow("Blur image",imageBlur)  #then we make gray image blur  
cv2.waitKey(0)