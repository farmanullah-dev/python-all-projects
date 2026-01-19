import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

# Load the image
url = "D:\\#PICS\\Camera Roll\\2023_04_03_14_52_IMG_0811.JPG"
pic = mpimg.imread(url)

# Define the coordinates for cropping (xmin, xmax, ymin, ymax)
xmin, xmax = 50, 2000# Example values for cropping width
ymin, ymax = 200, 2000 # Example values for cropping height

# Crop the image using NumPy slicing
cropped_image = pic[ymin:ymax, xmin:xmax]

# Display the cropped image
plt.imshow(cropped_image)
plt.axis('on')  # Optional, to show axis
plt.show()
