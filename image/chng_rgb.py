import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

url = "D:\\#PICS\\Camera Roll\\2023_04_03_14_52_IMG_0811.JPG"
pic = mpimg.imread(url)

# Display the original image
plt.imshow(pic)
plt.axis('on')
plt.show()

# Remove the green color channel
pic = np.copy(pic)  # Create a copy to avoid modifying the original image
pic[:, :, 1]=0 # Set the green channel values to zero

# Display the modified image without the green color channel
plt.imshow(pic)
plt.axis('on')
plt.show()
