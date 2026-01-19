import numpy as np
import cv2

img = np.zeros((3,3), dtype=np.uint8)  # now we have three table and each table represent R<G<B respectively.
img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
image=img.shape # for chack the structure  of image like rows and columns 
print(img)
print(image)  # This indicate (3,3,3)which means three channel in each pixel