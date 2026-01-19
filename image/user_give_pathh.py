import cv2

path=input("Enter the the path===")
print("You entered this = ",path)

img=cv2.imread(path,0) # (0) will convert direct into graycycle
img=cv2.resize(img,(500,760))

cv2.imshow("Converted image ",img)

k=cv2.waitkey(0)

if k==ord("s"):

 cv2.imwrite("D:\\output.png",img)

else:
 cv2.destroyAllWindows()
    