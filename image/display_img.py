import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

url = "D:\\#PICS\\Camera Roll\\2023_04_03_14_52_IMG_0811.JPG"
pic = mpimg.imread(url)

# Display the original image
plt.imshow(pic)
plt.axis('on')
plt.show()
print(pic.shape)  # for showing his matrixes


