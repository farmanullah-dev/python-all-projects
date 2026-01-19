import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

# Load the image
url = "D:\\#PICS\\Camera Roll\\2023_04_03_14_52_IMG_0811.JPG"
pic = mpimg.imread(url)

# Take the average pixel value across all pixels
avg_pixel_value = np.mean(pic, axis=(0, 1))

# Create a new image with a single pixel using the average pixel value
single_pixel_image = np.full((1, 1, 3), avg_pixel_value, dtype=np.float32)

# Display the single pixel image
plt.imshow(single_pixel_image)
plt.axis('off')  # Turn off axis
plt.show()
