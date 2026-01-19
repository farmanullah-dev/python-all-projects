import cv2
import numpy as np 

img1 = cv2.imread("F:\\Laptop image\\2560x1600-578493-mercedes-benz.jpg")
img2 = cv2.imread("F:\\Laptop image\\alonso-reyes-haZNHEV2WXQ-unsplash.jpg")

img1=cv2.resize(img1,(500,500))
img2=cv2.resize(img2,(500,500))
cv2.imshow("img1",img1)
cv2.imshow("img2",img2)


# add both images in one frame
result = img1+img2   # numpy addition 
result =cv2.resize(result,(500,500))
cv2.imshow("result",result)

#opn cv addtion of image 
result1 =cv2.add(img1,img2)
result1=cv2.resize(result1,(500,500))
cv2.imshow("result1",result1)

#some of both the weight w1+w2= 1 (maximum weight 1 ana chanye es sse zyada nai de sakty )
#function cv2.addweighted(img1,wt1,img2,wt2,seturation)
result2= cv2.addWeighted(img1,0.7,img2,0.3,3)  # extendent version
result2 =  cv2.resize(result2,(500,500))
cv2.imshow('result2',result2) 


cv2.waitKey(0)
cv2.destroyAllWindows



