import cv2
grayImage = cv2.imread("D:\#PICS\Peshawar\IMG_20231109_165948.jpg", cv2.IMREAD_GRAYSCALE)
cv2.imwrite("D:\#PICS\Peshawar\IMG_20231109_165948.jpg", grayImage)

print(grayImage)