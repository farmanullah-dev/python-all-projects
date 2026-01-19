import cv2

img=cv2.imread("F:\\Laptop image\\3D Hacker Wallpaper.png")

# for showing 
cv2.imshow("image", img)

# for appearing slow we need a waite key 
#if we put 1000 this mean for one second and if we put (0)this means infinity
cv2.waitKey(2000)