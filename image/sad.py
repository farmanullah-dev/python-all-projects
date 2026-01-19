import cv2
img = cv2.imread("C:\\Users\\Hp\Downloads\\istockphoto-467294055-1024x1024.jpg")
img = cv2.resize(img, (0,0), fx=0.5, fy=0.5)    
cv2.imshow('Saad', img)
cv2.waitKey(0)
cv2.destroyAllWindows()