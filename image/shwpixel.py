import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

# Load the image
url = "D:\\#PICS\\Camera Roll\\2023_04_03_14_52_IMG_0811.JPG"
pic = mpimg.imread(url)

# Print the shape of the image array
print("Image shape:", pic.shape)

# Print the first few pixels of the image array
print("First few pixels:\n", pic[:3, :3])

# Display the image
plt.imshow(pic)
plt.axis('on')
plt.show()
