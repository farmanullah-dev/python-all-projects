import cv2

faceCascade=cv2.CascadeClassifier("C:\\Users\\Hp\\Documents\\haarcascade_frontalface_default.xml")

img=cv2.imread("C:\\Users\\Hp\\Documents\\2022_12_02_21_26_IMG_0823.JPG")

image_gray=cv2.cvtColor(img ,cv2.COLOR_BGR2GRAY)

faces=faceCascade.detectMultiScale(image_gray,1.1,4)

for (x,y,w,h) in faces:
    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)

cv2.imshow("image",img)
cv2.waitKey(0)