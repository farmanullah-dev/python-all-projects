import cv2  

#import image
img=cv2.imread("D:\\#PICS\\Facebook\\FB_IMG_1615818063813.jpg")

# canny is a function in which we find the edge of image
imgedge=cv2.Canny(img,100,100) # first we give the name of the image 
                      #and then its edge detail that how many want


cv2.imshow("Edge_image",imgedge)

cv2.waitKey(0)