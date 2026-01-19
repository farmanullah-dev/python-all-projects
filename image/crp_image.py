import matplotlib.pyplot as plt
import cv2

url = "D:\\#PICS\\Camera Roll\\2023_04_03_14_52_IMG_0811.JPG"
pic = cv2.imread(url)

# Crop the image (specifying startY, endY, startX, endX)
cropped = pic[800:4000, 700:3000]

# Display the cropped region
plt.imshow(cropped)
plt.show()
