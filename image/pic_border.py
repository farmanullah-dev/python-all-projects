
import cv2 
import numpy as np

img=cv2.imread("F:\\Laptop image\\2560x1600-578493-mercedes-benz.jpg")
print(img.shape)

image=cv2.resize(img,(800,800))

#for border border property(img,border_width(4_sides),bordertype,border)
#border wwidth (top ,right ,bottum,left) 
bdr=cv2.copyMakeBorder(image,10,10,5,5,cv2.BORDER_CONSTANT,value=([255,0,125]))
#border have more types but this is good like ,isolate type ,transperent type etc.....

cv2.imshow("image",image)
cv2.imshow("Border image ",bdr)
cv2.waitKey(0)